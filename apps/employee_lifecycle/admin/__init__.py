from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.employee_lifecycle.models import (
    ApprovalAction,
    ApprovalRequest,
    Contract,
    ContractSignature,
    ContractVersion,
    Employee,
    EmployeeLifecycleState,
    EmployeePersonalData,
    FinalSettlement,
    Offer,
    OfferTemplate,
    OffboardingRecord,
    OnboardingChecklist,
    OnboardingTask,
    ProbationRecord,
)


@admin.register(Employee)
class EmployeeAdmin(ModelAdmin):
    list_display = ("employee_number", "user", "employment_status", "department", "position", "hire_date")
    list_filter = ("employment_status", "department", "country_code")
    search_fields = ("employee_number", "user__email")


@admin.register(EmployeeLifecycleState)
class EmployeeLifecycleStateAdmin(ModelAdmin):
    list_display = ("employee", "state", "entered_at", "exited_at")
    list_filter = ("state",)


@admin.register(OfferTemplate)
class OfferTemplateAdmin(ModelAdmin):
    list_display = ("template_name", "version", "created_at")


@admin.register(Offer)
class OfferAdmin(ModelAdmin):
    list_display = ("employee", "role_title", "status", "approved_at", "sent_at", "accepted_at")
    list_filter = ("status",)


@admin.register(Contract)
class ContractAdmin(ModelAdmin):
    list_display = ("employee", "contract_type", "country_code", "status", "start_date", "end_date")
    list_filter = ("contract_type", "status")


@admin.register(ContractVersion)
class ContractVersionAdmin(ModelAdmin):
    list_display = ("contract", "version_number", "created_at")


@admin.register(ContractSignature)
class ContractSignatureAdmin(ModelAdmin):
    list_display = ("contract", "signed_by", "signed_at", "signature_provider")


@admin.register(EmployeePersonalData)
class EmployeePersonalDataAdmin(ModelAdmin):
    list_display = ("employee", "status", "updated_at")
    list_filter = ("status",)


@admin.register(OnboardingChecklist)
class OnboardingChecklistAdmin(ModelAdmin):
    list_display = ("employee", "total_tasks", "completed_tasks", "is_completed")


@admin.register(OnboardingTask)
class OnboardingTaskAdmin(ModelAdmin):
    list_display = ("task_name", "checklist", "task_type", "status", "assigned_to_role", "due_date")
    list_filter = ("task_type", "status")


@admin.register(ProbationRecord)
class ProbationRecordAdmin(ModelAdmin):
    list_display = ("employee", "start_date", "end_date", "status", "decided_at")
    list_filter = ("status",)


@admin.register(OffboardingRecord)
class OffboardingRecordAdmin(ModelAdmin):
    list_display = ("employee", "exit_type", "status", "last_working_day", "completed_at")
    list_filter = ("exit_type", "status")


@admin.register(FinalSettlement)
class FinalSettlementAdmin(ModelAdmin):
    list_display = ("employee", "total_amount", "approval_status", "approved_at", "executed_at")
    list_filter = ("approval_status",)


@admin.register(ApprovalRequest)
class ApprovalRequestAdmin(ModelAdmin):
    list_display = ("entity_type", "entity_id", "status", "requested_by", "current_step", "created_at")
    list_filter = ("entity_type", "status")


@admin.register(ApprovalAction)
class ApprovalActionAdmin(ModelAdmin):
    list_display = ("approval_request", "action", "actor", "step_number", "created_at")
    list_filter = ("action",)
