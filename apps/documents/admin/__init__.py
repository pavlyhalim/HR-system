from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.documents.models import Document, DocumentAccessLog


@admin.register(Document)
class DocumentAdmin(ModelAdmin):
    list_display = ("title", "document_type", "entity_type", "version", "uploaded_by", "is_confidential")
    list_filter = ("document_type", "is_confidential")
    search_fields = ("title",)


@admin.register(DocumentAccessLog)
class DocumentAccessLogAdmin(ModelAdmin):
    list_display = ("document", "accessed_by", "access_type", "created_at")
    list_filter = ("access_type",)
