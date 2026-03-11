from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.core.models import AuditLog, SystemConfiguration


@admin.register(AuditLog)
class AuditLogAdmin(ModelAdmin):
    list_display = ("action", "entity_type", "entity_id", "user", "timestamp")
    list_filter = ("action", "entity_type")
    search_fields = ("entity_type", "entity_id", "user__email")
    readonly_fields = ("id", "user", "action", "entity_type", "entity_id", "changes", "ip_address", "user_agent", "timestamp")
    ordering = ("-timestamp",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(ModelAdmin):
    list_display = ("config_key", "config_category", "is_active", "updated_at")
    list_filter = ("config_category", "is_active")
    search_fields = ("config_key", "description")
