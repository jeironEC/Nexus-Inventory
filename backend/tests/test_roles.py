# Internal
import pytest

# DRF
from rest_framework import status

# Models
from nexus_inventory_backend.db.models import Role


@pytest.mark.django_db
def test_get_role_by_id_returns_200(api_client_auth, role_detail_url, admin_role):
    response = api_client_auth.get(role_detail_url(admin_role.pk))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_list_roles_returns_200(api_client_auth, roles_url):
    response = api_client_auth.get(roles_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_roles_ruturns_list(api_client_auth, roles_url, admin_role, cashier_role):
    response = api_client_auth.get(roles_url)
    assert len(response.data) == 2


@pytest.mark.django_db
def test_list_roles_fields_present(api_client_auth, roles_url, admin_role):
    response = api_client_auth.get(roles_url)
    data = response.data[0]
    assert set(data.keys()) == {"id", "name", "description", "created_at"}


@pytest.mark.django_db
def test_list_roles_unauthenticated_return_401(api_client, roles_url):
    response = api_client.get(roles_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_role_returns_201(api_client_auth, roles_url, payload_role_cashier):
    response = api_client_auth.post(roles_url, payload_role_cashier)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_role_persisted(api_client_auth, roles_url, payload_role_cashier):
    api_client_auth.post(roles_url, payload_role_cashier)
    assert Role.objects.filter(name="Cajero").exists()


@pytest.mark.django_db
def test_create_role_response_contains_fields(
    api_client_auth, roles_url, payload_role_cashier
):
    response = api_client_auth.post(roles_url, payload_role_cashier)
    assert response.data["name"] == "Cajero"


@pytest.mark.django_db
def test_create_role_duplicate_name_returns_400(
    api_client_auth, roles_url, admin_role, cashier_role, payload_role_cashier
):
    response = api_client_auth.post(roles_url, payload_role_cashier)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_role_duplicate_name_case_insensitive_returns_400(
    api_client_auth, roles_url, cashier_role, payload_role_cashier
):
    payload_role_cashier["name"] = cashier_role.name.upper()
    response = api_client_auth.post(roles_url, payload_role_cashier)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_role_missing_name_returns_400(
    api_client_auth, roles_url, payload_role_no_name
):
    response = api_client_auth.post(roles_url, payload_role_no_name)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_role_missing_description_returns_400(
    api_client_auth, roles_url, payload_role_no_description
):
    response = api_client_auth.post(roles_url, payload_role_no_description)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_role_unauthenticated_returns_401(
    api_client, roles_url, payload_role_cashier
):
    response = api_client.post(roles_url, payload_role_cashier)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_patch_role_updates_name(api_client_auth, role_detail_url, cashier_role):
    response = api_client_auth.patch(
        role_detail_url(cashier_role.pk), {"name": "Encargado de ventas"}
    )
    assert response.data["name"] == "Encargado de ventas"


@pytest.mark.django_db
def test_patch_role_updates_description(api_client_auth, role_detail_url, cashier_role):
    response = api_client_auth.patch(
        role_detail_url(cashier_role.pk),
        {"description": "Controla todos los usuarios del sistema"},
    )
    assert response.data["description"] == "Controla todos los usuarios del sistema"


@pytest.mark.django_db
def test_patch_role_persists_changes(api_client_auth, role_detail_url, admin_role):
    api_client_auth.patch(role_detail_url(admin_role.pk), {"name": "Cajero"})
    admin_role.refresh_from_db()
    assert admin_role.name == "Cajero"


@pytest.mark.django_db
def test_patch_role_nonexistent_returns_404(api_client_auth, role_detail_url):
    response = api_client_auth.patch(role_detail_url(999), {"name": "Inexistent"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_patch_role_duplicate_name_returns_400(
    api_client_auth, role_detail_url, sales_manager_role, purchasing_manager_role
):
    response = api_client_auth.patch(
        role_detail_url(sales_manager_role.pk), {"name": purchasing_manager_role.name}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_patch_role_same_name_on_self_returns_200(
    api_client_auth, role_detail_url, sales_manager_role
):
    response = api_client_auth.patch(
        role_detail_url(sales_manager_role.pk), {"name": sales_manager_role.name}
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_patch_role_unauthenticated_returns_401(
    api_client, role_detail_url, purchasing_manager_role
):
    response = api_client.patch(
        role_detail_url(purchasing_manager_role.pk), {"name": "x"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_role_returns_204(api_client_auth, role_detail_url, cashier_role):
    response = api_client_auth.delete(role_detail_url(cashier_role.pk))
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_role_remove_from_db(api_client_auth, role_detail_url, cashier_role):
    api_client_auth.delete(role_detail_url(cashier_role.pk))
    assert not Role.objects.filter(pk=cashier_role.pk).exists()


@pytest.mark.django_db
def test_delete_role_noexistent_returns_404(api_client_auth, role_detail_url):
    response = api_client_auth.delete(role_detail_url(999))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_role_unauthenticated_returns_401(
    api_client, role_detail_url, cashier_role
):
    response = api_client.delete(role_detail_url(cashier_role.pk))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
