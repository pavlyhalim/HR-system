from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.tna.models import (
    LearningPath,
    ManagerTNAInput,
    SkillGapAnalysis,
    TNACycle,
    TNAReport,
    TrainingPriority,
)


@admin.register(TNACycle)
class TNACycleAdmin(ModelAdmin):
    list_display = ("cycle_name", "cycle_type", "status", "start_date", "end_date")
    list_filter = ("status", "cycle_type")


@admin.register(SkillGapAnalysis)
class SkillGapAnalysisAdmin(ModelAdmin):
    list_display = ("employee_id", "cycle", "gap_severity")
    list_filter = ("gap_severity",)


@admin.register(ManagerTNAInput)
class ManagerTNAInputAdmin(ModelAdmin):
    list_display = ("manager", "employee_id", "cycle")


@admin.register(TrainingPriority)
class TrainingPriorityAdmin(ModelAdmin):
    list_display = ("competency_name", "priority", "affected_employees_count", "department")
    list_filter = ("priority",)


@admin.register(LearningPath)
class LearningPathAdmin(ModelAdmin):
    list_display = ("employee_id", "cycle", "completion_percentage", "target_completion_date")


@admin.register(TNAReport)
class TNAReportAdmin(ModelAdmin):
    list_display = ("cycle", "generated_at")
