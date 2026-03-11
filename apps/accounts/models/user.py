import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with role-based access."""

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        HR = "hr", "HR"
        MANAGER = "manager", "Manager"
        EMPLOYEE = "employee", "Employee"
        RECRUITER = "recruiter", "Recruiter"
        CANDIDATE = "candidate", "Candidate"
        INTERVIEWER = "interviewer", "Interviewer"
        AUDITOR = "auditor", "Auditor"
        EXECUTIVE = "executive", "Executive"
        STRATEGY_OWNER = "strategy_owner", "Strategy Owner"
        PAYROLL = "payroll", "Payroll"
        LEGAL = "legal", "Legal"
        IT = "it", "IT"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.EMPLOYEE, db_index=True)
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    calendar_connected = models.BooleanField(default=False)
    calendar_provider = models.CharField(max_length=30, blank=True)
    availability_preferences = models.JSONField(default=dict, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["role"]),
            models.Index(fields=["department"]),
        ]

    def __str__(self):
        return f"{self.get_full_name() or self.email} ({self.get_role_display()})"
