from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Employee(BaseModel):
    class EmploymentStatus(models.TextChoices):
        PREBOARDING = "preboarding", "Preboarding"
        ACTIVE = "active", "Active"
        ON_PROBATION = "on_probation", "On Probation"
        EXITING = "exiting", "Exiting"
        TERMINATED = "terminated", "Terminated"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="employee_profile")
    candidate_id = models.UUIDField(null=True, blank=True, help_text="FK to recruiter.Candidate")
    jd_id = models.UUIDField(null=True, blank=True, help_text="FK to job_description.JobDescription")
    employee_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    employment_status = models.CharField(max_length=20, choices=EmploymentStatus.choices, default=EmploymentStatus.PREBOARDING)
    department = models.CharField(max_length=200, blank=True)
    position = models.CharField(max_length=200, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    country_code = models.CharField(max_length=3, blank=True)
    reporting_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="direct_reports")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.employee_number or 'N/A'} - {self.user}"


class EmployeeLifecycleState(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="lifecycle_states")
    state = models.CharField(max_length=50)
    entered_at = models.DateTimeField(auto_now_add=True)
    exited_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-entered_at"]

    def __str__(self):
        return f"{self.employee} → {self.state}"


class OfferTemplate(BaseModel):
    template_name = models.CharField(max_length=200)
    template_content = models.JSONField(default=dict)
    version = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("template_name", "version")

    def __str__(self):
        return f"{self.template_name} v{self.version}"


class Offer(BaseModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        IN_APPROVAL = "in_approval", "In Approval"
        APPROVED = "approved", "Approved"
        SENT = "sent", "Sent"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="offers")
    template_version = models.ForeignKey(OfferTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    role_title = models.CharField(max_length=200)
    salary_data = models.JSONField(default=dict)
    benefits = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_offers")
    approved_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    def __str__(self):
        return f"Offer: {self.role_title} - {self.employee}"


class Contract(BaseModel):
    class ContractType(models.TextChoices):
        PERMANENT = "permanent", "Permanent"
        FIXED = "fixed", "Fixed-Term"
        PART_TIME = "part_time", "Part-Time"
        REMOTE = "remote", "Remote"
        CONSULTANT = "consultant", "Consultant"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        IN_APPROVAL = "in_approval", "In Approval"
        APPROVED = "approved", "Approved"
        SENT_FOR_SIGNATURE = "sent_for_signature", "Sent for Signature"
        SIGNED = "signed", "Signed"
        ACTIVE = "active", "Active"
        TERMINATED = "terminated", "Terminated"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="contracts")
    country_code = models.CharField(max_length=3)
    contract_type = models.CharField(max_length=20, choices=ContractType.choices)
    labor_law_version = models.CharField(max_length=50, blank=True)
    policy_version = models.CharField(max_length=50, blank=True)
    mandatory_clauses = models.JSONField(default=list, help_text="Policy-as-Data injected clauses")
    contract_content = models.JSONField(default=dict)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Contract: {self.employee} ({self.contract_type})"


class ContractVersion(BaseModel):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="versions")
    version_number = models.PositiveIntegerField(default=1)
    content_snapshot = models.JSONField(default=dict)
    changes_description = models.TextField(blank=True)

    class Meta:
        unique_together = ("contract", "version_number")

    def __str__(self):
        return f"{self.contract} v{self.version_number}"


class ContractSignature(BaseModel):
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, related_name="signature")
    signed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    signed_at = models.DateTimeField(null=True, blank=True)
    signature_provider = models.CharField(max_length=100, blank=True)
    evidence_path = models.CharField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Signature: {self.contract}"


class EmployeePersonalData(BaseModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"
        VERIFIED = "verified", "Verified"

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="personal_data")
    encrypted_payload = models.JSONField(default=dict, help_text="Field-level encrypted personal data")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Personal Data: {self.employee}"


