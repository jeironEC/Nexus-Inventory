# Internal
import pytest

# DRF
from rest_framework import status

# Models
from nexus_inventory_backend.db.models import Product

# Enums
from nexus_inventory_backend.db.enums import State


@pytest.mark.django_db
def test_get_product_by_id_returns_200(api_client_auth, product_detail_url, product):
    response = api_client_auth.get(product_detail_url(product.pk))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_list_products_returns_200(api_client_auth, products_url):
    response = api_client_auth.get(products_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_products_ruturns_list(
    api_client_auth, products_url, product, another_product
):
    response = api_client_auth.get(products_url)
    assert len(response.data) == 2


@pytest.mark.django_db
def test_list_products_fields_present(api_client_auth, products_url, product):
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
    }


@pytest.mark.django_db
def test_list_products_unauthenticated_return_401(api_client, products_url):
    response = api_client.get(products_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_returns_list_products_actives(api_client_auth, products_actives_url):
    response = api_client_auth.get(products_actives_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_returns_list_products_inactives(api_client_auth, products_inactives_url):
    response = api_client_auth.get(products_inactives_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_filter_products_by_category(api_client_auth, product):
    response = api_client_auth.get(f"/v1/products/?category={product.category_id}")
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_search_products(api_client_auth, product):
    response = api_client_auth.get(f"/v1/products/?search={product.name}")
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_create_product_returns_201(api_client_auth, products_url, payload_product):
    response = api_client_auth.post(products_url, payload_product)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_product_persisted(api_client_auth, products_url, payload_product):
    api_client_auth.post(products_url, payload_product)
    assert Product.objects.filter(name="Product").exists()


@pytest.mark.django_db
def test_create_product_response_contains_fields(
    api_client_auth, products_url, payload_product
):
    response = api_client_auth.post(products_url, payload_product)
    assert response.data["name"] == "Product"


@pytest.mark.django_db
def test_create_product_duplicate_name_returns_400(
    api_client_auth, products_url, product, payload_product
):
    response = api_client_auth.post(products_url, payload_product)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_product_duplicate_name_case_insensitive_returns_400(
    api_client_auth, products_url, product, payload_product
):
    payload_product["name"] = product.name.upper()
    response = api_client_auth.post(products_url, payload_product)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_product_missing_unique_code_returns_400(
    api_client_auth, products_url, payload_product_no_unique_code
):
    response = api_client_auth.post(products_url, payload_product_no_unique_code)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_product_unauthenticated_returns_401(
    api_client, products_url, payload_product
):
    response = api_client.post(products_url, payload_product)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_patch_product_updates_name(api_client_auth, product_detail_url, product):
    response = api_client_auth.patch(product_detail_url(product.pk), {"name": "Pants"})
    assert response.data["name"] == "Pants"


@pytest.mark.django_db
def test_patch_product_updates_description(
    api_client_auth, product_detail_url, product
):
    response = api_client_auth.patch(
        product_detail_url(product.pk),
        {"description": "A pants products"},
    )
    assert response.data["description"] == "A pants products"


@pytest.mark.django_db
def test_patch_product_persists_changes(api_client_auth, product_detail_url, product):
    api_client_auth.patch(product_detail_url(product.pk), {"name": "Laptops"})
    product.refresh_from_db()
    assert product.name == "Laptops"


@pytest.mark.django_db
def test_patch_product_nonexistent_returns_404(api_client_auth, product_detail_url):
    response = api_client_auth.patch(product_detail_url(999), {"name": "Inexistent"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_patch_product_duplicate_name_returns_400(
    api_client_auth, product_detail_url, product, another_product
):
    response = api_client_auth.patch(
        product_detail_url(product.pk), {"name": another_product.name}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_patch_product_same_name_on_self_returns_200(
    api_client_auth, product_detail_url, product
):
    response = api_client_auth.patch(
        product_detail_url(product.pk), {"name": product.name}
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_patch_product_unauthenticated_returns_401(
    api_client, product_detail_url, product
):
    response = api_client.patch(product_detail_url(product.pk), {"name": "x"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_activate_product_returns_200(api_client_auth, product_activate_url, product):
    product.state = State.INACTIVE
    product.save()

    response = api_client_auth.patch(product_activate_url(product.pk))

    product.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_deactivate_product_returns_200(
    api_client_auth, product_deactivate_url, product
):
    product.state = State.ACTIVE
    product.save()

    response = api_client_auth.patch(product_deactivate_url(product.pk))

    product.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_activate_product_not_found_returns_404(api_client_auth, product_activate_url):
    response = api_client_auth.patch(product_activate_url(999))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_deactivate_product_not_found_returns_404(
    api_client_auth, product_deactivate_url
):
    response = api_client_auth.patch(product_deactivate_url(999))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_product_returns_204(api_client_auth, product_detail_url, product):
    response = api_client_auth.delete(product_detail_url(product.pk))
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_product_remove_from_db(api_client_auth, product_detail_url, product):
    api_client_auth.delete(product_detail_url(product.pk))
    assert not Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_delete_product_noexistent_returns_404(api_client_auth, product_detail_url):
    response = api_client_auth.delete(product_detail_url(999))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_product_unauthenticated_returns_401(
    api_client, product_detail_url, product
):
    response = api_client.delete(product_detail_url(product.pk))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
