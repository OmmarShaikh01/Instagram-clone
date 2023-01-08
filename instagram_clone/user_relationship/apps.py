"""
App Config
"""
from django.apps import AppConfig


class UserRelationshipConfig(AppConfig):
    """
    User Relationship App Config
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "instagram_clone.user_relationship"
