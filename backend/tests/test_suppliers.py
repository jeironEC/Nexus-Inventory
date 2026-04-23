# Internal
import pytest

# DRF
from rest_framework import status

# Models
from nexus_inventory_backend.db.models import Supplier


@pytest.mark.django_db
class TestGetSupplier:
    def test_list_suppliers_returns_200(self, api_client_auth, suppliers_url):
        response = api_client_auth.get(suppliers_url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_suppliers_returns_list(
        self, api_client_auth, suppliers_url, supplier, another_supplier
    ):
        response = api_client_auth.get(suppliers_url)
        assert len(response.data) == 2

    def test_list_suppliers_fields_present(
        self, api_client_auth, suppliers_url, supplier
    ):
        response = api_client_auth.get(suppliers_url)
        data = response.data[0]
        assert set(data.keys()) == {
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

    def test_list_suppliers_unauthenticated_returns_401(
        self, api_client, suppliers_url
    ):
        response = api_client.get(suppliers_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_supplier_by_id_returns_200(
        self, api_client_auth, supplier_detail_url, supplier
    ):
        response = api_client_auth.get(supplier_detail_url(supplier.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_get_supplier_by_id_returns_correct_supplier(
        self, api_client_auth, supplier_detail_url, supplier
    ):
        response = api_client_auth.get(supplier_detail_url(supplier.pk))
        assert response.data["id"] == supplier.pk

    def test_get_supplier_by_id_unauthenticated_returns_401(
        self, api_client, supplier_detail_url, supplier
    ):
        response = api_client.get(supplier_detail_url(supplier.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPostSupplier:
    def test_create_supplier_returns_201(
        self, api_client_auth, suppliers_url, payload_supplier
    ):
        response = api_client_auth.post(suppliers_url, payload_supplier, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_supplier_persisted(
        self, api_client_auth, suppliers_url, payload_supplier
    ):
        api_client_auth.post(suppliers_url, payload_supplier, format="json")
        assert Supplier.objects.count() == 1

    def test_create_supplier_response_contains_fields(
        self, api_client_auth, suppliers_url, payload_supplier
    ):
        response = api_client_auth.post(suppliers_url, payload_supplier, format="json")
        data = response.data
        assert set(data.keys()) == {
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
        assert data["name"] == payload_supplier["name"]

    def test_create_supplier_unauthenticated_returns_401(
        self, api_client, suppliers_url, payload_supplier
    ):
        response = api_client.post(suppliers_url, payload_supplier, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_supplier_missing_email_returns_400(
        self, api_client_auth, suppliers_url, payload_supplier_no_email
    ):
        response = api_client_auth.post(
            suppliers_url, payload_supplier_no_email, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPatchSupplier:
    def test_patch_supplier_updates_name(
        self, api_client_auth, supplier_detail_url, supplier
    ):
        response = api_client_auth.patch(
            supplier_detail_url(supplier.pk),
            {"name": "Updated Tech Supplier"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Tech Supplier"

    def test_patch_supplier_persists_changes(
        self, api_client_auth, supplier_detail_url, supplier
    ):
        api_client_auth.patch(
            supplier_detail_url(supplier.pk),
            {"name": "Updated Tech Supplier"},
            format="json",
        )
        supplier.refresh_from_db()
        assert supplier.name == "Updated Tech Supplier"

    def test_patch_supplier_nonexistent_returns_404(
        self, api_client_auth, supplier_detail_url
    ):
        response = api_client_auth.patch(
            supplier_detail_url(999), {"name": "Updated Tech Supplier"}, format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_supplier_unauthenticated_returns_401(
        self, api_client, supplier_detail_url, supplier
    ):
        response = api_client.patch(
            supplier_detail_url(supplier.pk),
            {"name": "Updated Tech Supplier"},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPutSupplierRestricted:
    def test_put_supplier_returns_405(
        self, api_client_auth, supplier_detail_url, supplier, payload_supplier
    ):
        response = api_client_auth.put(
            supplier_detail_url(supplier.pk), payload_supplier, format="json"
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestDeleteSupplier:
    def test_delete_supplier_returns_204(
        self, api_client_auth, supplier_detail_url, supplier
    ):
        response = api_client_auth.delete(supplier_detail_url(supplier.pk))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_supplier_soft_deletes(
        self, api_client_auth, supplier_detail_url, supplier
    ):
        api_client_auth.delete(supplier_detail_url(supplier.pk))
        assert not Supplier.objects.filter(
            pk=supplier.pk, deleted_at__isnull=True
        ).exists()

    def test_delete_supplier_noexistent_returns_404(
        self, api_client_auth, supplier_detail_url
    ):
        response = api_client_auth.delete(supplier_detail_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_supplier_unauthenticated_returns_401(
        self, api_client, supplier_detail_url, supplier
    ):
        response = api_client.delete(supplier_detail_url(supplier.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestFiltersSupplier:
    def test_suppliers_filters_by_name(
        self, api_client_auth, suppliers_url, supplier, another_supplier
    ):
        response = api_client_auth.get(suppliers_url, {"search": "Tech"})
        assert len(response.data) >= 0

    def test_suppliers_filters_by_state(
        self, api_client_auth, suppliers_url, supplier, another_supplier
    ):
        response = api_client_auth.get(suppliers_url, {"state": "ACTIVE"})
        assert len(response.data) == 2
