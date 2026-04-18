# Internal
import pytest

# DRF
from rest_framework import status


@pytest.mark.django_db
class TestSalesPDF:
    def test_returns_200(self, api_client_auth, url_reports_sales_pdf):
        response = api_client_auth.get(url_reports_sales_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(self, api_client_auth, url_reports_sales_pdf):
        response = api_client_auth.get(url_reports_sales_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(self, api_client, url_reports_sales_pdf):
        response = api_client.get(url_reports_sales_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(self, api_client_auth, url_reports_sales_pdf):
        response = api_client_auth.get(url_reports_sales_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestSalesByCustomerPDF:
    def test_returns_200(self, api_client_auth, url_reports_sales_by_customer_pdf):
        response = api_client_auth.get(url_reports_sales_by_customer_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(self, api_client_auth, url_reports_sales_by_customer_pdf):
        response = api_client_auth.get(url_reports_sales_by_customer_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(
        self, api_client, url_reports_sales_by_customer_pdf
    ):
        response = api_client.get(url_reports_sales_by_customer_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(self, api_client_auth, url_reports_sales_by_customer_pdf):
        response = api_client_auth.get(url_reports_sales_by_customer_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestSalesByPaymentMethodPDF:
    def test_returns_200(
        self, api_client_auth, url_reports_sales_by_payment_method_pdf
    ):
        response = api_client_auth.get(url_reports_sales_by_payment_method_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(
        self, api_client_auth, url_reports_sales_by_payment_method_pdf
    ):
        response = api_client_auth.get(url_reports_sales_by_payment_method_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(
        self, api_client, url_reports_sales_by_payment_method_pdf
    ):
        response = api_client.get(url_reports_sales_by_payment_method_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(
        self, api_client_auth, url_reports_sales_by_payment_method_pdf
    ):
        response = api_client_auth.get(url_reports_sales_by_payment_method_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestSalesByPeriodPDF:
    def test_returns_200(self, api_client_auth, url_reports_sales_by_period_pdf):
        response = api_client_auth.get(url_reports_sales_by_period_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(self, api_client_auth, url_reports_sales_by_period_pdf):
        response = api_client_auth.get(url_reports_sales_by_period_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(
        self, api_client, url_reports_sales_by_period_pdf
    ):
        response = api_client.get(url_reports_sales_by_period_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(self, api_client_auth, url_reports_sales_by_period_pdf):
        response = api_client_auth.get(url_reports_sales_by_period_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestPurchasesPDF:
    def test_returns_200(self, api_client_auth, url_reports_purchases_pdf):
        response = api_client_auth.get(url_reports_purchases_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(self, api_client_auth, url_reports_purchases_pdf):
        response = api_client_auth.get(url_reports_purchases_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(self, api_client, url_reports_purchases_pdf):
        response = api_client.get(url_reports_purchases_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(self, api_client_auth, url_reports_purchases_pdf):
        response = api_client_auth.get(url_reports_purchases_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestPurchasesBySupplierPDF:
    def test_returns_200(self, api_client_auth, url_reports_purchases_by_supplier_pdf):
        response = api_client_auth.get(url_reports_purchases_by_supplier_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(
        self, api_client_auth, url_reports_purchases_by_supplier_pdf
    ):
        response = api_client_auth.get(url_reports_purchases_by_supplier_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(
        self, api_client, url_reports_purchases_by_supplier_pdf
    ):
        response = api_client.get(url_reports_purchases_by_supplier_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(
        self, api_client_auth, url_reports_purchases_by_supplier_pdf
    ):
        response = api_client_auth.get(url_reports_purchases_by_supplier_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestPurchasesByPeriodPDF:
    def test_returns_200(self, api_client_auth, url_reports_purchases_by_period_pdf):
        response = api_client_auth.get(url_reports_purchases_by_period_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(
        self, api_client_auth, url_reports_purchases_by_period_pdf
    ):
        response = api_client_auth.get(url_reports_purchases_by_period_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(
        self, api_client, url_reports_purchases_by_period_pdf
    ):
        response = api_client.get(url_reports_purchases_by_period_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(
        self, api_client_auth, url_reports_purchases_by_period_pdf
    ):
        response = api_client_auth.get(url_reports_purchases_by_period_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestInventoryPDF:
    def test_returns_200(self, api_client_auth, url_reports_inventory_pdf):
        response = api_client_auth.get(url_reports_inventory_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(self, api_client_auth, url_reports_inventory_pdf):
        response = api_client_auth.get(url_reports_inventory_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(self, api_client, url_reports_inventory_pdf):
        response = api_client.get(url_reports_inventory_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(self, api_client_auth, url_reports_inventory_pdf):
        response = api_client_auth.get(url_reports_inventory_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestInventoryLowStockPDF:
    def test_returns_200(self, api_client_auth, url_reports_inventory_low_stock_pdf):
        response = api_client_auth.get(url_reports_inventory_low_stock_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(
        self, api_client_auth, url_reports_inventory_low_stock_pdf
    ):
        response = api_client_auth.get(url_reports_inventory_low_stock_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(
        self, api_client, url_reports_inventory_low_stock_pdf
    ):
        response = api_client.get(url_reports_inventory_low_stock_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(
        self, api_client_auth, url_reports_inventory_low_stock_pdf
    ):
        response = api_client_auth.get(url_reports_inventory_low_stock_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestInventoryMovementsPDF:
    def test_returns_200(self, api_client_auth, url_reports_inventory_movements_pdf):
        response = api_client_auth.get(url_reports_inventory_movements_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(
        self, api_client_auth, url_reports_inventory_movements_pdf
    ):
        response = api_client_auth.get(url_reports_inventory_movements_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(
        self, api_client, url_reports_inventory_movements_pdf
    ):
        response = api_client.get(url_reports_inventory_movements_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(
        self, api_client_auth, url_reports_inventory_movements_pdf
    ):
        response = api_client_auth.get(url_reports_inventory_movements_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestProductsPDF:
    def test_returns_200(self, api_client_auth, url_reports_products_pdf):
        response = api_client_auth.get(url_reports_products_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(self, api_client_auth, url_reports_products_pdf):
        response = api_client_auth.get(url_reports_products_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(self, api_client, url_reports_products_pdf):
        response = api_client.get(url_reports_products_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(self, api_client_auth, url_reports_products_pdf):
        response = api_client_auth.get(url_reports_products_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestProductsTopSellingPDF:
    def test_returns_200(self, api_client_auth, url_reports_products_top_selling_pdf):
        response = api_client_auth.get(url_reports_products_top_selling_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(
        self, api_client_auth, url_reports_products_top_selling_pdf
    ):
        response = api_client_auth.get(url_reports_products_top_selling_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(
        self, api_client, url_reports_products_top_selling_pdf
    ):
        response = api_client.get(url_reports_products_top_selling_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(
        self, api_client_auth, url_reports_products_top_selling_pdf
    ):
        response = api_client_auth.get(url_reports_products_top_selling_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestProductsLowSellingPDF:
    def test_returns_200(self, api_client_auth, url_reports_products_low_selling_pdf):
        response = api_client_auth.get(url_reports_products_low_selling_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(
        self, api_client_auth, url_reports_products_low_selling_pdf
    ):
        response = api_client_auth.get(url_reports_products_low_selling_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(
        self, api_client, url_reports_products_low_selling_pdf
    ):
        response = api_client.get(url_reports_products_low_selling_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(
        self, api_client_auth, url_reports_products_low_selling_pdf
    ):
        response = api_client_auth.get(url_reports_products_low_selling_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestProductsMostPurchasedPDF:
    def test_returns_200(
        self, api_client_auth, url_reports_products_most_purchased_pdf
    ):
        response = api_client_auth.get(url_reports_products_most_purchased_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(
        self, api_client_auth, url_reports_products_most_purchased_pdf
    ):
        response = api_client_auth.get(url_reports_products_most_purchased_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(
        self, api_client, url_reports_products_most_purchased_pdf
    ):
        response = api_client.get(url_reports_products_most_purchased_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(
        self, api_client_auth, url_reports_products_most_purchased_pdf
    ):
        response = api_client_auth.get(url_reports_products_most_purchased_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestProductsByCategoryPDF:
    def test_returns_200(self, api_client_auth, url_reports_products_by_category_pdf):
        response = api_client_auth.get(url_reports_products_by_category_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(
        self, api_client_auth, url_reports_products_by_category_pdf
    ):
        response = api_client_auth.get(url_reports_products_by_category_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(
        self, api_client, url_reports_products_by_category_pdf
    ):
        response = api_client.get(url_reports_products_by_category_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(
        self, api_client_auth, url_reports_products_by_category_pdf
    ):
        response = api_client_auth.get(url_reports_products_by_category_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestCustomersPDF:
    def test_returns_200(self, api_client_auth, url_reports_customers_pdf):
        response = api_client_auth.get(url_reports_customers_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(self, api_client_auth, url_reports_customers_pdf):
        response = api_client_auth.get(url_reports_customers_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(self, api_client, url_reports_customers_pdf):
        response = api_client.get(url_reports_customers_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(self, api_client_auth, url_reports_customers_pdf):
        response = api_client_auth.get(url_reports_customers_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestCustomersTopPDF:
    def test_returns_200(self, api_client_auth, url_reports_customers_top_pdf):
        response = api_client_auth.get(url_reports_customers_top_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(self, api_client_auth, url_reports_customers_top_pdf):
        response = api_client_auth.get(url_reports_customers_top_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(self, api_client, url_reports_customers_top_pdf):
        response = api_client.get(url_reports_customers_top_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(self, api_client_auth, url_reports_customers_top_pdf):
        response = api_client_auth.get(url_reports_customers_top_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestInvoicesPDF:
    def test_returns_200(self, api_client_auth, url_reports_invoices_pdf):
        response = api_client_auth.get(url_reports_invoices_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(self, api_client_auth, url_reports_invoices_pdf):
        response = api_client_auth.get(url_reports_invoices_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(self, api_client, url_reports_invoices_pdf):
        response = api_client.get(url_reports_invoices_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(self, api_client_auth, url_reports_invoices_pdf):
        response = api_client_auth.get(url_reports_invoices_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestInvoicesSalesPDF:
    def test_returns_200(self, api_client_auth, url_reports_invoices_sales_pdf):
        response = api_client_auth.get(url_reports_invoices_sales_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(self, api_client_auth, url_reports_invoices_sales_pdf):
        response = api_client_auth.get(url_reports_invoices_sales_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(self, api_client, url_reports_invoices_sales_pdf):
        response = api_client.get(url_reports_invoices_sales_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(self, api_client_auth, url_reports_invoices_sales_pdf):
        response = api_client_auth.get(url_reports_invoices_sales_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestInvoicesPurchasesPDF:
    def test_returns_200(self, api_client_auth, url_reports_invoices_purchases_pdf):
        response = api_client_auth.get(url_reports_invoices_purchases_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(
        self, api_client_auth, url_reports_invoices_purchases_pdf
    ):
        response = api_client_auth.get(url_reports_invoices_purchases_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(
        self, api_client, url_reports_invoices_purchases_pdf
    ):
        response = api_client.get(url_reports_invoices_purchases_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(self, api_client_auth, url_reports_invoices_purchases_pdf):
        response = api_client_auth.get(url_reports_invoices_purchases_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestSaleReturnsPDF:
    def test_returns_200(self, api_client_auth, url_reports_sale_returns_pdf):
        response = api_client_auth.get(url_reports_sale_returns_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(self, api_client_auth, url_reports_sale_returns_pdf):
        response = api_client_auth.get(url_reports_sale_returns_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(self, api_client, url_reports_sale_returns_pdf):
        response = api_client.get(url_reports_sale_returns_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(self, api_client_auth, url_reports_sale_returns_pdf):
        response = api_client_auth.get(url_reports_sale_returns_pdf)
        assert len(response.content) > 0


@pytest.mark.django_db
class TestPurchaseReturnsPDF:
    def test_returns_200(self, api_client_auth, url_reports_purchase_returns_pdf):
        response = api_client_auth.get(url_reports_purchase_returns_pdf)
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_pdf(self, api_client_auth, url_reports_purchase_returns_pdf):
        response = api_client_auth.get(url_reports_purchase_returns_pdf)
        assert response["Content-Type"] == "application/pdf"

    def test_unauthorized_returns_401(
        self, api_client, url_reports_purchase_returns_pdf
    ):
        response = api_client.get(url_reports_purchase_returns_pdf)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pdf_has_content(self, api_client_auth, url_reports_purchase_returns_pdf):
        response = api_client_auth.get(url_reports_purchase_returns_pdf)
        assert len(response.content) > 0
