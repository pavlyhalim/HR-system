from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


# ──────────────────────────────────────────────────────────
# VACANCIES & JOB ADS
# ──────────────────────────────────────────────────────────


class Vacancy(BaseModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    class JobAdStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CLOSED = "closed", "Closed"

    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", "Full-Time"
        PART_TIME = "part_time", "Part-Time"
        CONTRACT = "contract", "Contract"

    jd_id = models.UUIDField(help_text="FK to JD Engine job description")
    jd_version = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=255)
    role_level = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=255, db_index=True)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    job_ad_status = models.CharField(max_length=20, choices=JobAdStatus.choices, default=JobAdStatus.DRAFT)
    is_internal = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vacancies")
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class JobAdvertisement(BaseModel):
    class Tone(models.TextChoices):
        PROFESSIONAL = "professional", "Professional"
        FRIENDLY = "friendly", "Friendly"
        BOLD = "bold", "Bold"

    class Length(models.TextChoices):
        SHORT = "short", "Short"
        MEDIUM = "medium", "Medium"
        DETAILED = "detailed", "Detailed"

    vacancy = models.OneToOneField(Vacancy, on_delete=models.CASCADE, related_name="job_ad")
    generated_content = models.TextField(blank=True)
    template_id = models.UUIDField(null=True, blank=True)
    tone = models.CharField(max_length=20, choices=Tone.choices, default=Tone.PROFESSIONAL)
    length = models.CharField(max_length=20, choices=Length.choices, default=Length.MEDIUM)
    seo_keywords = models.JSONField(default=list, blank=True)
    company_branding = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=Vacancy.JobAdStatus.choices, default=Vacancy.JobAdStatus.DRAFT)
    generated_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Job Advertisement"

    def __str__(self):
        return f"Ad for: {self.vacancy.title}"


class JobAdPublication(BaseModel):
    class Platform(models.TextChoices):
        LINKEDIN = "linkedin", "LinkedIn"
        INDEED = "indeed", "Indeed"
        CAREER_PORTAL = "career_portal", "Career Portal"
        CUSTOM = "custom", "Custom"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PAUSED = "paused", "Paused"
        CLOSED = "closed", "Closed"

    job_ad = models.ForeignKey(JobAdvertisement, on_delete=models.CASCADE, related_name="publications")
    platform = models.CharField(max_length=30, choices=Platform.choices)
    platform_job_id = models.CharField(max_length=255, blank=True)
    posted_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    budget_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta(BaseModel.Meta):
        verbose_name = "Job Ad Publication"

    def __str__(self):
        return f"{self.get_platform_display()} - {self.job_ad.vacancy.title}"


class JobAdAnalytics(BaseModel):
    publication = models.ForeignKey(JobAdPublication, on_delete=models.CASCADE, related_name="analytics")
    date = models.DateField(db_index=True)
    views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    applications = models.PositiveIntegerField(default=0)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    cost_per_application = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    source_quality_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta(BaseModel.Meta):
        verbose_name = "Job Ad Analytics"
        verbose_name_plural = "Job Ad Analytics"

    def __str__(self):
        return f"Analytics {self.date} - {self.publication}"


# ──────────────────────────────────────────────────────────
# CANDIDATES
# ──────────────────────────────────────────────────────────


class Candidate(BaseModel):
    class Source(models.TextChoices):
        LINKEDIN = "linkedin", "LinkedIn"
        INDEED = "indeed", "Indeed"
        REFERRAL = "referral", "Referral"
        DIRECT = "direct", "Direct"
        INTERNAL = "internal", "Internal"

    name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=30, blank=True)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.DIRECT)
    source_detail = models.JSONField(default=dict, blank=True)
    cv_file_path = models.CharField(max_length=500, blank=True)
    parsed_data = models.JSONField(default=dict, blank=True)
    competencies_extracted = models.JSONField(default=list, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Candidate"

    def __str__(self):
        return f"{self.name} ({self.email})"


class CandidateVacancy(BaseModel):
    """Junction table: candidate applied for a vacancy."""

    class PipelineStage(models.TextChoices):
        APPLIED = "applied", "Applied"
        SCREENED = "screened", "Screened"
        INTERVIEWED = "interviewed", "Interviewed"
        OFFERED = "offered", "Offered"
        HIRED = "hired", "Hired"
        REJECTED = "rejected", "Rejected"

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="applications")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    application_source = models.ForeignKey(JobAdPublication, on_delete=models.SET_NULL, null=True, blank=True)
    cv_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    interview_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    traditional_interview_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    integrity_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    combined_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    jd_match_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ai_reasoning = models.JSONField(default=dict, blank=True)
    jd_competency_gaps = models.JSONField(default=list, blank=True)
    rank_position = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=PipelineStage.choices, default=PipelineStage.APPLIED, db_index=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta(BaseModel.Meta):
        unique_together = [("candidate", "vacancy")]
        verbose_name = "Candidate Application"

    def __str__(self):
        return f"{self.candidate.name} → {self.vacancy.title} ({self.get_status_display()})"


