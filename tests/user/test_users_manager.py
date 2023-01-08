import base64
from pathlib import PurePath

import pytest
from django.core.files.images import ImageFile

from configs import SETTINGS
from instagram_clone.user.models import UserModel, UserModelManager


@pytest.fixture()
def fix_create_user():
    user = UserModel.objects.create_user(
        **dict(
            user_name="test_user",
            password="test_user_password_!#%&(",
            user_phone=1234567890,
            user_email="test_user@testmail.com",
        )
    )
    yield user
    UserModel.objects.delete_user(user.user_name)


@pytest.mark.django_db
def test_create_user():
    assert isinstance(UserModel.objects, UserModelManager)
    user = UserModel.objects.create_user(
        **dict(
            user_name="test_user",
            password="test_user_password_!#%&(",
            user_phone=1234567890,
            user_email="test_user@testmail.com",
        )
    )
    assert isinstance(user, UserModel)
    assert not user.user_account_isSuperUser
    assert not user.user_account_isStaff


@pytest.mark.django_db
def test_create_superuser():
    assert isinstance(UserModel.objects, UserModelManager)
    user = UserModel.objects.create_superuser(
        **dict(
            user_name="test_user",
            password="test_user_password_!#%&(",
            user_phone=1234567890,
            user_email="test_user@testmail.com",
        )
    )
    assert isinstance(user, UserModel)
    assert user.user_account_isSuperUser
    assert user.user_account_isStaff


# noinspection PyUnusedLocal,PyShadowingNames
@pytest.mark.django_db
@pytest.mark.parametrize("status", [True, False])
def test_set_private(fix_create_user, status):
    user = fix_create_user
    UserModel.objects.set_private_account(user_name=user.user_name, is_private=status)
    user.refresh_from_db()
    assert user.user_account_isPrivate == status


@pytest.mark.django_db
def test_set_mugshot(fix_create_user):
    import tempfile

    user = fix_create_user
    assert (
            UserModel.objects.get_user_mugshot(user.user_name).name
            == ImageFile(
        open(
            PurePath(SETTINGS.project_root, "data", "default_resources", "user_mugshot.png"),
            encoding="utf-8",
        )
    ).name
    )
    with tempfile.TemporaryFile() as blob:
        from tests.tests_runtime_data.data import png_encoded_data

        data = png_encoded_data.encode("utf-8")
        blob.write(data)
        assert UserModel.objects.set_user_mugshot(user.user_name, ImageFile(blob))
        assert base64.b64decode(data) == base64.b64decode(UserModel.objects.get_user_mugshot(user.user_name).read())
