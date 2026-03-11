from rest_framework import serializers

from apps.payroll.models import (
    BankFile,
    PayrollCycle,
    PayrollRecord,
    Payslip,
    SalaryStructure,
    TaxReport,
)


class SalaryStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryStructure
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class PayrollCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollCycle
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "total_gross", "total_deductions", "total_net")


class PayrollRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollRecord
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class PayslipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslip
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "generated_at")


class TaxReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxReport
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "generated_at")


class BankFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankFile
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "generated_at")
