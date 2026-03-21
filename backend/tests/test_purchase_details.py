# Internal
import pytest

# DRF
from rest_framework import status

# Models
from nexus_inventory_backend.db.models import Purchase, PurchaseDetail


@pytest.mark.django_db
class TestGetPurchaseDetail:
    def test_list_purchase_details_returns_200(
        self,
        api_client_auth,
        purchase_details_url,
        purchase,
        payload_purchase,
        purchases_url,
    ):
        api_client_auth.post(purchases_url, payload_purchase, format="json")
        created_purchase = Purchase.objects.first()
        response = api_client_auth.get(purchase_details_url(created_purchase.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_list_purchase_details_returns_nested_elements(
        self, api_client_auth, purchase_details_url, purchases_url, payload_purchase
    ):
        api_client_auth.post(purchases_url, payload_purchase, format="json")
        created_purchase = Purchase.objects.first()
        response = api_client_auth.get(purchase_details_url(created_purchase.pk))
        assert len(response.data) == 1

    def test_list_purchase_details_fields_present(
        self, api_client_auth, purchase_details_url, purchases_url, payload_purchase
    ):
        api_client_auth.post(purchases_url, payload_purchase, format="json")
        created_purchase = Purchase.objects.first()
        response = api_client_auth.get(purchase_details_url(created_purchase.pk))
        data = response.data[0]
        assert set(data.keys()) == {
            "id",
            "product",
            "inventory_movement",
            "quantity",
            "unit_cost",
            "subtotal",
            "created_at",
        }

    def test_list_purchase_details_unauthenticated_returns_401(
        self, api_client, purchase_details_url, purchase
    ):
        response = api_client.get(purchase_details_url(purchase.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_purchase_detail_by_id_returns_200(
        self,
        api_client_auth,
        purchase_detail_item_url,
        purchases_url,
        payload_purchase,
    ):
        api_client_auth.post(purchases_url, payload_purchase, format="json")
        created_purchase = Purchase.objects.first()
        detail = PurchaseDetail.objects.first()
        response = api_client_auth.get(
            purchase_detail_item_url(created_purchase.pk, detail.pk)
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_purchase_detail_by_id_returns_correct_detail(
        self,
        api_client_auth,
        purchase_detail_item_url,
        purchases_url,
        payload_purchase,
    ):
        api_client_auth.post(purchases_url, payload_purchase, format="json")
        created_purchase = Purchase.objects.first()
        detail = PurchaseDetail.objects.first()
        response = api_client_auth.get(
            purchase_detail_item_url(created_purchase.pk, detail.pk)
        )
        assert response.data["id"] == detail.pk

    def test_get_purchase_detail_invalid_purchase_returns_404(
        self, api_client_auth, purchase_details_url
    ):
        response = api_client_auth.get(purchase_details_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_purchase_detail_unauthenticated_returns_401(
        self,
        api_client,
        purchase_detail_item_url,
        purchase,
    ):
        response = api_client.get(purchase_detail_item_url(purchase.pk, 1))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPurchaseDetailMethodsRestricted:
    def test_purchase_detail_post_returns_405(
        self, api_client_auth, purchase_details_url, purchase
    ):
        response = api_client_auth.post(purchase_details_url(purchase.pk), {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_purchase_detail_put_returns_405(
        self,
        api_client_auth,
        purchase_detail_item_url,
        purchases_url,
        payload_purchase,
    ):
        api_client_auth.post(purchases_url, payload_purchase, format="json")
        created_purchase = Purchase.objects.first()
        detail = PurchaseDetail.objects.first()
        response = api_client_auth.put(
            purchase_detail_item_url(created_purchase.pk, detail.pk), {}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_purchase_detail_patch_returns_405(
        self,
        api_client_auth,
        purchase_detail_item_url,
        purchases_url,
        payload_purchase,
    ):
        api_client_auth.post(purchases_url, payload_purchase, format="json")
        created_purchase = Purchase.objects.first()
        detail = PurchaseDetail.objects.first()
        response = api_client_auth.patch(
            purchase_detail_item_url(created_purchase.pk, detail.pk), {}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_purchase_detail_delete_returns_405(
        self,
        api_client_auth,
        purchase_detail_item_url,
        purchases_url,
        payload_purchase,
    ):
        api_client_auth.post(purchases_url, payload_purchase, format="json")
        created_purchase = Purchase.objects.first()
        detail = PurchaseDetail.objects.first()
        response = api_client_auth.delete(
            purchase_detail_item_url(created_purchase.pk, detail.pk)
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
