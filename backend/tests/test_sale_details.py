# Internal
import pytest

# DRF
from rest_framework import status


@pytest.mark.django_db
class TestGetSaleDetail:
    def test_list_sale_details_returns_200(
        self, api_client_auth, sale_details_url, sale, sale_detail
    ):
        response = api_client_auth.get(sale_details_url(sale.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_list_sale_details_returns_nested_elements(
        self, api_client_auth, sale_details_url, sale, sale_detail
    ):
        response = api_client_auth.get(sale_details_url(sale.pk))
        assert len(response.data) == 1

    def test_list_sale_details_fields_present(
        self, api_client_auth, sale_details_url, sale, sale_detail
    ):
        response = api_client_auth.get(sale_details_url(sale.pk))
        data = response.data[0]
        assert set(data.keys()) == {
            "id",
            "product",
            "inventory_movement",
            "quantity",
            "unit_price",
            "subtotal",
            "created_at",
        }

    def test_list_sale_details_unauthenticated_returns_401(
        self, api_client, sale_details_url, sale
    ):
        response = api_client.get(sale_details_url(sale.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_sale_detail_by_id_returns_200(
        self, api_client_auth, sale_detail_item_url, sale, sale_detail
    ):
        response = api_client_auth.get(sale_detail_item_url(sale.pk, sale_detail.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_get_sale_detail_by_id_returns_correct_detail(
        self, api_client_auth, sale_detail_item_url, sale, sale_detail
    ):
        response = api_client_auth.get(sale_detail_item_url(sale.pk, sale_detail.pk))
        assert response.data["id"] == sale_detail.pk

    def test_get_sale_detail_invalid_sale_returns_404(
        self, api_client_auth, sale_details_url
    ):
        response = api_client_auth.get(sale_details_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_sale_detail_put_returns_405(
        self, api_client_auth, sale_detail_item_url, sale, sale_detail
    ):
        response = api_client_auth.put(
            sale_detail_item_url(sale.pk, sale_detail.pk), {}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_sale_detail_post_returns_405(
        self, api_client_auth, sale_details_url, sale
    ):
        response = api_client_auth.post(sale_details_url(sale.pk), {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
