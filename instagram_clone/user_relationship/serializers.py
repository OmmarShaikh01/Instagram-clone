"""
Model Serializers
"""
from __future__ import annotations

from rest_framework import serializers

from instagram_clone.user_relationship.models import UserRelationshipModel


class UserRelationshipModelSerializer(serializers.ModelSerializer):
    """
    UserRelationship Model Serializer
    """
    relationship_user = serializers.SerializerMethodField()
    relationship_friend = serializers.SerializerMethodField()

    class Meta:
        model = UserRelationshipModel
        fields = [
            "relationship_user",
            "relationship_friend",
            "relationship_status",
        ]

    def get_relationship_user(self, objs: UserRelationshipModel) -> str:
        """
        Field Serializer

        :param objs: Object to serialize
        :type objs: UserRelationshipModel

        :return: Json Serialized value
        :rtype: str
        """
        return objs.relationship_user_uuid.user_name

    def get_relationship_friend(self, objs: UserRelationshipModel) -> str:
        """
        Field Serializer

        :param objs: Object to serialize
        :type objs: UserRelationshipModel

        :return: Json Serialized value
        :rtype: str
        """
        return objs.relationship_friend_uuid.user_name
