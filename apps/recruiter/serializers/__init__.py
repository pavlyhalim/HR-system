from rest_framework import serializers

from apps.recruiter.models import (
    BusinessRule,
    Candidate,
    CandidateCommunicationLog,
    CandidateConsentRecord,
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


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "created_by")

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class JobAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAdvertisement
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "generated_at")


class JobAdPublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAdPublication
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class JobAdAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAdAnalytics
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "parsed_data", "competencies_extracted")


class CandidateVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateVacancy
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "cv_score", "interview_score", "combined_score", "rank_position", "ai_reasoning")


class CandidateCommunicationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateCommunicationLog
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "analysis_data", "integrity_analysis_data")


class InterviewInterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewInterviewer
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "generated_at")


class InterviewResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewResponse
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class InterviewFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewFeedback
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "submitted_at")


class InterviewFeedbackCalibrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewFeedbackCalibration
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class InterviewIntegritySignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewIntegritySignal
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class InterviewIntegrityReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewIntegrityReport
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "generated_at")


class CandidateConsentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateConsentRecord
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class IntegrityBaselineSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrityBaseline
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class HiringDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiringDecision
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class BusinessRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessRule
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class RuleExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleException
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class InternalMobilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalMobility
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "role_fit_score", "jd_competency_match", "skill_gaps")


class SuccessionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessionPlan
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class PromotionCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionCycle
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "promotion_score", "jd_competency_delta")


class InterviewerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewerProfile
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class InterviewerAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewerAvailability
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
