from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PasswordReset

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

    ordering = ("-date_joined",)

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


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'reset_id', 'created_when')

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'