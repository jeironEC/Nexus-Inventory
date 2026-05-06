# Internal
import pytest

# DRF
from rest_framework import status


@pytest.mark.django_db
class TestPasswordResetRequest:
    def test_request_returns_400_for_nonexistent_email(
        self, api_client_auth, url_password_reset_request
    ):
        response = api_client_auth.post(
            url_password_reset_request,
            {"email": "no-exist@test.com"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPasswordResetConfirm:
    def test_confirm_without_email_returns_400(
        self, api_client_auth, url_password_reset_confirm
    ):
        response = api_client_auth.post(
            url_password_reset_confirm,
            {"new_password": "NewPassword123"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_confirm_with_invalid_email_returns_400(
        self, api_client_auth, url_password_reset_confirm
    ):
        response = api_client_auth.post(
            url_password_reset_confirm,
            {
                "email": "test@gmail.com",
                "new_password": "NewPassword123",
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_confirm_changes_password(
        self, api_client_auth, admin_user, url_password_reset_confirm
    ):
        api_client_auth.post(
            url_password_reset_confirm,
            {
                "email": admin_user.email,
                "new_password": "NewPassword123",
            },
        )
        admin_user.refresh_from_db()
        assert admin_user.check_password("NewPassword123")
