from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from apps.accounts.models import User
from apps.employee_lifecycle.models import Employee, Offer, Contract, OnboardingTask


class EmployeeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")

    def test_create_employee(self):
        emp = Employee.objects.create(
            employment_status="preboarding",
            hire_date="2026-01-15",
        )
        self.assertEqual(emp.employment_status, "preboarding")
        self.assertIsNotNone(emp.id)


class EmployeeLifecycleAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hr_user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")
        self.client.force_authenticate(user=self.hr_user)

    def test_list_employees(self):
        response = self.client.get("/api/v1/lifecycle/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_list_offers(self):
        response = self.client.get("/api/v1/lifecycle/offers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_contracts(self):
        response = self.client.get("/api/v1/lifecycle/contracts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_onboarding_tasks(self):
        response = self.client.get("/api/v1/lifecycle/onboarding-tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_probation(self):
        response = self.client.get("/api/v1/lifecycle/probation/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_offboarding(self):
        response = self.client.get("/api/v1/lifecycle/offboarding/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_settlements(self):
        response = self.client.get("/api/v1/lifecycle/settlements/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_approvals(self):
        response = self.client.get("/api/v1/lifecycle/approvals/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated(self):
        client = APIClient()
        response = client.get("/api/v1/lifecycle/employees/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
