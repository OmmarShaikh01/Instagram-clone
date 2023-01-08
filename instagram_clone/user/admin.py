"""
Admin class for App Management
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from instagram_clone.user.models import UserModel


@admin.register(UserModel)
class UserModelAdmin(BaseUserAdmin):
    """
    Admin class for Usermodel
    """

    exclude = (
        "last_name",
        "is_active",
        "username",
        "first_name",
        "email",
        "date_joined",
        "is_staff",
    )

    fieldsets = (
        (
            "Account Information",
            {
                "fields": (
                    "user_name",
                    "user_mugshot",
                    "user_phone",
                    "user_email",
                )
            },
        ),
        (
            "Account Permissions",
            {
                "fields": (
                    "user_account_isPrivate",
                    "user_account_isSuperUser",
                    "user_account_isStaff",
                )
            },
        ),
    )

    list_display = (
        "user_name",
        "user_mugshot",
        "user_phone",
        "user_email",
        "user_account_isPrivate",
        "user_account_isSuperUser",
        "user_account_isStaff",
        "user_account_createdOn",
        "is_active",
    )

    list_filter = (
        "user_name",
        "user_phone",
        "user_email",
        "user_account_createdOn",
        "user_account_isPrivate",
        "user_account_isSuperUser",
        "user_account_isStaff",
    )

    ordering = ("user_account_createdOn",)
    filter_horizontal = []
