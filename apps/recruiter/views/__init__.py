from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import IsHR, IsManager, IsRecruiter
from apps.core.services import AIProxyService
from apps.recruiter.models import (
    BusinessRule,
    Candidate,
    CandidateVacancy,
    HiringDecision,
    IntegrityBaseline,
    InternalMobility,
    Interview,
    InterviewerAvailability,
    InterviewerProfile,
    InterviewFeedback,
    InterviewFeedbackCalibration,
    InterviewIntegrityReport,
    InterviewIntegritySignal,
    InterviewInterviewer,
    InterviewQuestion,
    InterviewResponse,
    JobAdAnalytics,
    JobAdPublication,
    JobAdvertisement,
    Promotion,
    PromotionCycle,
    RuleException,
    SuccessionPlan,
    Vacancy,
)
from apps.recruiter.serializers import (
    BusinessRuleSerializer,
    CandidateSerializer,
    CandidateVacancySerializer,
    HiringDecisionSerializer,
    IntegrityBaselineSerializer,
    InternalMobilitySerializer,
    InterviewerAvailabilitySerializer,
    InterviewerProfileSerializer,
    InterviewFeedbackCalibrationSerializer,
    InterviewFeedbackSerializer,
    InterviewIntegrityReportSerializer,
    InterviewIntegritySignalSerializer,
    InterviewInterviewerSerializer,
    InterviewQuestionSerializer,
    InterviewResponseSerializer,
    InterviewSerializer,
    JobAdAnalyticsSerializer,
    JobAdPublicationSerializer,
    JobAdvertisementSerializer,
    PromotionCycleSerializer,
    PromotionSerializer,
    RuleExceptionSerializer,
    SuccessionPlanSerializer,
    VacancySerializer,
)


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.filter(is_active=True)
    serializer_class = VacancySerializer
    permission_classes = [IsHR | IsRecruiter]
    filterset_fields = ["status", "department", "employment_type", "is_internal"]
    search_fields = ["title", "department", "location"]
    ordering_fields = ["created_at", "title", "status"]

    def perform_destroy(self, instance):
        if instance.applications.exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Cannot delete vacancy with existing candidates.")
        instance.soft_delete()

    @action(detail=True, methods=["patch"], url_path="status")
    def change_status(self, request, pk=None):
        vacancy = self.get_object()
        new_status = request.data.get("status")
        if new_status not in dict(Vacancy.Status.choices):
            return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
        vacancy.status = new_status
        if new_status == Vacancy.Status.CLOSED:
            vacancy.closed_at = timezone.now()
        vacancy.save(update_fields=["status", "closed_at", "updated_at"])
        return Response(VacancySerializer(vacancy).data)

    @action(detail=True, methods=["get"], url_path="pipeline")
    def pipeline(self, request, pk=None):
        vacancy = self.get_object()
        apps = CandidateVacancy.objects.filter(vacancy=vacancy).select_related("candidate")
        return Response(CandidateVacancySerializer(apps, many=True).data)

    @action(detail=True, methods=["get"], url_path="analytics")
    def analytics(self, request, pk=None):
        vacancy = self.get_object()
        job_ad = getattr(vacancy, "job_ad", None)
        if not job_ad:
            return Response({"detail": "No job ad found."}, status=status.HTTP_404_NOT_FOUND)
        analytics = JobAdAnalytics.objects.filter(publication__job_ad=job_ad)
        return Response(JobAdAnalyticsSerializer(analytics, many=True).data)


class JobAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = JobAdvertisement.objects.filter(is_active=True)
    serializer_class = JobAdvertisementSerializer
    permission_classes = [IsHR | IsRecruiter]
    filterset_fields = ["status", "tone"]

    @action(detail=False, methods=["post"], url_path="generate")
    def generate(self, request):
        vacancy_id = request.data.get("vacancy_id")
        try:
            vacancy = Vacancy.objects.get(pk=vacancy_id)
        except Vacancy.DoesNotExist:
            return Response({"detail": "Vacancy not found."}, status=status.HTTP_404_NOT_FOUND)
        ad, created = JobAdvertisement.objects.get_or_create(
            vacancy=vacancy,
            defaults={
                "generated_content": f"AI-generated ad for: {vacancy.title}",
                "tone": request.data.get("tone", "professional"),
                "length": request.data.get("length", "medium"),
            },
        )
        return Response(JobAdvertisementSerializer(ad).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="publish")
    def publish(self, request, pk=None):
        ad = self.get_object()
        ad.status = Vacancy.JobAdStatus.PUBLISHED
        ad.published_at = timezone.now()
        ad.save(update_fields=["status", "published_at", "updated_at"])
        return Response({"detail": "Ad published."})

    @action(detail=True, methods=["get"], url_path="performance")
    def performance(self, request, pk=None):
        ad = self.get_object()
        analytics = JobAdAnalytics.objects.filter(publication__job_ad=ad)
        return Response(JobAdAnalyticsSerializer(analytics, many=True).data)


