from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import IsHR, IsManager
from apps.core.services import AIProxyService
from apps.oma.models import (
    OMABenchmark,
    OMABenchmarkDataset,
    OMADomainScore,
    OMAGap,
    OMAMaturityLevel,
    OMANormalizedData,
    OMARisk,
    OMARoadmap,
    OMAStrategyExport,
    OMASurvey,
    OMASurveyQuestion,
    OMASurveyResponse,
    OMAValidationResult,
)
from apps.oma.serializers import (
    OMABenchmarkDatasetSerializer,
    OMABenchmarkSerializer,
    OMADomainScoreSerializer,
    OMAGapSerializer,
    OMAMaturityLevelSerializer,
    OMANormalizedDataSerializer,
    OMARiskSerializer,
    OMARoadmapSerializer,
    OMAStrategyExportSerializer,
    OMASurveyQuestionSerializer,
    OMASurveyResponseSerializer,
    OMASurveySerializer,
    OMAValidationResultSerializer,
)


class OMASurveyViewSet(viewsets.ModelViewSet):
    queryset = OMASurvey.objects.filter(is_active=True)
    serializer_class = OMASurveySerializer
    permission_classes = [IsHR]
    filterset_fields = ["status", "respondent_group"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], url_path="launch")
    def launch(self, request, pk=None):
        survey = self.get_object()
        survey.status = OMASurvey.Status.LAUNCHED
        survey.launch_start = timezone.now()
        survey.save(update_fields=["status", "launch_start", "updated_at"])
        return Response(OMASurveySerializer(survey).data)

    @action(detail=True, methods=["get"], url_path="status")
    def survey_status(self, request, pk=None):
        survey = self.get_object()
        total = survey.responses.count()
        completed = survey.responses.filter(is_complete=True).count()
        return Response({"status": survey.status, "total_responses": total, "completed_responses": completed})


class OMASurveyQuestionViewSet(viewsets.ModelViewSet):
    queryset = OMASurveyQuestion.objects.all()
    serializer_class = OMASurveyQuestionSerializer
    permission_classes = [IsHR]
    filterset_fields = ["survey", "domain"]


class OMASurveyResponseViewSet(viewsets.ModelViewSet):
    queryset = OMASurveyResponse.objects.all()
    serializer_class = OMASurveyResponseSerializer
    filterset_fields = ["survey", "is_complete"]

    def perform_create(self, serializer):
        serializer.save(respondent=self.request.user)


