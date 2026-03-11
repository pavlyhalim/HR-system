from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.oma.views import (
    OMABenchmarkDatasetViewSet,
    OMABenchmarkViewSet,
    OMADomainScoreViewSet,
    OMAGapViewSet,
    OMAMaturityLevelViewSet,
    OMANormalizationViewSet,
    OMARiskViewSet,
    OMARoadmapViewSet,
    OMAStrategyExportViewSet,
    OMASurveyQuestionViewSet,
    OMASurveyResponseViewSet,
    OMASurveyViewSet,
    OMAValidationViewSet,
)

router = DefaultRouter()
router.register("surveys", OMASurveyViewSet, basename="oma-survey")
router.register("questions", OMASurveyQuestionViewSet, basename="oma-question")
router.register("responses", OMASurveyResponseViewSet, basename="oma-response")
router.register("normalization", OMANormalizationViewSet, basename="oma-normalization")
router.register("domain-scores", OMADomainScoreViewSet, basename="oma-domain-score")
router.register("validation", OMAValidationViewSet, basename="oma-validation")
router.register("maturity", OMAMaturityLevelViewSet, basename="oma-maturity")
router.register("gaps", OMAGapViewSet, basename="oma-gap")
router.register("risks", OMARiskViewSet, basename="oma-risk")
router.register("roadmaps", OMARoadmapViewSet, basename="oma-roadmap")
router.register("benchmarks", OMABenchmarkViewSet, basename="oma-benchmark")
router.register("benchmark-datasets", OMABenchmarkDatasetViewSet, basename="oma-benchmark-dataset")
router.register("strategy-exports", OMAStrategyExportViewSet, basename="oma-strategy-export")

urlpatterns = [
    path("", include(router.urls)),
]
