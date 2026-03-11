from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.payroll.models import (
    BankFile,
    PayrollCycle,
    PayrollRecord,
    Payslip,
    SalaryStructure,
    TaxReport,
)


@admin.register(SalaryStructure)
class SalaryStructureAdmin(ModelAdmin):
    list_display = ("employee_id", "basic_salary", "currency", "effective_from", "effective_to")
    list_filter = ("currency",)


@admin.register(PayrollCycle)
class PayrollCycleAdmin(ModelAdmin):
    list_display = ("cycle_name", "status", "period_start", "period_end", "total_net", "executed_at")
    list_filter = ("status",)


@admin.register(PayrollRecord)
class PayrollRecordAdmin(ModelAdmin):
    list_display = ("employee_id", "cycle", "gross_pay", "net_pay", "anomaly_flagged")
    list_filter = ("anomaly_flagged",)


@admin.register(Payslip)
class PayslipAdmin(ModelAdmin):
    list_display = ("record", "generated_at")


@admin.register(TaxReport)
class TaxReportAdmin(ModelAdmin):
    list_display = ("cycle", "generated_at")


@admin.register(BankFile)
class BankFileAdmin(ModelAdmin):
    list_display = ("cycle", "file_type", "generated_at")