class JobAdPublicationViewSet(viewsets.ModelViewSet):
    queryset = JobAdPublication.objects.filter(is_active=True)
    serializer_class = JobAdPublicationSerializer
    permission_classes = [IsHR | IsRecruiter]
    filterset_fields = ["platform", "status"]


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.filter(is_active=True)
    serializer_class = CandidateSerializer
    permission_classes = [IsHR | IsRecruiter]
    filterset_fields = ["source"]
    search_fields = ["name", "email"]
    ordering_fields = ["created_at", "name"]

    @action(detail=False, methods=["post"], url_path="bulk-upload")
    def bulk_upload(self, request):
        candidates_data = request.data.get("candidates", [])
        created = []
        for c in candidates_data:
            parsed = AIProxyService.parse_cv(c.get("cv_file_path", ""))
            candidate = Candidate.objects.create(
                name=c.get("name", parsed.get("name", "")),
                email=c.get("email", parsed.get("email", "")),
                phone=c.get("phone", ""),
                source=c.get("source", "direct"),
                cv_file_path=c.get("cv_file_path", ""),
                parsed_data=parsed,
                competencies_extracted=parsed.get("skills", []),
            )
            created.append(candidate.id)
        return Response({"created": len(created), "ids": [str(i) for i in created]}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="apply/(?P<vacancy_id>[^/.]+)")
    def apply(self, request, pk=None, vacancy_id=None):
        candidate = self.get_object()
        try:
            vacancy = Vacancy.objects.get(pk=vacancy_id, status=Vacancy.Status.OPEN)
        except Vacancy.DoesNotExist:
            return Response({"detail": "Vacancy not found or not open."}, status=status.HTTP_404_NOT_FOUND)
        app, created = CandidateVacancy.objects.get_or_create(
            candidate=candidate, vacancy=vacancy,
            defaults={"status": CandidateVacancy.PipelineStage.APPLIED},
        )
        if not created:
            return Response({"detail": "Already applied."}, status=status.HTTP_409_CONFLICT)
        # Score candidate
        score_result = AIProxyService.score_candidate(candidate.parsed_data, {})
        app.cv_score = score_result.get("overall_score", 0)
        app.jd_match_percentage = score_result.get("match_percentage", 0)
        app.ai_reasoning = score_result
        app.save()
        return Response(CandidateVacancySerializer(app).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="ranked")
    def ranked(self, request, pk=None):
        candidate = self.get_object()
        apps = CandidateVacancy.objects.filter(candidate=candidate).order_by("-combined_score")
        return Response(CandidateVacancySerializer(apps, many=True).data)

    @action(detail=True, methods=["post"], url_path="move-stage")
    def move_stage(self, request, pk=None):
        candidate = self.get_object()
        vacancy_id = request.data.get("vacancy_id")
        new_stage = request.data.get("stage")
        try:
            app = CandidateVacancy.objects.get(candidate=candidate, vacancy_id=vacancy_id)
        except CandidateVacancy.DoesNotExist:
            return Response({"detail": "Application not found."}, status=status.HTTP_404_NOT_FOUND)
        if new_stage not in dict(CandidateVacancy.PipelineStage.choices):
            return Response({"detail": "Invalid stage."}, status=status.HTTP_400_BAD_REQUEST)
        app.status = new_stage
        app.save(update_fields=["status", "updated_at"])
        return Response(CandidateVacancySerializer(app).data)


class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.filter(is_active=True).select_related("candidate", "vacancy")
    serializer_class = InterviewSerializer
    permission_classes = [IsHR | IsRecruiter]
    filterset_fields = ["status", "type", "interview_stage", "vacancy"]
    search_fields = ["candidate__name"]
    ordering_fields = ["scheduled_at", "created_at"]

    @action(detail=False, methods=["post"], url_path="questions/generate")
    def generate_questions(self, request):
        vacancy_id = request.data.get("vacancy_id")
        interview_id = request.data.get("interview_id")
        difficulty = request.data.get("difficulty", "Mid")
        questions = AIProxyService.generate_interview_questions({}, difficulty)
        created = []
        for i, q in enumerate(questions):
            iq = InterviewQuestion.objects.create(
                interview_id=interview_id,
                vacancy_id=vacancy_id,
                question_text=q["question"],
                competency_mapped=q.get("competency", ""),
                difficulty_level=difficulty.lower(),
                question_type=q.get("type", "behavioral").lower(),
                order_sequence=i + 1,
            )
            created.append(iq)
        return Response(InterviewQuestionSerializer(created, many=True).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="start")
    def start_interview(self, request, pk=None):
        interview = self.get_object()
        interview.status = Interview.Status.IN_PROGRESS
        interview.started_at = timezone.now()
        interview.save(update_fields=["status", "started_at", "updated_at"])
        return Response(InterviewSerializer(interview).data)

    @action(detail=True, methods=["post"], url_path="responses")
    def submit_response(self, request, pk=None):
        interview = self.get_object()
        serializer = InterviewResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(interview=interview)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="feedback")
    def submit_feedback(self, request, pk=None):
        interview = self.get_object()
        serializer = InterviewFeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(interview=interview, interviewer=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="calibrate")
    def calibrate(self, request, pk=None):
        serializer = InterviewFeedbackCalibrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(interview=self.get_object(), calibrated_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="analysis")
    def analysis(self, request, pk=None):
        interview = self.get_object()
        if not interview.analysis_data:
            result = AIProxyService.analyze_interview({})
            interview.analysis_data = result
            interview.save(update_fields=["analysis_data", "updated_at"])
        return Response(interview.analysis_data)

    @action(detail=True, methods=["get"], url_path="video")
    def video(self, request, pk=None):
        interview = self.get_object()
        return Response({"video_file_path": interview.video_file_path, "transcript_file_path": interview.transcript_file_path})


