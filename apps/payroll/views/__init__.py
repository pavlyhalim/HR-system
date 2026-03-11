from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import IsHR
from apps.payroll.models import (
    BankFile,
    PayrollCycle,
    PayrollRecord,
    Payslip,
    SalaryStructure,
    TaxReport,
)
from apps.payroll.serializers import (
    BankFileSerializer,
    PayrollCycleSerializer,
    PayrollRecordSerializer,
    PayslipSerializer,
    SalaryStructureSerializer,
    TaxReportSerializer,
)


class SalaryStructureViewSet(viewsets.ModelViewSet):
    queryset = SalaryStructure.objects.filter(is_active=True)
    serializer_class = SalaryStructureSerializer
    permission_classes = [IsHR]
    filterset_fields = ["currency"]


class PayrollCycleViewSet(viewsets.ModelViewSet):
    queryset = PayrollCycle.objects.filter(is_active=True)
    serializer_class = PayrollCycleSerializer
    permission_classes = [IsHR]
    filterset_fields = ["status"]

    @action(detail=True, methods=["post"], url_path="validate")
    def validate_cycle(self, request, pk=None):
        cycle = self.get_object()
        cycle.status = PayrollCycle.Status.VALIDATED
        cycle.save(update_fields=["status", "updated_at"])
        return Response(PayrollCycleSerializer(cycle).data)

    @action(detail=True, methods=["post"], url_path="calculate")
    def calculate(self, request, pk=None):
        cycle = self.get_object()
        records = PayrollRecord.objects.filter(cycle=cycle)
        cycle.total_gross = sum(r.gross_pay for r in records)
        cycle.total_deductions = sum(sum(r.deductions.values()) for r in records if isinstance(r.deductions, dict))
        cycle.total_net = sum(r.net_pay for r in records)
        cycle.status = PayrollCycle.Status.CALCULATED
        cycle.save()
        return Response(PayrollCycleSerializer(cycle).data)

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        cycle = self.get_object()
        cycle.status = PayrollCycle.Status.APPROVED
        cycle.approved_by = request.user
        cycle.approved_at = timezone.now()
        cycle.save(update_fields=["status", "approved_by", "approved_at", "updated_at"])
        return Response(PayrollCycleSerializer(cycle).data)

    @action(detail=True, methods=["post"], url_path="execute")
    def execute(self, request, pk=None):
        cycle = self.get_object()
        if cycle.status != PayrollCycle.Status.APPROVED:
            return Response({"detail": "Only approved cycles can be executed."}, status=status.HTTP_400_BAD_REQUEST)
        cycle.status = PayrollCycle.Status.EXECUTED
        cycle.executed_at = timezone.now()
        cycle.save(update_fields=["status", "executed_at", "updated_at"])
        return Response(PayrollCycleSerializer(cycle).data)

    @action(detail=True, methods=["post"], url_path="generate-payslips")
    def generate_payslips(self, request, pk=None):
        cycle = self.get_object()
        records = PayrollRecord.objects.filter(cycle=cycle)
        created = 0
        for record in records:
            _, was_created = Payslip.objects.get_or_create(
                record=record,
                defaults={"payslip_data": {"gross": str(record.gross_pay), "net": str(record.net_pay)}},
            )
            if was_created:
                created += 1
        return Response({"detail": f"{created} payslips generated."})

    @action(detail=True, methods=["post"], url_path="generate-bank-file")
    def generate_bank_file(self, request, pk=None):
        cycle = self.get_object()
        bank_file = BankFile.objects.create(
            cycle=cycle,
            file_data={"records": PayrollRecord.objects.filter(cycle=cycle).count()},
        )
        return Response(BankFileSerializer(bank_file).data, status=status.HTTP_201_CREATED)


class PayrollRecordViewSet(viewsets.ModelViewSet):
    queryset = PayrollRecord.objects.all()
    serializer_class = PayrollRecordSerializer
    permission_classes = [IsHR]
    filterset_fields = ["cycle", "anomaly_flagged"]


class PayslipViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payslip.objects.all()
    serializer_class = PayslipSerializer
    permission_classes = [IsHR]


class TaxReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaxReport.objects.all()
    serializer_class = TaxReportSerializer
    permission_classes = [IsHR]


class BankFileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BankFile.objects.all()
    serializer_class = BankFileSerializer
    permission_classes = [IsHR]
