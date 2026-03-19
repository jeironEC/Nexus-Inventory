# Internal
import pytest

# DRF
from rest_framework import status

# Django
from django.utils import timezone

# Models
from nexus_inventory_backend.db.models import CustomerPromotion

# Datetime
from datetime import timedelta


@pytest.mark.django_db
class TestGetCustomerPromotion:
    def test_list_customer_promotions_returns_200(
        self, api_client_auth, customer_promotions_url
    ):
        response = api_client_auth.get(customer_promotions_url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_customer_promotions_returns_list(
        self,
        api_client_auth,
        customer_promotions_url,
        customer_promotion,
        another_customer_promotion,
    ):
        response = api_client_auth.get(customer_promotions_url)
        assert len(response.data) == 2

    def test_list_customer_promotions_fields_present(
        self,
        api_client_auth,
        customer_promotions_url,
        customer_promotion,
        another_customer_promotion,
    ):
        response = api_client_auth.get(customer_promotions_url)
        data = response.data[0]
        assert set(data.keys()) == {
            "id",
            "customer",
            "promotion",
            "applied",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        }

    def test_list_customer_promotions_unauthenticated_returns_401(
        self, api_client, customer_promotions_url
    ):
        response = api_client.get(customer_promotions_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_customer_promotions_by_id_returns_200(
        self, api_client_auth, customer_promotion_detail_url, customer_promotion
    ):
        response = api_client_auth.get(
            customer_promotion_detail_url(customer_promotion.pk)
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_customer_promotion_returns_correct_customer_promotion(
        self, api_client_auth, customer_promotion_detail_url, customer_promotion
    ):
        response = api_client_auth.get(
            customer_promotion_detail_url(customer_promotion.pk)
        )
        assert response.data["id"] == customer_promotion.pk

    def test_get_customer_promotions_by_id_unauthenticated_returns_401(
        self, api_client, customer_promotion_detail_url, customer_promotion
    ):
        response = api_client.get(customer_promotion_detail_url(customer_promotion.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPostCustomerPromotion:
    def test_create_customer_promotion_returns_201(
        self, api_client_auth, customer_promotions_url, payload_customer_promotion
    ):
        response = api_client_auth.post(
            customer_promotions_url, payload_customer_promotion
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_customer_promotion_persisted(
        self, api_client_auth, customer_promotions_url, payload_customer_promotion
    ):
        api_client_auth.post(customer_promotions_url, payload_customer_promotion)
        assert CustomerPromotion.objects.filter(
            customer_id=payload_customer_promotion["customer_id"]
        ).exists()

    def test_create_customer_promotion_response_contains_fields(
        self, api_client_auth, customer_promotions_url, payload_customer_promotion
    ):
        response = api_client_auth.post(
            customer_promotions_url, payload_customer_promotion
        )
        data = response.data
        assert set(data.keys()) == {
            "id",
            "promotion",
            "customer",
            "applied",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        }

    def test_create_customer_promotion_duplicate_email_returns_400(
        self, api_client_auth, customer_promotions_url, payload_customer_promotion
    ):
        api_client_auth.post(customer_promotions_url, payload_customer_promotion)
        response = api_client_auth.post(
            customer_promotions_url, payload_customer_promotion
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_customer_promotion_unauthenticated_returns_401(
        self, api_client, customer_promotions_url, payload_customer_promotion
    ):
        response = api_client.post(customer_promotions_url, payload_customer_promotion)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPatchCustomerPromotion:
    def test_patch_customer_promotion_updates_customer(
        self,
        api_client_auth,
        customer_promotion_detail_url,
        customer_promotion,
        another_customer,
    ):
        response = api_client_auth.patch(
            customer_promotion_detail_url(customer_promotion.pk),
            {"customer_id": another_customer.pk},
        )
        assert response.data["customer"]["id"] == another_customer.pk

    def test_patch_customer_promotion_persists_changes(
        self,
        api_client_auth,
        customer_promotion_detail_url,
        customer_promotion,
        another_customer,
    ):
        api_client_auth.patch(
            customer_promotion_detail_url(customer_promotion.pk),
            {"customer_id": another_customer.pk},
        )
        customer_promotion.refresh_from_db()
        assert customer_promotion.customer.pk == another_customer.pk

    def test_patch_customer_promotion_nonexistent_returns_404(
        self, api_client_auth, customer_promotion_detail_url
    ):
        response = api_client_auth.patch(
            customer_promotion_detail_url(999), {"customer": "Inexistent"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_customer_promotion_unauthenticated_returns_401(
        self, api_client, customer_promotion_detail_url, customer_promotion
    ):
        response = api_client.patch(
            customer_promotion_detail_url(customer_promotion.pk), {"promotion": "x"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDeleteCustomerPromotion:
    def test_delete_customer_promotion_returns_204(
        self, api_client_auth, customer_promotion_detail_url, customer_promotion
    ):
        response = api_client_auth.delete(
            customer_promotion_detail_url(customer_promotion.pk)
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_customer_promotion_remove_from_db(
        self, api_client_auth, customer_promotion_detail_url, customer_promotion
    ):
        api_client_auth.delete(customer_promotion_detail_url(customer_promotion.pk))
        assert not CustomerPromotion.objects.filter(pk=customer_promotion.pk).exists()

    def test_delete_customer_promotion_noexistent_returns_404(
        self, api_client_auth, customer_promotion_detail_url
    ):
        response = api_client_auth.delete(customer_promotion_detail_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_customer_promotion_unauthenticated_returns_401(
        self, api_client, customer_promotion_detail_url, customer_promotion
    ):
        response = api_client.delete(
            customer_promotion_detail_url(customer_promotion.pk)
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestFiltersCustomerPromotion:
    def test_customer_promotions_filters_by_applied(
        self,
        api_client_auth,
        customer_promotions_url,
        customer_promotion,
        another_customer_promotion,
    ):
        response = api_client_auth.get(customer_promotions_url, {"applied": True})
        assert len(response.data) == 1

    def test_customer_promotions_filters_date_from_correctly(
        self, api_client_auth, customer_promotions_url, customer_promotion
    ):
        today = timezone.now().date()
        response = api_client_auth.get(
            customer_promotions_url, {"date_from": str(today)}
        )
        assert len(response.data) >= 1

    def test_customer_promotions_filters_date_from_future_returns_empty(
        self, api_client_auth, customer_promotions_url, customer_promotion
    ):
        future = (timezone.now() + timedelta(days=30)).date()
        response = api_client_auth.get(
            customer_promotions_url, {"date_from": str(future)}
        )
        assert response.data == []

    def test_customer_promotions_filters_date_to_correctly(
        self, api_client_auth, customer_promotions_url, customer_promotion
    ):
        future = (timezone.now() + timedelta(days=30)).date()
        response = api_client_auth.get(
            customer_promotions_url, {"date_to": str(future)}
        )
        assert len(response.data) >= 1

    def test_customer_promotions_filters_date_from_past_returns_empty(
        self, api_client_auth, customer_promotions_url, customer_promotion
    ):
        past = (timezone.now() - timedelta(days=30)).date()
        response = api_client_auth.get(customer_promotions_url, {"date_to": str(past)})
        assert response.data == []

    def test_customer_promotions_filters_invalid_date_from_returns_400(
        self, api_client_auth, customer_promotions_url, customer_promotion
    ):
        response = api_client_auth.get(
            customer_promotions_url, {"date_from": "not-a-date"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_customer_promotions_filters_invalid_date_to_returns_400(
        self, api_client_auth, customer_promotions_url, customer_promotion
    ):
        response = api_client_auth.get(
            customer_promotions_url, {"date_to": "not-a-date"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_customer_promotions_filters_date_range_combined(
        self, api_client_auth, customer_promotions_url, customer_promotion
    ):
        today = timezone.now().date()
        future = (timezone.now() + timedelta(days=30)).date()
        response = api_client_auth.get(
            customer_promotions_url, {"date_from": str(today), "date_to": str(future)}
        )
        assert len(response.data) >= 1

    def test_customer_promotions_filters_applied_and_date_from(
        self, api_client_auth, customer_promotions_url, customer_promotion
    ):
        today = timezone.now().date()
        response = api_client_auth.get(
            customer_promotions_url,
            {
                "applied": True,
                "date_from": str(today),
            },
        )
        assert len(response.data) >= 1
