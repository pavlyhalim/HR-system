from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class PerformanceFramework(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    strategy_link = models.UUIDField(null=True, blank=True, help_text="FK to hr_strategy.HRStrategy")
    organizational_goals = models.JSONField(default=list)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ReviewCycle(BaseModel):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        ACTIVE = "active", "Active"
        REVIEW_PHASE = "review_phase", "Review Phase"
        CALIBRATION = "calibration", "Calibration"
        COMPLETED = "completed", "Completed"

    framework = models.ForeignKey(PerformanceFramework, on_delete=models.CASCADE, related_name="cycles")
    cycle_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.cycle_name


class GoalCascade(BaseModel):
    cycle = models.ForeignKey(ReviewCycle, on_delete=models.CASCADE, related_name="goals")
    employee_id = models.UUIDField()
    jd_id = models.UUIDField(null=True, blank=True, help_text="FK to job_description.JobDescription")
    organizational_goal = models.TextField(blank=True)
    role_goal = models.TextField()
    kpi_name = models.CharField(max_length=200)
    kpi_target = models.FloatField(null=True, blank=True)
    kpi_unit = models.CharField(max_length=50, blank=True)
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.kpi_name} for {self.employee_id}"


class PerformanceReview(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SELF_REVIEW = "self_review", "Self Review"
        MANAGER_REVIEW = "manager_review", "Manager Review"
        COMPLETED = "completed", "Completed"

    cycle = models.ForeignKey(ReviewCycle, on_delete=models.CASCADE, related_name="reviews")
    employee_id = models.UUIDField()
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews_given")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    self_assessment = models.JSONField(default=dict)
    manager_assessment = models.JSONField(default=dict)
    overall_score = models.FloatField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Review: {self.employee_id} ({self.status})"


class BiasDetectionResult(BaseModel):
    review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE, related_name="bias_results")
    bias_type = models.CharField(max_length=100)
    confidence = models.FloatField(help_text="0–1 confidence score")
    details = models.JSONField(default=dict)

    def __str__(self):
        return f"Bias: {self.bias_type} ({self.confidence})"


class CalibrationSession(BaseModel):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    cycle = models.ForeignKey(ReviewCycle, on_delete=models.CASCADE, related_name="calibrations")
    department = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    calibrated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    adjustments = models.JSONField(default=list)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Calibration: {self.cycle} - {self.department}"


class FinalRating(BaseModel):
    review = models.OneToOneField(PerformanceReview, on_delete=models.CASCADE, related_name="final_rating")
    rating = models.FloatField()
    rating_label = models.CharField(max_length=50, blank=True)
    calibrated = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Rating: {self.rating} ({self.rating_label})"
