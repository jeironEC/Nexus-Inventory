# Internal
import pytest

# DRF
from rest_framework import status


@pytest.mark.django_db
class TestGetInventory:
    def test_get_list_inventories_returns_200(self, api_client_auth, inventories_url):
        response = api_client_auth.get(inventories_url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_inventories_returns_list(
        self, api_client_auth, inventories_url, inventory, another_inventory
    ):
        response = api_client_auth.get(inventories_url)
        assert len(response.data) == 2

    def test_inventory_list_empty_returns_200(self, api_client_auth, inventories_url):
        response = api_client_auth.get(inventories_url)
        assert response.data == []
        assert response.status_code == status.HTTP_200_OK

    def test_inventory_list_fields_present(
        self, api_client_auth, inventories_url, inventory
    ):
        response = api_client_auth.get(inventories_url)
        data = response.data[0]
        assert set(data.keys()) == {
            "id",
            "product",
            "quantity",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        }

    def test_inventories_list_unauthenticated_returns_401(
        self, api_client, inventories_url
    ):
        response = api_client.get(inventories_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_inventory_retrieve_returns_200(
        self, api_client_auth, inventories_product_url, product, inventory
    ):
        response = api_client_auth.get(inventories_product_url(product.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_inventory_retrieve_correct_product(
        self, api_client_auth, inventories_product_url, product, inventory
    ):
        response = api_client_auth.get(inventories_product_url(product.pk))
        assert response.data["product"]["id"] == product.pk

    def test_inventory_retrieve_correct_quantity(
        self, api_client_auth, inventories_product_url, product, inventory
    ):
        response = api_client_auth.get(inventories_product_url(product.pk))
        assert response.data["quantity"] == inventory.quantity

    def test_inventory_retrieve_nonexistent_product_returns_404(
        self, api_client_auth, inventories_product_url, inventory
    ):
        response = api_client_auth.get(inventories_product_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_inventory_retrieve_404_detail_message(
        self, api_client_auth, inventories_product_url, inventory
    ):
        response = api_client_auth.get(inventories_product_url(999))
        assert "detail" in response.data

    def test_inventory_retrieve_unautheticated_returns_401(
        self, api_client, inventories_product_url, product
    ):
        response = api_client.get(inventories_product_url(product.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestFiltersInventory:
    def test_low_stock_returns_200(
        self, api_client_auth, inventories_low_stock_url, low_inventory
    ):
        response = api_client_auth.get(inventories_low_stock_url)
        assert response.status_code == status.HTTP_200_OK

    def test_low_stock_returns_only_low_items(
        self, api_client_auth, inventories_low_stock_url, low_inventory
    ):
        response = api_client_auth.get(inventories_low_stock_url)
        assert response.data[0]["quantity"] == 4

    def test_low_stock_all_above_threshold_returns_empty(
        self, api_client_auth, inventories_low_stock_url
    ):
        response = api_client_auth.get(inventories_low_stock_url)
        assert response.data == []

    def test_low_stock_unauthenticated_returns_401(
        self, api_client, inventories_low_stock_url
    ):
        response = api_client.get(inventories_low_stock_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
