# Internal
import pytest

# DRF
from rest_framework import status

# Models
from nexus_inventory_backend.db.models import Category

# Enums
from nexus_inventory_backend.db.enums import State


@pytest.mark.django_db
def test_get_category_by_id_returns_200(api_client_auth, category_detail_url, category):
    response = api_client_auth.get(category_detail_url(category.pk))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_list_categories_returns_200(api_client_auth, categories_url):
    response = api_client_auth.get(categories_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_categories_ruturns_list(
    api_client_auth, categories_url, category, another_category
):
    response = api_client_auth.get(categories_url)
    assert len(response.data) == 2


@pytest.mark.django_db
def test_list_categories_fields_present(api_client_auth, categories_url, category):
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


@pytest.mark.django_db
def test_list_categories_unauthenticated_return_401(api_client, categories_url):
    response = api_client.get(categories_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_returns_list_categories_actives(api_client_auth, categories_actives_url):
    response = api_client_auth.get(categories_actives_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_returns_list_categories_inactives(api_client_auth, categories_inactives_url):
    response = api_client_auth.get(categories_inactives_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_search_categories(api_client_auth, category):
    response = api_client_auth.get(f"/v1/categories/?search={category.name}")
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_create_category_returns_201(api_client_auth, categories_url, payload_category):
    response = api_client_auth.post(categories_url, payload_category)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_category_persisted(api_client_auth, categories_url, payload_category):
    api_client_auth.post(categories_url, payload_category)
    assert Category.objects.filter(name="Electronics").exists()


@pytest.mark.django_db
def test_create_category_response_contains_fields(
    api_client_auth, categories_url, payload_category
):
    response = api_client_auth.post(categories_url, payload_category)
    assert response.data["name"] == "Electronics"


@pytest.mark.django_db
def test_create_category_duplicate_name_returns_400(
    api_client_auth, categories_url, category, payload_category
):
    response = api_client_auth.post(categories_url, payload_category)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_category_duplicate_name_case_insensitive_returns_400(
    api_client_auth, categories_url, category, payload_category
):
    payload_category["name"] = category.name.upper()
    response = api_client_auth.post(categories_url, payload_category)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_category_missing_name_returns_400(
    api_client_auth, categories_url, payload_category_no_name
):
    response = api_client_auth.post(categories_url, payload_category_no_name)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_category_unauthenticated_returns_401(
    api_client, categories_url, payload_category
):
    response = api_client.post(categories_url, payload_category)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_patch_category_updates_name(api_client_auth, category_detail_url, category):
    response = api_client_auth.patch(
        category_detail_url(category.pk), {"name": "Pants"}
    )
    assert response.data["name"] == "Pants"


@pytest.mark.django_db
def test_patch_category_updates_description(
    api_client_auth, category_detail_url, category
):
    response = api_client_auth.patch(
        category_detail_url(category.pk),
        {"description": "A pants products"},
    )
    assert response.data["description"] == "A pants products"


@pytest.mark.django_db
def test_patch_category_persists_changes(
    api_client_auth, category_detail_url, category
):
    api_client_auth.patch(category_detail_url(category.pk), {"name": "Laptops"})
    category.refresh_from_db()
    assert category.name == "Laptops"


@pytest.mark.django_db
def test_patch_category_nonexistent_returns_404(api_client_auth, category_detail_url):
    response = api_client_auth.patch(category_detail_url(999), {"name": "Inexistent"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_patch_category_duplicate_name_returns_400(
    api_client_auth, category_detail_url, category, another_category
):
    response = api_client_auth.patch(
        category_detail_url(category.pk), {"name": another_category.name}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_patch_category_same_name_on_self_returns_200(
    api_client_auth, category_detail_url, category
):
    response = api_client_auth.patch(
        category_detail_url(category.pk), {"name": category.name}
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_patch_category_unauthenticated_returns_401(
    api_client, category_detail_url, category
):
    response = api_client.patch(category_detail_url(category.pk), {"name": "x"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_activate_category_returns_200(
    api_client_auth, category_activate_url, category
):
    category.state = State.INACTIVE
    category.save()

    response = api_client_auth.patch(category_activate_url(category.pk))

    category.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_deactivate_category_returns_200(
    api_client_auth, category_deactivate_url, category
):
    category.state = State.ACTIVE
    category.save()

    response = api_client_auth.patch(category_deactivate_url(category.pk))

    category.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_activate_category_not_found_returns_404(
    api_client_auth, category_activate_url
):
    response = api_client_auth.patch(category_activate_url(999))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_deactivate_category_not_found_returns_404(
    api_client_auth, category_deactivate_url
):
    response = api_client_auth.patch(category_deactivate_url(999))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_category_returns_204(api_client_auth, category_detail_url, category):
    response = api_client_auth.delete(category_detail_url(category.pk))
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_category_remove_from_db(api_client_auth, category_detail_url, category):
    api_client_auth.delete(category_detail_url(category.pk))
    assert not Category.objects.filter(pk=category.pk).exists()


@pytest.mark.django_db
def test_delete_category_noexistent_returns_404(api_client_auth, category_detail_url):
    response = api_client_auth.delete(category_detail_url(999))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_category_unauthenticated_returns_401(
    api_client, category_detail_url, category
):
    response = api_client.delete(category_detail_url(category.pk))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
