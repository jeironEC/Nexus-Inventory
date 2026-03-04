# Internal
import pytest

# HTTP
from http import HTTPStatus

# Django

# Rest framework
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_token_obtain_status(client, normal_user, url_token):
    response = client.post(
        url_token, {"email": normal_user.email, "password": "StrongPass123!"}
    )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_token_obtain_pair_data_keys(client, normal_user, url_token):
    response = client.post(
        url_token, {"email": normal_user.email, "password": "StrongPass123!"}
    )
    assert set(response.json().keys()) == {"access", "refresh"}


@pytest.mark.django_db
def test_token_obtain_pair_url(url_token):
    assert url_token == "/v1/auth/token/"


@pytest.mark.django_db
def test_token_refresh(client, normal_user, url_token_refresh):
    refresh = RefreshToken.for_user(normal_user)
    refresh_token = str(refresh)

    response = client.post(url_token_refresh, {"refresh": refresh_token})
    assert "access" in response.data


@pytest.mark.django_db
def test_token_verify(client, normal_user, url_token_verify):
    refresh = RefreshToken.for_user(normal_user)
    access_token = str(refresh.access_token)

    response = client.post(url_token_verify, {"token": access_token})
    assert response.status_code == HTTPStatus.OK
