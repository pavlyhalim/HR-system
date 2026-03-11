from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.recruiter.models import (
    BusinessRule,
    CalendarEvent,
    Candidate,
    CandidateCommunicationLog,
    CandidateConsentRecord,
    CandidateVacancy,
    HiringDecision,
    IntegrityBaseline,
    IntegrityDataAccessLog,
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
    JDCompetencyMapping,
    JobAdAnalytics,
    JobAdPublication,
    JobAdvertisement,
    Promotion,
    PromotionCycle,
    RuleException,
    SuccessionPlan,
    Vacancy,
)


@admin.register(Vacancy)
class VacancyAdmin(ModelAdmin):
    list_display = ("title", "department", "status", "employment_type", "is_internal", "created_at")
    list_filter = ("status", "department", "employment_type", "is_internal")
    search_fields = ("title", "department")


@admin.register(JobAdvertisement)
class JobAdvertisementAdmin(ModelAdmin):
    list_display = ("vacancy", "tone", "length", "status", "published_at")
    list_filter = ("status", "tone")


@admin.register(JobAdPublication)
class JobAdPublicationAdmin(ModelAdmin):
    list_display = ("job_ad", "platform", "status", "posted_at")
    list_filter = ("platform", "status")


@admin.register(JobAdAnalytics)
class JobAdAnalyticsAdmin(ModelAdmin):
    list_display = ("publication", "date", "views", "clicks", "applications", "conversion_rate")
    list_filter = ("date",)


@admin.register(Candidate)
class CandidateAdmin(ModelAdmin):
    list_display = ("name", "email", "source", "created_at")
    list_filter = ("source",)
    search_fields = ("name", "email")


@admin.register(CandidateVacancy)
class CandidateVacancyAdmin(ModelAdmin):
    list_display = ("candidate", "vacancy", "status", "cv_score", "combined_score", "rank_position")
    list_filter = ("status",)
    search_fields = ("candidate__name", "vacancy__title")


@admin.register(CandidateCommunicationLog)
class CandidateCommunicationLogAdmin(ModelAdmin):
    list_display = ("candidate", "communication_type", "direction", "status", "sent_at")
    list_filter = ("communication_type", "direction", "status")


@admin.register(Interview)
class InterviewAdmin(ModelAdmin):
    list_display = ("candidate", "vacancy", "type", "interview_stage", "status", "scheduled_at")
    list_filter = ("type", "status", "interview_stage")
    search_fields = ("candidate__name",)


@admin.register(InterviewInterviewer)
class InterviewInterviewerAdmin(ModelAdmin):
    list_display = ("interview", "interviewer", "role", "attendance_status", "feedback_submitted")
    list_filter = ("role", "attendance_status")


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(ModelAdmin):
    list_display = ("interview", "question_type", "difficulty_level", "order_sequence")
    list_filter = ("question_type", "difficulty_level")


@admin.register(InterviewResponse)
class InterviewResponseAdmin(ModelAdmin):
    list_display = ("interview", "question", "score", "created_at")


@admin.register(InterviewFeedback)
class InterviewFeedbackAdmin(ModelAdmin):
    list_display = ("interview", "interviewer", "overall_rating", "recommendation", "submitted_at")
    list_filter = ("recommendation",)


@admin.register(InterviewFeedbackCalibration)
class InterviewFeedbackCalibrationAdmin(ModelAdmin):
    list_display = ("interview", "consensus_rating", "calibrated_by", "calibrated_at")


@admin.register(InterviewIntegritySignal)
class InterviewIntegritySignalAdmin(ModelAdmin):
    list_display = ("interview", "timestamp", "anomaly_detected", "attention_score")
    list_filter = ("anomaly_detected",)


@admin.register(InterviewIntegrityReport)
class InterviewIntegrityReportAdmin(ModelAdmin):
    list_display = ("interview", "overall_integrity_score", "risk_level", "anomaly_count")
    list_filter = ("risk_level",)


@admin.register(CandidateConsentRecord)
class CandidateConsentRecordAdmin(ModelAdmin):
    list_display = ("candidate", "consent_type", "consent_given", "created_at")
    list_filter = ("consent_type", "consent_given")


@admin.register(IntegrityBaseline)
class IntegrityBaselineAdmin(ModelAdmin):
    list_display = ("role_level", "question_difficulty", "avg_attention_score", "sample_size")


@admin.register(IntegrityDataAccessLog)
class IntegrityDataAccessLogAdmin(ModelAdmin):
    list_display = ("user", "interview", "access_type", "created_at")
    list_filter = ("access_type",)


@admin.register(HiringDecision)
class HiringDecisionAdmin(ModelAdmin):
    list_display = ("candidate", "vacancy", "recommendation_type", "hr_decision", "combined_score", "decided_at")
    list_filter = ("recommendation_type", "hr_decision")


@admin.register(BusinessRule)
class BusinessRuleAdmin(ModelAdmin):
    list_display = ("rule_name", "category", "priority", "is_active")
    list_filter = ("category",)


@admin.register(RuleException)
class RuleExceptionAdmin(ModelAdmin):
    list_display = ("rule", "requested_by", "status", "created_at")
    list_filter = ("status",)


@admin.register(InternalMobility)
class InternalMobilityAdmin(ModelAdmin):
    list_display = ("employee", "vacancy", "application_type", "role_fit_score", "status")
    list_filter = ("status", "application_type")


@admin.register(SuccessionPlan)
class SuccessionPlanAdmin(ModelAdmin):
    list_display = ("successor_employee", "readiness_level", "jd_competency_gap_percentage", "business_rules_validated")
    list_filter = ("readiness_level",)


@admin.register(PromotionCycle)
class PromotionCycleAdmin(ModelAdmin):
    list_display = ("cycle_name", "status", "start_date", "end_date", "total_eligible_employees", "total_promoted")
    list_filter = ("status",)


@admin.register(Promotion)
class PromotionAdmin(ModelAdmin):
    list_display = ("employee", "current_role", "proposed_role", "promotion_score", "status", "decided_at")
    list_filter = ("status",)


@admin.register(InterviewerProfile)
class InterviewerProfileAdmin(ModelAdmin):
    list_display = ("user", "max_interviews_per_week", "total_interviews_conducted", "feedback_quality_score")


@admin.register(InterviewerAvailability)
class InterviewerAvailabilityAdmin(ModelAdmin):
    list_display = ("interviewer", "day_of_week", "start_time", "end_time", "is_available")


@admin.register(CalendarEvent)
class CalendarEventAdmin(ModelAdmin):
    list_display = ("interview", "calendar_provider", "last_synced_at")


@admin.register(JDCompetencyMapping)
class JDCompetencyMappingAdmin(ModelAdmin):
    list_display = ("competency_name", "proficiency_level", "is_critical", "weight_percentage")
    list_filter = ("proficiency_level", "is_critical")