class CandidateCommunicationLog(BaseModel):
    class CommType(models.TextChoices):
        EMAIL = "email", "Email"
        SMS = "sms", "SMS"
        CALL = "call", "Call"
        IN_APP = "in_app", "In-App"

    class Direction(models.TextChoices):
        INBOUND = "inbound", "Inbound"
        OUTBOUND = "outbound", "Outbound"

    class Status(models.TextChoices):
        SENT = "sent", "Sent"
        DELIVERED = "delivered", "Delivered"
        READ = "read", "Read"
        FAILED = "failed", "Failed"

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="communications")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="communications")
    communication_type = models.CharField(max_length=20, choices=CommType.choices)
    direction = models.CharField(max_length=20, choices=Direction.choices)
    subject = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SENT)
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Communication Log"

    def __str__(self):
        return f"{self.get_communication_type_display()} to {self.candidate.name}"


# ──────────────────────────────────────────────────────────
# INTERVIEWS
# ──────────────────────────────────────────────────────────


class Interview(BaseModel):
    class Type(models.TextChoices):
        AI_AVATAR = "ai_avatar", "AI Avatar"
        TRADITIONAL = "traditional", "Traditional"

    class Stage(models.TextChoices):
        SCREENING = "screening", "Screening"
        TECHNICAL = "technical", "Technical"
        HR = "hr", "HR"
        MANAGER = "manager", "Manager"
        PANEL = "panel", "Panel"

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In Progress"
        PAUSED = "paused", "Paused"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        NO_SHOW = "no_show", "No Show"

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="interviews")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="interviews")
    type = models.CharField(max_length=20, choices=Type.choices)
    interview_stage = models.CharField(max_length=20, choices=Stage.choices, default=Stage.SCREENING)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED, db_index=True)
    integrity_monitoring_enabled = models.BooleanField(default=False)
    consent_given = models.BooleanField(default=False)
    consent_timestamp = models.DateTimeField(null=True, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    meeting_link = models.URLField(max_length=500, blank=True)
    location = models.CharField(max_length=255, blank=True)
    video_file_path = models.CharField(max_length=500, blank=True)
    transcript_file_path = models.CharField(max_length=500, blank=True)
    analysis_data = models.JSONField(default=dict, blank=True)
    integrity_analysis_data = models.JSONField(default=dict, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Interview"

    def __str__(self):
        return f"{self.candidate.name} - {self.get_type_display()} ({self.get_status_display()})"


class InterviewInterviewer(BaseModel):
    class Role(models.TextChoices):
        PRIMARY = "primary", "Primary"
        PANEL = "panel", "Panel"
        OBSERVER = "observer", "Observer"

    class AttendanceStatus(models.TextChoices):
        CONFIRMED = "confirmed", "Confirmed"
        ATTENDED = "attended", "Attended"
        NO_SHOW = "no_show", "No Show"

    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="interviewers")
    interviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_interviews")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PRIMARY)
    calendar_event_id = models.CharField(max_length=255, blank=True)
    attendance_status = models.CharField(max_length=20, choices=AttendanceStatus.choices, default=AttendanceStatus.CONFIRMED)
    feedback_submitted = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Interview Interviewer"

    def __str__(self):
        return f"{self.interviewer} on {self.interview}"


class InterviewQuestion(BaseModel):
    class Difficulty(models.TextChoices):
        JUNIOR = "junior", "Junior"
        MID = "mid", "Mid"
        SENIOR = "senior", "Senior"

    class QuestionType(models.TextChoices):
        TECHNICAL = "technical", "Technical"
        BEHAVIORAL = "behavioral", "Behavioral"
        SITUATIONAL = "situational", "Situational"

    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="questions")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="interview_questions")
    question_text = models.TextField()
    competency_mapped = models.CharField(max_length=255, blank=True)
    jd_competency_id = models.UUIDField(null=True, blank=True)
    difficulty_level = models.CharField(max_length=20, choices=Difficulty.choices, default=Difficulty.MID)
    expected_response_time_seconds = models.PositiveIntegerField(default=120)
    question_type = models.CharField(max_length=20, choices=QuestionType.choices, default=QuestionType.BEHAVIORAL)
    order_sequence = models.PositiveIntegerField(default=0)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta(BaseModel.Meta):
        ordering = ["order_sequence"]
        verbose_name = "Interview Question"

    def __str__(self):
        return f"Q{self.order_sequence}: {self.question_text[:60]}"


