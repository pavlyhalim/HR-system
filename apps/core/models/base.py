import uuid

from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    """Abstract base model with UUID pk, timestamps, and soft delete."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def soft_delete(self):
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])


class AuditLog(models.Model):
    """Central audit log for tracking all system actions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    action = models.CharField(max_length=50, db_index=True)
    entity_type = models.CharField(max_length=100, db_index=True)
    entity_id = models.CharField(max_length=255, blank=True)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["entity_type", "entity_id"]),
        ]

    def __str__(self):
        return f"{self.action} on {self.entity_type} by {self.user}"


class SystemConfiguration(BaseModel):
    """System-wide configuration key/value store."""

    config_key = models.CharField(max_length=255, unique=True)
    config_value = models.JSONField(default=dict)
    config_category = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        verbose_name = "System Configuration"
        verbose_name_plural = "System Configurations"

    def __str__(self):
        return f"{self.config_key} ({self.config_category})"
