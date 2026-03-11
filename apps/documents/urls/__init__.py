from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.documents.views import DocumentAccessLogViewSet, DocumentViewSet

router = DefaultRouter()
router.register("documents", DocumentViewSet, basename="document")
router.register("access-logs", DocumentAccessLogViewSet, basename="document-access-log")

urlpatterns = [
    path("", include(router.urls)),
]