class InterviewResponse(BaseModel):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE, related_name="responses")
    response_text = models.TextField(blank=True)
    video_timestamp_start = models.FloatField(null=True, blank=True)
    video_timestamp_end = models.FloatField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    jd_competency_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ai_feedback = models.JSONField(default=dict, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Interview Response"

    def __str__(self):
        return f"Response to Q{self.question.order_sequence}"


class InterviewFeedback(BaseModel):
    class Recommendation(models.TextChoices):
        STRONG_HIRE = "strong_hire", "Strong Hire"
        HIRE = "hire", "Hire"
        MAYBE = "maybe", "Maybe"
        NO_HIRE = "no_hire", "No Hire"
        STRONG_NO = "strong_no", "Strong No"

    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="feedbacks")
    interviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interview_feedbacks")
    overall_rating = models.PositiveSmallIntegerField(help_text="1-5 rating")
    recommendation = models.CharField(max_length=20, choices=Recommendation.choices)
    competency_ratings = models.JSONField(default=dict, blank=True)
    strengths = models.TextField(blank=True)
    concerns = models.TextField(blank=True)
    red_flags = models.TextField(blank=True)
    cultural_fit_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    communication_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    technical_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    open_feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Interview Feedback"

    def __str__(self):
        return f"Feedback by {self.interviewer} - {self.get_recommendation_display()}"


class InterviewFeedbackCalibration(BaseModel):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="calibrations")
    calibration_session_date = models.DateField()
    original_scores = models.JSONField(default=dict)
    calibrated_scores = models.JSONField(default=dict)
    consensus_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discrepancies_noted = models.TextField(blank=True)
    calibration_notes = models.TextField(blank=True)
    calibrated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="calibrations_performed")
    calibrated_at = models.DateTimeField(auto_now_add=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Feedback Calibration"

    def __str__(self):
        return f"Calibration for {self.interview}"


# ──────────────────────────────────────────────────────────
# INTERVIEW INTEGRITY
# ──────────────────────────────────────────────────────────


class InterviewIntegritySignal(BaseModel):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="integrity_signals")
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField()
    eye_gaze_x = models.FloatField(default=0)
    eye_gaze_y = models.FloatField(default=0)
    on_screen = models.BooleanField(default=True)
    look_away_duration_ms = models.PositiveIntegerField(default=0)
    attention_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    head_pose_angles = models.JSONField(default=dict, blank=True)
    anomaly_detected = models.BooleanField(default=False)
    anomaly_type = models.CharField(max_length=100, blank=True)
    question_difficulty_context = models.CharField(max_length=50, blank=True)
    baseline_deviation_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta(BaseModel.Meta):
        verbose_name = "Integrity Signal"

    def __str__(self):
        return f"Signal at {self.timestamp} (anomaly={self.anomaly_detected})"


class InterviewIntegrityReport(BaseModel):
    class RiskLevel(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    interview = models.OneToOneField(Interview, on_delete=models.CASCADE, related_name="integrity_report")
    overall_integrity_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    risk_level = models.CharField(max_length=10, choices=RiskLevel.choices, default=RiskLevel.LOW)
    anomaly_count = models.PositiveIntegerField(default=0)
    total_look_away_time_seconds = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    attention_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    behavioral_patterns = models.JSONField(default=dict, blank=True)
    context_adjustments = models.JSONField(default=dict, blank=True)
    ai_reasoning = models.JSONField(default=dict, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Integrity Report"

    def __str__(self):
        return f"Integrity Report: {self.interview} ({self.get_risk_level_display()})"


class CandidateConsentRecord(BaseModel):
    class ConsentType(models.TextChoices):
        INTEGRITY = "integrity_monitoring", "Integrity Monitoring"
        DATA_PROCESSING = "data_processing", "Data Processing"
        COMMUNICATION = "communication", "Communication"

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="consent_records")
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="consent_records")
    consent_type = models.CharField(max_length=30, choices=ConsentType.choices)
    consent_given = models.BooleanField(default=False)
    consent_text_shown = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    withdrawn_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Consent Record"

    def __str__(self):
        return f"Consent ({self.get_consent_type_display()}) - {self.candidate.name}"


