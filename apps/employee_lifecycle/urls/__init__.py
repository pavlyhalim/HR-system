from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.employee_lifecycle.views import (
    ApprovalRequestViewSet,
    ContractViewSet,
    EmployeePersonalDataViewSet,
    EmployeeViewSet,
    FinalSettlementViewSet,
    OfferTemplateViewSet,
    OfferViewSet,
    OffboardingViewSet,
    OnboardingTaskViewSet,
    OnboardingViewSet,
    PreboardingViewSet,
    ProbationViewSet,
)

router = DefaultRouter()
router.register("employees", EmployeeViewSet, basename="employee")
router.register("preboarding", PreboardingViewSet, basename="preboarding")
router.register("offer-templates", OfferTemplateViewSet, basename="offer-template")
router.register("offers", OfferViewSet, basename="offer")
router.register("contracts", ContractViewSet, basename="contract")
router.register("personal-data", EmployeePersonalDataViewSet, basename="personal-data")
router.register("onboarding", OnboardingViewSet, basename="onboarding")
router.register("onboarding-tasks", OnboardingTaskViewSet, basename="onboarding-task")
router.register("probation", ProbationViewSet, basename="probation")
router.register("offboarding", OffboardingViewSet, basename="offboarding")
router.register("settlements", FinalSettlementViewSet, basename="settlement")
router.register("approvals", ApprovalRequestViewSet, basename="approval")

urlpatterns = [
    path("", include(router.urls)),
]
