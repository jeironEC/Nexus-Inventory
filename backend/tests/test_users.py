# Internal
import pytest

# DRF
from rest_framework import status

# Models
from nexus_inventory_backend.db.models import User


@pytest.mark.django_db
class TestGetUsers:
    def test_get_users_list(self, api_client_auth, url_users_list):
        response = api_client_auth.get(url_users_list)
        assert response.status_code == status.HTTP_200_OK

    def test_get_users_list_unauthenticated(self, api_client, url_users_list):
        response = api_client.get(url_users_list)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPostUsers:
    def test_admin_can_create_user(self, api_client_auth, url_users_list, payload_user):
        response = api_client_auth.post(url_users_list, payload_user)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="new@test.com").exists()

    def test_create_user_invalid(self, api_client_auth, url_users_list):
        response = api_client_auth.post(url_users_list, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_unauthenticated(
        self, api_client, url_users_list, payload_user
    ):
        response = api_client.post(url_users_list, payload_user)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestGetMe:
    def test_get_me(self, api_client, normal_user, url_user_me):
        api_client.force_authenticate(normal_user)
        response = api_client.get(url_user_me)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == normal_user.email

    def test_get_me_avatar_default_null(self, api_client_auth, url_user_me):
        response = api_client_auth.get(url_user_me)

        assert response.status_code == 200
        assert response.data["avatar"] is None

    def test_get_me_unauthenticated(self, api_client, url_user_me):
        response = api_client.get(url_user_me)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPatchMe:
    def test_patch_me_valid(self, api_client, normal_user, url_user_me):
        api_client.force_authenticate(normal_user)
        response = api_client.patch(url_user_me, {"email": "updated@test.com"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == "updated@test.com"

    def test_patch_me_avatar(self, api_client_auth, url_user_me):
        url = "https://example.com/avatar.png"

        response = api_client_auth.patch(url_user_me, {"avatar": url}, format="json")

        assert response.status_code == 200
        assert response.data["avatar"] == url

    def test_patch_me_avatar_invalid_url(self, api_client_auth, url_user_me):
        response = api_client_auth.patch(
            url_user_me, {"avatar": "not-a-url"}, format="json"
        )

        assert response.status_code == 400
        assert "avatar" in response.data

    def test_patch_me_unauthenticated(self, api_client, url_user_me):
        response = api_client.patch(url_user_me, {"first_name": "Updated"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDeleteMe:
    def test_soft_delete_me(self, api_client, normal_user, url_user_me):
        api_client.force_authenticate(normal_user)
        response = api_client.delete(url_user_me)
        normal_user.refresh_from_db()
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert normal_user.deleted_at is not None
        assert normal_user.is_active is False

    def test_delete_me_avatar(self, api_client_auth, normal_user, url_user_me):
        normal_user.avatar = "https://example.com/avatar.png"
        normal_user.save()

        response = api_client_auth.patch(url_user_me, {"avatar": None}, format="json")

        assert response.status_code == 200
        assert response.data["avatar"] is None

    def test_delete_me_unauthenticated(self, api_client, url_user_me):
        response = api_client.delete(url_user_me)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestFiltersUsers:
    def test_search_users(self, api_client_auth, url_users_list, normal_user):
        response = api_client_auth.get(f"{url_users_list}?search={normal_user.email}")
        assert response.status_code == status.HTTP_200_OK