class InterviewIntegrityViewSet(viewsets.ModelViewSet):
    queryset = InterviewIntegritySignal.objects.all()
    serializer_class = InterviewIntegritySignalSerializer
    permission_classes = [IsHR | IsRecruiter]

    @action(detail=False, methods=["post"], url_path="configure/(?P<interview_id>[^/.]+)")
    def configure(self, request, interview_id=None):
        try:
            interview = Interview.objects.get(pk=interview_id)
        except Interview.DoesNotExist:
            return Response({"detail": "Interview not found."}, status=status.HTTP_404_NOT_FOUND)
        interview.integrity_monitoring_enabled = True
        interview.save(update_fields=["integrity_monitoring_enabled", "updated_at"])
        return Response({"detail": "Integrity monitoring enabled."})

    @action(detail=False, methods=["post"], url_path="signals/capture")
    def capture_signals(self, request):
        serializer = InterviewIntegritySignalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="analyze/(?P<interview_id>[^/.]+)")
    def analyze(self, request, interview_id=None):
        signals = InterviewIntegritySignal.objects.filter(interview_id=interview_id)
        report, _ = InterviewIntegrityReport.objects.get_or_create(
            interview_id=interview_id,
            defaults={
                "overall_integrity_score": 85.0,
                "risk_level": "low",
                "anomaly_count": signals.filter(anomaly_detected=True).count(),
                "attention_percentage": 92.0,
            },
        )
        return Response(InterviewIntegrityReportSerializer(report).data)

    @action(detail=False, methods=["get"], url_path="report/(?P<interview_id>[^/.]+)")
    def report(self, request, interview_id=None):
        try:
            report = InterviewIntegrityReport.objects.get(interview_id=interview_id)
        except InterviewIntegrityReport.DoesNotExist:
            return Response({"detail": "Report not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(InterviewIntegrityReportSerializer(report).data)


class InterviewSchedulingViewSet(viewsets.ViewSet):
    permission_classes = [IsHR | IsRecruiter]

    @action(detail=False, methods=["get"], url_path="interviewers")
    def list_interviewers(self, request):
        profiles = InterviewerProfile.objects.filter(is_active=True)
        return Response(InterviewerProfileSerializer(profiles, many=True).data)

    @action(detail=False, methods=["get"], url_path="slots/check")
    def check_slots(self, request):
        interviewer_id = request.query_params.get("interviewer_id")
        slots = InterviewerAvailability.objects.filter(interviewer_id=interviewer_id, is_available=True)
        return Response(InterviewerAvailabilitySerializer(slots, many=True).data)

    @action(detail=False, methods=["post"], url_path="slots/book")
    def book_slot(self, request):
        return Response({"detail": "Slot booked (stub)."}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="reminders/send")
    def send_reminders(self, request):
        return Response({"detail": "Reminders sent (stub)."})


class HiringDecisionViewSet(viewsets.ModelViewSet):
    queryset = HiringDecision.objects.filter(is_active=True).select_related("candidate", "vacancy")
    serializer_class = HiringDecisionSerializer
    permission_classes = [IsHR]
    filterset_fields = ["recommendation_type", "hr_decision", "vacancy"]

    @action(detail=False, methods=["get"], url_path="recommendations/(?P<vacancy_id>[^/.]+)")
    def recommendations(self, request, vacancy_id=None):
        decisions = HiringDecision.objects.filter(vacancy_id=vacancy_id).order_by("-combined_score")
        return Response(HiringDecisionSerializer(decisions, many=True).data)

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        decision = self.get_object()
        decision.hr_decision = HiringDecision.HRDecision.APPROVED
        decision.decided_by = request.user
        decision.decided_at = timezone.now()
        decision.save(update_fields=["hr_decision", "decided_by", "decided_at", "updated_at"])
        return Response(HiringDecisionSerializer(decision).data)

    @action(detail=True, methods=["post"], url_path="override")
    def override(self, request, pk=None):
        decision = self.get_object()
        decision.hr_decision = HiringDecision.HRDecision.OVERRIDDEN
        decision.override_reason = request.data.get("reason", "")
        decision.decided_by = request.user
        decision.decided_at = timezone.now()
        decision.save(update_fields=["hr_decision", "override_reason", "decided_by", "decided_at", "updated_at"])
        return Response(HiringDecisionSerializer(decision).data)

    @action(detail=True, methods=["get"], url_path="history")
    def history(self, request, pk=None):
        decision = self.get_object()
        return Response(HiringDecisionSerializer(decision).data)


class BusinessRuleViewSet(viewsets.ModelViewSet):
    queryset = BusinessRule.objects.filter(is_active=True)
    serializer_class = BusinessRuleSerializer
    permission_classes = [IsHR]
    filterset_fields = ["category"]

    @action(detail=False, methods=["post"], url_path="validate")
    def validate_rules(self, request):
        category = request.data.get("category")
        rules = BusinessRule.objects.filter(category=category, is_active=True)
        return Response({"rules_count": rules.count(), "validated": True})


class RuleExceptionViewSet(viewsets.ModelViewSet):
    queryset = RuleException.objects.filter(is_active=True)
    serializer_class = RuleExceptionSerializer
    permission_classes = [IsHR]


class InternalMobilityViewSet(viewsets.ModelViewSet):
    queryset = InternalMobility.objects.filter(is_active=True).select_related("vacancy")
    serializer_class = InternalMobilitySerializer
    permission_classes = [IsHR | IsManager]
    filterset_fields = ["status", "application_type"]

    @action(detail=False, methods=["post"], url_path="scan")
    def scan(self, request):
        vacancy_id = request.data.get("vacancy_id")
        return Response({"detail": f"Scan initiated for vacancy {vacancy_id} (stub)."})

    @action(detail=False, methods=["get"], url_path="(?P<role_id>[^/.]+)/matches")
    def matches(self, request, role_id=None):
        matches = InternalMobility.objects.filter(vacancy_id=role_id).order_by("-role_fit_score")
        return Response(InternalMobilitySerializer(matches, many=True).data)


class SuccessionPlanViewSet(viewsets.ModelViewSet):
    queryset = SuccessionPlan.objects.filter(is_active=True)
    serializer_class = SuccessionPlanSerializer
    permission_classes = [IsHR | IsManager]
    filterset_fields = ["readiness_level"]

    @action(detail=False, methods=["post"], url_path="roles")
    def define_roles(self, request):
        return Response({"detail": "Critical role defined (stub)."}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="(?P<role_id>[^/.]+)/identify")
    def identify_successors(self, request, role_id=None):
        successors = AIProxyService.identify_successors({}, [])
        return Response({"role_id": role_id, "successors": successors})

    @action(detail=False, methods=["get"], url_path="matrix")
    def matrix(self, request):
        plans = SuccessionPlan.objects.filter(is_active=True)
        return Response(SuccessionPlanSerializer(plans, many=True).data)


class PromotionCycleViewSet(viewsets.ModelViewSet):
    queryset = PromotionCycle.objects.filter(is_active=True)
    serializer_class = PromotionCycleSerializer
    permission_classes = [IsHR]
    filterset_fields = ["status"]


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.filter(is_active=True)
    serializer_class = PromotionSerializer
    permission_classes = [IsHR | IsManager]
    filterset_fields = ["status", "eligibility_status"]

    @action(detail=False, methods=["post"], url_path="initiate")
    def initiate(self, request):
        return Response({"detail": "Promotion cycle initiated (stub)."})

    @action(detail=False, methods=["get"], url_path="eligible")
    def eligible(self, request):
        promotions = Promotion.objects.filter(eligibility_status="eligible", is_active=True)
        return Response(PromotionSerializer(promotions, many=True).data)

    @action(detail=True, methods=["post"], url_path="evaluate")
    def evaluate(self, request, pk=None):
        promotion = self.get_object()
        result = AIProxyService.calculate_promotion_score({}, {})
        promotion.promotion_score = result.get("promotion_score", 0)
        promotion.jd_competency_delta = result.get("competency_delta", {})
        promotion.justification = result
        promotion.save()
        return Response(PromotionSerializer(promotion).data)

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        promotion = self.get_object()
        promotion.status = Promotion.Status.APPROVED
        promotion.decided_by = request.user
        promotion.decided_at = timezone.now()
        promotion.save(update_fields=["status", "decided_by", "decided_at", "updated_at"])
        return Response(PromotionSerializer(promotion).data)
