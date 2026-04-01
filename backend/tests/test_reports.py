# Internal
import pytest

# DRF
from rest_framework import status


@pytest.mark.django_db
class TestSaleReportViewSet:
    def test_sales_report_returns_200(self, api_client_auth, url_reports_sales):
        response = api_client_auth.get(url_reports_sales)
        assert response.status_code == status.HTTP_200_OK

    def test_sales_report_fields_present(
        self, api_client_auth, sale, url_reports_sales
    ):
        response = api_client_auth.get(url_reports_sales)
        assert set(response.data.keys()) == {
            "total_sales",
            "total_revenue",
            "total_tax",
            "average_ticket",
            "canceled_sales",
        }

    def test_sales_report_counts_completed_sales(
        self, api_client_auth, sale, another_sale, url_reports_sales
    ):
        response = api_client_auth.get(url_reports_sales)
        assert response.data["total_sales"] == 2

    def test_sales_report_unauthenticated_returns_401(
        self, api_client, url_reports_sales
    ):
        response = api_client.get(url_reports_sales)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_sales_by_customer_returns_200(
        self, api_client_auth, url_reports_sales_by_customer
    ):
        response = api_client_auth.get(url_reports_sales_by_customer)
        assert response.status_code == status.HTTP_200_OK

    def test_sales_by_customer_returns_list(
        self, api_client_auth, sale, url_reports_sales_by_customer
    ):
        response = api_client_auth.get(url_reports_sales_by_customer)
        assert isinstance(response.data, list)

    def test_sales_by_customer_fields_present(
        self, api_client_auth, sale, url_reports_sales_by_customer
    ):
        response = api_client_auth.get(url_reports_sales_by_customer)
        if response.data:
            assert set(response.data[0].keys()) == {
                "customer_id",
                "customer_name",
                "total_sales",
                "total_revenue",
            }

    def test_sales_by_payment_method_returns_200(
        self, api_client_auth, url_reports_sales_by_payment_method
    ):
        response = api_client_auth.get(url_reports_sales_by_payment_method)
        assert response.status_code == status.HTTP_200_OK

    def test_sales_by_payment_method_returns_list(
        self, api_client_auth, sale, url_reports_sales_by_payment_method
    ):
        response = api_client_auth.get(url_reports_sales_by_payment_method)
        assert isinstance(response.data, list)

    def test_sales_by_payment_method_fields_present(
        self, api_client_auth, sale, url_reports_sales_by_payment_method
    ):
        response = api_client_auth.get(url_reports_sales_by_payment_method)
        if response.data:
            assert set(response.data[0].keys()) == {
                "payment_method",
                "total_sales",
                "total_revenue",
            }

    def test_sales_by_period_returns_200(
        self, api_client_auth, url_reports_sales_by_period
    ):
        response = api_client_auth.get(url_reports_sales_by_period)
        assert response.status_code == status.HTTP_200_OK

    def test_sales_by_period_returns_list(
        self, api_client_auth, sale, url_reports_sales_by_period
    ):
        response = api_client_auth.get(url_reports_sales_by_period)
        assert isinstance(response.data, list)

    def test_sales_by_period_fields_present(
        self, api_client_auth, sale, url_reports_sales_by_period
    ):
        response = api_client_auth.get(url_reports_sales_by_period)
        if response.data:
            assert set(response.data[0].keys()) == {
                "period",
                "total_sales",
                "total_revenue",
            }

    def test_sales_by_period_unauthenticated_returns_401(
        self, api_client, url_reports_sales_by_period
    ):
        response = api_client.get(url_reports_sales_by_period)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPurchaseReportViewSet:
    def test_purchases_report_returns_200(self, api_client_auth, url_reports_purchases):
        response = api_client_auth.get(url_reports_purchases)
        assert response.status_code == status.HTTP_200_OK

    def test_purchases_report_fields_present(
        self, api_client_auth, purchase, url_reports_purchases
    ):
        response = api_client_auth.get(url_reports_purchases)
        assert set(response.data.keys()) == {
            "total_purchases",
            "total_spent",
            "average_purchase",
            "canceled_purchases",
        }

    def test_purchases_report_counts_completed_purchases(
        self, api_client_auth, purchase, another_purchase, url_reports_purchases
    ):
        response = api_client_auth.get(url_reports_purchases)
        assert response.data["total_purchases"] == 2

    def test_purchases_report_unauthenticated_returns_401(
        self, api_client, url_reports_purchases
    ):
        response = api_client.get(url_reports_purchases)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_purchases_by_supplier_returns_200(
        self, api_client_auth, url_reports_purchases_by_supplier
    ):
        response = api_client_auth.get(url_reports_purchases_by_supplier)
        assert response.status_code == status.HTTP_200_OK

    def test_purchases_by_supplier_returns_list(
        self, api_client_auth, purchase, url_reports_purchases_by_supplier
    ):
        response = api_client_auth.get(url_reports_purchases_by_supplier)
        assert isinstance(response.data, list)

    def test_purchases_by_supplier_fields_present(
        self, api_client_auth, purchase, url_reports_purchases_by_supplier
    ):
        response = api_client_auth.get(url_reports_purchases_by_supplier)
        if response.data:
            assert set(response.data[0].keys()) == {
                "supplier_id",
                "supplier_name",
                "total_purchases",
                "total_spent",
            }

    def test_purchases_by_period_returns_200(
        self, api_client_auth, url_reports_purchases_by_period
    ):
        response = api_client_auth.get(url_reports_purchases_by_period)
        assert response.status_code == status.HTTP_200_OK

    def test_purchases_by_period_returns_list(
        self, api_client_auth, purchase, url_reports_purchases_by_period
    ):
        response = api_client_auth.get(url_reports_purchases_by_period)
        assert isinstance(response.data, list)

    def test_purchases_by_period_fields_present(
        self, api_client_auth, purchase, url_reports_purchases_by_period
    ):
        response = api_client_auth.get(url_reports_purchases_by_period)
        if response.data:
            assert set(response.data[0].keys()) == {
                "period",
                "total_purchases",
                "total_spent",
            }


