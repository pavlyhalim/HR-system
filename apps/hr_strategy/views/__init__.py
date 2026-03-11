from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import IsHR
from apps.core.services import AIProxyService
from apps.hr_strategy.models import (
    HRStrategy,
    InitiativeDependency,
    StrategicInitiative,
    StrategicPillar,
    StrategyBenchmark,
    StrategyConfidenceLevel,
    StrategyExecutionLink,
    StrategyExplainability,
    StrategyKPI,
    StrategyReadinessScore,
    StrategyRiskAnalysis,
    StrategyRoadmap,
    StrategyVersion,
)
from apps.hr_strategy.serializers import (
    HRStrategySerializer,
    InitiativeDependencySerializer,
    StrategicInitiativeSerializer,
    StrategicPillarSerializer,
    StrategyBenchmarkSerializer,
    StrategyConfidenceLevelSerializer,
    StrategyExecutionLinkSerializer,
    StrategyExplainabilitySerializer,
    StrategyKPISerializer,
    StrategyReadinessScoreSerializer,
    StrategyRiskAnalysisSerializer,
    StrategyRoadmapSerializer,
    StrategyVersionSerializer,
)


class HRStrategyViewSet(viewsets.ModelViewSet):
    queryset = HRStrategy.objects.filter(is_active=True)
    serializer_class = HRStrategySerializer
    permission_classes = [IsHR]
    filterset_fields = ["status"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], url_path="version")
    def create_version(self, request, pk=None):
        strategy = self.get_object()
        last_version = strategy.versions.order_by("-version_number").first()
        new_num = (last_version.version_number + 1) if last_version else 1
        version = StrategyVersion.objects.create(strategy=strategy, version_number=new_num)
        strategy.current_version = version
        strategy.save(update_fields=["current_version", "updated_at"])
        return Response(StrategyVersionSerializer(version).data, status=status.HTTP_201_CREATED)


class StrategyVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StrategyVersion.objects.all()
    serializer_class = StrategyVersionSerializer
    permission_classes = [IsHR]
    filterset_fields = ["strategy"]


class StrategicPillarViewSet(viewsets.ModelViewSet):
    queryset = StrategicPillar.objects.filter(is_active=True)
    serializer_class = StrategicPillarSerializer
    permission_classes = [IsHR]
    filterset_fields = ["strategy_version"]
    ordering_fields = ["priority"]


class StrategicInitiativeViewSet(viewsets.ModelViewSet):
    queryset = StrategicInitiative.objects.filter(is_active=True).select_related("pillar")
    serializer_class = StrategicInitiativeSerializer
    permission_classes = [IsHR]
    filterset_fields = ["status", "pillar"]

    @action(detail=True, methods=["patch"], url_path="status")
    def change_status(self, request, pk=None):
        initiative = self.get_object()
        new_status = request.data.get("status")
        if new_status not in dict(StrategicInitiative.Status.choices):
            return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
        initiative.status = new_status
        initiative.save(update_fields=["status", "updated_at"])
        return Response(StrategicInitiativeSerializer(initiative).data)

    @action(detail=True, methods=["post"], url_path="link-module")
    def link_module(self, request, pk=None):
        initiative = self.get_object()
        link = StrategyExecutionLink.objects.create(
            initiative=initiative,
            module_name=request.data.get("module_name", ""),
        )
        return Response(StrategyExecutionLinkSerializer(link).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="execution-status")
    def execution_status(self, request, pk=None):
        links = StrategyExecutionLink.objects.filter(initiative=self.get_object())
        return Response(StrategyExecutionLinkSerializer(links, many=True).data)

    @action(detail=True, methods=["get"], url_path="readiness")
    def readiness(self, request, pk=None):
        scores = StrategyReadinessScore.objects.filter(initiative=self.get_object()).order_by("-calculated_at")
        return Response(StrategyReadinessScoreSerializer(scores, many=True).data)

    @action(detail=True, methods=["get"], url_path="risk")
    def risk(self, request, pk=None):
        risks = StrategyRiskAnalysis.objects.filter(initiative=self.get_object())
        return Response(StrategyRiskAnalysisSerializer(risks, many=True).data)


class InitiativeDependencyViewSet(viewsets.ModelViewSet):
    queryset = InitiativeDependency.objects.all()
    serializer_class = InitiativeDependencySerializer
    permission_classes = [IsHR]


class StrategyKPIViewSet(viewsets.ModelViewSet):
    queryset = StrategyKPI.objects.filter(is_active=True)
    serializer_class = StrategyKPISerializer
    permission_classes = [IsHR]
    filterset_fields = ["initiative"]


class StrategyRoadmapViewSet(viewsets.ModelViewSet):
    queryset = StrategyRoadmap.objects.filter(is_active=True)
    serializer_class = StrategyRoadmapSerializer
    permission_classes = [IsHR]
    filterset_fields = ["strategy_version"]


class StrategyReadinessViewSet(viewsets.ModelViewSet):
    queryset = StrategyReadinessScore.objects.all()
    serializer_class = StrategyReadinessScoreSerializer
    permission_classes = [IsHR]

    @action(detail=False, methods=["post"], url_path="calculate")
    def calculate(self, request):
        initiative_id = request.data.get("initiative_id")
        result = AIProxyService.generate_hr_strategy({}, {})
        score = StrategyReadinessScore.objects.create(
            initiative_id=initiative_id,
            readiness_score=result.get("readiness_score", 50),
            scoring_breakdown=result,
        )
        return Response(StrategyReadinessScoreSerializer(score).data, status=status.HTTP_201_CREATED)


class StrategyConfidenceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StrategyConfidenceLevel.objects.all()
    serializer_class = StrategyConfidenceLevelSerializer
    permission_classes = [IsHR]
    filterset_fields = ["strategy_version", "confidence_level"]


class StrategyBenchmarkViewSet(viewsets.ModelViewSet):
    queryset = StrategyBenchmark.objects.filter(is_active=True)
    serializer_class = StrategyBenchmarkSerializer
    permission_classes = [IsHR]
    filterset_fields = ["benchmark_type"]

    @action(detail=False, methods=["post"], url_path="run")
    def run_benchmark(self, request):
        version_id = request.data.get("strategy_version_id")
        benchmark = StrategyBenchmark.objects.create(
            strategy_version_id=version_id,
            benchmark_type=request.data.get("type", "industry"),
            variance_data={"overall": "at_benchmark"},
        )
        return Response(StrategyBenchmarkSerializer(benchmark).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="report")
    def report(self, request):
        version_id = request.query_params.get("strategy_version_id")
        benchmarks = StrategyBenchmark.objects.filter(strategy_version_id=version_id)
        return Response(StrategyBenchmarkSerializer(benchmarks, many=True).data)


class StrategyExplainabilityViewSet(viewsets.ModelViewSet):
    queryset = StrategyExplainability.objects.filter(is_active=True)
    serializer_class = StrategyExplainabilitySerializer
    permission_classes = [IsHR]
    filterset_fields = ["entity_type"]


class StrategyRiskViewSet(viewsets.ModelViewSet):
    queryset = StrategyRiskAnalysis.objects.filter(is_active=True)
    serializer_class = StrategyRiskAnalysisSerializer
    permission_classes = [IsHR]
    filterset_fields = ["risk_type", "severity", "initiative"]
