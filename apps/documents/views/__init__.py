from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import IsHR
from apps.documents.models import Document, DocumentAccessLog
from apps.documents.serializers import DocumentAccessLogSerializer, DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.filter(is_active=True)
    serializer_class = DocumentSerializer
    permission_classes = [IsHR]
    filterset_fields = ["document_type", "entity_type", "is_confidential"]
    search_fields = ["title"]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=["get"], url_path="access-log")
    def access_log(self, request, pk=None):
        logs = DocumentAccessLog.objects.filter(document=self.get_object())
        return Response(DocumentAccessLogSerializer(logs, many=True).data)

    @action(detail=True, methods=["post"], url_path="log-access")
    def log_access(self, request, pk=None):
        log = DocumentAccessLog.objects.create(
            document=self.get_object(),
            accessed_by=request.user,
            access_type=request.data.get("access_type", "view"),
        )
        return Response(DocumentAccessLogSerializer(log).data)


class DocumentAccessLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DocumentAccessLog.objects.all()
    serializer_class = DocumentAccessLogSerializer
    permission_classes = [IsHR]
    filterset_fields = ["document", "access_type"]