@pytest.mark.django_db
class TestInventoryReportViewSet:
    def test_inventory_report_returns_200(self, api_client_auth, url_reports_inventory):
        response = api_client_auth.get(url_reports_inventory)
        assert response.status_code == status.HTTP_200_OK

    def test_inventory_report_returns_list(
        self, api_client_auth, inventory, url_reports_inventory
    ):
        response = api_client_auth.get(url_reports_inventory)
        assert isinstance(response.data, list)

    def test_inventory_report_fields_present(
        self, api_client_auth, inventory, url_reports_inventory
    ):
        response = api_client_auth.get(url_reports_inventory)
        if response.data:
            assert set(response.data[0].keys()) == {
                "product_id",
                "product_name",
                "category",
                "quantity",
                "sale_price",
                "stock_value",
            }

    def test_inventory_report_unauthenticated_returns_401(
        self, api_client, url_reports_inventory
    ):
        response = api_client.get(url_reports_inventory)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_inventory_low_stock_returns_200(
        self, api_client_auth, url_reports_inventory_low_stock
    ):
        response = api_client_auth.get(url_reports_inventory_low_stock)
        assert response.status_code == status.HTTP_200_OK

    def test_inventory_low_stock_returns_list(
        self, api_client_auth, inventory, url_reports_inventory_low_stock
    ):
        response = api_client_auth.get(url_reports_inventory_low_stock)
        assert isinstance(response.data, list)

    def test_inventory_low_stock_fields_present(
        self, api_client_auth, inventory, url_reports_inventory_low_stock
    ):
        response = api_client_auth.get(url_reports_inventory_low_stock)
        if response.data:
            assert set(response.data[0].keys()) == {
                "product_id",
                "product_name",
                "category",
                "quantity",
                "threshold",
            }

    def test_inventory_movements_report_returns_200(
        self, api_client_auth, url_reports_inventory_movements
    ):
        response = api_client_auth.get(url_reports_inventory_movements)
        assert response.status_code == status.HTTP_200_OK

    def test_inventory_movements_report_returns_list(
        self, api_client_auth, inventory_movements, url_reports_inventory_movements
    ):
        response = api_client_auth.get(url_reports_inventory_movements)
        assert isinstance(response.data, list)

    def test_inventory_movements_report_fields_present(
        self, api_client_auth, inventory_movements, url_reports_inventory_movements
    ):
        response = api_client_auth.get(url_reports_inventory_movements)
        if response.data:
            assert set(response.data[0].keys()) == {
                "product_id",
                "product_name",
                "movement_type",
                "quantity",
                "user",
                "created_at",
            }


