# Internal
import pytest

# DRF
from rest_framework import status

# Django
from django.utils import timezone

# Models
from nexus_inventory_backend.db.models import (
    SaleReturn,
    SaleReturnDetail,
    InventoryMovement,
    SaleDetail,
)

# Enums
from nexus_inventory_backend.db.enums import MovementType

# Datetime
from datetime import timedelta


@pytest.mark.django_db
class TestGetSaleReturn:
    def test_list_sale_returns_returns_200(self, api_client_auth, sale_returns_url):
        response = api_client_auth.get(sale_returns_url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_sale_returns_returns_list(
        self, api_client_auth, sale_returns_url, sale_return
    ):
        response = api_client_auth.get(sale_returns_url)
        assert len(response.data) >= 1

    def test_list_sale_returns_fields_present(
        self, api_client_auth, sale_returns_url, sale_return
    ):
        response = api_client_auth.get(sale_returns_url)
        data = response.data[0]
        assert set(data.keys()) == {
            "id",
            "sale",
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

    def test_list_sale_returns_sale_nested_fields(
        self, api_client_auth, sale_returns_url, sale_return
    ):
        response = api_client_auth.get(sale_returns_url)
        sale_data = response.data[0]["sale"]
        assert "id" in sale_data
        assert "customer" in sale_data

    def test_list_sale_returns_unauthenticated_returns_401(
        self, api_client, sale_returns_url
    ):
        response = api_client.get(sale_returns_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_sale_return_by_id_returns_200(
        self, api_client_auth, sale_return_detail_url, sale_return
    ):
        response = api_client_auth.get(sale_return_detail_url(sale_return.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_get_sale_return_by_id_returns_correct_return(
        self, api_client_auth, sale_return_detail_url, sale_return
    ):
        response = api_client_auth.get(sale_return_detail_url(sale_return.pk))
        assert response.data["id"] == sale_return.pk

    def test_get_sale_return_by_id_unauthenticated_returns_401(
        self, api_client, sale_return_detail_url, sale_return
    ):
        response = api_client.get(sale_return_detail_url(sale_return.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPostSaleReturn:
    def test_create_sale_return_returns_201(
        self,
        api_client_auth,
        sale_returns_url,
        sale,
        product,
        admin_user,
    ):
        inventory_movement = InventoryMovement.objects.create(
            product=product,
            user=admin_user,
            movement_type=MovementType.OUT,
            quantity=2,
        )
        SaleDetail.objects.create(
            sale=sale,
            product=product,
            inventory_movement=inventory_movement,
            quantity=2,
            unit_price=50.00,
            subtotal=100.00,
        )
        payload = {
            "sale": sale.pk,
            "reason": "Product defective",
            "details": [
                {"product_id": product.pk, "quantity": 1, "unit_price": "50.00"}
            ],
        }
        response = api_client_auth.post(sale_returns_url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_sale_return_persisted(
        self,
        api_client_auth,
        sale_returns_url,
        sale,
        product,
        admin_user,
    ):
        inventory_movement = InventoryMovement.objects.create(
            product=product,
            user=admin_user,
            movement_type=MovementType.OUT,
            quantity=2,
        )
        SaleDetail.objects.create(
            sale=sale,
            product=product,
            inventory_movement=inventory_movement,
            quantity=2,
            unit_price=50.00,
            subtotal=100.00,
        )
        payload = {
            "sale": sale.pk,
            "reason": "Product defective",
            "details": [
                {"product_id": product.pk, "quantity": 1, "unit_price": "50.00"}
            ],
        }
        api_client_auth.post(sale_returns_url, payload, format="json")
        assert SaleReturn.objects.count() == 1
        assert SaleReturnDetail.objects.count() == 1

    def test_create_sale_return_creates_inventory_movement_in(
        self,
        api_client_auth,
        sale_returns_url,
        sale,
        product,
        admin_user,
    ):
        inventory_movement = InventoryMovement.objects.create(
            product=product,
            user=admin_user,
            movement_type=MovementType.OUT,
            quantity=2,
        )
        SaleDetail.objects.create(
            sale=sale,
            product=product,
            inventory_movement=inventory_movement,
            quantity=2,
            unit_price=50.00,
            subtotal=100.00,
        )
        payload = {
            "sale": sale.pk,
            "reason": "Product defective",
            "details": [
                {"product_id": product.pk, "quantity": 1, "unit_price": "50.00"}
            ],
        }
        api_client_auth.post(sale_returns_url, payload, format="json")

        sale_return = SaleReturn.objects.first()
        sale_return_detail = SaleReturnDetail.objects.filter(
            sale_return=sale_return
        ).first()
        movement = sale_return_detail.inventory_movement
        assert movement.movement_type == MovementType.IN
        assert movement.product == product

    def test_create_sale_return_response_contains_fields(
        self,
        api_client_auth,
        sale_returns_url,
        sale,
        product,
        admin_user,
    ):
        inventory_movement = InventoryMovement.objects.create(
            product=product,
            user=admin_user,
            movement_type=MovementType.OUT,
            quantity=2,
        )
        SaleDetail.objects.create(
            sale=sale,
            product=product,
            inventory_movement=inventory_movement,
            quantity=2,
            unit_price=50.00,
            subtotal=100.00,
        )
        payload = {
            "sale": sale.pk,
            "reason": "Product defective",
            "details": [
                {"product_id": product.pk, "quantity": 1, "unit_price": "50.00"}
            ],
        }
        response = api_client_auth.post(sale_returns_url, payload, format="json")
        data = response.data
        assert "sale" in data
        assert data["reason"] == "Product defective"

    def test_create_sale_return_unauthenticated_returns_401(
        self,
        api_client,
        sale_returns_url,
        sale,
        product,
        admin_user,
    ):
        inventory_movement = InventoryMovement.objects.create(
            product=product,
            user=admin_user,
            movement_type=MovementType.OUT,
            quantity=2,
        )
        SaleDetail.objects.create(
            sale=sale,
            product=product,
            inventory_movement=inventory_movement,
            quantity=2,
            unit_price=50.00,
            subtotal=100.00,
        )
        payload = {
            "sale": sale.pk,
            "reason": "Product defective",
            "details": [
                {"product_id": product.pk, "quantity": 1, "unit_price": "50.00"}
            ],
        }
        response = api_client.post(sale_returns_url, payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_sale_return_missing_details_returns_400(
        self,
        api_client_auth,
        sale_returns_url,
        sale,
        product,
        admin_user,
    ):
        inventory_movement = InventoryMovement.objects.create(
            product=product,
            user=admin_user,
            movement_type=MovementType.OUT,
            quantity=2,
        )
        SaleDetail.objects.create(
            sale=sale,
            product=product,
            inventory_movement=inventory_movement,
            quantity=2,
            unit_price=50.00,
            subtotal=100.00,
        )
        payload = {
            "sale": sale.pk,
            "reason": "Product defective",
            "details": [],
        }
        response = api_client_auth.post(sale_returns_url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_sale_return_exceeds_quantity_returns_400(
        self,
        api_client_auth,
        sale_returns_url,
        sale,
        product,
        admin_user,
    ):
        inventory_movement = InventoryMovement.objects.create(
            product=product,
            user=admin_user,
            movement_type=MovementType.OUT,
            quantity=2,
        )
        SaleDetail.objects.create(
            sale=sale,
            product=product,
            inventory_movement=inventory_movement,
            quantity=2,
            unit_price=50.00,
            subtotal=100.00,
        )
        payload = {
            "sale": sale.pk,
            "reason": "Product defective",
            "details": [
                {"product_id": product.pk, "quantity": 100, "unit_price": "50.00"}
            ],
        }
        response = api_client_auth.post(sale_returns_url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPatchSaleReturn:
    def test_patch_sale_return_nonexistent_returns_404(
        self, api_client_auth, sale_return_detail_url
    ):
        response = api_client_auth.patch(
            sale_return_detail_url(999), {"reason": "Updated reason"}, format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_sale_return_updates_reason(
        self, api_client_auth, sale_return_detail_url, sale_return
    ):
        response = api_client_auth.patch(
            sale_return_detail_url(sale_return.pk),
            {"reason": "Updated reason"},
            format="json",
        )
        assert response.data["reason"] == "Updated reason"

    def test_patch_sale_return_persists_changes(
        self, api_client_auth, sale_return_detail_url, sale_return
    ):
        api_client_auth.patch(
            sale_return_detail_url(sale_return.pk),
            {"reason": "Updated reason"},
            format="json",
        )
        sale_return.refresh_from_db()
        assert sale_return.reason == "Updated reason"

    def test_patch_sale_return_unauthenticated_returns_401(
        self, api_client, sale_return_detail_url, sale_return
    ):
        response = api_client.patch(
            sale_return_detail_url(sale_return.pk),
            {"reason": "Updated reason"},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDeleteSaleReturn:
    def test_delete_sale_return_returns_204(
        self, api_client_auth, sale_return_detail_url, sale_return
    ):
        response = api_client_auth.delete(sale_return_detail_url(sale_return.pk))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_sale_return_soft_deletes(
        self, api_client_auth, sale_return_detail_url, sale_return
    ):
        api_client_auth.delete(sale_return_detail_url(sale_return.pk))
        assert not SaleReturn.objects.filter(
            pk=sale_return.pk, deleted_at__isnull=True
        ).exists()

    def test_delete_sale_return_nonexistent_returns_404(
        self, api_client_auth, sale_return_detail_url
    ):
        response = api_client_auth.delete(sale_return_detail_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_sale_return_unauthenticated_returns_401(
        self, api_client, sale_return_detail_url, sale_return
    ):
        response = api_client.delete(sale_return_detail_url(sale_return.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestFiltersSaleReturn:
    def test_sale_returns_filters_by_state(
        self, api_client_auth, sale_returns_url, sale_return
    ):
        response = api_client_auth.get(sale_returns_url, {"state": "COMPLETED"})
        assert len(response.data) >= 1

    def test_sale_returns_filters_date_from_correctly(
        self, api_client_auth, sale_returns_url, sale_return
    ):
        today = timezone.now().date()
        response = api_client_auth.get(sale_returns_url, {"date_from": str(today)})
        assert len(response.data) >= 1

    def test_sale_returns_filters_date_from_future_returns_empty(
        self, api_client_auth, sale_returns_url, sale_return
    ):
        future = (timezone.now() + timedelta(days=30)).date()
        response = api_client_auth.get(sale_returns_url, {"date_from": str(future)})
        assert response.data == []

    def test_sale_returns_filters_by_sale_id(
        self, api_client_auth, sale_returns_url, sale_return, sale
    ):
        response = api_client_auth.get(sale_returns_url, {"sale_id": sale.pk})
        assert len(response.data) >= 1
        assert response.data[0]["sale"]["id"] == sale.pk


@pytest.mark.django_db
class TestSaleReturnDetails:
    def test_list_sale_return_details_returns_200(
        self,
        api_client_auth,
        sale_return_details_url,
        sale_return,
        sale_return_detail,
    ):
        response = api_client_auth.get(sale_return_details_url(sale_return.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_list_sale_return_details_returns_nested_elements(
        self,
        api_client_auth,
        sale_return_details_url,
        sale_return,
        sale_return_detail,
    ):
        response = api_client_auth.get(sale_return_details_url(sale_return.pk))
        assert len(response.data) >= 1

    def test_list_sale_return_details_fields_present(
        self,
        api_client_auth,
        sale_return_details_url,
        sale_return,
        sale_return_detail,
    ):
        response = api_client_auth.get(sale_return_details_url(sale_return.pk))
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

    def test_list_sale_return_details_unauthenticated_returns_401(
        self, api_client, sale_return_details_url, sale_return
    ):
        response = api_client.get(sale_return_details_url(sale_return.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_sale_return_detail_by_id_returns_200(
        self,
        api_client_auth,
        sale_return_detail_item_url,
        sale_return,
        sale_return_detail,
    ):
        response = api_client_auth.get(
            sale_return_detail_item_url(sale_return.pk, sale_return_detail.pk)
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_sale_return_detail_by_id_returns_correct_detail(
        self,
        api_client_auth,
        sale_return_detail_item_url,
        sale_return,
        sale_return_detail,
    ):
        response = api_client_auth.get(
            sale_return_detail_item_url(sale_return.pk, sale_return_detail.pk)
        )
        assert response.data["id"] == sale_return_detail.pk

    def test_get_sale_return_detail_invalid_return_returns_404(
        self, api_client_auth, sale_return_details_url
    ):
        response = api_client_auth.get(sale_return_details_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_sale_return_detail_unauthenticated_returns_401(
        self, api_client, sale_return_detail_item_url, sale_return, sale_return_detail
    ):
        response = api_client.get(
            sale_return_detail_item_url(sale_return.pk, sale_return_detail.pk)
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_sale_return_detail_post_returns_405(
        self, api_client_auth, sale_return_details_url, sale_return
    ):
        response = api_client_auth.post(sale_return_details_url(sale_return.pk), {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_sale_return_detail_put_returns_405(
        self,
        api_client_auth,
        sale_return_detail_item_url,
        sale_return,
        sale_return_detail,
    ):
        response = api_client_auth.put(
            sale_return_detail_item_url(sale_return.pk, sale_return_detail.pk), {}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_sale_return_detail_patch_returns_405(
        self,
        api_client_auth,
        sale_return_detail_item_url,
        sale_return,
        sale_return_detail,
    ):
        response = api_client_auth.patch(
            sale_return_detail_item_url(sale_return.pk, sale_return_detail.pk), {}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_sale_return_detail_delete_returns_405(
        self,
        api_client_auth,
        sale_return_detail_item_url,
        sale_return,
        sale_return_detail,
    ):
        response = api_client_auth.delete(
            sale_return_detail_item_url(sale_return.pk, sale_return_detail.pk)
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
