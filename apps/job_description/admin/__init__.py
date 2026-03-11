from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.job_description.models import (
    JDApprovalLog,
    JDBenchmarkResult,
    JDCompetency,
    JDConsumerReference,
    JobAnalysisInput,
    JobDescription,
    JobDescriptionVersion,
)


@admin.register(JobAnalysisInput)
class JobAnalysisInputAdmin(ModelAdmin):
    list_display = ("role_title", "department", "status", "created_by", "created_at")
    list_filter = ("status", "department")
    search_fields = ("role_title", "department")


@admin.register(JobDescription)
class JobDescriptionAdmin(ModelAdmin):
    list_display = ("__str__", "status", "created_by", "approved_by", "approved_at", "created_at")
    list_filter = ("status",)
    search_fields = ("id",)


@admin.register(JobDescriptionVersion)
class JobDescriptionVersionAdmin(ModelAdmin):
    list_display = ("__str__", "version_number", "created_at")
    list_filter = ("version_number",)


@admin.register(JDCompetency)
class JDCompetencyAdmin(ModelAdmin):
    list_display = ("competency_name", "proficiency_level", "weight", "is_mandatory", "jd_version")
    list_filter = ("proficiency_level", "is_mandatory")
    search_fields = ("competency_name",)


@admin.register(JDBenchmarkResult)
class JDBenchmarkResultAdmin(ModelAdmin):
    list_display = ("jd_version", "benchmark_source", "created_at")
    list_filter = ("benchmark_source",)


@admin.register(JDApprovalLog)
class JDApprovalLogAdmin(ModelAdmin):
    list_display = ("jd_version", "action", "actor", "created_at")
    list_filter = ("action",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(JDConsumerReference)
class JDConsumerReferenceAdmin(ModelAdmin):
    list_display = ("jd_version", "consumer_service", "reference_type", "referenced_at")
    list_filter = ("consumer_service", "reference_type")
