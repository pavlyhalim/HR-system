from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from apps.accounts.models import User


class UserModelTests(TestCase):
    def test_create_user_with_email(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role="employee",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.role, "employee")
        self.assertTrue(user.check_password("testpass123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_user_str(self):
        user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="pass123",
            first_name="John",
            last_name="Doe",
        )
        self.assertIn("John Doe", str(user))

    def test_user_roles(self):
        for role_value, role_label in User.Role.choices:
            user = User.objects.create_user(
                username=f"user_{role_value}",
                email=f"{role_value}@example.com",
                password="pass123",
                role=role_value,
            )
            self.assertEqual(user.role, role_value)

    def test_email_unique(self):
        User.objects.create_user(username="u1", email="dup@example.com", password="pass123")
        with self.assertRaises(Exception):
            User.objects.create_user(username="u2", email="dup@example.com", password="pass123")


class AuthAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role="hr",
        )

    def test_login_success(self):
        response = self.client.post("/api/v1/auth/login/", {"email": "test@example.com", "password": "testpass123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password(self):
        response = self.client.post("/api/v1/auth/login/", {"email": "test@example.com", "password": "wrongpass"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        response = self.client.post("/api/v1/auth/login/", {"email": "nonexistent@example.com", "password": "pass123"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/auth/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_profile_unauthenticated(self):
        response = self.client.get("/api/v1/auth/profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register(self):
        response = self.client.post("/api/v1/auth/register/", {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "ComplexPass123!",
            "password_confirm": "ComplexPass123!",
            "first_name": "New",
            "last_name": "User",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_register_password_mismatch(self):
        response = self.client.post("/api/v1/auth/register/", {
            "email": "mismatch@example.com",
            "username": "mismatch",
            "password": "ComplexPass123!",
            "password_confirm": "DifferentPass123!",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/v1/auth/change-password/", {
            "old_password": "testpass123",
            "new_password": "NewComplexPass123!",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewComplexPass123!"))

    def test_user_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/auth/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_refresh(self):
        login_resp = self.client.post("/api/v1/auth/login/", {"email": "test@example.com", "password": "testpass123"})
        refresh_token = login_resp.data["refresh"]
        response = self.client.post("/api/v1/auth/token/refresh/", {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
