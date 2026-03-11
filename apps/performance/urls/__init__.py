from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.performance.views import (
    CalibrationSessionViewSet,
    FinalRatingViewSet,
    GoalCascadeViewSet,
    PerformanceFrameworkViewSet,
    PerformanceReviewViewSet,
    ReviewCycleViewSet,
)

router = DefaultRouter()
router.register("frameworks", PerformanceFrameworkViewSet, basename="framework")
router.register("cycles", ReviewCycleViewSet, basename="review-cycle")
router.register("goals", GoalCascadeViewSet, basename="goal")
router.register("reviews", PerformanceReviewViewSet, basename="review")
router.register("calibrations", CalibrationSessionViewSet, basename="calibration")
router.register("ratings", FinalRatingViewSet, basename="rating")

urlpatterns = [
    path("", include(router.urls)),
]