@pytest.mark.django_db
class TestProductReportViewSet:
    def test_top_selling_returns_200(
        self, api_client_auth, url_reports_products_top_selling
    ):
        response = api_client_auth.get(url_reports_products_top_selling)
        assert response.status_code == status.HTTP_200_OK

    def test_top_selling_returns_list(
        self, api_client_auth, url_reports_products_top_selling
    ):
        response = api_client_auth.get(url_reports_products_top_selling)
        assert isinstance(response.data, list)

    def test_top_selling_unauthenticated_returns_401(
        self, api_client, url_reports_products_top_selling
    ):
        response = api_client.get(url_reports_products_top_selling)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_low_selling_returns_200(
        self, api_client_auth, url_reports_products_low_selling
    ):
        response = api_client_auth.get(url_reports_products_low_selling)
        assert response.status_code == status.HTTP_200_OK

    def test_low_selling_returns_list(
        self, api_client_auth, url_reports_products_low_selling
    ):
        response = api_client_auth.get(url_reports_products_low_selling)
        assert isinstance(response.data, list)

    def test_most_purchased_returns_200(
        self, api_client_auth, url_reports_products_most_purchased
    ):
        response = api_client_auth.get(url_reports_products_most_purchased)
        assert response.status_code == status.HTTP_200_OK

    def test_most_purchased_returns_list(
        self, api_client_auth, url_reports_products_most_purchased
    ):
        response = api_client_auth.get(url_reports_products_most_purchased)
        assert isinstance(response.data, list)

    def test_by_category_returns_200(
        self, api_client_auth, url_reports_products_by_category
    ):
        response = api_client_auth.get(url_reports_products_by_category)
        assert response.status_code == status.HTTP_200_OK

    def test_by_category_returns_list(
        self, api_client_auth, url_reports_products_by_category
    ):
        response = api_client_auth.get(url_reports_products_by_category)
        assert isinstance(response.data, list)


@pytest.mark.django_db
class TestCustomerReportViewSet:
    def test_top_customers_returns_200(
        self, api_client_auth, url_reports_customers_top
    ):
        response = api_client_auth.get(url_reports_customers_top)
        assert response.status_code == status.HTTP_200_OK

    def test_top_customers_returns_list(
        self, api_client_auth, sale, url_reports_customers_top
    ):
        response = api_client_auth.get(url_reports_customers_top)
        assert isinstance(response.data, list)

    def test_top_customers_fields_present(
        self, api_client_auth, sale, url_reports_customers_top
    ):
        response = api_client_auth.get(url_reports_customers_top)
        if response.data:
            assert set(response.data[0].keys()) == {
                "customer_id",
                "customer_name",
                "total_purchases",
                "total_spent",
            }

    def test_top_customers_unauthenticated_returns_401(
        self, api_client, url_reports_customers_top
    ):
        response = api_client.get(url_reports_customers_top)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_customer_promotions_report_returns_200(
        self, api_client_auth, url_reports_customers_promotions
    ):
        response = api_client_auth.get(url_reports_customers_promotions)
        assert response.status_code == status.HTTP_200_OK

    def test_customer_promotions_report_returns_list(
        self, api_client_auth, customer_promotion, url_reports_customers_promotions
    ):
        response = api_client_auth.get(url_reports_customers_promotions)
        assert isinstance(response.data, list)

    def test_customer_promotions_report_fields_present(
        self, api_client_auth, customer_promotion, url_reports_customers_promotions
    ):
        response = api_client_auth.get(url_reports_customers_promotions)
        if response.data:
            assert set(response.data[0].keys()) == {
                "customer_id",
                "customer_name",
                "total_promotions",
                "applied_promotions",
            }


