from django.utils import timezone
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import IsHR, IsManager
from apps.core.services import AIProxyService
from apps.job_description.models import (
    JDApprovalLog,
    JDBenchmarkResult,
    JDCompetency,
    JDConsumerReference,
    JobAnalysisInput,
    JobDescription,
    JobDescriptionVersion,
)
from apps.job_description.serializers import (
    JDApprovalLogSerializer,
    JDBenchmarkResultSerializer,
    JDCompetencySerializer,
    JDConsumerReferenceSerializer,
    JDGenerateSerializer,
    JDApproveRejectSerializer,
    JobAnalysisInputSerializer,
    JobDescriptionSerializer,
    JobDescriptionVersionSerializer,
)


class JobAnalysisInputViewSet(viewsets.ModelViewSet):
    """CRUD for job analysis questionnaire inputs."""

    queryset = JobAnalysisInput.objects.filter(is_active=True)
    serializer_class = JobAnalysisInputSerializer
    permission_classes = [IsHR | IsManager]
    filterset_fields = ["status", "department"]
    search_fields = ["role_title", "department"]
    ordering_fields = ["created_at", "role_title"]


class JobDescriptionViewSet(viewsets.ModelViewSet):
    """JD lifecycle management — CRUD, generation, approval, versioning, export."""

    queryset = JobDescription.objects.filter(is_active=True).select_related("current_version", "created_by")
    serializer_class = JobDescriptionSerializer
    permission_classes = [IsHR | IsManager]
    filterset_fields = ["status"]
    search_fields = ["current_version__structured_model"]
    ordering_fields = ["created_at", "status"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=["post"], url_path="generate")
    def generate(self, request):
        """Generate a JD from a job analysis input via AI."""
        serializer = JDGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            job_analysis = JobAnalysisInput.objects.get(pk=serializer.validated_data["job_analysis_id"])
        except JobAnalysisInput.DoesNotExist:
            return Response({"detail": "Job analysis not found."}, status=status.HTTP_404_NOT_FOUND)

        if job_analysis.status != JobAnalysisInput.Status.SUBMITTED:
            return Response({"detail": "Job analysis must be submitted before generation."}, status=status.HTTP_400_BAD_REQUEST)

        ai_result = AIProxyService.generate_jd({
            "role_title": job_analysis.role_title,
            "department": job_analysis.department,
            "tasks": job_analysis.tasks,
            "tools": job_analysis.tools,
            "reporting_line": job_analysis.reporting_line,
        })

        jd = JobDescription.objects.create(
            job_analysis=job_analysis,
            created_by=request.user,
            status=JobDescription.Status.DRAFT,
        )
        version = JobDescriptionVersion.objects.create(
            jd=jd,
            version_number=1,
            structured_model={**ai_result, "role_title": job_analysis.role_title},
        )
        # Create competencies from AI result
        for comp in ai_result.get("competencies", []):
            JDCompetency.objects.create(
                jd_version=version,
                competency_name=comp.get("name", ""),
                proficiency_level=comp.get("proficiency", "Mid"),
                weight=comp.get("weight", 0),
            )
        jd.current_version = version
        jd.save(update_fields=["current_version", "updated_at"])

        return Response(JobDescriptionSerializer(jd).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="submit-approval")
    def submit_approval(self, request, pk=None):
        jd = self.get_object()
        if jd.status != JobDescription.Status.DRAFT:
            return Response({"detail": "Only draft JDs can be submitted."}, status=status.HTTP_400_BAD_REQUEST)
        JDApprovalLog.objects.create(
            jd_version=jd.current_version,
            action=JDApprovalLog.Action.SUBMITTED,
            actor=request.user,
        )
        return Response({"detail": "Submitted for approval."})

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        jd = self.get_object()
        serializer = JDApproveRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jd.status = JobDescription.Status.APPROVED
        jd.approved_by = request.user
        jd.approved_at = timezone.now()
        jd.save(update_fields=["status", "approved_by", "approved_at", "updated_at"])
        JDApprovalLog.objects.create(
            jd_version=jd.current_version,
            action=JDApprovalLog.Action.APPROVED,
            actor=request.user,
            reason=serializer.validated_data.get("reason", ""),
        )
        return Response({"detail": "JD approved."})

    @action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        jd = self.get_object()
        serializer = JDApproveRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        JDApprovalLog.objects.create(
            jd_version=jd.current_version,
            action=JDApprovalLog.Action.REJECTED,
            actor=request.user,
            reason=serializer.validated_data.get("reason", ""),
        )
        return Response({"detail": "JD rejected."})

    @action(detail=True, methods=["post"], url_path="version")
    def create_version(self, request, pk=None):
        """Create a new version of a JD."""
        jd = self.get_object()
        latest_version = jd.versions.order_by("-version_number").first()
        new_version_number = (latest_version.version_number + 1) if latest_version else 1
        structured_model = request.data.get("structured_model", latest_version.structured_model if latest_version else {})
        version = JobDescriptionVersion.objects.create(
            jd=jd,
            version_number=new_version_number,
            structured_model=structured_model,
        )
        jd.current_version = version
        jd.status = JobDescription.Status.DRAFT
        jd.save(update_fields=["current_version", "status", "updated_at"])
        return Response(JobDescriptionVersionSerializer(version).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="versions")
    def list_versions(self, request, pk=None):
        jd = self.get_object()
        versions = jd.versions.all()
        return Response(JobDescriptionVersionSerializer(versions, many=True).data)

    @action(detail=True, methods=["get"], url_path="export")
    def export(self, request, pk=None):
        """Export JD as machine-readable JSON model."""
        jd = self.get_object()
        if not jd.current_version:
            return Response({"detail": "No version available."}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "jd_id": str(jd.id),
            "version": jd.current_version.version_number,
            "status": jd.status,
            "model": jd.current_version.structured_model,
            "competencies": JDCompetencySerializer(jd.current_version.competencies.all(), many=True).data,
        })

    @action(detail=True, methods=["post"], url_path="benchmark")
    def benchmark(self, request, pk=None):
        """Run benchmarking on current JD version."""
        jd = self.get_object()
        if not jd.current_version:
            return Response({"detail": "No version to benchmark."}, status=status.HTTP_404_NOT_FOUND)
        # AI stub benchmark
        benchmark = JDBenchmarkResult.objects.create(
            jd_version=jd.current_version,
            benchmark_source=request.data.get("source", "O*NET"),
            deviations={"role_inflation": False, "missing_competencies": []},
            risk_flags="",
        )
        return Response(JDBenchmarkResultSerializer(benchmark).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="validate")
    def validate_jd(self, request, pk=None):
        """Run deterministic validation rules on JD."""
        jd = self.get_object()
        if not jd.current_version:
            return Response({"detail": "No version to validate."}, status=status.HTTP_404_NOT_FOUND)
        # Basic validation rules
        model = jd.current_version.structured_model
        errors = []
        if not model.get("responsibilities"):
            errors.append("Missing responsibilities.")
        if not model.get("competencies") and not jd.current_version.competencies.exists():
            errors.append("Missing competencies.")
        validation_result = {"valid": len(errors) == 0, "errors": errors}
        jd.current_version.validation_results = validation_result
        jd.current_version.save(update_fields=["validation_results", "updated_at"])
        return Response(validation_result)

    @action(detail=True, methods=["get"], url_path="approval-history")
    def approval_history(self, request, pk=None):
        jd = self.get_object()
        logs = JDApprovalLog.objects.filter(jd_version__jd=jd).order_by("-created_at")
        return Response(JDApprovalLogSerializer(logs, many=True).data)


class JDCompetencyViewSet(viewsets.ModelViewSet):
    queryset = JDCompetency.objects.filter(is_active=True)
    serializer_class = JDCompetencySerializer
    permission_classes = [IsHR | IsManager]
    filterset_fields = ["jd_version", "is_mandatory", "proficiency_level"]


class JDConsumerReferenceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JDConsumerReference.objects.filter(is_active=True)
    serializer_class = JDConsumerReferenceSerializer
    filterset_fields = ["consumer_service", "reference_type"]
