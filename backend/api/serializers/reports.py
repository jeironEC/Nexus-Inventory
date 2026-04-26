# DRF
from rest_framework import serializers

# --- SALES ---


class SaleReportSerializer(serializers.Serializer):
    total_sales = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_tax = serializers.DecimalField(max_digits=14, decimal_places=2)
    average_ticket = serializers.DecimalField(max_digits=14, decimal_places=2)
    canceled_sales = serializers.IntegerField()


class SaleByCustomerSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(allow_null=True)
    customer_name = serializers.CharField(allow_null=True)
    total_sales = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=14, decimal_places=2)


class SaleByPaymentMethodSerializer(serializers.Serializer):
    payment_method = serializers.CharField()
    payment_method_display = serializers.CharField(required=False)
    total_sales = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=14, decimal_places=2)


class SaleByPeriodSerializer(serializers.Serializer):
    period = serializers.CharField()
    total_sales = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=14, decimal_places=2)


# --- PURCHASES ---


class PurchaseReportSerializer(serializers.Serializer):
    total_purchases = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_tax = serializers.DecimalField(max_digits=14, decimal_places=2, default=0)
    canceled_purchases = serializers.IntegerField()


class PurchaseBySupplierSerializer(serializers.Serializer):
    supplier_id = serializers.IntegerField(allow_null=True)
    supplier_name = serializers.CharField(allow_null=True)
    total_purchases = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=14, decimal_places=2)


class PurchaseByPeriodSerializer(serializers.Serializer):
    period = serializers.CharField()
    total_purchases = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=14, decimal_places=2)


# --- INVENTORY ---


class InventoryReportSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    category = serializers.CharField()
    quantity = serializers.IntegerField()
    sale_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock_value = serializers.DecimalField(max_digits=14, decimal_places=2)


class InventoryLowStockSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    category = serializers.CharField()
    quantity = serializers.IntegerField()
    threshold = serializers.IntegerField()
    sale_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock_value = serializers.DecimalField(max_digits=14, decimal_places=2)


class InventoryMovementReportSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    movement_type = serializers.CharField()
    quantity = serializers.IntegerField()
    user = serializers.CharField()
    created_at = serializers.DateTimeField()


# --- PRODUCTS ---


class ProductByCategorySerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    category_name = serializers.CharField()
    total_products = serializers.IntegerField()
    total_quantity_sold = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=14, decimal_places=2)


class ProductPerformanceSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    category = serializers.CharField()
    total_quantity_sold = serializers.IntegerField(required=False)
    total_revenue = serializers.DecimalField(
        max_digits=14, decimal_places=2, required=False
    )
    total_quantity_purchased = serializers.IntegerField(required=False)
    total_spent = serializers.DecimalField(
        max_digits=14, decimal_places=2, required=False
    )


# --- CUSTOMERS ---


class CustomerReportSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    customer_name = serializers.CharField()
    total_purchases = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=14, decimal_places=2)


# --- INVOICES ---


class InvoiceSummarySerializer(serializers.Serializer):
    total_invoices = serializers.IntegerField()
    issued_invoices = serializers.IntegerField()
    canceled_invoices = serializers.IntegerField()
    pdf_generated = serializers.IntegerField()


# --- RETURNS ---


class ReturnReportSummarySerializer(serializers.Serializer):
    total_returns = serializers.IntegerField()
    completed_returns = serializers.IntegerField()
    canceled_returns = serializers.IntegerField()
    total_refund_amount = serializers.DecimalField(max_digits=14, decimal_places=2)


class ReturnDetailReportSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    customer_name = serializers.CharField(required=False)
    supplier_name = serializers.CharField(required=False)
    reason = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    state = serializers.CharField()
