"""
Model and Manager Classes
"""

from __future__ import annotations

from django.db import models


# pylint:disable = W0237
class ContentModelManager(models.Manager):
    """

    """


# Model Defination -----------------------------------------------------------------------------------------------------
class ContentModel(models.Model):  # pragma: no cover
    """

    """
    objects = ContentModelManager
