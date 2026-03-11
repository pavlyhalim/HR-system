from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.tna.views import (
    LearningPathViewSet,
    ManagerTNAInputViewSet,
    SkillGapAnalysisViewSet,
    TNACycleViewSet,
    TNAReportViewSet,
    TrainingPriorityViewSet,
)

router = DefaultRouter()
router.register("cycles", TNACycleViewSet, basename="tna-cycle")
router.register("skill-gaps", SkillGapAnalysisViewSet, basename="skill-gap")
router.register("manager-inputs", ManagerTNAInputViewSet, basename="manager-input")
router.register("priorities", TrainingPriorityViewSet, basename="training-priority")
router.register("learning-paths", LearningPathViewSet, basename="learning-path")
router.register("reports", TNAReportViewSet, basename="tna-report")

urlpatterns = [
    path("", include(router.urls)),
]
