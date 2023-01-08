"""
App Views
"""
from typing import Optional

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from instagram_clone.user.models import UserModel
from instagram_clone.user_relationship.models import UserRelationshipModel
from instagram_clone.user_relationship.serializers import UserRelationshipModelSerializer


class UserRelationshipView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserRelationshipModel.objects.all()
    serializer_class = UserRelationshipModelSerializer
    parser_classes = [JSONParser]

    @action(detail=True, methods=["POST"], url_name="send_friend_req")
    def send_friend_req(self, request: Request, pk: Optional[str] = None):
        if not pk or pk == request.data["friend"]:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        user = UserModel.objects.filter(user_name=pk).first()
        user_friend = UserModel.objects.filter(user_name=request.data["friend"]).first()

        if not user and not user_friend:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        data = UserRelationshipModel.objects.send_friend_req(user, user_friend)
        if data:
            return Response({"message": "Success"}, status=HTTP_200_OK)
        else:
            return Response({"message": "Failed, Request Exists"}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"], url_name="accept_friend_req")
    def accept_friend_req(self, request: Request, pk: Optional[str] = None):
        if not pk or pk == request.data["friend"]:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        user = UserModel.objects.filter(user_name=pk).first()
        user_friend = UserModel.objects.filter(user_name=request.data["friend"]).first()

        if not user and not user_friend:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        data = UserRelationshipModel.objects.accept_friend_req(user, user_friend)
        if data:
            return Response({"message": "Success"}, status=HTTP_200_OK)
        else:
            return Response({"message": "Failed, Request Doesnt Exists"}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"], url_name="reject_friend_req")
    def reject_friend_req(self, request: Request, pk: Optional[str] = None):
        if not pk or pk == request.data["friend"]:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        user = UserModel.objects.filter(user_name=pk).first()
        user_friend = UserModel.objects.filter(user_name=request.data["friend"]).first()

        if not user and not user_friend:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        data = UserRelationshipModel.objects.reject_friend_req(user, user_friend)
        if data:
            return Response({"message": "Success"}, status=HTTP_200_OK)
        else:
            return Response({"message": "Failed, Request Doesnt Exists"}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"], url_name="block_user")
    def block_user(self, request: Request, pk: Optional[str] = None):
        if not pk or pk == request.data["friend"]:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        user = UserModel.objects.filter(user_name=pk).first()
        user_friend = UserModel.objects.filter(user_name=request.data["friend"]).first()

        if not user and not user_friend:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        data = UserRelationshipModel.objects.block_user(user, user_friend)
        if data:
            return Response({"message": "Success"}, status=HTTP_200_OK)
        else:
            return Response({"message": "Failed, Request Dont Exists"}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"], url_name="unblock_user")
    def unblock_user(self, request: Request, pk: Optional[str] = None):
        if not pk or pk == request.data["friend"]:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        user = UserModel.objects.filter(user_name=pk).first()
        user_friend = UserModel.objects.filter(user_name=request.data["friend"]).first()

        if not user and not user_friend:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        data = UserRelationshipModel.objects.unblock_user(user, user_friend)
        if data:
            return Response({"message": "Success"}, status=HTTP_200_OK)
        else:
            return Response({"message": "Failed, Request Dont Exists"}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"], url_name="get_user_followers")
    def get_user_followers(self, request: Request, pk: Optional[str] = None):
        if not pk:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        user = UserModel.objects.filter(user_name=pk).first()

        if not user:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        data = UserRelationshipModel.objects.get_user_followers(user)
        serializer = UserRelationshipModelSerializer(data, many=True)
        if data:
            return Response({"message": "Success", "data": serializer.data}, status=HTTP_200_OK)
        else:
            return Response({"message": "Failed, Request Dont Exists"}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"], url_name="get_user_following")
    def get_user_following(self, request: Request, pk: Optional[str] = None):
        if not pk:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        user = UserModel.objects.filter(user_name=pk).first()

        if not user:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        data = UserRelationshipModel.objects.get_user_following(user)
        serializer = UserRelationshipModelSerializer(data, many=True)
        if data:
            return Response({"message": "Success", "data": serializer.data}, status=HTTP_200_OK)
        else:
            return Response({"message": "Failed, Request Dont Exists"}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"], url_name="get_user_blocked")
    def get_user_blocked(self, request: Request, pk: Optional[str] = None):
        if not pk:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        user = UserModel.objects.filter(user_name=pk).first()

        if not user:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        data = UserRelationshipModel.objects.get_user_blocked(user)
        serializer = UserRelationshipModelSerializer(data, many=True)
        if data:
            return Response({"message": "Success", "data": serializer.data}, status=HTTP_200_OK)
        else:
            return Response({"message": "Failed, Request Dont Exists"}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"], url_name="get_user_pending_req")
    def get_user_pending_req(self, request: Request, pk: Optional[str] = None):
        if not pk:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        user = UserModel.objects.filter(user_name=pk).first()

        if not user:
            return Response({"message": "Failed"}, status=HTTP_400_BAD_REQUEST)

        data = UserRelationshipModel.objects.get_user_pending_req(user)
        serializer = UserRelationshipModelSerializer(data, many=True)
        if data:
            return Response({"message": "Success", "data": serializer.data}, status=HTTP_200_OK)
        else:
            return Response({"message": "Failed, Request Dont Exists"}, status=HTTP_400_BAD_REQUEST)