@pytest.mark.django_db
class TestInvoiceReportViewSet:
    def test_invoices_report_returns_200(self, api_client_auth, url_reports_invoices):
        response = api_client_auth.get(url_reports_invoices)
        assert response.status_code == status.HTTP_200_OK

    def test_invoices_report_fields_present(
        self, api_client_auth, invoice_sale, url_reports_invoices
    ):
        response = api_client_auth.get(url_reports_invoices)
        assert set(response.data.keys()) == {
            "total_invoices",
            "issued_invoices",
            "canceled_invoices",
            "pdf_generated",
        }

    def test_invoices_report_counts_invoices(
        self, api_client_auth, invoice_purchase, url_reports_invoices
    ):
        response = api_client_auth.get(url_reports_invoices)
        assert response.data["total_invoices"] == 1
        assert response.data["issued_invoices"] == 1
        assert response.data["canceled_invoices"] == 0

    def test_invoices_report_unauthenticated_returns_401(
        self, api_client, url_reports_invoices
    ):
        response = api_client.get(url_reports_invoices)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestInvoiceReportViewSetSalesAndPurchases:
    def test_invoices_sales_report_returns_200(
        self, api_client_auth, url_reports_invoices_sales
    ):
        response = api_client_auth.get(url_reports_invoices_sales)
        assert response.status_code == status.HTTP_200_OK

    def test_invoices_sales_report_returns_only_sale_invoices(
        self,
        api_client_auth,
        invoice_sale,
        invoice_purchase,
        url_reports_invoices_sales,
    ):
        response = api_client_auth.get(url_reports_invoices_sales)
        assert response.data["total_invoices"] == 1

    def test_invoices_purchases_report_returns_200(
        self, api_client_auth, url_reports_invoices_purchases
    ):
        response = api_client_auth.get(url_reports_invoices_purchases)
        assert response.status_code == status.HTTP_200_OK

    def test_invoices_purchases_report_returns_only_purchase_invoices(
        self,
        api_client_auth,
        invoice_sale,
        invoice_purchase,
        url_reports_invoices_purchases,
    ):
        response = api_client_auth.get(url_reports_invoices_purchases)
        assert response.data["total_invoices"] == 1

    def test_invoices_sales_unauthenticated_returns_401(
        self, api_client, url_reports_invoices_sales
    ):
        response = api_client.get(url_reports_invoices_sales)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invoices_purchases_unauthenticated_returns_401(
        self, api_client, url_reports_invoices_purchases
    ):
        response = api_client.get(url_reports_invoices_purchases)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestSaleReturnReportViewSet:
    def test_sale_returns_report_returns_200(
        self, api_client_auth, url_reports_sale_returns
    ):
        response = api_client_auth.get(url_reports_sale_returns)
        assert response.status_code == status.HTTP_200_OK

    def test_sale_returns_report_fields_present(
        self, api_client_auth, url_reports_sale_returns
    ):
        response = api_client_auth.get(url_reports_sale_returns)
        assert set(response.data.keys()) == {
            "total_returns",
            "completed_returns",
            "canceled_returns",
            "total_refund_amount",
        }

    def test_sale_returns_report_unauthenticated_returns_401(
        self, api_client, url_reports_sale_returns
    ):
        response = api_client.get(url_reports_sale_returns)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPurchaseReturnReportViewSet:
    def test_purchase_returns_report_returns_200(
        self, api_client_auth, url_reports_purchase_returns
    ):
        response = api_client_auth.get(url_reports_purchase_returns)
        assert response.status_code == status.HTTP_200_OK

    def test_purchase_returns_report_fields_present(
        self, api_client_auth, url_reports_purchase_returns
    ):
        response = api_client_auth.get(url_reports_purchase_returns)
        assert set(response.data.keys()) == {
            "total_returns",
            "completed_returns",
            "canceled_returns",
            "total_refund_amount",
        }

    def test_purchase_returns_report_unauthenticated_returns_401(
        self, api_client, url_reports_purchase_returns
    ):
        response = api_client.get(url_reports_purchase_returns)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
