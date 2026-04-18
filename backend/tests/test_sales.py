# Internal
import pytest

# DRF
from rest_framework import status

# Django
from django.utils import timezone

# Models
from nexus_inventory_backend.db.models import Sale, SaleDetail, Invoice

# Enums

# Datetime
from datetime import timedelta


@pytest.mark.django_db
class TestGetSale:
    def test_list_sales_returns_200(self, api_client_auth, sales_url):
        response = api_client_auth.get(sales_url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_sales_returns_list(
        self, api_client_auth, sales_url, sale, another_sale, sale_detail
    ):
        response = api_client_auth.get(sales_url)
        assert len(response.data) == 2

    def test_list_sales_fields_present(
        self, api_client_auth, sales_url, sale, another_sale, sale_detail
    ):
        response = api_client_auth.get(sales_url)
        data = response.data[0]
        assert set(data.keys()) == {
            "id",
            "company",
            "customer",
            "user",
            "discount_amount",
            "subtotal",
            "tax_percentage",
            "tax_amount",
            "total_amount",
            "payment_method",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "updated_by",
            "deleted_by",
        }

    def test_list_sales_unauthenticated_returns_401(self, api_client, sales_url):
        response = api_client.get(sales_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_sale_by_id_returns_200(self, api_client_auth, sale_detail_url, sale):
        response = api_client_auth.get(sale_detail_url(sale.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_get_sale_by_id_returns_correct_sale(
        self, api_client_auth, sale_detail_url, sale
    ):
        response = api_client_auth.get(sale_detail_url(sale.pk))
        assert response.data["id"] == sale.pk

    def test_get_sale_by_id_unauthenticated_returns_401(
        self, api_client, sale_detail_url, sale
    ):
        response = api_client.get(sale_detail_url(sale.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPostSale:
    def test_create_sale_returns_201(self, api_client_auth, sales_url, payload_sale):
        response = api_client_auth.post(sales_url, payload_sale, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_sale_persisted(self, api_client_auth, sales_url, payload_sale):
        api_client_auth.post(sales_url, payload_sale, format="json")

        assert Sale.objects.count() == 1
        assert SaleDetail.objects.count() == 1
        assert Invoice.objects.count() == 1

    def test_create_sale_response_contains_fields(
        self, api_client_auth, sales_url, purchase, payload_sale
    ):
        response = api_client_auth.post(sales_url, payload_sale, format="json")
        data = response.data

        assert set(data.keys()) == {
            "id",
            "company_id",
            "customer_id",
            "tax_percentage",
            "payment_method",
            "details",
        }
        assert data["payment_method"] == payload_sale["payment_method"]

    def test_create_sale_unauthenticated_returns_401(
        self, api_client, sales_url, payload_sale
    ):
        response = api_client.post(sales_url, payload_sale, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_sale_missing_details_returns_400(
        self, api_client_auth, sales_url, payload_sale
    ):
        payload_sale["details"] = []
        response = api_client_auth.post(sales_url, payload_sale, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPatchSale:
    def test_patch_sale_updates_payment_method(
        self, api_client_auth, sale_detail_url, sale
    ):
        response = api_client_auth.patch(
            sale_detail_url(sale.pk), {"payment_method": "CARD"}, format="json"
        )
        assert response.data["payment_method"] == "CARD"

    def test_patch_sale_persists_changes(self, api_client_auth, sale_detail_url, sale):
        api_client_auth.patch(
            sale_detail_url(sale.pk), {"payment_method": "CARD"}, format="json"
        )
        sale.refresh_from_db()
        assert sale.payment_method == "CARD"

    def test_patch_sale_nonexistent_returns_404(self, api_client_auth, sale_detail_url):
        response = api_client_auth.patch(
            sale_detail_url(999), {"payment_method": "CARD"}, format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_sale_unauthenticated_returns_401(
        self, api_client, sale_detail_url, sale
    ):
        response = api_client.patch(
            sale_detail_url(sale.pk), {"payment_method": "CARD"}, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDeleteSale:
    def test_delete_sale_returns_204(self, api_client_auth, sale_detail_url, sale):
        response = api_client_auth.delete(sale_detail_url(sale.pk))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_sale_remove_from_db(self, api_client_auth, sale_detail_url, sale):
        api_client_auth.delete(sale_detail_url(sale.pk))
        assert not Sale.objects.filter(pk=sale.pk).exists()

    def test_delete_sale_noexistent_returns_404(self, api_client_auth, sale_detail_url):
        response = api_client_auth.delete(sale_detail_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_sale_unauthenticated_returns_401(
        self, api_client, sale_detail_url, sale
    ):
        response = api_client.delete(sale_detail_url(sale.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestFiltersSale:
    def test_sales_filters_by_state(
        self, api_client_auth, sales_url, sale, another_sale
    ):
        response = api_client_auth.get(sales_url, {"state": "COMPLETED"})
        assert len(response.data) == 2

    def test_sales_filters_date_from_correctly(self, api_client_auth, sales_url, sale):
        today = timezone.now().date()
        response = api_client_auth.get(sales_url, {"date_from": str(today)})
        assert len(response.data) >= 1

    def test_sales_filters_date_from_future_returns_empty(
        self, api_client_auth, sales_url, sale
    ):
        future = (timezone.now() + timedelta(days=30)).date()
        response = api_client_auth.get(sales_url, {"date_from": str(future)})
        assert response.data == []

    def test_sales_filters_user_id(self, api_client_auth, sales_url, sale, admin_user):
        response = api_client_auth.get(sales_url, {"user_id": admin_user.pk})
        assert len(response.data) == 1
        assert response.data[0]["user"]["id"] == admin_user.pk

    def test_sales_filters_customer_id(
        self, api_client_auth, sales_url, sale, customer
    ):
        response = api_client_auth.get(sales_url, {"customer_id": customer.pk})
        assert len(response.data) == 1
        assert response.data[0]["customer"]["id"] == customer.pk
