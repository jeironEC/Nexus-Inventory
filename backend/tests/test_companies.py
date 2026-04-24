# Internal
import pytest

# DRF
from rest_framework import status

# Models
from nexus_inventory_backend.db.models import Company


@pytest.mark.django_db
class TestGetCompany:
    def test_get_company_by_id_returns_200(
        self, api_client_auth, company_detail_url, company
    ):
        response = api_client_auth.get(company_detail_url(company.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_get_company_by_id_nonexistent_returns_404(
        self, api_client_auth, company_detail_url
    ):
        response = api_client_auth.get(company_detail_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_list_companies_returns_200(self, api_client_auth, companies_url):
        response = api_client_auth.get(companies_url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_companies_returns_list(self, api_client_auth, companies_url, company):
        response = api_client_auth.get(companies_url)
        assert len(response.data) >= 1

    def test_list_companies_fields_present(
        self, api_client_auth, companies_url, company
    ):
        response = api_client_auth.get(companies_url)
        data = response.data[0]
        assert set(data.keys()) == {
            "id",
            "nif",
            "name",
            "address",
            "number_phone",
            "email",
            "website",
            "logo",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        }

    def test_list_companies_unauthenticated_return_401(self, api_client, companies_url):
        response = api_client.get(companies_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPostCompany:
    def test_create_company_returns_201(
        self, api_client_auth, companies_url, payload_company
    ):
        response = api_client_auth.post(companies_url, payload_company)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_company_persisted(
        self, api_client_auth, companies_url, payload_company
    ):
        api_client_auth.post(companies_url, payload_company)
        assert Company.objects.filter(nif="A09876543").exists()

    def test_create_company_response_contains_fields(
        self, api_client_auth, companies_url, payload_company
    ):
        response = api_client_auth.post(companies_url, payload_company)
        data = response.data
        assert set(data.keys()) >= {
            "id",
            "nif",
            "name",
        }

    def test_create_company_unauthenticated_returns_401(
        self, api_client, companies_url, payload_company
    ):
        response = api_client.post(companies_url, payload_company)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_company_duplicate_nif_returns_400(
        self, api_client_auth, companies_url, company, payload_company
    ):
        payload = {**payload_company, "nif": company.nif}
        response = api_client_auth.post(companies_url, payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPatchCompany:
    def test_patch_company_updates_name(
        self, api_client_auth, company_detail_url, company
    ):
        response = api_client_auth.patch(
            company_detail_url(company.pk), {"name": "New Company Name"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "New Company Name"

    def test_patch_company_persists_changes(
        self, api_client_auth, company_detail_url, company
    ):
        api_client_auth.patch(
            company_detail_url(company.pk), {"name": "Updated Company"}
        )
        company.refresh_from_db()
        assert company.name == "Updated Company"

    def test_patch_company_nonexistent_returns_404(
        self, api_client_auth, company_detail_url
    ):
        response = api_client_auth.patch(company_detail_url(999), {"name": "Test"})
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteCompany:
    def test_delete_company_returns_204(
        self, api_client_auth, company_detail_url, company
    ):
        response = api_client_auth.delete(company_detail_url(company.pk))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_company_soft_deletes(
        self, api_client_auth, company_detail_url, company
    ):
        api_client_auth.delete(company_detail_url(company.pk))
        company.refresh_from_db()
        assert company.deleted_at is not None

    def test_delete_company_nonexistent_returns_404(
        self, api_client_auth, company_detail_url
    ):
        response = api_client_auth.delete(company_detail_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestStateCompany:
    def test_activate_company_returns_200(
        self, api_client_auth, company_activate_url, company
    ):
        company.is_active = False
        company.save()
        response = api_client_auth.patch(company_activate_url(company.pk))
        company.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK

    def test_deactivate_company_returns_200(
        self, api_client_auth, company_deactivate_url, company
    ):
        company.is_active = True
        company.save()
        response = api_client_auth.patch(company_deactivate_url(company.pk))
        company.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK

    def test_activate_company_not_found_returns_404(
        self, api_client_auth, company_activate_url
    ):
        response = api_client_auth.patch(company_activate_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_deactivate_company_not_found_returns_404(
        self, api_client_auth, company_deactivate_url
    ):
        response = api_client_auth.patch(company_deactivate_url(999))
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestFiltersCompany:
    def test_search_companies(self, api_client_auth, companies_url, company):
        response = api_client_auth.get(f"{companies_url}?search={company.name}")
        assert len(response.data) >= 1

    def test_filter_state_companies(self, api_client_auth, companies_url, company):
        response = api_client_auth.get(f"{companies_url}?is_active={company.is_active}")
        assert len(response.data) >= 1
