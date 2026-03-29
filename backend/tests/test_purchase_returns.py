# Internal
import pytest

# DRF
from rest_framework import status

# Django
from django.utils import timezone

# Models
from nexus_inventory_backend.db.models import (
    PurchaseReturn,
    PurchaseReturnDetail,
    InventoryMovement,
    PurchaseDetail,
)

# Enums
from nexus_inventory_backend.db.enums import OperationState, MovementType

# Datetime
from datetime import timedelta


@pytest.mark.django_db
class TestGetPurchaseReturn:
    def test_list_purchase_returns_returns_200(
        self, api_client_auth, purchase_returns_url
    ):
        response = api_client_auth.get(purchase_returns_url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_purchase_returns_returns_list(
        self, api_client_auth, purchase_returns_url, purchase_return
    ):
        response = api_client_auth.get(purchase_returns_url)
        assert len(response.data) >= 1

    def test_list_purchase_returns_fields_present(
        self, api_client_auth, purchase_returns_url, purchase_return
    ):
        response = api_client_auth.get(purchase_returns_url)
        data = response.data[0]
        assert set(data.keys()) == {
            "id",
            "purchase",
            "user",
            "reason",
            "total_amount",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "updated_by",
            "deleted_by",
        }

    def test_list_purchase_returns_purchase_nested_fields(
        self, api_client_auth, purchase_returns_url, purchase_return
    ):
        response = api_client_auth.get(purchase_returns_url)
        purchase_data = response.data[0]["purchase"]
        assert "id" in purchase_data
        assert "supplier" in purchase_data

    def test_list_purchase_returns_unauthenticated_returns_401(
        self, api_client, purchase_returns_url
    ):
        response = api_client.get(purchase_returns_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_purchase_return_by_id_returns_200(
        self, api_client_auth, purchase_return_detail_url, purchase_return
    ):
        response = api_client_auth.get(purchase_return_detail_url(purchase_return.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_get_purchase_return_by_id_returns_correct_return(
        self, api_client_auth, purchase_return_detail_url, purchase_return
    ):
        response = api_client_auth.get(purchase_return_detail_url(purchase_return.pk))
        assert response.data["id"] == purchase_return.pk

    def test_get_purchase_return_by_id_unauthenticated_returns_401(
        self, api_client, purchase_return_detail_url, purchase_return
    ):
        response = api_client.get(purchase_return_detail_url(purchase_return.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPostPurchaseReturn:
    def test_create_purchase_return_returns_201(
        self,
        api_client_auth,
        purchase_returns_url,
        purchase,
        product,
        admin_user,
    ):
        inventory_movement = InventoryMovement.objects.create(
            product=product,
            user=admin_user,
            movement_type=MovementType.IN,
            quantity=2,
        )
        PurchaseDetail.objects.create(
            purchase=purchase,
            product=product,
            inventory_movement=inventory_movement,
            quantity=2,
            unit_cost=100.00,
            subtotal=200.00,
        )
        payload = {
            "purchase_id": purchase.pk,
            "reason": "Product defective",
            "details": [
                {"product_id": product.pk, "quantity": 1, "unit_cost": "100.00"}
            ],
        }
        response = api_client_auth.post(purchase_returns_url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_purchase_return_persisted(
        self,
        api_client_auth,
        purchase_returns_url,
        purchase,
        product,
        admin_user,
    ):
        inventory_movement = InventoryMovement.objects.create(
            product=product,
            user=admin_user,
            movement_type=MovementType.IN,
            quantity=2,
        )
        PurchaseDetail.objects.create(
            purchase=purchase,
            product=product,
            inventory_movement=inventory_movement,
            quantity=2,
            unit_cost=100.00,
            subtotal=200.00,
        )
        payload = {
            "purchase_id": purchase.pk,
            "reason": "Product defective",
            "details": [
                {"product_id": product.pk, "quantity": 1, "unit_cost": "100.00"}
            ],
        }
        api_client_auth.post(purchase_returns_url, payload, format="json")
        assert PurchaseReturn.objects.count() == 1
        assert PurchaseReturnDetail.objects.count() == 1

    def test_create_purchase_return_creates_inventory_movement_out(
        self,
        api_client_auth,
        purchase_returns_url,
        purchase,
        product,
        admin_user,
    ):
        inventory_movement = InventoryMovement.objects.create(
            product=product,
            user=admin_user,
            movement_type=MovementType.IN,
            quantity=2,
        )
        PurchaseDetail.objects.create(
            purchase=purchase,
            product=product,
            inventory_movement=inventory_movement,
            quantity=2,
            unit_cost=100.00,
            subtotal=200.00,
        )
        payload = {
            "purchase_id": purchase.pk,
            "reason": "Product defective",
            "details": [
                {"product_id": product.pk, "quantity": 1, "unit_cost": "100.00"}
            ],
        }
        api_client_auth.post(purchase_returns_url, payload, format="json")

        purchase_return = PurchaseReturn.objects.first()
        purchase_return_detail = PurchaseReturnDetail.objects.filter(
            purchase_return=purchase_return
        ).first()
        movement = purchase_return_detail.inventory_movement
        assert movement.movement_type == MovementType.OUT
        assert movement.product == product

    def test_create_purchase_return_response_contains_fields(
        self,
        api_client_auth,
        purchase_returns_url,
        purchase,
        product,
        admin_user,
    ):
        inventory_movement = InventoryMovement.objects.create(
            product=product,
            user=admin_user,
            movement_type=MovementType.IN,
            quantity=2,
        )
        PurchaseDetail.objects.create(
            purchase=purchase,
            product=product,
            inventory_movement=inventory_movement,
            quantity=2,
            unit_cost=100.00,
            subtotal=200.00,
        )
        payload = {
            "purchase_id": purchase.pk,
            "reason": "Product defective",
            "details": [
                {"product_id": product.pk, "quantity": 1, "unit_cost": "100.00"}
            ],
        }
        response = api_client_auth.post(purchase_returns_url, payload, format="json")
        data = response.data
        assert "purchase" in data or "purchase_id" in data
        assert data["reason"] == "Product defective"

    def test_create_purchase_return_unauthenticated_returns_401(
        self,
        api_client,
        purchase_returns_url,
        purchase,
        product,
        admin_user,
    ):
        inventory_movement = InventoryMovement.objects.create(
            product=product,
            user=admin_user,
            movement_type=MovementType.IN,
            quantity=2,
        )
        PurchaseDetail.objects.create(
            purchase=purchase,
            product=product,
            inventory_movement=inventory_movement,
            quantity=2,
            unit_cost=100.00,
            subtotal=200.00,
        )
        payload = {
            "purchase_id": purchase.pk,
            "reason": "Product defective",
            "details": [
                {"product_id": product.pk, "quantity": 1, "unit_cost": "100.00"}
            ],
        }
        response = api_client.post(purchase_returns_url, payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_purchase_return_missing_details_returns_400(
        self,
        api_client_auth,
        purchase_returns_url,
        purchase,
    ):
        payload = {
            "purchase_id": purchase.pk,
            "reason": "Product defective",
            "details": [],
        }
        response = api_client_auth.post(purchase_returns_url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_purchase_return_exceeds_quantity_returns_400(
        self,
        api_client_auth,
        purchase_returns_url,
        purchase,
        product,
        admin_user,
    ):
        inventory_movement = InventoryMovement.objects.create(
            product=product,
            user=admin_user,
            movement_type=MovementType.IN,
            quantity=2,
        )
        PurchaseDetail.objects.create(
            purchase=purchase,
            product=product,
            inventory_movement=inventory_movement,
            quantity=2,
            unit_cost=100.00,
            subtotal=200.00,
        )
        payload = {
            "purchase_id": purchase.pk,
            "reason": "Product defective",
            "details": [
                {"product_id": product.pk, "quantity": 100, "unit_cost": "100.00"}
            ],
        }
        response = api_client_auth.post(purchase_returns_url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPatchPurchaseReturn:
    def test_patch_purchase_return_nonexistent_returns_404(
        self, api_client_auth, purchase_return_detail_url
    ):
        response = api_client_auth.patch(
            purchase_return_detail_url(999),
            {"reason": "Updated reason"},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_purchase_return_updates_reason(
        self, api_client_auth, purchase_return_detail_url, purchase_return
    ):
        response = api_client_auth.patch(
            purchase_return_detail_url(purchase_return.pk),
            {"reason": "Updated reason"},
            format="json",
        )
        assert response.data["reason"] == "Updated reason"

    def test_patch_purchase_return_persists_changes(
        self, api_client_auth, purchase_return_detail_url, purchase_return
    ):
        api_client_auth.patch(
            purchase_return_detail_url(purchase_return.pk),
            {"reason": "Updated reason"},
            format="json",
        )
        purchase_return.refresh_from_db()
        assert purchase_return.reason == "Updated reason"

    def test_patch_purchase_return_unauthenticated_returns_401(
        self, api_client, purchase_return_detail_url, purchase_return
    ):
        response = api_client.patch(
            purchase_return_detail_url(purchase_return.pk),
            {"reason": "Updated reason"},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDeletePurchaseReturn:
    def test_delete_purchase_return_returns_204(
        self, api_client_auth, purchase_return_detail_url, purchase_return
    ):
        response = api_client_auth.delete(
            purchase_return_detail_url(purchase_return.pk)
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_purchase_return_soft_deletes(
        self, api_client_auth, purchase_return_detail_url, purchase_return
    ):
        api_client_auth.delete(purchase_return_detail_url(purchase_return.pk))
        assert not PurchaseReturn.objects.filter(
            pk=purchase_return.pk, deleted_at__isnull=True
        ).exists()

    def test_delete_purchase_return_nonexistent_returns_404(
        self, api_client_auth, purchase_return_detail_url
    ):
        response = api_client_auth.delete(purchase_return_detail_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_purchase_return_unauthenticated_returns_401(
        self, api_client, purchase_return_detail_url, purchase_return
    ):
        response = api_client.delete(purchase_return_detail_url(purchase_return.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestStatePurchaseReturn:
    def test_cancel_purchase_return_returns_200(
        self, api_client_auth, purchase_return_cancel_url, purchase_return
    ):
        response = api_client_auth.patch(purchase_return_cancel_url(purchase_return.pk))
        purchase_return.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert purchase_return.state == OperationState.CANCELED
        assert response.data["state"] == "CANCELED"

    def test_cancel_already_canceled_returns_400(
        self, api_client_auth, purchase_return_cancel_url, purchase_return
    ):
        purchase_return.state = OperationState.CANCELED
        purchase_return.save()
        response = api_client_auth.patch(purchase_return_cancel_url(purchase_return.pk))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cancel_unauthenticated_returns_401(
        self, api_client, purchase_return_cancel_url, purchase_return
    ):
        response = api_client.patch(purchase_return_cancel_url(purchase_return.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestFiltersPurchaseReturn:
    def test_purchase_returns_filters_by_state(
        self, api_client_auth, purchase_returns_url, purchase_return
    ):
        response = api_client_auth.get(purchase_returns_url, {"state": "COMPLETED"})
        assert len(response.data) >= 1

    def test_purchase_returns_filters_date_from_correctly(
        self, api_client_auth, purchase_returns_url, purchase_return
    ):
        today = timezone.now().date()
        response = api_client_auth.get(purchase_returns_url, {"date_from": str(today)})
        assert len(response.data) >= 1

    def test_purchase_returns_filters_date_from_future_returns_empty(
        self, api_client_auth, purchase_returns_url, purchase_return
    ):
        future = (timezone.now() + timedelta(days=30)).date()
        response = api_client_auth.get(purchase_returns_url, {"date_from": str(future)})
        assert response.data == []

    def test_purchase_returns_filters_by_purchase_id(
        self, api_client_auth, purchase_returns_url, purchase_return, purchase
    ):
        response = api_client_auth.get(
            purchase_returns_url, {"purchase_id": purchase.pk}
        )
        assert len(response.data) >= 1
        assert response.data[0]["purchase"]["id"] == purchase.pk


@pytest.mark.django_db
class TestPurchaseReturnDetails:
    def test_list_purchase_return_details_returns_200(
        self,
        api_client_auth,
        purchase_return_details_url,
        purchase_return,
        purchase_return_detail,
    ):
        response = api_client_auth.get(purchase_return_details_url(purchase_return.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_list_purchase_return_details_returns_nested_elements(
        self,
        api_client_auth,
        purchase_return_details_url,
        purchase_return,
        purchase_return_detail,
    ):
        response = api_client_auth.get(purchase_return_details_url(purchase_return.pk))
        assert len(response.data) >= 1

    def test_list_purchase_return_details_fields_present(
        self,
        api_client_auth,
        purchase_return_details_url,
        purchase_return,
        purchase_return_detail,
    ):
        response = api_client_auth.get(purchase_return_details_url(purchase_return.pk))
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

    def test_list_purchase_return_details_unauthenticated_returns_401(
        self, api_client, purchase_return_details_url, purchase_return
    ):
        response = api_client.get(purchase_return_details_url(purchase_return.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_purchase_return_detail_by_id_returns_200(
        self,
        api_client_auth,
        purchase_return_detail_item_url,
        purchase_return,
        purchase_return_detail,
    ):
        response = api_client_auth.get(
            purchase_return_detail_item_url(
                purchase_return.pk, purchase_return_detail.pk
            )
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_purchase_return_detail_by_id_returns_correct_detail(
        self,
        api_client_auth,
        purchase_return_detail_item_url,
        purchase_return,
        purchase_return_detail,
    ):
        response = api_client_auth.get(
            purchase_return_detail_item_url(
                purchase_return.pk, purchase_return_detail.pk
            )
        )
        assert response.data["id"] == purchase_return_detail.pk

    def test_get_purchase_return_detail_invalid_return_returns_404(
        self, api_client_auth, purchase_return_details_url
    ):
        response = api_client_auth.get(purchase_return_details_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_purchase_return_detail_unauthenticated_returns_401(
        self,
        api_client,
        purchase_return_detail_item_url,
        purchase_return,
        purchase_return_detail,
    ):
        response = api_client.get(
            purchase_return_detail_item_url(
                purchase_return.pk, purchase_return_detail.pk
            )
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_purchase_return_detail_post_returns_405(
        self, api_client_auth, purchase_return_details_url, purchase_return
    ):
        response = api_client_auth.post(
            purchase_return_details_url(purchase_return.pk), {}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_purchase_return_detail_put_returns_405(
        self,
        api_client_auth,
        purchase_return_detail_item_url,
        purchase_return,
        purchase_return_detail,
    ):
        response = api_client_auth.put(
            purchase_return_detail_item_url(
                purchase_return.pk, purchase_return_detail.pk
            ),
            {},
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_purchase_return_detail_patch_returns_405(
        self,
        api_client_auth,
        purchase_return_detail_item_url,
        purchase_return,
        purchase_return_detail,
    ):
        response = api_client_auth.patch(
            purchase_return_detail_item_url(
                purchase_return.pk, purchase_return_detail.pk
            ),
            {},
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_purchase_return_detail_delete_returns_405(
        self,
        api_client_auth,
        purchase_return_detail_item_url,
        purchase_return,
        purchase_return_detail,
    ):
        response = api_client_auth.delete(
            purchase_return_detail_item_url(
                purchase_return.pk, purchase_return_detail.pk
            )
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
