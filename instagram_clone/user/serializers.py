"""
Model Serializers
"""
from __future__ import annotations

from rest_framework import serializers

from instagram_clone.user.models import UserModel


class UserModelSerializer(serializers.ModelSerializer):
    """
    User Model Serializer
    """

    class Meta:
        model = UserModel
        fields = [
            "user_name",
            "user_mugshot",
            "user_phone",
            "user_email",
            "last_login",
            "user_account_is_active",
            "user_account_createdOn",
            "user_account_isPrivate",
        ]
