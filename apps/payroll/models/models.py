from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class SalaryStructure(BaseModel):
    employee_id = models.UUIDField(help_text="FK to employee_lifecycle.Employee")
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    allowances = models.JSONField(default=dict)
    currency = models.CharField(max_length=3, default="SAR")
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Salary: {self.employee_id} - {self.basic_salary} {self.currency}"


class PayrollCycle(BaseModel):
    class Status(models.TextChoices):
        INITIATED = "initiated", "Initiated"
        VALIDATED = "validated", "Validated"
        CALCULATED = "calculated", "Calculated"
        APPROVED = "approved", "Approved"
        EXECUTED = "executed", "Executed"
        ARCHIVED = "archived", "Archived"

    cycle_name = models.CharField(max_length=200)
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INITIATED)
    total_gross = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_net = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    executed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.cycle_name


class PayrollRecord(BaseModel):
    cycle = models.ForeignKey(PayrollCycle, on_delete=models.CASCADE, related_name="records")
    employee_id = models.UUIDField()
    gross_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deductions = models.JSONField(default=dict)
    taxes = models.JSONField(default=dict)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    anomaly_flagged = models.BooleanField(default=False)
    anomaly_details = models.TextField(blank=True)

    class Meta:
        unique_together = ("cycle", "employee_id")

    def __str__(self):
        return f"Payroll: {self.employee_id} - {self.net_pay}"


class Payslip(BaseModel):
    record = models.OneToOneField(PayrollRecord, on_delete=models.CASCADE, related_name="payslip")
    payslip_data = models.JSONField(default=dict)
    generated_at = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"Payslip: {self.record}"


class TaxReport(BaseModel):
    cycle = models.ForeignKey(PayrollCycle, on_delete=models.CASCADE, related_name="tax_reports")
    report_data = models.JSONField(default=dict)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tax Report: {self.cycle}"


class BankFile(BaseModel):
    cycle = models.ForeignKey(PayrollCycle, on_delete=models.CASCADE, related_name="bank_files")
    file_type = models.CharField(max_length=50, default="bank_transfer")
    file_path = models.CharField(max_length=500, blank=True)
    file_data = models.JSONField(default=dict)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bank File: {self.cycle} ({self.file_type})"
