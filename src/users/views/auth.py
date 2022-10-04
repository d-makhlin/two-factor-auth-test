from typing import Any

from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.services.user_service import UserService
from users.views.serializers import (
    UserLoginSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


class AuthView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(request_body=UserLoginSerializer)
    @action(methods=("post",), detail=False, url_path="login")
    def login(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = authenticate(
            username=validated_data["username"], password=validated_data["password"]
        )
        if user is not None and user.is_active:
            login(request, user)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "user_id": user.id,
                    "username": user.username,
                },
            )
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(request_body=UserRegisterSerializer)
    @action(methods=("post",), detail=False, url_path="register")
    def register(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        serializer.save()
        user = authenticate(
            request,
            username=validated_data.get("username"),
            password=validated_data.get("password"),
        )
        url = ""
        if validated_data.get("use_two_step_auth"):
            user.is_active = False
            url = UserService.init_account_verification(
                user, validated_data.get("email")
            )
            user.save()
        return Response(url, status=status.HTTP_201_CREATED)

    @action(methods=("get",), detail=False, url_path="verify")
    def verify(self, request: Request) -> Response:
        token = request.query_params.get("token")
        uid = urlsafe_base64_decode(request.query_params.get("id")).decode()
        user = get_object_or_404(self.queryset, pk=uid)
        return (
            Response(status=status.HTTP_202_ACCEPTED)
            if UserService.check_account_token(user, token)
            else Response(status=status.HTTP_400_BAD_REQUEST)
        )