class IntegrityBaseline(BaseModel):
    role_level = models.CharField(max_length=100)
    question_difficulty = models.CharField(max_length=50)
    avg_attention_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    avg_look_away_duration_ms = models.PositiveIntegerField(default=0)
    anomaly_threshold_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sample_size = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        unique_together = [("role_level", "question_difficulty")]
        verbose_name = "Integrity Baseline"

    def __str__(self):
        return f"Baseline: {self.role_level} / {self.question_difficulty}"


class IntegrityDataAccessLog(BaseModel):
    class AccessType(models.TextChoices):
        VIEW = "view", "View"
        EXPORT = "export", "Export"
        DELETE = "delete", "Delete"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="integrity_access_logs")
    access_type = models.CharField(max_length=10, choices=AccessType.choices)
    purpose = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Integrity Data Access Log"

    def __str__(self):
        return f"{self.user} {self.get_access_type_display()} - {self.interview}"


# ──────────────────────────────────────────────────────────
# HIRING DECISIONS
# ──────────────────────────────────────────────────────────


class HiringDecision(BaseModel):
    class RecommendationType(models.TextChoices):
        HIRE = "hire", "Hire"
        REJECT = "reject", "Reject"
        HOLD = "hold", "Hold"

    class HRDecision(models.TextChoices):
        APPROVED = "approved", "Approved"
        OVERRIDDEN = "overridden", "Overridden"

    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="decisions")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="decisions")
    recommendation_type = models.CharField(max_length=10, choices=RecommendationType.choices)
    cv_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    interview_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    traditional_interview_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    integrity_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    combined_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    jd_match_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    business_rules_passed = models.BooleanField(default=True)
    failed_rules = models.JSONField(default=list, blank=True)
    ai_reasoning = models.JSONField(default=dict, blank=True)
    hr_decision = models.CharField(max_length=20, choices=HRDecision.choices, blank=True)
    override_reason = models.TextField(blank=True)
    cost_per_hire = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    time_to_hire_days = models.PositiveIntegerField(default=0)
    decided_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Hiring Decision"

    def __str__(self):
        return f"{self.candidate.name} → {self.vacancy.title}: {self.get_recommendation_type_display()}"


# ──────────────────────────────────────────────────────────
# BUSINESS RULES
# ──────────────────────────────────────────────────────────


class BusinessRule(BaseModel):
    category = models.CharField(max_length=100, db_index=True, help_text="hiring / mobility / succession / promotion")
    rule_name = models.CharField(max_length=255)
    rule_definition = models.JSONField(default=dict)
    priority = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        verbose_name = "Business Rule"
        ordering = ["category", "priority"]

    def __str__(self):
        return f"{self.category}: {self.rule_name}"


class RuleException(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    rule = models.ForeignKey(BusinessRule, on_delete=models.CASCADE, related_name="exceptions")
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rule_exception_requests")
    entity_type = models.CharField(max_length=100)
    entity_id = models.UUIDField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="rule_exception_reviews")
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Rule Exception"

    def __str__(self):
        return f"Exception for {self.rule.rule_name} ({self.get_status_display()})"


# ──────────────────────────────────────────────────────────
# INTERNAL MOBILITY, SUCCESSION, PROMOTIONS
# ──────────────────────────────────────────────────────────


class InternalMobility(BaseModel):
    class ApplicationType(models.TextChoices):
        SELF = "self_nomination", "Self Nomination"
        MANAGER = "manager_recommendation", "Manager Recommendation"

    class Status(models.TextChoices):
        APPLIED = "applied", "Applied"
        UNDER_REVIEW = "under_review", "Under Review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mobility_applications")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="mobility_applications")
    target_jd_id = models.UUIDField()
    current_jd_id = models.UUIDField(null=True, blank=True)
    application_type = models.CharField(max_length=30, choices=ApplicationType.choices)
    role_fit_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    jd_competency_match = models.JSONField(default=dict, blank=True)
    skill_gaps = models.JSONField(default=list, blank=True)
    gap_closure_timeline_months = models.PositiveIntegerField(default=0)
    eligibility_status = models.CharField(max_length=30, default="eligible")
    failed_rules = models.JSONField(default=list, blank=True)
    manager_endorsement = models.BooleanField(default=False)
    endorsed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="mobility_endorsements")
    endorsed_at = models.DateTimeField(null=True, blank=True)
    recommendation = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPLIED, db_index=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Internal Mobility"
        verbose_name_plural = "Internal Mobility Records"

    def __str__(self):
        return f"{self.employee} → {self.vacancy.title}"


