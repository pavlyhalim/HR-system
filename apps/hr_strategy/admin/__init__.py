from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.hr_strategy.models import (
    HRStrategy,
    InitiativeDependency,
    StrategicInitiative,
    StrategicPillar,
    StrategyBenchmark,
    StrategyConfidenceLevel,
    StrategyExecutionLink,
    StrategyExplainability,
    StrategyKPI,
    StrategyReadinessScore,
    StrategyRiskAnalysis,
    StrategyRoadmap,
    StrategyVersion,
)


@admin.register(HRStrategy)
class HRStrategyAdmin(ModelAdmin):
    list_display = ("organization_id", "status", "created_by", "created_at")
    list_filter = ("status",)


@admin.register(StrategyVersion)
class StrategyVersionAdmin(ModelAdmin):
    list_display = ("strategy", "version_number", "created_at")


@admin.register(StrategicPillar)
class StrategicPillarAdmin(ModelAdmin):
    list_display = ("name", "strategy_version", "priority")
    list_filter = ("strategy_version",)


@admin.register(StrategicInitiative)
class StrategicInitiativeAdmin(ModelAdmin):
    list_display = ("objective", "pillar", "status", "owner", "timeline_start", "timeline_end")
    list_filter = ("status",)


@admin.register(InitiativeDependency)
class InitiativeDependencyAdmin(ModelAdmin):
    list_display = ("initiative", "depends_on", "dependency_type")


@admin.register(StrategyKPI)
class StrategyKPIAdmin(ModelAdmin):
    list_display = ("kpi_name", "initiative", "target_value", "current_value", "unit")


@admin.register(StrategyRoadmap)
class StrategyRoadmapAdmin(ModelAdmin):
    list_display = ("phase_name", "strategy_version", "start_date", "end_date", "order")


@admin.register(StrategyReadinessScore)
class StrategyReadinessScoreAdmin(ModelAdmin):
    list_display = ("initiative", "readiness_score", "calculated_at")


@admin.register(StrategyConfidenceLevel)
class StrategyConfidenceLevelAdmin(ModelAdmin):
    list_display = ("strategy_version", "confidence_level", "aggregate_readiness", "calculated_at")
    list_filter = ("confidence_level",)


@admin.register(StrategyBenchmark)
class StrategyBenchmarkAdmin(ModelAdmin):
    list_display = ("strategy_version", "benchmark_type", "dataset_version")
    list_filter = ("benchmark_type",)


@admin.register(StrategyExecutionLink)
class StrategyExecutionLinkAdmin(ModelAdmin):
    list_display = ("initiative", "module_name", "execution_status")
    list_filter = ("execution_status",)


@admin.register(StrategyExplainability)
class StrategyExplainabilityAdmin(ModelAdmin):
    list_display = ("entity_type", "entity_id", "created_at")
    list_filter = ("entity_type",)


@admin.register(StrategyRiskAnalysis)
class StrategyRiskAnalysisAdmin(ModelAdmin):
    list_display = ("initiative", "risk_type", "severity")
    list_filter = ("risk_type", "severity")
