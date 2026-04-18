# Internal
import pytest

# DRF
from rest_framework import status

# Django
from django.utils import timezone

# Models

# Enums
from nexus_inventory_backend.db.enums import InvoiceState

# Datetime
from datetime import timedelta


@pytest.mark.django_db
class TestGetInvoice:
    def test_list_invoices_returns_200(self, api_client_auth, invoices_url):
        response = api_client_auth.get(invoices_url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_invoices_returns_list(
        self, api_client_auth, invoices_url, invoice_sale, invoice_purchase
    ):
        response = api_client_auth.get(invoices_url)
        assert len(response.data) == 2

    def test_list_invoices_fields_present(
        self, api_client_auth, invoices_url, invoice_sale
    ):
        response = api_client_auth.get(invoices_url)
        data = response.data[0]
        assert set(data.keys()) == {
            "id",
            "company",
            "sale",
            "purchase",
            "invoice_type",
            "number_invoice",
            "pdf_generated",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
        }

    def test_list_invoices_sale_nested_fields(
        self, api_client_auth, invoices_url, invoice_sale
    ):
        response = api_client_auth.get(invoices_url)
        data = response.data[0]["sale"]
        assert set(data.keys()) == {
            "id",
            "company",
            "customer",
            "user",
            "discount_amount",
            "subtotal",
            "tax_percentage",
            "tax_amount",
            "total_amount",
            "payment_method",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "updated_by",
            "deleted_by",
        }

    def test_list_invoices_purchase_nested_fields(
        self, api_client_auth, invoices_url, invoice_purchase
    ):
        response = api_client_auth.get(invoices_url)
        data = response.data[0]["purchase"]
        assert set(data.keys()) == {
            "id",
            "company",
            "supplier",
            "user",
            "total_amount",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "updated_by",
            "deleted_by",
        }

    def test_list_invoices_unauthenticated_returns_401(self, api_client, invoices_url):
        response = api_client.get(invoices_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_invoice_by_id_returns_200(
        self, api_client_auth, invoice_detail_url, invoice_sale
    ):
        response = api_client_auth.get(invoice_detail_url(invoice_sale.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_get_invoice_by_id_returns_correct_invoice(
        self, api_client_auth, invoice_detail_url, invoice_purchase
    ):
        response = api_client_auth.get(invoice_detail_url(invoice_purchase.pk))
        assert response.data["id"] == invoice_purchase.pk

    def test_get_invoice_by_id_unauthenticated_returns_401(
        self, api_client, invoice_detail_url, invoice_sale
    ):
        response = api_client.get(invoice_detail_url(invoice_sale.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestInvoicePostAndPutRestricted:
    def test_post_invoice_returns_405(self, api_client_auth, invoices_url):
        response = api_client_auth.post(invoices_url, {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_invoice_returns_405(
        self, api_client_auth, invoice_detail_url, invoice_sale
    ):
        response = api_client_auth.put(invoice_detail_url(invoice_sale.pk), {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_patch_invoice_returns_405_if_not_cancel(
        self, api_client_auth, invoice_detail_url, invoice_purchase
    ):
        response = api_client_auth.patch(
            invoice_detail_url(invoice_purchase.pk), {"state": "some"}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_invoice_returns_405(
        self, api_client_auth, invoice_detail_url, invoice_sale
    ):
        response = api_client_auth.delete(invoice_detail_url(invoice_sale.pk))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestStateInvoice:
    def test_cancel_invoice_returns_200(
        self, api_client_auth, invoice_cancel_url, invoice_purchase
    ):
        response = api_client_auth.patch(invoice_cancel_url(invoice_purchase.pk))
        invoice_purchase.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert invoice_purchase.state == InvoiceState.CANCELED
        assert response.data["state"] == "CANCELED"

    def test_cancel_already_canceled_returns_400(
        self, api_client_auth, invoice_cancel_url, invoice_sale
    ):
        invoice_sale.state = InvoiceState.CANCELED
        invoice_sale.save()
        response = api_client_auth.patch(invoice_cancel_url(invoice_sale.pk))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cancel_unauthenticated_returns_401(
        self, api_client, invoice_cancel_url, invoice_purchase
    ):
        response = api_client.patch(invoice_cancel_url(invoice_purchase.pk))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestFiltersInvoice:
    def test_invoices_filters_by_state(
        self, api_client_auth, invoices_url, invoice_sale, invoice_purchase
    ):
        response = api_client_auth.get(invoices_url, {"state": InvoiceState.ISSUED})
        assert len(response.data) == 2

    def test_invoices_filters_date_from_correctly(
        self, api_client_auth, invoices_url, invoice_sale
    ):
        today = timezone.now().date()
        response = api_client_auth.get(invoices_url, {"date_from": str(today)})
        assert len(response.data) >= 1

    def test_invoices_filters_date_from_future_returns_empty(
        self, api_client_auth, invoices_url, invoice_purchase
    ):
        future = (timezone.now() + timedelta(days=30)).date()
        response = api_client_auth.get(invoices_url, {"date_from": str(future)})
        assert response.data == []

    def test_invoices_filters_by_type_sale(
        self, api_client_auth, invoices_url, invoice_sale, invoice_purchase
    ):
        response = api_client_auth.get(invoices_url, {"invoice_type": "SALE"})
        assert len(response.data) == 1
        assert response.data[0]["invoice_type"] == "SALE"

    def test_invoices_filters_by_type_purchase(
        self, api_client_auth, invoices_url, invoice_sale, invoice_purchase
    ):
        response = api_client_auth.get(invoices_url, {"invoice_type": "PURCHASE"})
        assert len(response.data) == 1
        assert response.data[0]["invoice_type"] == "PURCHASE"

    def test_invoices_filters_by_pdf_generated(
        self, api_client_auth, invoices_url, invoice_sale
    ):
        response = api_client_auth.get(invoices_url, {"pdf_generated": "true"})
        assert response.status_code == status.HTTP_200_OK

    def test_invoices_filters_by_sale_id(
        self, api_client_auth, invoices_url, invoice_sale, invoice_purchase
    ):
        response = api_client_auth.get(invoices_url, {"sale_id": invoice_sale.sale.pk})
        assert len(response.data) == 1
        assert response.data[0]["invoice_type"] == "SALE"

    def test_invoices_filters_by_purchase_id(
        self, api_client_auth, invoices_url, invoice_sale, invoice_purchase
    ):
        response = api_client_auth.get(
            invoices_url, {"purchase_id": invoice_purchase.purchase.pk}
        )
        assert len(response.data) == 1
        assert response.data[0]["invoice_type"] == "PURCHASE"

    def test_invoices_filters_by_sale_id_not_found(self, api_client_auth, invoices_url):
        response = api_client_auth.get(invoices_url, {"sale_id": 99999})
        assert response.data == []
