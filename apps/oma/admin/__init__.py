from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.oma.models import (
    OMABenchmark,
    OMABenchmarkDataset,
    OMADomainScore,
    OMAGap,
    OMAMaturityLevel,
    OMANormalizedData,
    OMARisk,
    OMARoadmap,
    OMAStrategyExport,
    OMASurvey,
    OMASurveyQuestion,
    OMASurveyResponse,
    OMAValidationResult,
)


@admin.register(OMASurvey)
class OMASurveyAdmin(ModelAdmin):
    list_display = ("title", "respondent_group", "status", "launch_start", "launch_end")
    list_filter = ("status", "respondent_group")


@admin.register(OMASurveyQuestion)
class OMASurveyQuestionAdmin(ModelAdmin):
    list_display = ("survey", "domain", "question_type", "weight", "order")
    list_filter = ("domain", "question_type")


@admin.register(OMASurveyResponse)
class OMASurveyResponseAdmin(ModelAdmin):
    list_display = ("survey", "respondent", "is_complete", "submitted_at")
    list_filter = ("is_complete",)


@admin.register(OMANormalizedData)
class OMANormalizedDataAdmin(ModelAdmin):
    list_display = ("survey", "version", "created_at")


@admin.register(OMADomainScore)
class OMADomainScoreAdmin(ModelAdmin):
    list_display = ("domain_name", "score", "weight", "calculated_at")
    list_filter = ("domain_name",)


@admin.register(OMAValidationResult)
class OMAValidationResultAdmin(ModelAdmin):
    list_display = ("survey", "rule_name", "result")
    list_filter = ("result",)


@admin.register(OMAMaturityLevel)
class OMAMaturityLevelAdmin(ModelAdmin):
    list_display = ("overall_level", "confirmed", "confirmed_at")
    list_filter = ("overall_level", "confirmed")


@admin.register(OMAGap)
class OMAGapAdmin(ModelAdmin):
    list_display = ("domain_name", "severity", "maturity_driver")
    list_filter = ("severity", "domain_name")


@admin.register(OMARisk)
class OMARiskAdmin(ModelAdmin):
    list_display = ("domain_name", "severity")
    list_filter = ("severity", "domain_name")


@admin.register(OMARoadmap)
class OMARoadmapAdmin(ModelAdmin):
    list_display = ("quarter", "version", "created_by", "created_at")


@admin.register(OMABenchmark)
class OMABenchmarkAdmin(ModelAdmin):
    list_display = ("benchmark_type", "classification_value", "dataset_version")
    list_filter = ("benchmark_type",)


@admin.register(OMABenchmarkDataset)
class OMABenchmarkDatasetAdmin(ModelAdmin):
    list_display = ("name", "version", "source")


@admin.register(OMAStrategyExport)
class OMAStrategyExportAdmin(ModelAdmin):
    list_display = ("maturity_level", "acknowledged", "exported_at")
    list_filter = ("acknowledged",)
