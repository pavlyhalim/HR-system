from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.payroll.views import (
    BankFileViewSet,
    PayrollCycleViewSet,
    PayrollRecordViewSet,
    PayslipViewSet,
    SalaryStructureViewSet,
    TaxReportViewSet,
)

router = DefaultRouter()
router.register("salary-structures", SalaryStructureViewSet, basename="salary-structure")
router.register("cycles", PayrollCycleViewSet, basename="payroll-cycle")
router.register("records", PayrollRecordViewSet, basename="payroll-record")
router.register("payslips", PayslipViewSet, basename="payslip")
router.register("tax-reports", TaxReportViewSet, basename="tax-report")
router.register("bank-files", BankFileViewSet, basename="bank-file")

urlpatterns = [
    path("", include(router.urls)),
]
