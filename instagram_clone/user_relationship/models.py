"""
Model and Manager Classes
"""

from __future__ import annotations

import uuid
from typing import Optional

from django.db import models
from django.db.models import QuerySet

from instagram_clone.user.models import UserModel

REQUEST_PENDING = "PND"
FRIEND = "FRD"
BLOCKED = "BLK"


class UserRelationshipModelManager(models.Manager):
    """"""

    def send_friend_req(self, from_user: UserModel, to_user: UserModel) -> Optional[UserRelationshipModel]:
        if not self.filter(
                relationship_user_uuid=from_user,
                relationship_friend_uuid=to_user,
                relationship_status=REQUEST_PENDING,
        ).first():
            relationship = self.model(
                relationship_user_uuid=from_user,
                relationship_friend_uuid=to_user,
                relationship_status=REQUEST_PENDING,
            )
            relationship.save(self._db)
            return relationship
        return None

    def accept_friend_req(self, from_user: UserModel, to_user: UserModel) -> Optional[UserRelationshipModel]:
        relationship = self.filter(
            relationship_user_uuid=from_user,
            relationship_friend_uuid=to_user,
            relationship_status=REQUEST_PENDING,
        ).first()
        if relationship:
            relationship.relationship_status = FRIEND
            relationship.save(self._db)
            return relationship
        else:
            return None

    def reject_friend_req(self, from_user: UserModel, to_user: UserModel) -> bool:
        relationship_qs = self.filter(
            relationship_user_uuid=from_user,
            relationship_friend_uuid=to_user,
            relationship_status=REQUEST_PENDING,
        )
        if relationship_qs.first():
            self.filter(
                relationship_user_uuid=from_user,
                relationship_friend_uuid=to_user,
                relationship_status=REQUEST_PENDING,
            ).delete()
            return True
        else:
            return False

    def block_user(self, from_user: UserModel, to_user: UserModel) -> Optional[UserRelationshipModel]:
        relationship = self.filter(
            relationship_user_uuid=from_user,
            relationship_friend_uuid=to_user,
            relationship_status=FRIEND,
        ).first()
        if relationship:
            relationship.relationship_status = BLOCKED
            relationship.save(self._db)
            return relationship
        else:
            return None

    def unblock_user(self, from_user: UserModel, to_user: UserModel) -> Optional[UserRelationshipModel]:
        relationship = self.filter(
            relationship_user_uuid=from_user,
            relationship_friend_uuid=to_user,
            relationship_status=BLOCKED,
        ).first()
        if relationship:
            relationship.relationship_status = FRIEND
            relationship.save(self._db)
            return relationship
        else:
            return None

    def get_user_followers(self, user: UserModel) -> Optional[QuerySet]:
        relationships = self.filter(
            relationship_friend_uuid=user,
            relationship_status=FRIEND,
        )
        if relationships:
            return relationships
        else:
            return None

    def get_user_following(self, user: UserModel) -> Optional[QuerySet]:
        relationships = self.filter(
            relationship_user_uuid=user,
            relationship_status=FRIEND,
        )
        if relationships:
            return relationships
        else:
            return None

    def get_user_blocked(self, user: UserModel) -> Optional[QuerySet]:
        relationships = self.filter(
            relationship_user_uuid=user,
            relationship_status=BLOCKED,
        )
        if relationships:
            return relationships
        else:
            return None

    def get_user_pending_req(self, user: UserModel) -> Optional[QuerySet]:
        relationships = self.filter(
            relationship_user_uuid=user,
            relationship_status=REQUEST_PENDING,
        )
        if relationships:
            return relationships
        else:
            return None


# Model Defination -----------------------------------------------------------------------------------------------------
class UserRelationshipModel(models.Model):
    """"""

    relationship_uuid = models.UUIDField(
        primary_key=True,
        help_text="relationship uuid to use as primary key, Django autogenerates this field",
        auto_created=True,
        default=uuid.uuid4,
        editable=False,
    )
    relationship_user_uuid = models.ForeignKey(
        "user.UserModel", on_delete=models.CASCADE, related_name="relationship_user_uuid", to_field="user_uuid"
    )
    relationship_friend_uuid = models.ForeignKey(
        "user.UserModel", on_delete=models.CASCADE, related_name="relationship_friend_uuid", to_field="user_uuid"
    )
    relationship_status = models.CharField(
        max_length=3,
        choices=[
            (REQUEST_PENDING, "REQUEST_PENDING"),
            (FRIEND, "FRIEND"),
            (BLOCKED, "BLOCKED"),
        ],
        blank=False,
    )
    objects = UserRelationshipModelManager()

    def __str__(self):
        return f"<{self.relationship_user_uuid}>|<{self.relationship_friend_uuid}>: {self.relationship_status}"
