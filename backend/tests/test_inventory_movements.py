# Internal
import pytest

# Models

# DRF
from rest_framework import status

# Django
from django.utils import timezone

# Datetime
from datetime import timedelta


def test_get_list_inventory_movements_returns_200(
    api_client_auth, inventory_movements_url
):
    response = api_client_auth.get(inventory_movements_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_inventory_movements_returns_list(
    api_client_auth,
    inventory_movements_url,
    inventory_movements,
    another_inventory_movements,
):
    response = api_client_auth.get(inventory_movements_url)
    assert len(response.data) == 2


@pytest.mark.django_db
def test_inventory_movements_list_empty_returns_200(
    api_client_auth, inventory_movements_url
):
    response = api_client_auth.get(inventory_movements_url)
    assert response.data == []
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_inventory_movements_list_fields_present(
    api_client_auth, inventory_movements_url, inventory_movements
):
    response = api_client_auth.get(inventory_movements_url)
    data = response.data[0]

    assert set(data.keys()) == {
        "id",
        "product",
        "user",
        "quantity",
        "created_at",
    }


@pytest.mark.django_db
def test_inventory_movements_product_nested_fields(
    api_client_auth, inventory_movements_url, inventory_movements
):
    response = api_client_auth.get(inventory_movements_url)
    data = response.data[0]["product"]
    assert set(data.keys()) == {
        "id",
        "category",
        "name",
        "description",
        "unique_code",
        "sale_price",
        "purchase_price",
        "state",
        "created_at",
        "updated_at",
    }


@pytest.mark.django_db
def test_inventory_movements_user_nested_fields(
    api_client_auth, inventory_movements_url, inventory_movements
):
    response = api_client_auth.get(inventory_movements_url)
    data = response.data[0]["user"]
    assert set(data.keys()) == {
        "first_name",
        "last_name",
        "email",
        "updated_at",
    }


@pytest.mark.django_db
def test_inventory_movements_user_is_null_when_not_set(
    api_client_auth, inventory_movements_url, another_inventory_movements
):
    response = api_client_auth.get(inventory_movements_url)
    assert response.data[0]["user"] is None


@pytest.mark.django_db
def test_inventory_movements_ordered_by_created_at_descending(
    api_client_auth,
    inventory_movements_url,
    inventory_movements,
    another_inventory_movements,
):
    response = api_client_auth.get(inventory_movements_url)
    dates = [item["created_at"] for item in response.data]
    assert dates == sorted(dates, reverse=True)


@pytest.mark.django_db
def test_inventory_movements_list_unauthenticated_returns_401(
    api_client, inventory_movements_url
):
    response = api_client.get(inventory_movements_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_inventory_movements_by_id_returns_200(
    api_client_auth, inventory_movements_detail_url, inventory_movements
):
    response = api_client_auth.get(
        inventory_movements_detail_url(inventory_movements.pk)
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_inventory_movements_correct(
    api_client_auth, inventory_movements_detail_url, inventory_movements
):
    response = api_client_auth.get(
        inventory_movements_detail_url(inventory_movements.pk)
    )
    assert response.data["id"] == inventory_movements.pk


@pytest.mark.django_db
def test_inventory_movements_correct_product(
    api_client_auth, inventory_movements_detail_url, inventory_movements, product
):
    response = api_client_auth.get(
        inventory_movements_detail_url(inventory_movements.pk)
    )
    assert response.data["product"]["id"] == product.pk


@pytest.mark.django_db
def test_inventory_movements_by_id_returns_404(
    api_client_auth, inventory_movements_detail_url
):
    response = api_client_auth.get(inventory_movements_detail_url(999))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_inventory_movements_by_id_returns_404_contains_detail(
    api_client_auth, inventory_movements_detail_url
):
    response = api_client_auth.get(inventory_movements_detail_url(999))
    assert "detail" in response.data


@pytest.mark.django_db
def test_inventory_movements_by_id_returns_401(
    api_client, inventory_movements_detail_url
):
    response = api_client.get(inventory_movements_detail_url(999))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_inventory_movements_filters_by_product_id(
    api_client_auth,
    inventory_movements_url,
    inventory_movements,
    another_inventory_movements,
    product,
):
    response = api_client_auth.get(inventory_movements_url, {"product_id": product.pk})
    assert all(item["product"]["id"] == product.pk for item in response.data)


@pytest.mark.django_db
def test_inventory_movements_filters_by_product_id_unknown_returns_empty(
    api_client_auth, inventory_movements_url, inventory_movements
):
    response = api_client_auth.get(inventory_movements_url, {"product_id": 999})
    assert response.data == []


@pytest.mark.django_db
def test_inventory_movements_filters_by_product_id_invalid_return_400(
    api_client_auth, inventory_movements_url, inventory_movements
):
    response = api_client_auth.get(inventory_movements_url, {"product_id": "abc"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_inventory_movements_filters_by_user_id(
    api_client_auth,
    inventory_movements_url,
    inventory_movements,
    another_inventory_movements,
    admin_user,
):
    response = api_client_auth.get(inventory_movements_url, {"user_id": admin_user.pk})
    assert response.data[0]["user"]["email"] == admin_user.email


@pytest.mark.django_db
def test_inventory_movements_filters_by_user_id_unknown_returns_empty(
    api_client_auth, inventory_movements_url, inventory_movements
):
    response = api_client_auth.get(inventory_movements_url, {"user_id": 999})
    assert response.data == []


@pytest.mark.django_db
def test_inventory_movements_filters_by_user_id_invalid_return_400(
    api_client_auth, inventory_movements_url, inventory_movements
):
    response = api_client_auth.get(inventory_movements_url, {"user_id": "abc"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_inventory_movements_filters_date_from_correctly(
    api_client_auth, inventory_movements_url, inventory_movements
):
    today = timezone.now().date()
    response = api_client_auth.get(inventory_movements_url, {"date_from": str(today)})
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_inventory_movements_filters_date_from_future_returns_empty(
    api_client_auth, inventory_movements_url, inventory_movements
):
    future = (timezone.now() + timedelta(days=30)).date()
    response = api_client_auth.get(inventory_movements_url, {"date_from": str(future)})
    assert response.data == []


@pytest.mark.django_db
def test_inventory_movements_filters_date_to_correctly(
    api_client_auth, inventory_movements_url, inventory_movements
):
    future = (timezone.now() + timedelta(days=30)).date()
    response = api_client_auth.get(inventory_movements_url, {"date_to": str(future)})
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_inventory_movements_filters_date_from_past_returns_empty(
    api_client_auth, inventory_movements_url, inventory_movements
):
    past = (timezone.now() - timedelta(days=30)).date()
    response = api_client_auth.get(inventory_movements_url, {"date_to": str(past)})
    assert response.data == []


@pytest.mark.django_db
def test_inventory_movements_filters_invalid_date_from_returns_400(
    api_client_auth, inventory_movements_url, inventory_movements
):
    response = api_client_auth.get(inventory_movements_url, {"date_from": "not-a-date"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_inventory_movements_filters_invalid_date_to_returns_400(
    api_client_auth, inventory_movements_url, inventory_movements
):
    response = api_client_auth.get(inventory_movements_url, {"date_to": "not-a-date"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_inventory_movements_filters_date_range_combined(
    api_client_auth, inventory_movements_url, inventory_movements
):
    today = timezone.now().date()
    future = (timezone.now() + timedelta(days=30)).date()
    response = api_client_auth.get(
        inventory_movements_url, {"date_from": str(today), "date_to": str(future)}
    )
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_inventory_movements_filters_product_id_and_date_from(
    api_client_auth, inventory_movements_url, inventory_movements, product
):
    today = timezone.now().date()
    response = api_client_auth.get(
        inventory_movements_url,
        {
            "product_id": product.pk,
            "date_from": str(today),
        },
    )
    assert all(item["product"]["id"] == product.pk for item in response.data)


@pytest.mark.django_db
def test_inventory_movements_filters_product_id_and_user_id(
    api_client_auth, inventory_movements_url, inventory_movements, product, admin_user
):
    response = api_client_auth.get(
        inventory_movements_url,
        {
            "product_id": product.pk,
            "user_id": admin_user.pk,
        },
    )
    assert len(response.data) == 1
