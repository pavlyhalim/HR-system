from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.hr_strategy.views import (
    HRStrategyViewSet,
    InitiativeDependencyViewSet,
    StrategicInitiativeViewSet,
    StrategicPillarViewSet,
    StrategyBenchmarkViewSet,
    StrategyConfidenceViewSet,
    StrategyExplainabilityViewSet,
    StrategyKPIViewSet,
    StrategyReadinessViewSet,
    StrategyRiskViewSet,
    StrategyRoadmapViewSet,
    StrategyVersionViewSet,
)

router = DefaultRouter()
router.register("strategies", HRStrategyViewSet, basename="strategy")
router.register("versions", StrategyVersionViewSet, basename="strategy-version")
router.register("pillars", StrategicPillarViewSet, basename="pillar")
router.register("initiatives", StrategicInitiativeViewSet, basename="initiative")
router.register("dependencies", InitiativeDependencyViewSet, basename="dependency")
router.register("kpis", StrategyKPIViewSet, basename="kpi")
router.register("roadmaps", StrategyRoadmapViewSet, basename="roadmap")
router.register("readiness", StrategyReadinessViewSet, basename="readiness")
router.register("confidence", StrategyConfidenceViewSet, basename="confidence")
router.register("benchmarks", StrategyBenchmarkViewSet, basename="benchmark")
router.register("explainability", StrategyExplainabilityViewSet, basename="explainability")
router.register("risks", StrategyRiskViewSet, basename="risk")

urlpatterns = [
    path("", include(router.urls)),
]
