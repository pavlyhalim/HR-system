from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from apps.accounts.models import User


class OMAAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hr_user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")
        self.client.force_authenticate(user=self.hr_user)

    def test_list_surveys(self):
        response = self.client.get("/api/v1/oma/surveys/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_domain_scores(self):
        response = self.client.get("/api/v1/oma/domain-scores/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_maturity(self):
        response = self.client.get("/api/v1/oma/maturity/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_gaps(self):
        response = self.client.get("/api/v1/oma/gaps/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_risks(self):
        response = self.client.get("/api/v1/oma/risks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_roadmaps(self):
        response = self.client.get("/api/v1/oma/roadmaps/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_benchmarks(self):
        response = self.client.get("/api/v1/oma/benchmarks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class HRStrategyAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hr_user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")
        self.client.force_authenticate(user=self.hr_user)

    def test_list_strategies(self):
        response = self.client.get("/api/v1/strategy/strategies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_pillars(self):
        response = self.client.get("/api/v1/strategy/pillars/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_initiatives(self):
        response = self.client.get("/api/v1/strategy/initiatives/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_kpis(self):
        response = self.client.get("/api/v1/strategy/kpis/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_readiness(self):
        response = self.client.get("/api/v1/strategy/readiness/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_confidence(self):
        response = self.client.get("/api/v1/strategy/confidence/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_benchmarks(self):
        response = self.client.get("/api/v1/strategy/benchmarks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TNAAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hr_user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")
        self.client.force_authenticate(user=self.hr_user)

    def test_list_cycles(self):
        response = self.client.get("/api/v1/tna/cycles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_skill_gaps(self):
        response = self.client.get("/api/v1/tna/skill-gaps/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_learning_paths(self):
        response = self.client.get("/api/v1/tna/learning-paths/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PayrollAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hr_user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")
        self.client.force_authenticate(user=self.hr_user)

    def test_list_payroll_cycles(self):
        response = self.client.get("/api/v1/payroll/cycles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_salary_structures(self):
        response = self.client.get("/api/v1/payroll/salary-structures/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_payslips(self):
        response = self.client.get("/api/v1/payroll/payslips/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PerformanceAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hr_user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")
        self.client.force_authenticate(user=self.hr_user)

    def test_list_frameworks(self):
        response = self.client.get("/api/v1/performance/frameworks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_cycles(self):
        response = self.client.get("/api/v1/performance/cycles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_reviews(self):
        response = self.client.get("/api/v1/performance/reviews/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NotificationsDocumentsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hr_user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")
        self.client.force_authenticate(user=self.hr_user)

    def test_list_notifications(self):
        response = self.client.get("/api/v1/notifications/notifications/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_documents(self):
        response = self.client.get("/api/v1/documents/documents/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
