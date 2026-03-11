from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ("email", "username", "first_name", "last_name", "role", "department", "is_active")
    list_filter = ("role", "is_active", "department")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("HR Info", {"fields": ("role", "department", "phone", "calendar_connected", "calendar_provider", "availability_preferences")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("HR Info", {"fields": ("email", "role", "department")}),
    )
