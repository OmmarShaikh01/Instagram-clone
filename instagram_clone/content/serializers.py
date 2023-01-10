"""
Model Serializers
"""
from __future__ import annotations

from rest_framework import serializers

from instagram_clone.content.models import ContentModel


class ContentModelSerializer(serializers.ModelSerializer):
    """
    Content Model Serializer
    """

    class Meta:
        model = ContentModel
