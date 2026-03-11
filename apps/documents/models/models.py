from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Document(BaseModel):
    class DocumentType(models.TextChoices):
        OFFER_LETTER = "offer_letter", "Offer Letter"
        CONTRACT = "contract", "Contract"
        PAYSLIP = "payslip", "Payslip"
        REPORT = "report", "Report"
        POLICY = "policy", "Policy"
        OTHER = "other", "Other"

    title = models.CharField(max_length=300)
    document_type = models.CharField(max_length=20, choices=DocumentType.choices)
    entity_type = models.CharField(max_length=50, blank=True, help_text="Related entity type (offer, contract, etc.)")
    entity_id = models.UUIDField(null=True, blank=True)
    file_path = models.CharField(max_length=500)
    file_size = models.PositiveIntegerField(default=0)
    mime_type = models.CharField(max_length=100, blank=True)
    version = models.PositiveIntegerField(default=1)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_confidential = models.BooleanField(default=False)
    retention_until = models.DateField(null=True, blank=True, help_text="Legal retention date")

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["entity_type", "entity_id"])]

    def __str__(self):
        return self.title


class DocumentAccessLog(BaseModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="access_logs")
    accessed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=20, help_text="view / download / share")

    def __str__(self):
        return f"{self.accessed_by} → {self.document} ({self.access_type})"
