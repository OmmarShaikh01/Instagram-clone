"""
App Config
"""
from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    User App Config
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "instagram_clone.content"