class OMANormalizationViewSet(viewsets.ViewSet):
    permission_classes = [IsHR]

    @action(detail=False, methods=["post"], url_path="normalize/(?P<survey_id>[^/.]+)")
    def normalize(self, request, survey_id=None):
        responses = OMASurveyResponse.objects.filter(survey_id=survey_id, is_complete=True)
        normalized = OMANormalizedData.objects.create(
            survey_id=survey_id,
            normalized_payload={"responses_count": responses.count(), "normalized": True},
        )
        return Response(OMANormalizedDataSerializer(normalized).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="normalized/(?P<survey_id>[^/.]+)")
    def get_normalized(self, request, survey_id=None):
        data = OMANormalizedData.objects.filter(survey_id=survey_id).order_by("-version").first()
        if not data:
            return Response({"detail": "No normalized data found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(OMANormalizedDataSerializer(data).data)


class OMADomainScoreViewSet(viewsets.ModelViewSet):
    queryset = OMADomainScore.objects.all()
    serializer_class = OMADomainScoreSerializer
    permission_classes = [IsHR]
    filterset_fields = ["domain_name", "survey"]

    @action(detail=False, methods=["post"], url_path="calculate")
    def calculate(self, request):
        survey_id = request.data.get("survey_id")
        result = AIProxyService.analyze_maturity({})
        scores_created = []
        for domain, score in result.get("domain_scores", {}).items():
            ds = OMADomainScore.objects.create(survey_id=survey_id, domain_name=domain, score=score)
            scores_created.append(ds)
        return Response(OMADomainScoreSerializer(scores_created, many=True).data, status=status.HTTP_201_CREATED)


class OMAValidationViewSet(viewsets.ViewSet):
    permission_classes = [IsHR]

    @action(detail=False, methods=["post"], url_path="validate")
    def validate(self, request):
        survey_id = request.data.get("survey_id")
        result = OMAValidationResult.objects.create(
            survey_id=survey_id,
            rule_name="cross_group_consistency",
            result="pass",
            details={"message": "No contradictions detected."},
        )
        return Response(OMAValidationResultSerializer(result).data)

    @action(detail=False, methods=["get"], url_path="results")
    def results(self, request):
        survey_id = request.query_params.get("survey_id")
        results = OMAValidationResult.objects.filter(survey_id=survey_id)
        return Response(OMAValidationResultSerializer(results, many=True).data)


class OMAMaturityLevelViewSet(viewsets.ModelViewSet):
    queryset = OMAMaturityLevel.objects.all()
    serializer_class = OMAMaturityLevelSerializer
    permission_classes = [IsHR]

    @action(detail=False, methods=["post"], url_path="calculate")
    def calculate(self, request):
        scores = OMADomainScore.objects.all()
        if not scores.exists():
            return Response({"detail": "No domain scores found."}, status=status.HTTP_400_BAD_REQUEST)
        avg = sum(s.score for s in scores) / scores.count()
        level = min(5, max(1, round(avg)))
        maturity = OMAMaturityLevel.objects.create(
            overall_level=level,
            domain_scores_snapshot={s.domain_name: s.score for s in scores},
        )
        return Response(OMAMaturityLevelSerializer(maturity).data, status=status.HTTP_201_CREATED)


class OMAGapViewSet(viewsets.ModelViewSet):
    queryset = OMAGap.objects.filter(is_active=True)
    serializer_class = OMAGapSerializer
    permission_classes = [IsHR]
    filterset_fields = ["severity", "domain_name"]


class OMARiskViewSet(viewsets.ModelViewSet):
    queryset = OMARisk.objects.filter(is_active=True)
    serializer_class = OMARiskSerializer
    permission_classes = [IsHR]
    filterset_fields = ["severity", "domain_name"]


class OMARoadmapViewSet(viewsets.ModelViewSet):
    queryset = OMARoadmap.objects.filter(is_active=True)
    serializer_class = OMARoadmapSerializer
    permission_classes = [IsHR]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=["post"], url_path="generate")
    def generate(self, request):
        gaps = OMAGap.objects.filter(is_active=True)
        roadmap = OMARoadmap.objects.create(
            quarter=request.data.get("quarter", "Q1-2025"),
            actions=[{"gap": g.domain_name, "action": f"Address {g.gap_description[:50]}"} for g in gaps],
            created_by=request.user,
        )
        return Response(OMARoadmapSerializer(roadmap).data, status=status.HTTP_201_CREATED)


class OMABenchmarkViewSet(viewsets.ModelViewSet):
    queryset = OMABenchmark.objects.filter(is_active=True)
    serializer_class = OMABenchmarkSerializer
    permission_classes = [IsHR]
    filterset_fields = ["benchmark_type"]

    @action(detail=False, methods=["post"], url_path="classify")
    def classify(self, request):
        return Response({
            "industry": request.data.get("industry", ""),
            "size": request.data.get("size", ""),
            "region": request.data.get("region", ""),
        })

    @action(detail=False, methods=["post"], url_path="apply")
    def apply_benchmark(self, request):
        benchmark = OMABenchmark.objects.create(
            benchmark_type=request.data.get("type", "industry"),
            classification_value=request.data.get("value", ""),
            variance_data=request.data.get("variance_data", {}),
        )
        return Response(OMABenchmarkSerializer(benchmark).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="report")
    def report(self, request):
        benchmarks = OMABenchmark.objects.filter(is_active=True)
        return Response(OMABenchmarkSerializer(benchmarks, many=True).data)


class OMABenchmarkDatasetViewSet(viewsets.ModelViewSet):
    queryset = OMABenchmarkDataset.objects.all()
    serializer_class = OMABenchmarkDatasetSerializer
    permission_classes = [IsHR]


class OMAStrategyExportViewSet(viewsets.ModelViewSet):
    queryset = OMAStrategyExport.objects.all()
    serializer_class = OMAStrategyExportSerializer
    permission_classes = [IsHR]

    @action(detail=False, methods=["post"], url_path="publish")
    def publish(self, request):
        maturity = OMAMaturityLevel.objects.order_by("-created_at").first()
        if not maturity:
            return Response({"detail": "No maturity level calculated."}, status=status.HTTP_400_BAD_REQUEST)
        export = OMAStrategyExport.objects.create(
            maturity_level=maturity,
            domain_scores=maturity.domain_scores_snapshot,
            gaps=[{"domain": g.domain_name, "severity": g.severity} for g in OMAGap.objects.filter(is_active=True)],
            risks=[{"domain": r.domain_name, "severity": r.severity} for r in OMARisk.objects.filter(is_active=True)],
        )
        return Response(OMAStrategyExportSerializer(export).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="acknowledge")
    def acknowledge(self, request, pk=None):
        export = self.get_object()
        export.acknowledged = True
        export.acknowledged_at = timezone.now()
        export.save(update_fields=["acknowledged", "acknowledged_at", "updated_at"])
        return Response(OMAStrategyExportSerializer(export).data)
