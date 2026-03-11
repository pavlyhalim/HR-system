from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # API v1
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/jd/", include("apps.job_description.urls")),
    path("api/v1/", include("apps.recruiter.urls")),
    path("api/v1/lifecycle/", include("apps.employee_lifecycle.urls")),
    path("api/v1/oma/", include("apps.oma.urls")),
    path("api/v1/strategy/", include("apps.hr_strategy.urls")),
    path("api/v1/tna/", include("apps.tna.urls")),
    path("api/v1/payroll/", include("apps.payroll.urls")),
    path("api/v1/performance/", include("apps.performance.urls")),
    path("api/v1/notifications/", include("apps.notifications.urls")),
    path("api/v1/documents/", include("apps.documents.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
