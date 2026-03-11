from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from apps.accounts.models import User
from apps.job_description.models import JobAnalysisInput, JobDescription, JobDescriptionVersion, JDCompetency


class JobAnalysisInputModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")

    def test_create_job_analysis(self):
        ja = JobAnalysisInput.objects.create(
            created_by=self.user,
            role_title="Software Engineer",
            department="Engineering",
            tasks=["Write code", "Review PRs"],
            tools=["Python", "Django"],
            reporting_line="Engineering Manager",
            status="draft",
        )
        self.assertEqual(ja.role_title, "Software Engineer")
        self.assertEqual(ja.status, "draft")
        self.assertIsNotNone(ja.id)

    def test_job_analysis_str(self):
        ja = JobAnalysisInput.objects.create(
            created_by=self.user,
            role_title="Data Analyst",
            department="Analytics",
        )
        self.assertIn("Data Analyst", str(ja))


class JobDescriptionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")

    def test_create_jd_with_version(self):
        jd = JobDescription.objects.create(created_by=self.user, status="draft")
        version = JobDescriptionVersion.objects.create(
            jd=jd,
            version_number=1,
            structured_model={"purpose": "Test role", "responsibilities": ["Task 1"]},
        )
        jd.current_version = version
        jd.save()
        self.assertEqual(jd.current_version.version_number, 1)

    def test_jd_competency(self):
        jd = JobDescription.objects.create(created_by=self.user, status="draft")
        version = JobDescriptionVersion.objects.create(jd=jd, version_number=1, structured_model={})
        comp = JDCompetency.objects.create(
            jd_version=version,
            competency_name="Python",
            proficiency_level="senior",
            weight=80,
            is_mandatory=True,
        )
        self.assertEqual(comp.competency_name, "Python")
        self.assertTrue(comp.is_mandatory)


class JobDescriptionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hr_user = User.objects.create_user(username="hr", email="hr@test.com", password="pass123", role="hr")
        self.client.force_authenticate(user=self.hr_user)

    def test_create_job_analysis(self):
        response = self.client.post("/api/v1/jd/job-analysis/", {
            "role_title": "Backend Engineer",
            "department": "Engineering",
            "tasks": ["Build APIs"],
            "tools": ["Django", "PostgreSQL"],
            "reporting_line": "Tech Lead",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["role_title"], "Backend Engineer")

    def test_list_job_analyses(self):
        JobAnalysisInput.objects.create(
            created_by=self.hr_user, role_title="Role 1", department="Dept 1",
        )
        response = self.client.get("/api/v1/jd/job-analysis/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_list_job_descriptions(self):
        response = self.client.get("/api/v1/jd/job-descriptions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_create_job_description(self):
        response = self.client.post("/api/v1/jd/job-descriptions/", {
            "status": "draft",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_access(self):
        client = APIClient()
        response = client.get("/api/v1/jd/job-descriptions/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
