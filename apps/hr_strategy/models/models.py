from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class HRStrategy(BaseModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    organization_id = models.CharField(max_length=100, blank=True)
    current_version = models.OneToOneField("StrategyVersion", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name_plural = "HR Strategies"

    def __str__(self):
        return f"HR Strategy ({self.status})"


class StrategyVersion(BaseModel):
    strategy = models.ForeignKey(HRStrategy, on_delete=models.CASCADE, related_name="versions")
    version_number = models.PositiveIntegerField(default=1)

    class Meta(BaseModel.Meta):
        unique_together = ("strategy", "version_number")

    def __str__(self):
        return f"Strategy v{self.version_number}"


class StrategicPillar(BaseModel):
    strategy_version = models.ForeignKey(StrategyVersion, on_delete=models.CASCADE, related_name="pillars")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.PositiveIntegerField(default=1)
    business_objective = models.TextField(blank=True)

    class Meta:
        ordering = ["priority"]

    def __str__(self):
        return self.name


class StrategicInitiative(BaseModel):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"

    pillar = models.ForeignKey(StrategicPillar, on_delete=models.CASCADE, related_name="initiatives")
    objective = models.TextField()
    scope = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timeline_start = models.DateField(null=True, blank=True)
    timeline_end = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)

    def __str__(self):
        return f"{self.objective[:60]}"


class InitiativeDependency(BaseModel):
    initiative = models.ForeignKey(StrategicInitiative, on_delete=models.CASCADE, related_name="dependencies")
    depends_on = models.ForeignKey(StrategicInitiative, on_delete=models.CASCADE, related_name="dependents")
    dependency_type = models.CharField(max_length=50, default="blocks")

    class Meta:
        unique_together = ("initiative", "depends_on")

    def __str__(self):
        return f"{self.initiative} → {self.depends_on}"


class StrategyKPI(BaseModel):
    initiative = models.ForeignKey(StrategicInitiative, on_delete=models.CASCADE, related_name="kpis")
    kpi_name = models.CharField(max_length=200)
    target_value = models.FloatField(null=True, blank=True)
    current_value = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    measurement_frequency = models.CharField(max_length=50, default="monthly")

    def __str__(self):
        return self.kpi_name


class StrategyRoadmap(BaseModel):
    strategy_version = models.ForeignKey(StrategyVersion, on_delete=models.CASCADE, related_name="roadmaps")
    phase_name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    milestones = models.JSONField(default=list)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.phase_name


class StrategyReadinessScore(BaseModel):
    initiative = models.ForeignKey(StrategicInitiative, on_delete=models.CASCADE, related_name="readiness_scores")
    readiness_score = models.FloatField(help_text="0-100")
    scoring_breakdown = models.JSONField(default=dict, help_text="maturity, capability, culture, resources")
    calculated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Readiness: {self.readiness_score} for {self.initiative}"


class StrategyConfidenceLevel(BaseModel):
    class Confidence(models.TextChoices):
        HIGH = "high", "High"
        MEDIUM = "medium", "Medium"
        LOW = "low", "Low"

    strategy_version = models.ForeignKey(StrategyVersion, on_delete=models.CASCADE, related_name="confidence_levels")
    confidence_level = models.CharField(max_length=10, choices=Confidence.choices)
    aggregate_readiness = models.FloatField(default=0)
    calculated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Confidence: {self.confidence_level}"


class StrategyBenchmark(BaseModel):
    class BenchmarkType(models.TextChoices):
        INDUSTRY = "industry", "Industry"
        SIZE = "size", "Company Size"
        REGION = "region", "Region"

    strategy_version = models.ForeignKey(StrategyVersion, on_delete=models.CASCADE, related_name="benchmarks")
    benchmark_type = models.CharField(max_length=20, choices=BenchmarkType.choices)
    variance_data = models.JSONField(default=dict)
    dataset_version = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Benchmark: {self.benchmark_type}"


class StrategyExecutionLink(BaseModel):
    class ExecutionStatus(models.TextChoices):
        LINKED = "linked", "Linked"
        ACTIVE = "active", "Active"
        BROKEN = "broken", "Broken"
        INACTIVE = "inactive", "Inactive"

    initiative = models.ForeignKey(StrategicInitiative, on_delete=models.CASCADE, related_name="execution_links")
    module_name = models.CharField(max_length=100, help_text="e.g. recruitment, performance, tna")
    execution_status = models.CharField(max_length=20, choices=ExecutionStatus.choices, default=ExecutionStatus.LINKED)
    execution_data = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.initiative} → {self.module_name} ({self.execution_status})"


class StrategyExplainability(BaseModel):
    entity_type = models.CharField(max_length=50, help_text="pillar / initiative")
    entity_id = models.UUIDField()
    explanation_text = models.TextField()
    data_sources = models.JSONField(default=list)

    class Meta:
        indexes = [models.Index(fields=["entity_type", "entity_id"])]

    def __str__(self):
        return f"Explanation: {self.entity_type} #{self.entity_id}"


class StrategyRiskAnalysis(BaseModel):
    class RiskType(models.TextChoices):
        OPERATIONAL = "operational", "Operational"
        TALENT = "talent", "Talent"
        FINANCIAL = "financial", "Financial"

    class Severity(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    initiative = models.ForeignKey(StrategicInitiative, on_delete=models.CASCADE, related_name="risks")
    risk_type = models.CharField(max_length=20, choices=RiskType.choices)
    severity = models.CharField(max_length=10, choices=Severity.choices)
    impact_description = models.TextField()
    mitigation = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Strategy Risk Analyses"

    def __str__(self):
        return f"Risk: {self.risk_type} ({self.severity})"
