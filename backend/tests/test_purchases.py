# Internal
import pytest

# DRF
from rest_framework import status

# Django
from django.utils import timezone

# Models
from nexus_inventory_backend.db.models import Purchase, PurchaseDetail

# Enums

# Datetime
from datetime import timedelta


@pytest.mark.django_db
class TestGetPurchase:
    def test_list_purchases_returns_200(self, api_client_auth, purchases_url):
        response = api_client_auth.get(purchases_url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_purchases_returns_list(
        self, api_client_auth, purchases_url, purchase, another_purchase
    ):
        response = api_client_auth.get(purchases_url)
        assert len(response.data) == 2

    def test_list_purchases_fields_present(
        self, api_client_auth, purchases_url, purchase
    ):
        response = api_client_auth.get(purchases_url)
        data = response.data[0]
        assert set(data.keys()) == {
            "id",
            "company",
            "supplier",
            "user",
            "total_amount",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "updated_by",
            "deleted_by",
        }

    def test_list_purchases_supplier_nested_fields(
        self, api_client_auth, purchases_url, purchase
    ):
        response = api_client_auth.get(purchases_url)
        supplier_data = response.data[0]["supplier"]
        assert set(supplier_data.keys()) == {
            "id",
            "name",
            "nif",
            "email",
            "number_phone",
            "address",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        }

    def test_list_purchases_unauthenticated_returns_401(
        self, api_client, purchases_url
    ):
        response = api_client.get(purchases_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_purchase_by_id_returns_200(
        self, api_client_auth, purchase_detail_url, purchase
    ):
        response = api_client_auth.get(purchase_detail_url(purchase.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_get_purchase_by_id_returns_correct_purchase(
        self, api_client_auth, purchase_detail_url, purchase
    ):
        response = api_client_auth.get(purchase_detail_url(purchase.pk))
        assert response.data["id"] == purchase.pk

    def test_get_purchase_by_id_unauthenticated_returns_401(
        self, api_client, purchase_detail_url, purchase
    ):
        response = api_client.get(purchase_detail_url(purchase.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPostPurchase:
    def test_create_purchase_returns_201(
        self, api_client_auth, purchases_url, payload_purchase
    ):
        response = api_client_auth.post(purchases_url, payload_purchase, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_purchase_persisted(
        self, api_client_auth, purchases_url, payload_purchase
    ):
        api_client_auth.post(purchases_url, payload_purchase, format="json")
        assert Purchase.objects.count() == 1
        assert PurchaseDetail.objects.count() == 1

    def test_create_purchase_calculates_total_amount(
        self, api_client_auth, purchases_url, payload_purchase
    ):
        api_client_auth.post(purchases_url, payload_purchase, format="json")
        purchase = Purchase.objects.first()
        assert purchase.total_amount == 200.00

    def test_create_purchase_response_contains_fields(
        self, api_client_auth, purchases_url, payload_purchase
    ):
        response = api_client_auth.post(purchases_url, payload_purchase, format="json")
        data = response.data
        assert set(data.keys()) == {"id", "company_id", "supplier_id", "details"}

    def test_create_purchase_unauthenticated_returns_401(
        self, api_client, purchases_url, payload_purchase
    ):
        response = api_client.post(purchases_url, payload_purchase, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_purchase_missing_details_returns_400(
        self, api_client_auth, purchases_url, payload_purchase
    ):
        payload_purchase["details"] = []
        response = api_client_auth.post(purchases_url, payload_purchase, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPatchPurchase:
    def test_patch_purchase_nonexistent_returns_404(
        self, api_client_auth, purchase_detail_url
    ):
        response = api_client_auth.patch(
            purchase_detail_url(999), {"supplier_id": 1}, format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_purchase_unauthenticated_returns_401(
        self, api_client, purchase_detail_url, purchase
    ):
        response = api_client.patch(purchase_detail_url(purchase.pk), {}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPutPurchaseRestricted:
    def test_put_purchase_returns_405(
        self, api_client_auth, purchase_detail_url, purchase, payload_purchase
    ):
        response = api_client_auth.put(
            purchase_detail_url(purchase.pk), payload_purchase, format="json"
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestDeletePurchase:
    def test_delete_purchase_returns_204(
        self, api_client_auth, purchase_detail_url, purchase
    ):
        response = api_client_auth.delete(purchase_detail_url(purchase.pk))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_purchase_soft_deletes(
        self, api_client_auth, purchase_detail_url, purchase
    ):
        api_client_auth.delete(purchase_detail_url(purchase.pk))
        assert not Purchase.objects.filter(
            pk=purchase.pk, deleted_at__isnull=True
        ).exists()

    def test_delete_purchase_noexistent_returns_404(
        self, api_client_auth, purchase_detail_url
    ):
        response = api_client_auth.delete(purchase_detail_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_purchase_unauthenticated_returns_401(
        self, api_client, purchase_detail_url, purchase
    ):
        response = api_client.delete(purchase_detail_url(purchase.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestFiltersPurchase:
    def test_purchases_filters_by_state(
        self, api_client_auth, purchases_url, purchase, another_purchase
    ):
        response = api_client_auth.get(purchases_url, {"state": "COMPLETED"})
        assert len(response.data) == 2

    def test_purchases_filters_date_from_correctly(
        self, api_client_auth, purchases_url, purchase
    ):
        today = timezone.now().date()
        response = api_client_auth.get(purchases_url, {"date_from": str(today)})
        assert len(response.data) >= 1

    def test_purchases_filters_date_from_future_returns_empty(
        self, api_client_auth, purchases_url, purchase
    ):
        future = (timezone.now() + timedelta(days=30)).date()
        response = api_client_auth.get(purchases_url, {"date_from": str(future)})
        assert response.data == []

    def test_purchases_filters_by_supplier_id(
        self, api_client_auth, purchases_url, purchase, supplier
    ):
        response = api_client_auth.get(purchases_url, {"supplier_id": supplier.pk})
        assert len(response.data) == 1
        assert response.data[0]["supplier"]["id"] == supplier.pk
