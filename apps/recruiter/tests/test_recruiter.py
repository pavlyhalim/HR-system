from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from apps.accounts.models import User
from apps.recruiter.models import Vacancy, Candidate, CandidateVacancy, Interview, HiringDecision
import uuid


class VacancyModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")

    def test_create_vacancy(self):
        v = Vacancy.objects.create(
            jd_id=uuid.uuid4(),
            title="Senior Python Developer",
            role_level="Senior",
            department="Engineering",
            employment_type="full_time",
            location="Remote",
            status="draft",
            created_by=self.user,
        )
        self.assertEqual(v.title, "Senior Python Developer")
        self.assertEqual(v.status, "draft")

    def test_vacancy_str(self):
        v = Vacancy.objects.create(
            jd_id=uuid.uuid4(),
            title="Data Engineer",
            department="Data",
            created_by=self.user,
        )
        self.assertIn("Data Engineer", str(v))


class CandidateModelTests(TestCase):
    def test_create_candidate(self):
        c = Candidate.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="+1234567890",
            source="linkedin",
        )
        self.assertEqual(c.name, "John Doe")
        self.assertEqual(c.source, "linkedin")

    def test_candidate_str(self):
        c = Candidate.objects.create(name="Jane Smith", email="jane@example.com")
        self.assertIn("Jane Smith", str(c))


class VacancyAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hr_user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")
        self.client.force_authenticate(user=self.hr_user)

    def test_list_vacancies(self):
        response = self.client.get("/api/v1/vacancies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_create_vacancy(self):
        jd_id = str(uuid.uuid4())
        response = self.client.post("/api/v1/vacancies/", {
            "jd_id": jd_id,
            "title": "Product Manager",
            "role_level": "Mid",
            "department": "Product",
            "employment_type": "full_time",
            "location": "New York",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Product Manager")

    def test_retrieve_vacancy(self):
        v = Vacancy.objects.create(
            jd_id=uuid.uuid4(), title="QA Engineer", department="QA", created_by=self.hr_user,
        )
        response = self.client.get(f"/api/v1/vacancies/{v.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "QA Engineer")

    def test_update_vacancy(self):
        v = Vacancy.objects.create(
            jd_id=uuid.uuid4(), title="DevOps Engineer", department="Infra", created_by=self.hr_user,
        )
        response = self.client.patch(f"/api/v1/vacancies/{v.id}/", {"title": "SRE"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "SRE")

    def test_unauthenticated(self):
        client = APIClient()
        response = client.get("/api/v1/vacancies/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CandidateAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hr_user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")
        self.client.force_authenticate(user=self.hr_user)

    def test_list_candidates(self):
        response = self.client.get("/api/v1/candidates/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_candidate(self):
        response = self.client.post("/api/v1/candidates/", {
            "name": "Bob Smith",
            "email": "bob@example.com",
            "phone": "+1234567890",
            "source": "indeed",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Bob Smith")


class InterviewAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hr_user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")
        self.client.force_authenticate(user=self.hr_user)

    def test_list_interviews(self):
        response = self.client.get("/api/v1/interviews/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class HiringDecisionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hr_user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")
        self.client.force_authenticate(user=self.hr_user)

    def test_list_decisions(self):
        response = self.client.get("/api/v1/decisions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MobilitySuccessionPromotionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hr_user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")
        self.client.force_authenticate(user=self.hr_user)

    def test_list_mobility(self):
        response = self.client.get("/api/v1/mobility/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_succession(self):
        response = self.client.get("/api/v1/succession/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_promotions(self):
        response = self.client.get("/api/v1/promotions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_promotion_cycles(self):
        response = self.client.get("/api/v1/promotion-cycles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
