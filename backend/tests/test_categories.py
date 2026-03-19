# Internal
import pytest

# DRF
from rest_framework import status

# Models
from nexus_inventory_backend.db.models import Category

# Enums
from nexus_inventory_backend.db.enums import State


@pytest.mark.django_db
class TestGetCategory:
    def test_get_category_by_id_returns_200(
        self, api_client_auth, category_detail_url, category
    ):
        response = api_client_auth.get(category_detail_url(category.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_get_category_by_id_nonexistent_returns_404(
        self, api_client_auth, category_detail_url
    ):
        response = api_client_auth.get(category_detail_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_list_categories_returns_200(self, api_client_auth, categories_url):
        response = api_client_auth.get(categories_url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_categories_returns_list(
        self, api_client_auth, categories_url, category, another_category
    ):
        response = api_client_auth.get(categories_url)
        assert len(response.data) == 2

    def test_list_categories_fields_present(
        self, api_client_auth, categories_url, category
    ):
        response = api_client_auth.get(categories_url)
        data = response.data[0]
        assert set(data.keys()) == {
            "id",
            "name",
            "description",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        }

    def test_list_categories_unauthenticated_return_401(
        self, api_client, categories_url
    ):
        response = api_client.get(categories_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPostCategory:
    def test_create_category_returns_201(
        self, api_client_auth, categories_url, payload_category
    ):
        response = api_client_auth.post(categories_url, payload_category)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_category_persisted(
        self, api_client_auth, categories_url, payload_category
    ):
        api_client_auth.post(categories_url, payload_category)
        assert Category.objects.filter(name="Electronics").exists()

    def test_create_category_response_contains_fields(
        self, api_client_auth, categories_url, payload_category
    ):
        response = api_client_auth.post(categories_url, payload_category)
        assert response.data["name"] == "Electronics"

    def test_create_category_duplicate_name_returns_400(
        self, api_client_auth, categories_url, category, payload_category
    ):
        response = api_client_auth.post(categories_url, payload_category)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_category_duplicate_name_case_insensitive_returns_400(
        self, api_client_auth, categories_url, category, payload_category
    ):
        payload_category["name"] = category.name.upper()
        response = api_client_auth.post(categories_url, payload_category)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_category_missing_name_returns_400(
        self, api_client_auth, categories_url, payload_category_no_name
    ):
        response = api_client_auth.post(categories_url, payload_category_no_name)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_category_unauthenticated_returns_401(
        self, api_client, categories_url, payload_category
    ):
        response = api_client.post(categories_url, payload_category)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPatchCategory:
    def test_patch_category_updates_name(
        self, api_client_auth, category_detail_url, category
    ):
        response = api_client_auth.patch(
            category_detail_url(category.pk), {"name": "Pants"}
        )
        assert response.data["name"] == "Pants"

    def test_patch_category_updates_description(
        self, api_client_auth, category_detail_url, category
    ):
        response = api_client_auth.patch(
            category_detail_url(category.pk), {"description": "A pants products"}
        )
        assert response.data["description"] == "A pants products"

    def test_patch_category_persists_changes(
        self, api_client_auth, category_detail_url, category
    ):
        api_client_auth.patch(category_detail_url(category.pk), {"name": "Laptops"})
        category.refresh_from_db()
        assert category.name == "Laptops"

    def test_patch_category_nonexistent_returns_404(
        self, api_client_auth, category_detail_url
    ):
        response = api_client_auth.patch(
            category_detail_url(999), {"name": "Inexistent"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_category_duplicate_name_returns_400(
        self, api_client_auth, category_detail_url, category, another_category
    ):
        response = api_client_auth.patch(
            category_detail_url(category.pk), {"name": another_category.name}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_category_same_name_on_self_returns_200(
        self, api_client_auth, category_detail_url, category
    ):
        response = api_client_auth.patch(
            category_detail_url(category.pk), {"name": category.name}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_patch_category_unauthenticated_returns_401(
        self, api_client, category_detail_url, category
    ):
        response = api_client.patch(category_detail_url(category.pk), {"name": "x"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDeleteCategory:
    def test_delete_category_returns_204(
        self, api_client_auth, category_detail_url, category
    ):
        response = api_client_auth.delete(category_detail_url(category.pk))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_category_remove_from_db(
        self, api_client_auth, category_detail_url, category
    ):
        api_client_auth.delete(category_detail_url(category.pk))
        assert not Category.objects.filter(pk=category.pk).exists()

    def test_delete_category_noexistent_returns_404(
        self, api_client_auth, category_detail_url
    ):
        response = api_client_auth.delete(category_detail_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_category_unauthenticated_returns_401(
        self, api_client, category_detail_url, category
    ):
        response = api_client.delete(category_detail_url(category.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestStateCategory:
    def test_activate_category_returns_200(
        self, api_client_auth, category_activate_url, category
    ):
        category.state = State.INACTIVE
        category.save()
        response = api_client_auth.patch(category_activate_url(category.pk))
        category.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK

    def test_deactivate_category_returns_200(
        self, api_client_auth, category_deactivate_url, category
    ):
        category.state = State.ACTIVE
        category.save()
        response = api_client_auth.patch(category_deactivate_url(category.pk))
        category.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK

    def test_activate_category_not_found_returns_404(
        self, api_client_auth, category_activate_url
    ):
        response = api_client_auth.patch(category_activate_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_deactivate_category_not_found_returns_404(
        self, api_client_auth, category_deactivate_url
    ):
        response = api_client_auth.patch(category_deactivate_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestFiltersCategory:
    def test_returns_list_categories_actives(
        self, api_client_auth, categories_actives_url
    ):
        response = api_client_auth.get(categories_actives_url)
        assert response.status_code == status.HTTP_200_OK

    def test_returns_list_categories_inactives(
        self, api_client_auth, categories_inactives_url
    ):
        response = api_client_auth.get(categories_inactives_url)
        assert response.status_code == status.HTTP_200_OK

    def test_search_categories(self, api_client_auth, categories_url, category):
        response = api_client_auth.get(f"{categories_url}?search={category.name}")
        assert len(response.data) >= 1

    def test_filter_state_categories(self, api_client_auth, categories_url, category):
        response = api_client_auth.get(f"{categories_url}?state={category.state}")
        assert len(response.data) >= 1
