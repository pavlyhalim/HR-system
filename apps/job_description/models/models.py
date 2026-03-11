from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class JobAnalysisInput(BaseModel):
    """Structured questionnaire input for JD creation."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_analyses")
    role_title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    tasks = models.JSONField(default=list, help_text="List of main tasks/responsibilities")
    tools = models.JSONField(default=list, help_text="Tools and systems used")
    reporting_line = models.CharField(max_length=255, blank=True)
    working_conditions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Job Analysis Input"
        verbose_name_plural = "Job Analysis Inputs"

    def __str__(self):
        return f"{self.role_title} - {self.department}"


class JobDescription(BaseModel):
    """Master JD record with governance and approval tracking."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        APPROVED = "approved", "Approved"
        ARCHIVED = "archived", "Archived"

    job_analysis = models.ForeignKey(JobAnalysisInput, on_delete=models.PROTECT, related_name="job_descriptions", null=True, blank=True)
    current_version = models.OneToOneField("JobDescriptionVersion", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_jds")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_jds")
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Job Description"
        verbose_name_plural = "Job Descriptions"

    def __str__(self):
        version = self.current_version
        title = version.structured_model.get("role_title", "Untitled") if version and version.structured_model else "Untitled"
        return f"JD-{self.pk.__str__()[:8]} ({title})"


class JobDescriptionVersion(BaseModel):
    """Immutable JD version with full structured model."""

    jd = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name="versions")
    version_number = models.PositiveIntegerField()
    structured_model = models.JSONField(default=dict, help_text="Full structured JD: purpose, responsibilities, competencies, KPIs")
    benchmark_summary = models.JSONField(default=dict, blank=True)
    validation_results = models.JSONField(default=dict, blank=True)

    class Meta(BaseModel.Meta):
        unique_together = [("jd", "version_number")]
        verbose_name = "JD Version"
        verbose_name_plural = "JD Versions"

    def __str__(self):
        return f"JD-{self.jd_id.__str__()[:8]} v{self.version_number}"


class JDCompetency(BaseModel):
    """Competency mapped to a JD version with proficiency and weight."""

    jd_version = models.ForeignKey(JobDescriptionVersion, on_delete=models.CASCADE, related_name="competencies")
    competency_name = models.CharField(max_length=255)
    proficiency_level = models.CharField(max_length=50, help_text="Junior / Mid / Senior / Expert")
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Weight percentage")
    is_mandatory = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        verbose_name = "JD Competency"
        verbose_name_plural = "JD Competencies"

    def __str__(self):
        return f"{self.competency_name} ({self.proficiency_level})"


class JDBenchmarkResult(BaseModel):
    """Benchmark comparison result for a JD version."""

    jd_version = models.ForeignKey(JobDescriptionVersion, on_delete=models.CASCADE, related_name="benchmarks")
    benchmark_source = models.CharField(max_length=100, help_text="O*NET / ESCO / Industry DB")
    deviations = models.JSONField(default=dict)
    risk_flags = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "JD Benchmark Result"
        verbose_name_plural = "JD Benchmark Results"

    def __str__(self):
        return f"Benchmark for JD v{self.jd_version.version_number} ({self.benchmark_source})"


class JDApprovalLog(BaseModel):
    """Immutable approval/rejection audit trail."""

    class Action(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    jd_version = models.ForeignKey(JobDescriptionVersion, on_delete=models.CASCADE, related_name="approval_logs")
    action = models.CharField(max_length=20, choices=Action.choices, db_index=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "JD Approval Log"
        verbose_name_plural = "JD Approval Logs"

    def __str__(self):
        return f"{self.action} by {self.actor} on JD v{self.jd_version.version_number}"


class JDConsumerReference(BaseModel):
    """Tracks which engines consume which JD version."""

    jd_version = models.ForeignKey(JobDescriptionVersion, on_delete=models.CASCADE, related_name="consumer_references")
    consumer_service = models.CharField(max_length=100, help_text="Recruiter / Performance / TNA / Mobility")
    reference_type = models.CharField(max_length=50, help_text="Vacancy / KPI / Promotion")
    referenced_at = models.DateTimeField(auto_now_add=True)

    class Meta(BaseModel.Meta):
        verbose_name = "JD Consumer Reference"
        verbose_name_plural = "JD Consumer References"

    def __str__(self):
        return f"{self.consumer_service} -> JD v{self.jd_version.version_number}"
