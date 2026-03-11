from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.job_description.views import (
    JDCompetencyViewSet,
    JDConsumerReferenceViewSet,
    JobAnalysisInputViewSet,
    JobDescriptionViewSet,
)

router = DefaultRouter()
router.register("job-analysis", JobAnalysisInputViewSet, basename="job-analysis")
router.register("job-descriptions", JobDescriptionViewSet, basename="job-description")
router.register("jd-competencies", JDCompetencyViewSet, basename="jd-competency")
router.register("jd-consumers", JDConsumerReferenceViewSet, basename="jd-consumer")

urlpatterns = [
    path("", include(router.urls)),
]
