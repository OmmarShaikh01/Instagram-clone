"""
App Views
"""
import base64
import tempfile
from typing import Optional

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import update_last_login
from django.core.files.images import ImageFile
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    parser_classes,
    permission_classes,
    renderer_classes,
)
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from instagram_clone.user.models import UserModel
from instagram_clone.user.serializers import UserModelSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([BasicAuthentication])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def signup_user(request: Request):
    """
    registered user in

    REQ: [POST] user/make_account_private
    DATA: {
        user_name: str
        user_phone: int
        user_email: str
        password: str
    }
    DESC: registered user in
    """
    user_info = dict()
    serialized_data = request.data

    if "password" in serialized_data.keys():
        user_info["password"] = serialized_data["password"]
    else:
        return Response(
            dict(message="Missing UserInfoAttribute [password]"),
            status=status.HTTP_400_BAD_REQUEST,
        )

    if "user_name" in serialized_data.keys():
        user_info["user_name"] = serialized_data["user_name"]
    else:
        return Response(
            dict(message="Missing UserInfoAttribute [user_name]"),
            status=status.HTTP_400_BAD_REQUEST,
        )

    if "user_phone" in serialized_data.keys() and (
            isinstance(serialized_data.get("user_phone"), int)
            and 1000000000 <= serialized_data.get("user_phone") <= 9999999999
    ):
        user_info["user_phone"] = serialized_data["user_phone"]
    else:
        return Response(
            dict(message="Missing UserInfoAttribute [user_phone]"),
            status=status.HTTP_400_BAD_REQUEST,
        )

    if "user_email" in serialized_data.keys():
        user_info["user_email"] = serialized_data["user_email"]
    else:
        return Response(
            dict(message="Missing UserInfoAttribute [user_email]"),
            status=status.HTTP_400_BAD_REQUEST,
        )

    if UserModel.objects.create_user(**user_info) is not None:
        user = authenticate(request, username=user_info["user_name"], password=user_info["password"])
        if user is not None:
            login(request, user)
            user.user_account_is_active = True
            update_last_login(None, user)
            user.save()
            return Response({"message": "Success"}, status=status.HTTP_201_CREATED)

    return Response(
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([BasicAuthentication])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def login_user(request: Request):
    """
    Logs registered user in

    REQ: [POST] user/login_user
    DATA: {
        user_name: str | user_phone: int | user_email: str
        password: str
    }
    DESC: Logs registered user in
    """
    user_info = dict()
    serialized_data = request.data

    if "password" in serialized_data.keys():
        user_info["password"] = serialized_data["password"]
    else:
        return Response(
            dict(message="Missing UserInfoAttribute [password]"),
            status=status.HTTP_400_BAD_REQUEST,
        )

    if "user_name" in serialized_data.keys():
        user = UserModel.objects.filter(user_name=serialized_data["user_name"]).first()

    elif "user_phone" in serialized_data.keys():
        user = UserModel.objects.filter(user_phone=serialized_data["user_phone"]).first()

    elif "user_email" in serialized_data.keys():
        user = UserModel.objects.filter(user_email=serialized_data["user_email"]).first()

    else:
        return Response(
            dict(message="Missing UserInfoAttribute [user_name, user_phone, user_email]"),
            status=status.HTTP_400_BAD_REQUEST,
        )

    if user:
        password = serialized_data["password"]
        user = authenticate(request, username=user.user_name, password=password)
        if user is not None:
            login(request, user)
            user.user_account_is_active = True
            update_last_login(None, user)
            user.save()

        return Response({"message": "Success"}, status=status.HTTP_201_CREATED)

    return Response(
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request: Request):
    """
    Logs the current user Out

    REQ: [POST] user/logout_user
    DATA: None
    DESC: Logs the current user Out
    """
    update_last_login(None, request.user)
    UserModel.objects.filter(user_uuid=request.user.user_uuid).update(user_account_is_active=False)
    logout(request)
    return Response({"message": "Success"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def make_account_private(request: Request, user_name: Optional[str] = None):
    """
    Sets users Public visibility to private

    REQ: [POST] user/user_name/make_account_private
    DATA: None
    DESC: sets user profile Visibility
    """
    if user_name:
        UserModel.objects.set_private_account(user_name=user_name, is_private=True)
        return Response({"message": "Success"}, status=status.HTTP_200_OK)
    return Response({"message": "Failed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def make_account_public(request: Request, user_name: Optional[str] = None):
    """
    Sets users Public visibility to public

    REQ: [POST] user/user_name/make_account_public
    DATA: None
    DESC: sets user profile Visibility
    """
    if user_name:
        UserModel.objects.set_private_account(user_name=user_name, is_private=False)
        return Response({"message": "Success"}, status=status.HTTP_200_OK)
    return Response({"message": "Failed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_user_mugshot(request: Request, user_name: Optional[str] = None):
    """
    Gets user Mugshot

    REQ: [POST] user/user_name/set_user_mugshot
    DATA: {file: b64encoded str}
    DESC: sets user profile picture
    """
    user = UserModel.objects.filter(user_name=user_name).first()
    if not user:
        return Response({"message": f"Failed, {user_name} User Doest exist"}, status=status.HTTP_400_BAD_REQUEST)

    if not request.data.get("file"):
        return Response({"message": "Failed, Resource Data Empty"}, status=status.HTTP_400_BAD_REQUEST)

    with tempfile.TemporaryFile() as valid_image:
        valid_image.write(base64.b64decode(request.data["file"]))
        if UserModel.objects.set_user_mugshot(user_name, valid_image):
            return Response({"message": "Success"}, status=status.HTTP_200_OK)
    return Response({"message": "Failed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_user_mugshot(request: Request, user_name: Optional[str] = None):
    """
    Gets user Mugshot

    REQ: [GET] user/user_name/get_user_mugshot
    DATA: None
    DESC: gets user profile picture
    RSP:  {file: b64encoded str}
    """
    valid_image = UserModel.objects.get_user_mugshot(user_name)
    if isinstance(valid_image, ImageFile):
        return Response({"file": base64.b64encode(valid_image.read())})
    return Response({"message": "Failed"}, status=status.HTTP_400_BAD_REQUEST)


class ListUserView(ListAPIView):
    """
    User get and list request processor

    REQ: [GET] user/
    DATA: None
    DESC: gets all the users
    RSP:

    REQ: [GET] user/user_name
    DATA: None
    DESC: gets users that match the usernmae
    RSP:
    """
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserModelSerializer

    def get(self, request, user_name: Optional[str] = None, *args, **kwargs):
        if user_name:
            user = UserModel.objects.filter(user_name=user_name).first()
            serializer = UserModelSerializer(user)
            return Response(serializer.data)
        return super().get(request, *args, **kwargs)
