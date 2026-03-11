from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.notifications.views import NotificationTemplateViewSet, NotificationViewSet

router = DefaultRouter()
router.register("notifications", NotificationViewSet, basename="notification")
router.register("templates", NotificationTemplateViewSet, basename="notification-template")

urlpatterns = [
    path("", include(router.urls)),
]
