"""
App Urls
"""

from django.urls import path
from rest_framework import routers

from instagram_clone.user.views import (
    ListUserView,
    get_user_mugshot,
    login_user,
    logout_user,
    make_account_private,
    make_account_public,
    set_user_mugshot,
    signup_user,
)

router = routers.DefaultRouter()
url_path = (
    path("user/signup/", signup_user, name="signup_user"),
    path("user/login/", login_user, name="login_user"),
    path("user/logout/", logout_user, name="logout_user"),
    path(
        "user/<str:user_name>/make_account_private",
        make_account_private,
        name="make_account_private",
    ),
    path("user/<str:user_name>/make_account_public", make_account_public, name="make_account_public"),
    path("user/<str:user_name>/set_user_mugshot", set_user_mugshot, name="set_user_mugshot"),
    path("user/<str:user_name>/get_user_mugshot", get_user_mugshot, name="get_user_mugshot"),
    path("user/", ListUserView.as_view(), name="list_users"),
    path("user/<str:user_name>", ListUserView.as_view(), name="get_user"),
)
