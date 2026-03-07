# Internal
import pytest

# DRF
from rest_framework import status

# Models
from nexus_inventory_backend.db.models import User


@pytest.mark.django_db
def test_admin_can_create_user(api_client_auth, url_users_list, payload_user):
    response = api_client_auth.post(url_users_list, payload_user)

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="new@test.com").exists()


@pytest.mark.django_db
def test_get_me(api_client, normal_user, url_user_me):
    api_client.force_authenticate(normal_user)

    response = api_client.get(url_user_me)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == normal_user.email


@pytest.mark.django_db
def test_soft_delete_me(api_client, normal_user, url_user_me):
    api_client.force_authenticate(normal_user)

    response = api_client.delete(url_user_me)

    normal_user.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert normal_user.deleted_at is not None
    assert normal_user.is_active is False


def test_register_throttling(api_client_auth, url_users_list, payload_user):
    for i in range(6):
        response = api_client_auth.post(url_users_list, payload_user)

    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
