from rest_framework.permissions import BasePermission


class IsHR(BasePermission):
    """Allows access only to HR users."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ("hr", "admin")


class IsManager(BasePermission):
    """Allows access only to managers."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ("manager", "hr", "admin")


class IsEmployee(BasePermission):
    """Allows access to any authenticated employee."""

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsRecruiter(BasePermission):
    """Allows access only to recruiters."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ("recruiter", "hr", "admin")


class IsAuditor(BasePermission):
    """Allows read-only access to auditors."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == "auditor":
            return request.method in ("GET", "HEAD", "OPTIONS")
        return False


class IsAdmin(BasePermission):
    """Allows access only to admin users."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
