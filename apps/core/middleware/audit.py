import logging
import threading

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("apps.core.audit")
_request_local = threading.local()


def get_current_request():
    return getattr(_request_local, "request", None)


class AuditLogMiddleware(MiddlewareMixin):
    """Middleware that stores the current request for audit logging."""

    def process_request(self, request):
        _request_local.request = request

    def process_response(self, request, response):
        _request_local.request = None
        return response
