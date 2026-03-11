from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Notification(BaseModel):
    class Channel(models.TextChoices):
        EMAIL = "email", "Email"
        IN_APP = "in_app", "In-App"
        SMS = "sms", "SMS"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"
        READ = "read", "Read"

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    channel = models.CharField(max_length=10, choices=Channel.choices, default=Channel.IN_APP)
    subject = models.CharField(max_length=300)
    body = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    entity_type = models.CharField(max_length=50, blank=True, help_text="Related entity type")
    entity_id = models.UUIDField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["recipient", "status"])]

    def __str__(self):
        return f"{self.subject} → {self.recipient}"


class NotificationTemplate(BaseModel):
    template_key = models.CharField(max_length=100, unique=True)
    subject_template = models.CharField(max_length=300)
    body_template = models.TextField()
    channel = models.CharField(max_length=10, choices=Notification.Channel.choices, default=Notification.Channel.EMAIL)

    def __str__(self):
        return self.template_key
