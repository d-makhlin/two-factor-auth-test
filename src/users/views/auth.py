from typing import Any

from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from users.views.serializers import UserLoginSerializer
from users.views.forms import UserRegisterForm
from users.models import User
from users.views.serializers import UserSerializer


class AuthView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=("post",), detail=False, url_path="login")
    def login(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = authenticate(request)
        if user is not None:
            login(request, user)
            return Response(
                status=status.HTTP_200_OK,
                data={"user_id": user.id, "username": user.username},
            )
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=("post",), detail=False, url_path="register")
    def register(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        form = UserRegisterForm(request.data)
        if form.is_valid():
            form.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            status=status.HTTP_400_BAD_REQUEST, data={"errors": form.errors}
        )
