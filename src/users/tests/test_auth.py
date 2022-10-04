from pydoc import cli
import pytest
from rest_framework import status

from rest_framework.test import APIClient

from users.models import User
from users.tests.factory import UserFactory


@pytest.mark.django_db
def test_user_auth_flow__one_step() -> None:
    client = APIClient()
    response = client.post(
        "/api/users/auth/register/",
        data={
            "username": "test",
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test",
            "phone_no": "+123",
            "use_two_step_auth": False,
            "password1": "secrettestpass1",
            "password2": "secrettestpass1",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.filter(username="test", email="test@test.com").first()
    assert user.is_active


@pytest.mark.django_db
def test_user_auth_flow__two_step() -> None:
    client = APIClient()
    response = client.post(
        "/api/users/auth/register/",
        data={
            "username": "test",
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test",
            "phone_no": "+123",
            "use_two_step_auth": True,
            "password1": "secrettestpass1",
            "password2": "secrettestpass1",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.filter(username="test", email="test@test.com").first()
    assert not user.is_active

    verify_url = response.data
    response = client.get(verify_url)

    assert response.status_code == status.HTTP_202_ACCEPTED
    user.refresh_from_db()
    assert user.is_active

    response = client.get(verify_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_auth_flow__two_step__wrong_token() -> None:
    client = APIClient()
    response = client.post(
        "/api/users/auth/register/",
        data={
            "username": "test",
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test",
            "phone_no": "+123",
            "use_two_step_auth": True,
            "password1": "secrettestpass1",
            "password2": "secrettestpass1",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.filter(username="test", email="test@test.com").first()
    assert not user.is_active

    verify_url: str = response.data
    verify_url = verify_url[:-1]
    response = client.get(verify_url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user.refresh_from_db()
    assert not user.is_active


@pytest.mark.django_db
def test_user_login__active() -> None:
    user = UserFactory(username="test_login")
    user.set_password("test_login")
    user.is_active = True
    user.save()
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(
        "/api/users/auth/login/",
        data={"username": "test_login", "password": "test_login"},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_login__inactive() -> None:
    user = UserFactory(username="test_login")
    user.set_password("test_login")
    client = APIClient()
    client.force_authenticate(user=user)
    user.is_active = False
    user.save()
    response = client.post(
        "/api/users/auth/login/",
        data={"username": "test_login", "password": "test_login"},
        format="json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_login__wrong_creds() -> None:
    user = UserFactory(username="test_login")
    user.set_password("test_login")
    user.is_active = True
    user.save()
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(
        "/api/users/auth/login/",
        data={"username": "test_login", "password": "wrong"},
        format="json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
