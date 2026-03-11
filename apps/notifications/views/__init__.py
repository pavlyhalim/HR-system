from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.permissions import IsHR
from apps.notifications.models import Notification, NotificationTemplate
from apps.notifications.serializers import NotificationSerializer, NotificationTemplateSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "channel"]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=["post"], url_path="read")
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.status = Notification.Status.READ
        notification.read_at = timezone.now()
        notification.save(update_fields=["status", "read_at", "updated_at"])
        return Response(NotificationSerializer(notification).data)

    @action(detail=False, methods=["post"], url_path="read-all")
    def mark_all_read(self, request):
        Notification.objects.filter(
            recipient=request.user, status=Notification.Status.SENT,
        ).update(status=Notification.Status.READ, read_at=timezone.now())
        return Response({"detail": "All notifications marked as read."})

    @action(detail=False, methods=["get"], url_path="unread-count")
    def unread_count(self, request):
        count = Notification.objects.filter(
            recipient=request.user, status__in=[Notification.Status.PENDING, Notification.Status.SENT],
        ).count()
        return Response({"unread_count": count})


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.filter(is_active=True)
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsHR]
