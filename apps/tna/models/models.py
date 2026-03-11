from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class TNACycle(BaseModel):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"

    cycle_name = models.CharField(max_length=200)
    cycle_type = models.CharField(max_length=20, default="annual", help_text="annual / ad_hoc")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.cycle_name


class SkillGapAnalysis(BaseModel):
    cycle = models.ForeignKey(TNACycle, on_delete=models.CASCADE, related_name="analyses")
    employee_id = models.UUIDField(help_text="FK to employee_lifecycle.Employee")
    jd_competencies = models.JSONField(default=list)
    current_competencies = models.JSONField(default=list)
    gaps = models.JSONField(default=list)
    gap_severity = models.CharField(max_length=20, default="medium")

    def __str__(self):
        return f"Skill Gap: {self.employee_id}"


class ManagerTNAInput(BaseModel):
    cycle = models.ForeignKey(TNACycle, on_delete=models.CASCADE, related_name="manager_inputs")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.UUIDField()
    observations = models.JSONField(default=dict)
    recommended_training = models.JSONField(default=list)

    def __str__(self):
        return f"TNA Input by {self.manager} for {self.employee_id}"


class TrainingPriority(BaseModel):
    class Priority(models.TextChoices):
        HIGH = "high", "High"
        MEDIUM = "medium", "Medium"
        LOW = "low", "Low"

    cycle = models.ForeignKey(TNACycle, on_delete=models.CASCADE, related_name="priorities")
    competency_name = models.CharField(max_length=200)
    priority = models.CharField(max_length=10, choices=Priority.choices)
    affected_employees_count = models.PositiveIntegerField(default=0)
    department = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Training Priorities"

    def __str__(self):
        return f"{self.competency_name} ({self.priority})"


class LearningPath(BaseModel):
    employee_id = models.UUIDField()
    cycle = models.ForeignKey(TNACycle, on_delete=models.CASCADE, related_name="learning_paths")
    recommended_courses = models.JSONField(default=list)
    development_plan = models.JSONField(default=dict)
    target_completion_date = models.DateField(null=True, blank=True)
    completion_percentage = models.FloatField(default=0)

    def __str__(self):
        return f"Learning Path: {self.employee_id}"


class TNAReport(BaseModel):
    cycle = models.ForeignKey(TNACycle, on_delete=models.CASCADE, related_name="reports")
    summary = models.JSONField(default=dict)
    top_gaps = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TNA Report for {self.cycle}"
