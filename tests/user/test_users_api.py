import base64
from pathlib import PurePath

import django.utils.log
import pytest
from django.test import Client
from django.urls import reverse

from configs import SETTINGS
from instagram_clone.user.models import UserModel


@pytest.fixture()
def fix_signup_user(client) -> UserModel:
    user_info = dict()
    user_info["user_name"] = "test_user"
    user_info["password"] = "test_user_password_!#%&("
    user_info["user_phone"] = 1236547890
    user_info["user_email"] = "test_user@testmail.com"
    response = client.post(reverse("signup_user"), data=user_info, content_type="application/json")
    assert response.status_code == 201
    yield UserModel.objects.get(user_name=user_info["user_name"])
    UserModel.objects.filter(user_uuid=UserModel.objects.get(user_name=user_info["user_name"]).user_uuid).delete()


@pytest.fixture()
def fix_png_data(client) -> str:
    from tests.tests_runtime_data.data import png_encoded_data

    return png_encoded_data


def test_sign_up_1(client: Client):
    # test for invalid json request
    response = client.post(reverse("signup_user"), data=dict())
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 415


@pytest.mark.django_db
def test_sign_up_2(client: Client):
    # test for empty json request
    response = client.post(reverse("signup_user"), data=dict(), content_type="application/json")
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 400

    user_info = dict()
    user_info["user_name"] = "test_user"
    response = client.post(reverse("signup_user"), data=user_info, content_type="application/json")
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 400

    user_info["password"] = "test_user_password_!#%&("
    response = client.post(reverse("signup_user"), data=user_info, content_type="application/json")
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 400

    user_info["user_phone"] = 1236547890
    response = client.post(reverse("signup_user"), data=user_info, content_type="application/json")
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 400

    user_info["user_email"] = "test_user@testmail.com"
    response = client.post(reverse("signup_user"), data=user_info, content_type="application/json")
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    user = UserModel.objects.get(user_name=user_info["user_name"])
    user.refresh_from_db()
    assert user.user_account_is_active
    assert response.status_code == 201


@pytest.mark.django_db
def test_sign_up_3(client: Client):
    # test for valid json request
    user_info = dict()
    user_info["user_name"] = "test_user"
    user_info["password"] = "test_user_password_!#%&("
    user_info["user_phone"] = 1236547890
    user_info["user_email"] = "test_user@testmail.com"
    response = client.post(reverse("signup_user"), data=user_info, content_type="application/json")
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    user = UserModel.objects.get(user_name=user_info["user_name"])
    user.refresh_from_db()
    assert user.user_account_is_active
    assert response.status_code == 201


# noinspection PyTypeChecker
@pytest.mark.django_db
@pytest.mark.parametrize("user_phone", ["qwieckjlndsjakhdf", 10, 10000000000, None])
def test_sign_up_4(client, user_phone):
    # Invalid Phone number Format
    user_info = dict()
    user_info["user_name"] = "test_user"
    user_info["password"] = "test_user_password_!#%&("
    user_info["user_phone"] = user_phone
    user_info["user_email"] = "test_user@testmail.com"
    response = client.post(reverse("signup_user"), data=user_info, content_type="application/json")
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 400


# pylint:disable = W0621
@pytest.mark.django_db
def test_login_user_1(client: Client, fix_signup_user):
    # test for invalid json request
    response = client.post(reverse("login_user"), data=dict())
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 415


# pylint:disable = W0621
@pytest.mark.django_db
def test_login_user_2(client: Client, fix_signup_user):
    # test for empty json request
    response = client.post(reverse("login_user"), data=dict(), content_type="application/json")
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 400


# pylint:disable = W0621
@pytest.mark.parametrize(
    "user_info",
    [
        dict(user_email="test_user@testmail.com", password="test_user_password_!#%&("),
        dict(user_phone=1236547890, password="test_user_password_!#%&("),
        dict(user_name="test_user", password="test_user_password_!#%&("),
    ],
)
@pytest.mark.django_db(transaction=True)
def test_login_user_3(client: Client, user_info, fix_signup_user):
    # test for valid json request(email login)
    response = client.post(reverse("login_user"), data=user_info, content_type="application/json")
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    user = fix_signup_user
    user.refresh_from_db()
    assert user.user_account_is_active
    assert response.status_code == 201


