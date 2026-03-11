from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.performance.models import (
    BiasDetectionResult,
    CalibrationSession,
    FinalRating,
    GoalCascade,
    PerformanceFramework,
    PerformanceReview,
    ReviewCycle,
)


@admin.register(PerformanceFramework)
class PerformanceFrameworkAdmin(ModelAdmin):
    list_display = ("name", "created_by", "created_at")


@admin.register(ReviewCycle)
class ReviewCycleAdmin(ModelAdmin):
    list_display = ("cycle_name", "framework", "status", "start_date", "end_date")
    list_filter = ("status",)


@admin.register(GoalCascade)
class GoalCascadeAdmin(ModelAdmin):
    list_display = ("kpi_name", "employee_id", "cycle", "kpi_target", "weight")


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(ModelAdmin):
    list_display = ("employee_id", "cycle", "status", "overall_score", "submitted_at")
    list_filter = ("status",)


@admin.register(BiasDetectionResult)
class BiasDetectionResultAdmin(ModelAdmin):
    list_display = ("review", "bias_type", "confidence")


@admin.register(CalibrationSession)
class CalibrationSessionAdmin(ModelAdmin):
    list_display = ("cycle", "department", "status", "calibrated_by", "completed_at")
    list_filter = ("status",)


@admin.register(FinalRating)
class FinalRatingAdmin(ModelAdmin):
    list_display = ("review", "rating", "rating_label", "calibrated", "approved_at")
    list_filter = ("calibrated",)
