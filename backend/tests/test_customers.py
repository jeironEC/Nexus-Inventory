# Internal
import pytest

# DRF
from rest_framework import status

# Django
from django.utils import timezone

# Models
from nexus_inventory_backend.db.models import Customer

# Enums
from nexus_inventory_backend.db.enums import State

# Datetime
from datetime import timedelta


@pytest.mark.django_db
def test_list_customers_returns_200(api_client_auth, customers_url):
    response = api_client_auth.get(customers_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_customers_returns_list(
    api_client_auth, customers_url, customer, another_customer
):
    response = api_client_auth.get(customers_url)
    assert len(response.data) == 2


@pytest.mark.django_db
def test_list_customers_fields_present(
    api_client_auth, customers_url, customer, another_customer
):
    response = api_client_auth.get(customers_url)
    data = response.data[0]
    assert set(data.keys()) == {
        "id",
        "first_name",
        "last_name",
        "email",
        "number_phone",
        "address",
        "state",
        "created_at",
        "updated_at",
    }


@pytest.mark.django_db
def test_list_customers_unauthenticated_returns_401(api_client, customers_url):
    response = api_client.get(customers_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_customer_by_id_returns_200(api_client_auth, customer_detail_url, customer):
    response = api_client_auth.get(customer_detail_url(customer.pk))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_customer_by_id_returns_correct_customer(
    api_client_auth, customer_detail_url, customer
):
    response = api_client_auth.get(customer_detail_url(customer.pk))
    assert response.data["id"] == customer.pk


@pytest.mark.django_db
def test_get_promotions_customer_returns_list(
    api_client_auth, customer_list_promotions_url, customer_promotion, customer
):
    response = api_client_auth.get(customer_list_promotions_url(customer.pk))
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_get_customer_by_id_unauthenticated_returns_401(
    api_client, customer_detail_url, customer
):
    response = api_client.get(customer_detail_url(customer.pk))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_customer_returns_201(api_client_auth, customers_url, payload_customer):
    response = api_client_auth.post(customers_url, payload_customer)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_customer_persisted(api_client_auth, customers_url, payload_customer):
    api_client_auth.post(customers_url, payload_customer)
    assert Customer.objects.filter(first_name="Abel").exists()


@pytest.mark.django_db
def test_create_customer_response_contains_fields(
    api_client_auth, customers_url, payload_customer
):
    response = api_client_auth.post(customers_url, payload_customer)
    data = response.data

    for field in payload_customer:
        assert data[field] == payload_customer[field]


@pytest.mark.django_db
def test_create_customer_duplicate_email_returns_400(
    api_client_auth, customers_url, customer, payload_customer
):
    api_client_auth.post(customers_url, payload_customer)
    response = api_client_auth.post(customers_url, payload_customer)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_customer_unauthenticated_returns_401(
    api_client, customers_url, payload_customer
):
    response = api_client.post(customers_url, payload_customer)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_customer_promotion_returns_201(
    api_client_auth, customer_promotion_assign_url, customer, promotion
):
    response = api_client_auth.post(
        customer_promotion_assign_url(customer.pk), {"promotion": promotion.pk}
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_patch_customer_updates_first_name(
    api_client_auth, customer_detail_url, customer
):
    response = api_client_auth.patch(
        customer_detail_url(customer.pk), {"first_name": "Alberto"}
    )
    assert response.data["first_name"] == "Alberto"


@pytest.mark.django_db
def test_patch_customer_persists_changes(
    api_client_auth, customer_detail_url, customer
):
    api_client_auth.patch(customer_detail_url(customer.pk), {"first_name": "Alberto"})
    customer.refresh_from_db()
    assert customer.first_name == "Alberto"


@pytest.mark.django_db
def test_patch_customer_nonexistent_returns_404(api_client_auth, customer_detail_url):
    response = api_client_auth.patch(
        customer_detail_url(999), {"first_name": "Inexistent"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_patch_customer_duplicate_email_returns_400(
    api_client_auth, customer_detail_url, customer, another_customer
):
    response = api_client_auth.patch(
        customer_detail_url(customer.pk), {"email": another_customer.email}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_patch_customer_unauthenticated_returns_401(
    api_client, customer_detail_url, customer
):
    response = api_client.patch(customer_detail_url(customer.pk), {"name": "x"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_customer_returns_204(api_client_auth, customer_detail_url, customer):
    response = api_client_auth.delete(customer_detail_url(customer.pk))
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_customer_remove_from_db(api_client_auth, customer_detail_url, customer):
    api_client_auth.delete(customer_detail_url(customer.pk))
    assert not Customer.objects.filter(pk=customer.pk).exists()


@pytest.mark.django_db
def test_delete_customer_noexistent_returns_404(api_client_auth, customer_detail_url):
    response = api_client_auth.delete(customer_detail_url(999))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_customer_unauthenticated_returns_401(
    api_client, customer_detail_url, customer
):
    response = api_client.delete(customer_detail_url(customer.pk))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_customers_filters_by_state_active(
    api_client_auth,
    customers_url,
    customer,
    another_customer,
):
    response = api_client_auth.get(customers_url, {"state": State.ACTIVE})
    assert len(response.data) == 2


@pytest.mark.django_db
def test_customers_filters_by_state_invalid_returns_400(
    api_client_auth, customers_url, customer
):
    response = api_client_auth.get(customers_url, {"state": "PRIVATE"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_customers_filters_date_from_correctly(
    api_client_auth, customers_url, customer
):
    today = timezone.now().date()
    response = api_client_auth.get(customers_url, {"date_from": str(today)})
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_customers_filters_date_from_future_returns_empty(
    api_client_auth, customers_url, customer
):
    future = (timezone.now() + timedelta(days=30)).date()
    response = api_client_auth.get(customers_url, {"date_from": str(future)})
    assert response.data == []


@pytest.mark.django_db
def test_customers_filters_date_to_correctly(api_client_auth, customers_url, customer):
    future = (timezone.now() + timedelta(days=30)).date()
    response = api_client_auth.get(customers_url, {"date_to": str(future)})
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_customers_filters_date_from_past_returns_empty(
    api_client_auth, customers_url, customer
):
    past = (timezone.now() - timedelta(days=30)).date()
    response = api_client_auth.get(customers_url, {"date_to": str(past)})
    assert response.data == []


@pytest.mark.django_db
def test_customers_filters_invalid_date_from_returns_400(
    api_client_auth, customers_url, customer
):
    response = api_client_auth.get(customers_url, {"date_from": "not-a-date"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_customers_filters_invalid_date_to_returns_400(
    api_client_auth, customers_url, customer
):
    response = api_client_auth.get(customers_url, {"date_to": "not-a-date"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_customers_filters_date_range_combined(
    api_client_auth, customers_url, customer
):
    today = timezone.now().date()
    future = (timezone.now() + timedelta(days=30)).date()
    response = api_client_auth.get(
        customers_url, {"date_from": str(today), "date_to": str(future)}
    )
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_customers_filters_state_and_date_from(
    api_client_auth, customers_url, customer
):
    today = timezone.now().date()
    response = api_client_auth.get(
        customers_url,
        {
            "state": State.ACTIVE,
            "date_from": str(today),
        },
    )
    assert len(response.data) >= 1
