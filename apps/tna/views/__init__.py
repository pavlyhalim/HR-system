from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import IsHR, IsManager
from apps.tna.models import (
    LearningPath,
    ManagerTNAInput,
    SkillGapAnalysis,
    TNACycle,
    TNAReport,
    TrainingPriority,
)
from apps.tna.serializers import (
    LearningPathSerializer,
    ManagerTNAInputSerializer,
    SkillGapAnalysisSerializer,
    TNACycleSerializer,
    TNAReportSerializer,
    TrainingPrioritySerializer,
)


class TNACycleViewSet(viewsets.ModelViewSet):
    queryset = TNACycle.objects.filter(is_active=True)
    serializer_class = TNACycleSerializer
    permission_classes = [IsHR]
    filterset_fields = ["status", "cycle_type"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], url_path="analyze")
    def analyze(self, request, pk=None):
        cycle = self.get_object()
        report = TNAReport.objects.create(
            cycle=cycle,
            summary={"total_gaps": cycle.analyses.count()},
            top_gaps=[],
            recommendations=[],
        )
        return Response(TNAReportSerializer(report).data, status=status.HTTP_201_CREATED)


class SkillGapAnalysisViewSet(viewsets.ModelViewSet):
    queryset = SkillGapAnalysis.objects.filter(is_active=True)
    serializer_class = SkillGapAnalysisSerializer
    permission_classes = [IsHR]
    filterset_fields = ["cycle", "gap_severity"]


class ManagerTNAInputViewSet(viewsets.ModelViewSet):
    queryset = ManagerTNAInput.objects.filter(is_active=True)
    serializer_class = ManagerTNAInputSerializer
    permission_classes = [IsHR | IsManager]
    filterset_fields = ["cycle", "manager"]


class TrainingPriorityViewSet(viewsets.ModelViewSet):
    queryset = TrainingPriority.objects.filter(is_active=True)
    serializer_class = TrainingPrioritySerializer
    permission_classes = [IsHR]
    filterset_fields = ["cycle", "priority"]


class LearningPathViewSet(viewsets.ModelViewSet):
    queryset = LearningPath.objects.filter(is_active=True)
    serializer_class = LearningPathSerializer
    permission_classes = [IsHR | IsManager]
    filterset_fields = ["cycle"]


class TNAReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TNAReport.objects.all()
    serializer_class = TNAReportSerializer
    permission_classes = [IsHR]
    filterset_fields = ["cycle"]