class SuccessionPlan(BaseModel):
    class Readiness(models.TextChoices):
        READY = "ready", "Ready"
        WITHIN_6_12 = "6_12mo", "6-12 months"
        OVER_12 = "12_plus", "12+ months"

    critical_role_id = models.UUIDField(db_index=True)
    target_jd_id = models.UUIDField()
    successor_employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="succession_plans")
    readiness_level = models.CharField(max_length=20, choices=Readiness.choices)
    jd_competency_gap_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    competency_data = models.JSONField(default=dict, blank=True)
    development_plan = models.JSONField(default=dict, blank=True)
    business_rules_validated = models.BooleanField(default=False)
    validation_notes = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Succession Plan"

    def __str__(self):
        return f"Successor: {self.successor_employee} ({self.get_readiness_level_display()})"


class PromotionCycle(BaseModel):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    cycle_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN, db_index=True)
    total_eligible_employees = models.PositiveIntegerField(default=0)
    total_promoted = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="promotion_cycles")

    class Meta(BaseModel.Meta):
        verbose_name = "Promotion Cycle"

    def __str__(self):
        return f"{self.cycle_name} ({self.get_status_display()})"


class Promotion(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="promotions")
    promotion_cycle = models.ForeignKey(PromotionCycle, on_delete=models.CASCADE, related_name="promotions", null=True, blank=True)
    current_jd_id = models.UUIDField(null=True, blank=True)
    target_jd_id = models.UUIDField(null=True, blank=True)
    current_role = models.CharField(max_length=255)
    proposed_role = models.CharField(max_length=255)
    promotion_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    jd_competency_delta = models.JSONField(default=dict, blank=True)
    eligibility_status = models.CharField(max_length=30, default="eligible")
    failed_rules = models.JSONField(default=list, blank=True)
    justification = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    decided_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="promotion_decisions")
    decided_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Promotion"

    def __str__(self):
        return f"{self.employee}: {self.current_role} → {self.proposed_role}"


# ──────────────────────────────────────────────────────────
# SUPPORTING
# ──────────────────────────────────────────────────────────


class InterviewerProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interviewer_profile")
    interview_types = models.JSONField(default=list, blank=True)
    competency_expertise = models.JSONField(default=list, blank=True)
    max_interviews_per_week = models.PositiveIntegerField(default=5)
    avg_rating_given = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_interviews_conducted = models.PositiveIntegerField(default=0)
    feedback_quality_score = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    last_calibration_date = models.DateField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Interviewer Profile"

    def __str__(self):
        return f"Interviewer: {self.user}"


class InterviewerAvailability(BaseModel):
    interviewer = models.ForeignKey(InterviewerProfile, on_delete=models.CASCADE, related_name="availability_slots")
    day_of_week = models.PositiveSmallIntegerField(help_text="0=Monday, 6=Sunday")
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    buffer_minutes_between = models.PositiveIntegerField(default=15)

    class Meta(BaseModel.Meta):
        verbose_name = "Interviewer Availability"
        verbose_name_plural = "Interviewer Availabilities"

    def __str__(self):
        return f"{self.interviewer.user} - Day {self.day_of_week}"


class CalendarEvent(BaseModel):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="calendar_events")
    external_calendar_id = models.CharField(max_length=255, blank=True)
    calendar_provider = models.CharField(max_length=50, blank=True)
    event_link = models.URLField(max_length=500, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Calendar Event"

    def __str__(self):
        return f"Event: {self.interview}"


class JDCompetencyMapping(BaseModel):
    jd_id = models.UUIDField(db_index=True)
    competency_id = models.CharField(max_length=255)
    competency_name = models.CharField(max_length=255)
    proficiency_level = models.CharField(max_length=50)
    is_critical = models.BooleanField(default=False)
    weight_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta(BaseModel.Meta):
        verbose_name = "JD Competency Mapping"

    def __str__(self):
        return f"{self.competency_name} ({self.proficiency_level})"
