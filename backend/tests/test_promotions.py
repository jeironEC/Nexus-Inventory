# Internal
import pytest

# DRF
from rest_framework import status

# Django
from django.utils import timezone

# Models
from nexus_inventory_backend.db.models import Promotion

# Enums
from nexus_inventory_backend.db.enums import State

# Datetime
from datetime import timedelta


@pytest.mark.django_db
class TestGetPromotion:
    def test_list_promotions_returns_200(self, api_client_auth, promotions_url):
        response = api_client_auth.get(promotions_url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_promotions_returns_list(
        self, api_client_auth, promotions_url, promotion, another_promotion
    ):
        response = api_client_auth.get(promotions_url)
        assert len(response.data) == 2

    def test_list_promotions_fields_present(
        self, api_client_auth, promotions_url, promotion, another_promotion
    ):
        response = api_client_auth.get(promotions_url)
        data = response.data[0]
        assert set(data.keys()) == {
            "id",
            "name",
            "description",
            "discount_percentage",
            "start_date",
            "end_date",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        }

    def test_list_promotions_unauthenticated_returns_401(
        self, api_client, promotions_url
    ):
        response = api_client.get(promotions_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_promotion_by_id_returns_200(
        self, api_client_auth, promotion_detail_url, promotion
    ):
        response = api_client_auth.get(promotion_detail_url(promotion.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_get_promotion_by_id_returns_correct_promotion(
        self, api_client_auth, promotion_detail_url, promotion
    ):
        response = api_client_auth.get(promotion_detail_url(promotion.pk))
        assert response.data["id"] == promotion.pk

    def test_get_promotion_by_id_unauthenticated_returns_401(
        self, api_client, promotion_detail_url, promotion
    ):
        response = api_client.get(promotion_detail_url(promotion.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPostPromotion:
    def test_create_promotion_returns_201(
        self, api_client_auth, promotions_url, payload_promotion
    ):
        response = api_client_auth.post(promotions_url, payload_promotion)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_promotion_persisted(
        self, api_client_auth, promotions_url, payload_promotion
    ):
        api_client_auth.post(promotions_url, payload_promotion)
        assert Promotion.objects.filter(name="promotion 2026").exists()

    def test_create_promotion_response_contains_fields(
        self, api_client_auth, promotions_url, payload_promotion
    ):
        response = api_client_auth.post(promotions_url, payload_promotion)
        data = response.data
        assert data["name"] == payload_promotion["name"]

    def test_create_promotion_unauthenticated_returns_401(
        self, api_client, promotions_url, payload_promotion
    ):
        response = api_client.post(promotions_url, payload_promotion)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPatchPromotion:
    def test_patch_promotion_updates_name(
        self, api_client_auth, promotion_detail_url, promotion
    ):
        response = api_client_auth.patch(
            promotion_detail_url(promotion.pk), {"name": "promotion 2030"}
        )
        assert response.data["name"] == "promotion 2030"

    def test_patch_promotion_persists_changes(
        self, api_client_auth, promotion_detail_url, promotion
    ):
        api_client_auth.patch(
            promotion_detail_url(promotion.pk), {"name": "promotion 2030"}
        )
        promotion.refresh_from_db()
        assert promotion.name == "promotion 2030"

    def test_patch_promotion_nonexistent_returns_404(
        self, api_client_auth, promotion_detail_url
    ):
        response = api_client_auth.patch(
            promotion_detail_url(999), {"name": "Inexistent"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_promotion_unauthenticated_returns_401(
        self, api_client, promotion_detail_url, promotion
    ):
        response = api_client.patch(promotion_detail_url(promotion.pk), {"name": "x"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDeletePromotion:
    def test_delete_promotion_returns_204(
        self, api_client_auth, promotion_detail_url, promotion
    ):
        response = api_client_auth.delete(promotion_detail_url(promotion.pk))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_promotion_remove_from_db(
        self, api_client_auth, promotion_detail_url, promotion
    ):
        api_client_auth.delete(promotion_detail_url(promotion.pk))
        assert not Promotion.objects.filter(pk=promotion.pk).exists()

    def test_delete_promotion_noexistent_returns_404(
        self, api_client_auth, promotion_detail_url
    ):
        response = api_client_auth.delete(promotion_detail_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_promotion_unauthenticated_returns_401(
        self, api_client, promotion_detail_url, promotion
    ):
        response = api_client.delete(promotion_detail_url(promotion.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestFiltersPromotion:
    def test_promotions_filters_by_state_active(
        self, api_client_auth, promotions_url, promotion, another_promotion
    ):
        response = api_client_auth.get(promotions_url, {"state": State.ACTIVE})
        assert len(response.data) == 2

    def test_promotions_filters_by_state_invalid_returns_400(
        self, api_client_auth, promotions_url, promotion
    ):
        response = api_client_auth.get(promotions_url, {"state": "PRIVATE"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_promotions_filters_start_date_correctly(
        self, api_client_auth, promotions_url, promotion
    ):
        today = timezone.now().date()
        response = api_client_auth.get(promotions_url, {"date_from": str(today)})
        assert len(response.data) >= 1

    def test_promotions_filters_start_date_future_returns_empty(
        self, api_client_auth, promotions_url, promotion
    ):
        future = (timezone.now() + timedelta(days=30)).date()
        response = api_client_auth.get(promotions_url, {"date_from": str(future)})
        assert response.data == []

    def test_promotions_filters_end_date_correctly(
        self, api_client_auth, promotions_url, promotion
    ):
        future = (timezone.now() + timedelta(days=30)).date()
        response = api_client_auth.get(promotions_url, {"date_to": str(future)})
        assert len(response.data) >= 1

    def test_promotions_filters_end_date_past_returns_empty(
        self, api_client_auth, promotions_url, promotion
    ):
        past = (timezone.now() - timedelta(days=30)).date()
        response = api_client_auth.get(promotions_url, {"date_to": str(past)})
        assert response.data == []

    def test_promtions_filters_invalid_start_date_returns_400(
        self, api_client_auth, promotions_url, promotion
    ):
        response = api_client_auth.get(promotions_url, {"date_to": "not-a-date"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_promotions_filters_invalid_end_date_returns_400(
        self, api_client_auth, promotions_url, promotion
    ):
        response = api_client_auth.get(promotions_url, {"date_to": "not-a-date"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_promotions_filters_date_range_combined(
        self, api_client_auth, promotions_url, promotion
    ):
        today = timezone.now().date()
        future = (timezone.now() + timedelta(days=30)).date()
        response = api_client_auth.get(
            promotions_url, {"start_date": str(today), "date_to": str(future)}
        )
        assert len(response.data) >= 1

    def test_promotions_filters_state_and_date_from(
        self, api_client_auth, promotions_url, promotion
    ):
        today = timezone.now().date()
        response = api_client_auth.get(
            promotions_url,
            {
                "state": State.ACTIVE,
                "date_from": str(today),
            },
        )
        assert len(response.data) >= 1

    def test_promotions_filters_discount_percentage(
        self, api_client_auth, promotions_url, promotion, another_promotion
    ):
        response = api_client_auth.get(promotions_url, {"discount_percentage__gt": 20})
        assert len(response.data) == 2
