from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class OMASurvey(BaseModel):
    class RespondentGroup(models.TextChoices):
        HR = "hr", "HR"
        MANAGER = "manager", "Manager"
        EMPLOYEE = "employee", "Employee"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        LAUNCHED = "launched", "Launched"
        CLOSED = "closed", "Closed"
        ANALYZED = "analyzed", "Analyzed"

    title = models.CharField(max_length=200)
    respondent_group = models.CharField(max_length=20, choices=RespondentGroup.choices)
    launch_start = models.DateTimeField(null=True, blank=True)
    launch_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    anonymous = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.respondent_group})"


class OMASurveyQuestion(BaseModel):
    survey = models.ForeignKey(OMASurvey, on_delete=models.CASCADE, related_name="questions")
    domain = models.CharField(max_length=100, help_text="Maturity domain this maps to")
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, default="scale", help_text="scale / free_text / multiple_choice")
    weight = models.FloatField(default=1.0)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:60]}"


class OMASurveyResponse(BaseModel):
    survey = models.ForeignKey(OMASurvey, on_delete=models.CASCADE, related_name="responses")
    respondent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    response_payload = models.JSONField(default=dict)
    is_complete = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Response for {self.survey}"


class OMANormalizedData(BaseModel):
    survey = models.ForeignKey(OMASurvey, on_delete=models.CASCADE, related_name="normalized_data")
    normalized_payload = models.JSONField(default=dict)
    outliers_flagged = models.JSONField(default=list)
    version = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Normalized data v{self.version} for {self.survey}"


class OMADomainScore(BaseModel):
    survey = models.ForeignKey(OMASurvey, on_delete=models.CASCADE, related_name="domain_scores", null=True, blank=True)
    domain_name = models.CharField(max_length=100)
    score = models.FloatField(help_text="1-5 maturity score")
    weight = models.FloatField(default=1.0)
    calculated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.domain_name}: {self.score}"


class OMAValidationResult(BaseModel):
    survey = models.ForeignKey(OMASurvey, on_delete=models.CASCADE, related_name="validation_results", null=True, blank=True)
    rule_name = models.CharField(max_length=200)
    result = models.CharField(max_length=20, help_text="pass / warning / fail")
    details = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.rule_name}: {self.result}"


class OMAMaturityLevel(BaseModel):
    class Level(models.IntegerChoices):
        INITIAL = 1, "Initial"
        EMERGING = 2, "Emerging"
        DEFINED = 3, "Defined"
        MANAGED = 4, "Managed"
        OPTIMIZED = 5, "Optimized"

    overall_level = models.IntegerField(choices=Level.choices)
    domain_scores_snapshot = models.JSONField(default=dict)
    confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    confirmed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Maturity Level: {self.get_overall_level_display()}"


class OMAGap(BaseModel):
    class Severity(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    domain_name = models.CharField(max_length=100)
    gap_description = models.TextField()
    severity = models.CharField(max_length=10, choices=Severity.choices)
    maturity_driver = models.CharField(max_length=200, blank=True)
    actionable_insight = models.TextField(blank=True)

    def __str__(self):
        return f"Gap: {self.domain_name} ({self.severity})"


class OMARisk(BaseModel):
    class Severity(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    domain_name = models.CharField(max_length=100)
    risk_description = models.TextField()
    severity = models.CharField(max_length=10, choices=Severity.choices)
    impact = models.TextField(blank=True)
    mitigation = models.TextField(blank=True)

    def __str__(self):
        return f"Risk: {self.domain_name} ({self.severity})"


class OMARoadmap(BaseModel):
    quarter = models.CharField(max_length=10, help_text="e.g. Q1-2025")
    actions = models.JSONField(default=list)
    version = models.PositiveIntegerField(default=1)
    priority_order = models.JSONField(default=list)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Roadmap {self.quarter} v{self.version}"


class OMABenchmark(BaseModel):
    class BenchmarkType(models.TextChoices):
        INDUSTRY = "industry", "Industry"
        SIZE = "size", "Company Size"
        REGION = "region", "Region"

    benchmark_type = models.CharField(max_length=20, choices=BenchmarkType.choices)
    classification_value = models.CharField(max_length=100, help_text="e.g. Technology, 500-1000, Middle East")
    variance_data = models.JSONField(default=dict, help_text="Per-domain: above/at/below")
    dataset_version = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Benchmark: {self.benchmark_type} - {self.classification_value}"


class OMABenchmarkDataset(BaseModel):
    name = models.CharField(max_length=200)
    dataset = models.JSONField(default=dict)
    version = models.CharField(max_length=50)
    source = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("name", "version")

    def __str__(self):
        return f"{self.name} v{self.version}"


class OMAStrategyExport(BaseModel):
    maturity_level = models.ForeignKey(OMAMaturityLevel, on_delete=models.CASCADE, related_name="exports")
    domain_scores = models.JSONField(default=dict)
    gaps = models.JSONField(default=list)
    risks = models.JSONField(default=list)
    acknowledged = models.BooleanField(default=False)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    exported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Strategy Export ({self.exported_at})"
