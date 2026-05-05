# Internal
import pytest

# DRF
from rest_framework import status

# Models
from nexus_inventory_backend.db.models import PasswordResetOTP


@pytest.mark.django_db
class TestPasswordResetRequest:
    def test_request_returns_200_for_nonexistent_email(
        self, api_client_auth, url_password_reset_request
    ):
        response = api_client_auth.post(
            url_password_reset_request,
            {"email": "no-exist@test.com"},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_request_creates_otp(
        self, api_client_auth, admin_user, url_password_reset_request
    ):
        api_client_auth.post(
            url_password_reset_request,
            {"email": admin_user.email},
        )
        otp = PasswordResetOTP.objects.filter(email=admin_user.email).first()
        assert otp is not None

    def test_request_creates_otp_unused(
        self, api_client_auth, admin_user, url_password_reset_request
    ):
        api_client_auth.post(
            url_password_reset_request,
            {"email": admin_user.email},
        )
        otp = PasswordResetOTP.objects.filter(email=admin_user.email).first()
        assert otp.is_used is False


@pytest.mark.django_db
class TestPasswordResetVerify:
    def test_verify_correct_otp(
        self, api_client_auth, admin_user, valid_otp, url_password_reset_verify
    ):
        otp_code, _ = valid_otp

        response = api_client_auth.post(
            url_password_reset_verify,
            {
                "email": admin_user.email,
                "otp": otp_code,
            },
        )
        assert response.status_code == status.HTTP_200_OK

    def test_verify_expired_otp(
        self, api_client_auth, admin_user, valid_otp, url_password_reset_verify
    ):
        from django.utils import timezone
        from datetime import timedelta

        otp_code, record = valid_otp

        record.expires_at = timezone.now() - timedelta(minutes=16)
        record.save(update_fields=["expires_at"])

        response = api_client_auth.post(
            url_password_reset_verify,
            {
                "email": admin_user.email,
                "otp": otp_code,
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_verify_returns_reset_token(
        self, api_client_auth, admin_user, valid_otp, url_password_reset_verify
    ):
        otp_code, _ = valid_otp

        response = api_client_auth.post(
            url_password_reset_verify,
            {"email": admin_user.email, "otp": otp_code},
        )
        assert "reset_token" in response.data


@pytest.mark.django_db
class TestPasswordResetConfirm:
    def test_confirm_without_token_returns_400(
        self, api_client_auth, url_password_reset_confirm
    ):
        response = api_client_auth.post(
            url_password_reset_confirm,
            {"new_password": "NewPassword123"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_confirm_with_invalid_token_returns_400(
        self, api_client_auth, url_password_reset_confirm
    ):
        response = api_client_auth.post(
            url_password_reset_confirm,
            {
                "reset_token": "00000000-0000-0000-00000000",
                "new_password": "NewPassword123",
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_confirm_with_used_token_returns_400(
        self, api_client_auth, used_token, url_password_reset_confirm
    ):
        response = api_client_auth.post(
            url_password_reset_confirm,
            {
                "reset_token": str(used_token),
                "new_password": "NewPassword123",
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_confirm_changes_password(
        self, api_client_auth, admin_user, valid_token, url_password_reset_confirm
    ):
        api_client_auth.post(
            url_password_reset_confirm,
            {
                "reset_token": str(valid_token),
                "new_password": "NewPassword123",
            },
        )
        admin_user.refresh_from_db()
        assert admin_user.check_password("NewPassword123")
