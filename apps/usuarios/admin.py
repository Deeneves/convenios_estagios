from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("cpf", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("cpf", "email", "first_name", "last_name")
    ordering = ("cpf",)
    fieldsets = (
        (None, {"fields": ("cpf", "password")}),
        ("Informacoes pessoais", {"fields": ("first_name", "last_name", "email")}),
        ("Papel", {"fields": ("role",)}),
        (
            "Permissoes",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("cpf", "password1", "password2", "role", "is_staff", "is_superuser"),
            },
        ),
    )

