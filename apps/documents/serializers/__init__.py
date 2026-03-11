from rest_framework import serializers

from apps.documents.models import Document, DocumentAccessLog


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class DocumentAccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentAccessLog
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
