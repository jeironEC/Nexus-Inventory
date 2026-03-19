# Internal
import pytest

# DRF
from rest_framework import status

# Models
from nexus_inventory_backend.db.models import Product

# Enums
from nexus_inventory_backend.db.enums import State


@pytest.mark.django_db
class TestGetProduct:
    def test_get_product_by_id_returns_200(
        self, api_client_auth, product_detail_url, product
    ):
        response = api_client_auth.get(product_detail_url(product.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_get_product_by_id_nonexistent_returns_404(
        self, api_client_auth, product_detail_url
    ):
        response = api_client_auth.get(product_detail_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_list_products_returns_200(self, api_client_auth, products_url):
        response = api_client_auth.get(products_url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_products_returns_list(
        self, api_client_auth, products_url, product, another_product
    ):
        response = api_client_auth.get(products_url)
        assert len(response.data) == 2

    def test_list_products_fields_present(self, api_client_auth, products_url, product):
        response = api_client_auth.get(products_url)
        data = response.data[0]
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
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        }

    def test_list_products_unauthenticated_return_401(self, api_client, products_url):
        response = api_client.get(products_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPostProduct:
    def test_create_product_returns_201(
        self, api_client_auth, products_url, payload_product
    ):
        response = api_client_auth.post(products_url, payload_product)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_product_persisted(
        self, api_client_auth, products_url, payload_product
    ):
        api_client_auth.post(products_url, payload_product)
        assert Product.objects.filter(name="Product").exists()

    def test_create_product_response_contains_fields(
        self, api_client_auth, products_url, payload_product
    ):
        response = api_client_auth.post(products_url, payload_product)
        assert response.data["name"] == "Product"

    def test_create_product_duplicate_name_returns_400(
        self, api_client_auth, products_url, product, payload_product
    ):
        response = api_client_auth.post(products_url, payload_product)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_product_duplicate_name_case_insensitive_returns_400(
        self, api_client_auth, products_url, product, payload_product
    ):
        payload_product["name"] = product.name.upper()
        response = api_client_auth.post(products_url, payload_product)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_product_missing_unique_code_returns_400(
        self, api_client_auth, products_url, payload_product_no_unique_code
    ):
        response = api_client_auth.post(products_url, payload_product_no_unique_code)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_product_unauthenticated_returns_401(
        self, api_client, products_url, payload_product
    ):
        response = api_client.post(products_url, payload_product)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPatchProduct:
    def test_patch_product_updates_name(
        self, api_client_auth, product_detail_url, product
    ):
        response = api_client_auth.patch(
            product_detail_url(product.pk), {"name": "Pants"}
        )
        assert response.data["name"] == "Pants"

    def test_patch_product_updates_description(
        self, api_client_auth, product_detail_url, product
    ):
        response = api_client_auth.patch(
            product_detail_url(product.pk), {"description": "A pants products"}
        )
        assert response.data["description"] == "A pants products"

    def test_patch_product_persists_changes(
        self, api_client_auth, product_detail_url, product
    ):
        api_client_auth.patch(product_detail_url(product.pk), {"name": "Laptops"})
        product.refresh_from_db()
        assert product.name == "Laptops"

    def test_patch_product_nonexistent_returns_404(
        self, api_client_auth, product_detail_url
    ):
        response = api_client_auth.patch(
            product_detail_url(999), {"name": "Inexistent"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_product_duplicate_name_returns_400(
        self, api_client_auth, product_detail_url, product, another_product
    ):
        response = api_client_auth.patch(
            product_detail_url(product.pk), {"name": another_product.name}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_product_same_name_on_self_returns_200(
        self, api_client_auth, product_detail_url, product
    ):
        response = api_client_auth.patch(
            product_detail_url(product.pk), {"name": product.name}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_patch_product_unauthenticated_returns_401(
        self, api_client, product_detail_url, product
    ):
        response = api_client.patch(product_detail_url(product.pk), {"name": "x"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDeleteProduct:
    def test_delete_product_returns_204(
        self, api_client_auth, product_detail_url, product
    ):
        response = api_client_auth.delete(product_detail_url(product.pk))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_product_remove_from_db(
        self, api_client_auth, product_detail_url, product
    ):
        api_client_auth.delete(product_detail_url(product.pk))
        assert not Product.objects.filter(pk=product.pk).exists()

    def test_delete_product_noexistent_returns_404(
        self, api_client_auth, product_detail_url
    ):
        response = api_client_auth.delete(product_detail_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_product_unauthenticated_returns_401(
        self, api_client, product_detail_url, product
    ):
        response = api_client.delete(product_detail_url(product.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestStateProduct:
    def test_activate_product_returns_200(
        self, api_client_auth, product_activate_url, product
    ):
        product.state = State.INACTIVE
        product.save()
        response = api_client_auth.patch(product_activate_url(product.pk))
        product.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK

    def test_deactivate_product_returns_200(
        self, api_client_auth, product_deactivate_url, product
    ):
        product.state = State.ACTIVE
        product.save()
        response = api_client_auth.patch(product_deactivate_url(product.pk))
        product.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK

    def test_activate_product_not_found_returns_404(
        self, api_client_auth, product_activate_url
    ):
        response = api_client_auth.patch(product_activate_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_deactivate_product_not_found_returns_404(
        self, api_client_auth, product_deactivate_url
    ):
        response = api_client_auth.patch(product_deactivate_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestFiltersProduct:
    def test_returns_list_products_actives(self, api_client_auth, products_actives_url):
        response = api_client_auth.get(products_actives_url)
        assert response.status_code == status.HTTP_200_OK

    def test_returns_list_products_inactives(
        self, api_client_auth, products_inactives_url
    ):
        response = api_client_auth.get(products_inactives_url)
        assert response.status_code == status.HTTP_200_OK

    def test_filter_products_by_category(self, api_client_auth, products_url, product):
        response = api_client_auth.get(f"{products_url}?category={product.category_id}")
        assert len(response.data) >= 1

    def test_search_products(self, api_client_auth, products_url, product):
        response = api_client_auth.get(f"{products_url}?search={product.name}")
        assert len(response.data) >= 1