class OnboardingChecklist(BaseModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="onboarding_checklist")
    total_tasks = models.PositiveIntegerField(default=0)
    completed_tasks = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Onboarding: {self.employee} ({self.completed_tasks}/{self.total_tasks})"


class OnboardingTask(BaseModel):
    class TaskType(models.TextChoices):
        HR = "hr", "HR"
        IT = "it", "IT"
        MANAGER = "manager", "Manager"
        EMPLOYEE = "employee", "Employee"
        ORIENTATION = "orientation", "Orientation"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        SKIPPED = "skipped", "Skipped"

    checklist = models.ForeignKey(OnboardingChecklist, on_delete=models.CASCADE, related_name="tasks")
    task_name = models.CharField(max_length=200)
    task_description = models.TextField(blank=True)
    task_type = models.CharField(max_length=20, choices=TaskType.choices)
    assigned_to_role = models.CharField(max_length=50)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    depends_on = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="dependents")
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.task_name} ({self.status})"


class ProbationRecord(BaseModel):
    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "In Progress"
        REVIEW_PENDING = "review_pending", "Review Pending"
        CONFIRMED = "confirmed", "Confirmed"
        EXTENDED = "extended", "Extended"
        TERMINATED = "terminated", "Terminated"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="probation_records")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    manager_evaluation = models.JSONField(default=dict)
    evaluation_notes = models.TextField(blank=True)
    decided_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Probation: {self.employee} ({self.status})"


class OffboardingRecord(BaseModel):
    class ExitType(models.TextChoices):
        VOLUNTARY = "voluntary", "Voluntary"
        INVOLUNTARY = "involuntary", "Involuntary"
        RETIREMENT = "retirement", "Retirement"
        END_OF_CONTRACT = "end_of_contract", "End of Contract"

    class Status(models.TextChoices):
        INITIATED = "initiated", "Initiated"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="offboarding_records")
    exit_type = models.CharField(max_length=20, choices=ExitType.choices)
    exit_reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INITIATED)
    initiated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="initiated_offboardings")
    last_working_day = models.DateField(null=True, blank=True)
    exit_interview_completed = models.BooleanField(default=False)
    asset_return_completed = models.BooleanField(default=False)
    access_revoked = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Offboarding: {self.employee} ({self.exit_type})"


class FinalSettlement(BaseModel):
    class ApprovalStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SUBMITTED = "submitted", "Submitted"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        EXECUTED = "executed", "Executed"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="final_settlements")
    offboarding = models.OneToOneField(OffboardingRecord, on_delete=models.CASCADE, related_name="settlement")
    breakdown = models.JSONField(default=dict, help_text="salary, leave, deductions, EOSB breakdown")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    approval_status = models.CharField(max_length=20, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_settlements")
    approved_at = models.DateTimeField(null=True, blank=True)
    executed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Settlement: {self.employee} ({self.approval_status})"


class ApprovalRequest(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        ESCALATED = "escalated", "Escalated"

    entity_type = models.CharField(max_length=50, help_text="offer / contract / settlement")
    entity_id = models.UUIDField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="approval_requests")
    approval_chain = models.JSONField(default=list, help_text="Ordered list of approver role/user IDs")
    current_step = models.PositiveIntegerField(default=0)
    sla_hours = models.PositiveIntegerField(default=48)
    escalated_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        indexes = [models.Index(fields=["entity_type", "entity_id"])]

    def __str__(self):
        return f"Approval: {self.entity_type} #{self.entity_id} ({self.status})"


class ApprovalAction(BaseModel):
    class ActionType(models.TextChoices):
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        ESCALATED = "escalated", "Escalated"
        COMMENTED = "commented", "Commented"

    approval_request = models.ForeignKey(ApprovalRequest, on_delete=models.CASCADE, related_name="actions")
    action = models.CharField(max_length=20, choices=ActionType.choices)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    step_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.action} by {self.actor}"