# pylint:disable = W0621
@pytest.mark.django_db
def test_logout_user_1(client: Client, fix_signup_user):
    # test for valid logout success
    response = client.post(reverse("logout_user"), content_type="application/json")
    user = fix_signup_user
    user.refresh_from_db()
    assert not user.user_account_is_active
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 200

    response = client.post(reverse("logout_user"), content_type="application/json")
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 403


@pytest.mark.django_db
def test_logout_user_2(client: Client):
    # test for valid logout failure
    response = client.post(reverse("logout_user"), content_type="application/json")
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 403


@pytest.mark.django_db
def test_make_account_private(client: Client, fix_signup_user):
    user = fix_signup_user
    response = client.post(reverse("make_account_private", kwargs={"user_name": "test_user"}))
    user.refresh_from_db()
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 200
    assert user.user_account_isPrivate


@pytest.mark.django_db
def test_make_account_public(client: Client, fix_signup_user):
    user = fix_signup_user
    response = client.post(reverse("make_account_private", kwargs={"user_name": "test_user"}))
    response = client.post(reverse("make_account_public", kwargs={"user_name": "test_user"}))
    user.refresh_from_db()
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 200
    assert not user.user_account_isPrivate


@pytest.mark.django_db
def test_set_user_mugshot(client: Client, fix_signup_user, fix_png_data):
    user = fix_signup_user
    # sets new image
    data = fix_png_data
    response = client.post(
        reverse("set_user_mugshot", kwargs={"user_name": "test_user"}),
        data={"file": data},
        content_type="application/json",
        medida_type="image/png",
    )
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 200

    # checks if it returns newly set image
    response = client.get(reverse("get_user_mugshot", kwargs={"user_name": "test_user"}))
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert data == response.data["file"].decode("utf-8")


@pytest.mark.django_db
def test_get_user_mugshot_1(client: Client, fix_signup_user, fix_png_data):
    user = fix_signup_user
    # tests for default Return
    response = client.get(reverse("get_user_mugshot", kwargs={"user_name": "test_user"}))
    django.utils.log.log_response(f"Response data: {response.data}", response=response)

    assert response.data["file"] == base64.b64encode(
        open(PurePath(SETTINGS.project_root, "data", "default_resources", "user_mugshot.png"), "rb").read()
    )

    # sets new image
    data = fix_png_data
    response = client.post(
        reverse("set_user_mugshot", kwargs={"user_name": "test_user"}),
        data={"file": data},
        content_type="application/json",
        medida_type="image/png",
    )
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 200

    # checks if it returns newly set image
    response = client.get(reverse("get_user_mugshot", kwargs={"user_name": "test_user"}))
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert data == response.data["file"].decode("utf-8")


@pytest.mark.django_db
def test_get_user_mugshot_2(client: Client):
    response = client.get(reverse("get_user_mugshot", kwargs={"user_name": "test_user"}))
    django.utils.log.log_response(f"Response data: {response.data}", response=response)
    assert response.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_get_user(client: Client):
    # test for valid json request
    user_info = (
        dict(
            user_name="test_user_0",
            password="test_user_0_password_!#%&(",
            user_phone=1236547890,
            user_email="test_user_0@testmail.com",
        ),
        dict(
            user_name="test_user_1",
            password="test_user_1_password_!#%&(",
            user_phone=1234567890,
            user_email="test_user_1@testmail.com",
        ),
    )
    client.post(reverse("signup_user"), data=user_info[0], content_type="application/json")
    client.post(reverse("signup_user"), data=user_info[1], content_type="application/json")

    response = client.get(reverse("list_users"), content_type="application/json")
    assert len(response.data) == 2
    response = client.get(reverse("get_user", kwargs={"user_name": "test_user_1"}), content_type="application/json")
    assert len([response.data]) == 1
