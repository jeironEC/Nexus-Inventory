# Internal
import pytest

# DRF
from rest_framework import status


@pytest.mark.django_db
def test_get_list_inventories_returns_200(api_client_auth, inventories_url):
    response = api_client_auth.get(inventories_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_inventories_returns_list(
    api_client_auth, inventories_url, inventory, another_inventory
):
    response = api_client_auth.get(inventories_url)
    assert len(response.data) == 2


@pytest.mark.django_db
def test_inventory_list_empty_returns_200(api_client_auth, inventories_url):
    response = api_client_auth.get(inventories_url)
    assert response.data == []
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_inventory_list_fields_present(api_client_auth, inventories_url, inventory):
    response = api_client_auth.get(inventories_url)
    data = response.data[0]

    assert set(data.keys()) == {
        "id",
        "product",
        "quantity",
        "updated_at",
    }


@pytest.mark.django_db
def test_inventories_list_unauthenticated_returns_401(api_client, inventories_url):
    response = api_client.get(inventories_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_inventory_retrieve_returns_200(
    api_client_auth, inventories_product_url, product, inventory
):
    response = api_client_auth.get(inventories_product_url(product.pk))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_inventory_retrieve_correct_product(
    api_client_auth, inventories_product_url, product, inventory
):
    response = api_client_auth.get(inventories_product_url(product.pk))

    assert response.data["product"]["id"] == product.pk


@pytest.mark.django_db
def test_inventory_retrieve_correct_quantity(
    api_client_auth, inventories_product_url, product, inventory
):
    response = api_client_auth.get(inventories_product_url(product.pk))
    assert response.data["quantity"] == inventory.quantity


@pytest.mark.django_db
def test_inventory_retrieve_nonexistent_product_returns_404(
    api_client_auth, inventories_product_url, inventory
):
    response = api_client_auth.get(inventories_product_url(999))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_inventory_retrieve_404_detail_message(
    api_client_auth, inventories_product_url, inventory
):
    response = api_client_auth.get(inventories_product_url(999))
    assert "detail" in response.data


@pytest.mark.django_db
def test_inventory_retrieve_unautheticated_returns_401(
    api_client, inventories_product_url, product
):
    response = api_client.get(inventories_product_url(product.pk))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_low_stock_returns_200(
    api_client_auth, inventories_low_stock_url, low_inventory
):
    response = api_client_auth.get(inventories_low_stock_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_low_stock_returns_only_low_items(
    api_client_auth, inventories_low_stock_url, low_inventory
):
    response = api_client_auth.get(inventories_low_stock_url)
    assert response.data[0]["quantity"] == 4


@pytest.mark.django_db
def test_low_stock_all_above_threshold_returns_empty(
    api_client_auth, inventories_low_stock_url
):
    response = api_client_auth.get(inventories_low_stock_url)
    assert response.data == []


@pytest.mark.django_db
def test_low_stock_unauthenticated_returns_401(api_client, inventories_low_stock_url):
    response = api_client.get(inventories_low_stock_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
