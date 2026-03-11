from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.notifications.models import Notification, NotificationTemplate


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ("subject", "recipient", "channel", "status", "sent_at", "read_at")
    list_filter = ("channel", "status")
    search_fields = ("subject", "recipient__email")


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(ModelAdmin):
    list_display = ("template_key", "channel", "created_at")
    list_filter = ("channel",)
