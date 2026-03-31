# Internal
import pytest

# DRF
from rest_framework import status

# Django
from django.utils import timezone

# Models
from nexus_inventory_backend.db.models import Promotion, CustomerPromotion

# Enums
from nexus_inventory_backend.db.enums import State

# Datetime
from datetime import timedelta, date


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
            "can_apply",
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
            "can_apply",
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
        response = api_client_auth.get(customer_promotions_url, {"applied": False})
        assert len(response.data) >= 1

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
                "applied": False,
                "date_from": str(today),
            },
        )
        assert len(response.data) >= 1


@pytest.mark.django_db
class TestCustomerPromotionValidations:
    def test_create_with_inactive_customer_returns_400(
        self,
        api_client_auth,
        customer_promotions_url,
        payload_customer_promotion,
        customer_inactive,
        promotion,
    ):
        payload = {
            "customer_id": customer_inactive.pk,
            "promotion_id": promotion.pk,
        }
        response = api_client_auth.post(customer_promotions_url, payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Customer is not active" in response.data["detail"]

    def test_create_with_inactive_promotion_returns_400(
        self,
        api_client_auth,
        customer_promotions_url,
        payload_customer_promotion,
        customer,
        promotion_inactive,
    ):
        payload = {
            "customer_id": customer.pk,
            "promotion_id": promotion_inactive.pk,
        }
        response = api_client_auth.post(customer_promotions_url, payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Promotion is not active" in response.data["detail"]

    def test_create_with_expired_promotion_returns_400(
        self,
        api_client_auth,
        customer_promotions_url,
        customer,
    ):
        expired_promotion = Promotion.objects.create(
            name="Expired Promo",
            discount_percentage=10,
            start_date=date(2020, 1, 1),
            end_date=date(2020, 12, 31),
            state=State.ACTIVE,
        )
        payload = {
            "customer_id": customer.pk,
            "promotion_id": expired_promotion.pk,
        }
        response = api_client_auth.post(customer_promotions_url, payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Promotion has expired" in response.data["detail"]

    def test_create_applied_default_false(
        self,
        api_client_auth,
        customer_promotions_url,
        payload_customer_promotion,
    ):
        response = api_client_auth.post(
            customer_promotions_url, payload_customer_promotion
        )
        assert not response.data["applied"]


@pytest.mark.django_db
class TestCustomerPromotionApply:
    def test_apply_promotion_returns_200(
        self, api_client_auth, customer_promotion_apply_url, customer_promotion
    ):
        response = api_client_auth.patch(
            customer_promotion_apply_url(customer_promotion.pk)
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["applied"]

    def test_apply_promotion_persists(
        self, api_client_auth, customer_promotion_apply_url, customer_promotion
    ):
        api_client_auth.patch(customer_promotion_apply_url(customer_promotion.pk))
        customer_promotion.refresh_from_db()
        assert customer_promotion.applied

    def test_apply_promotion_unauthenticated_returns_401(
        self, api_client, customer_promotion_apply_url, customer_promotion
    ):
        response = api_client.patch(customer_promotion_apply_url(customer_promotion.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_apply_promotion_nonexistent_returns_404(
        self, api_client_auth, customer_promotion_apply_url
    ):
        response = api_client_auth.patch(customer_promotion_apply_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCustomerPromotionCanApply:
    def test_can_apply_true_when_valid(
        self, api_client_auth, customer_promotions_url, customer_promotion
    ):
        response = api_client_auth.get(customer_promotions_url)
        assert response.data[0]["can_apply"]

    def test_can_apply_false_when_applied(
        self, api_client_auth, customer_promotions_url, customer_promotion
    ):
        customer_promotion.applied = True
        customer_promotion.save()
        response = api_client_auth.get(customer_promotions_url)
        assert not response.data[0]["can_apply"]

    def test_can_apply_false_when_customer_inactive(
        self, api_client_auth, customer_promotions_url, customer_promotion
    ):
        customer_promotion.customer.state = State.INACTIVE
        customer_promotion.customer.save()
        response = api_client_auth.get(customer_promotions_url)
        assert not response.data[0]["can_apply"]

    def test_can_apply_false_when_promotion_inactive(
        self, api_client_auth, customer_promotions_url, customer_promotion
    ):
        customer_promotion.promotion.state = State.INACTIVE
        customer_promotion.promotion.save()
        response = api_client_auth.get(customer_promotions_url)
        assert not response.data[0]["can_apply"]

    def test_can_apply_false_when_promotion_expired(
        self, api_client_auth, customer_promotions_url, customer_promotion
    ):
        customer_promotion.promotion.end_date = date(2020, 12, 31)
        customer_promotion.promotion.save()
        response = api_client_auth.get(customer_promotions_url)
        assert not response.data[0]["can_apply"]
