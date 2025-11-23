from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "user_name", "is_active", "is_staff", "blocked")
    list_filter = ("is_active", "is_staff", "blocked")
    search_fields = ("email", "user_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Особиста інформація", {"fields": ("user_name",)}),
        ("Права доступу", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Модерація", {"fields": ("blocked",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "user_name", "password1", "password2", "is_active", "is_staff", "is_superuser", "blocked"),
        }),
    )