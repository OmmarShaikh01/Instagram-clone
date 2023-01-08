"""
Model and Manager Classes
"""

from __future__ import annotations

import uuid
from pathlib import PurePath
from typing import IO, Optional, Union

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.files.images import ImageFile
from django.db import models

from configs import SETTINGS


# pylint:disable = W0237
class UserModelManager(UserManager):
    def _create_user(self, user_name: str, user_email: str, password: str, **extra_fields) -> UserModel:
        """
        Creates UserModel Entry in DB

        :param user_name: Username
        :type user_name: str
        :param user_email: User Email
        :type user_email: str
        :param password: User Password
        :type password: str

        :return: Created User
        :rtype: UserModel
        """
        user_email = self.normalize_email(user_email)
        user_name = AbstractBaseUser.normalize_username(user_name)
        user = self.model(user_name=user_name, user_email=user_email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def delete_user(self, user_name: str) -> None:
        """
        Delets the Usermodel Entry matching the username

        :param user_name: Username
        :type user_name: str

        :return: None
        :rtype: None
        """
        return self.filter(user_name=user_name).delete()

    # noinspection PyMethodOverriding
    def create_user(self, user_name: str, user_email: str, password: str, **extra_fields) -> UserModel:
        """
        Creates UserModel Entry in DB, with Normal Permissions

        :param user_name: Username
        :type user_name: str
        :param user_email: User Email
        :type user_email: str
        :param password: User Password
        :type password: str

        :return: Created User
        :rtype: UserModel
        """
        extra_fields.setdefault("user_account_isStaff", False)
        extra_fields.setdefault("user_account_isSuperUser", False)
        return self._create_user(user_name, user_email, password, **extra_fields)

    # noinspection PyMethodOverriding
    def create_superuser(self, user_name: str, user_email: str, password: str, **extra_fields) -> UserModel:
        """
        Creates UserModel Entry in DB, with Superuser Permissions

        :param user_name: Username
        :type user_name: str
        :param user_email: User Email
        :type user_email: str
        :param password: User Password
        :type password: str

        :return: Created User
        :rtype: UserModel
        """
        extra_fields.setdefault("user_account_isStaff", True)
        extra_fields.setdefault("user_account_isSuperUser", True)

        if extra_fields.get("user_account_isStaff") is not True:
            raise ValueError("SuperUser must have is_staff=True.")
        if extra_fields.get("user_account_isSuperUser") is not True:
            raise ValueError("SuperUser must have is_superuser=True.")

        return self._create_user(user_name, user_email, password, **extra_fields)

    def set_user_mugshot(self, user_name: str, mugshot: Union[ImageFile, IO]) -> bool:
        """
        Sets Users Profile Picture

        :param user_name: username
        :type user_name: str
        :param mugshot: profile picture to set
        :type mugshot: Union[ImageFile, IO]

        :return: True if successful otherwise false
        :rtype: bool
        """
        user = self.filter(user_name=user_name).first()
        if user:
            user.user_mugshot.delete(save=False)
            user.user_mugshot.save(self.user_mugshot_directory_path(user), mugshot)
            if bool(user.user_mugshot):
                return True
        return False

    def get_user_mugshot(self, user_name: str) -> Optional[ImageFile]:
        """
        Returns the Stored Profile picture otherwise Default picture.

        :param user_name: username
        :type user_name: str

        :return: Profile Picture
        :rtype: Optional[ImageFile]
        """
        user = self.filter(user_name=user_name).first()
        if not user:
            return None
        elif not bool(user.user_mugshot):
            return self.user_mugshot_default_file_obj()
        elif user and user.user_mugshot:
            from instagram_clone import settings

            return ImageFile(open(PurePath(settings.MEDIA_ROOT, user.user_mugshot.name), "rb"))

    def set_private_account(self, user_name: str, is_private: bool = True) -> None:
        """
        Sets the Accounts Visibility status

        :param user_name: Usename
        :type user_name: str
        :param is_private: Public Visibility Status
        :type is_private: bool

        :return: None
        :rtype: None
        """
        self.filter(user_name=user_name).update(user_account_isPrivate=is_private)

    @staticmethod
    def user_mugshot_directory_path(instance: UserModel, *args) -> str:
        """
        Generates URI for mugshot. File will be uploaded to MEDIA_ROOT/user_mugshot/<uuid>.<extension>

        :param instance: User model instance
        :type instance: UserModel

        :return: Resource path
        :rtype: str
        """
        return f"user_mugshot/{instance.user_uuid}.png"

    @staticmethod
    def user_mugshot_default_file_obj() -> ImageFile:
        """
        Return default mugshot for user account.

        :return: Profile Picture
        :rtype: ImageFile
        """
        return ImageFile(
            open(
                PurePath(SETTINGS.project_root, "data", "default_resources", "user_mugshot.png"),
                "rb",
            )
        )


# Model Defination -----------------------------------------------------------------------------------------------------
class UserModel(AbstractBaseUser, PermissionsMixin):  # pragma: no cover
    """
    Model
    """
    user_uuid = models.UUIDField(
        primary_key=True,
        help_text="user uuid to use as primary key, django autogenerates this field",
        auto_created=True,
        default=uuid.uuid4,
        editable=False,
    )
    user_name = models.CharField(
        max_length=64,
        blank=False,
        unique=True,
        default="",
        help_text="unique username to use for identifying and searching accounts",
    )
    user_mugshot = models.ImageField(
        upload_to=UserModelManager.user_mugshot_directory_path,
        blank=False,
        default="",
        help_text="profile mugshot to display, if isnt provided use default mugshot",
    )
    user_phone = models.IntegerField(
        blank=False,
        help_text="user phone number to link the account to and provide 2fa",
        unique=True,
    )
    user_email = models.EmailField(
        blank=False,
        default="",
        help_text="user email to link the account to and provide 2fa",
        unique=True,
    )
    user_account_createdOn = models.DateField(
        auto_now=True,
        help_text="shows the account creation date",
    )
    user_account_isPrivate = models.BooleanField(
        blank=False,
        default=False,
        help_text="flag to enable private accounts",
    )
    user_account_isSuperUser = models.BooleanField(
        blank=False,
        default=False,
        help_text="flag to enable root accounts",
    )
    user_account_isStaff = models.BooleanField(
        blank=False,
        default=False,
        help_text="flag to enable staff accounts",
    )
    user_account_is_active = models.BooleanField(
        blank=False,
        default=False,
        help_text="flag to enable online status",
    )

    USERNAME_FIELD = "user_name"
    EMAIL_FIELD = "user_email"
    REQUIRED_FIELDS = ["user_phone", "user_email"]
    objects = UserModelManager()

    @property
    def is_staff(self):
        return self.user_account_isStaff

    def has_perm(self, perm: str, obj: Optional[UserModel] = None):  # FIX: custom superuser column
        return self.user_account_isSuperUser and self.user_account_isStaff

    def has_module_perms(self, app_label: str):  # FIX: custom superuser column
        return self.user_account_isSuperUser and self.user_account_isStaff

    def __str__(self):
        return str(self.user_name)
