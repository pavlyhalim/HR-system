from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.recruiter.views import (
    BusinessRuleViewSet,
    CandidateViewSet,
    HiringDecisionViewSet,
    InternalMobilityViewSet,
    InterviewIntegrityViewSet,
    InterviewSchedulingViewSet,
    InterviewViewSet,
    JobAdPublicationViewSet,
    JobAdvertisementViewSet,
    PromotionCycleViewSet,
    PromotionViewSet,
    RuleExceptionViewSet,
    SuccessionPlanViewSet,
    VacancyViewSet,
)

router = DefaultRouter()
router.register("vacancies", VacancyViewSet, basename="vacancy")
router.register("job-ads", JobAdvertisementViewSet, basename="job-ad")
router.register("job-ad-publications", JobAdPublicationViewSet, basename="job-ad-publication")
router.register("candidates", CandidateViewSet, basename="candidate")
router.register("interviews", InterviewViewSet, basename="interview")
router.register("integrity", InterviewIntegrityViewSet, basename="integrity")
router.register("scheduling", InterviewSchedulingViewSet, basename="scheduling")
router.register("decisions", HiringDecisionViewSet, basename="decision")
router.register("rules", BusinessRuleViewSet, basename="business-rule")
router.register("rule-exceptions", RuleExceptionViewSet, basename="rule-exception")
router.register("mobility", InternalMobilityViewSet, basename="mobility")
router.register("succession", SuccessionPlanViewSet, basename="succession")
router.register("promotion-cycles", PromotionCycleViewSet, basename="promotion-cycle")
router.register("promotions", PromotionViewSet, basename="promotion")

urlpatterns = [
    path("", include(router.urls)),
]
