from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "username",
        "is_staff",
        "is_active",
        "date_joined",
    )

    ordering = ("email",)

    fieldsets = UserAdmin.fieldsets + (
        (None, {
            "fields": ("bio","avatar"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            "fields": ("email", "avatar")
        }),
    )

    search_fields = ("email", "username")

# admin.site.register(User)