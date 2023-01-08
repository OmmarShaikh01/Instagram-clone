import os.path

import pytest
from django.core.management import call_command
from django.test import Client
from django.urls import reverse
from loguru import logger


@pytest.fixture(scope='module', autouse=True)
def fix_django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command(
            'loaddata',
            os.path.join(
                os.path.dirname(
                    os.path.dirname(__file__)
                ),
                "user",
                'load_data.json'
            )
        )

@pytest.fixture
def fix_client(db, client: Client) -> Client:
    data = dict(user_name="admin_1", password="qwerty123456")
    response = client.post(reverse("login_user"), data=data, content_type="application/json")
    logger.debug(response.status_code)
    return client


class TestUserRelationshipAPI:

    def test_send_friend_req_1(self, fix_client: Client):
        response = fix_client.post(
            reverse(
                "user-send_friend_req",
                kwargs = dict(pk = "admin_1")
            ),
            data = dict(friend="admin_2"),
            content_type="application/json"
        )
        logger.debug(response.status_code)
        assert response.status_code == 200

    def test_2(self, fix_client: Client):
        response = fix_client.post(
            reverse(
                "user-send_friend_req",
                kwargs = dict(pk = "admin_1")
            ),
            data = dict(friend="admin_2"),
            content_type="application/json"
        )
        logger.debug(response.status_code)
        assert response.status_code == 200

    def test_3(self, fix_client: Client):
        response = fix_client.post(
            reverse(
                "user-send_friend_req",
                kwargs = dict(pk = "admin_1")
            ),
            data = dict(friend="admin_2"),
            content_type="application/json"
        )
        logger.debug(response.status_code)
        assert response.status_code == 200

    def test_4(self, fix_client: Client):
        response = fix_client.post(
            reverse(
                "user-send_friend_req",
                kwargs = dict(pk = "admin_1")
            ),
            data = dict(friend="admin_2"),
            content_type="application/json"
        )
        logger.debug(response.status_code)
        assert response.status_code == 200
