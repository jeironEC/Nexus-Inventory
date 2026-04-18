# DRF
from rest_framework import serializers


class SaleReportSerializer(serializers.Serializer):
    total_sales = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_tax = serializers.DecimalField(max_digits=14, decimal_places=2)
    average_ticket = serializers.DecimalField(max_digits=14, decimal_places=2)
    canceled_sales = serializers.IntegerField()


class SaleReturnReportSerializer(serializers.Serializer):
    total_returns = serializers.IntegerField()
    completed_returns = serializers.IntegerField()
    canceled_returns = serializers.IntegerField()
    total_refund_amount = serializers.DecimalField(max_digits=14, decimal_places=2)


class PurchaseReturnReportSerializer(serializers.Serializer):
    total_returns = serializers.IntegerField()
    completed_returns = serializers.IntegerField()
    canceled_returns = serializers.IntegerField()
    total_refund_amount = serializers.DecimalField(max_digits=14, decimal_places=2)


class SaleByCustomerSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(allow_null=True)
    customer_name = serializers.CharField(allow_null=True)
    total_sales = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=14, decimal_places=2)


class SaleByPaymentMethodSerializer(serializers.Serializer):
    payment_method = serializers.CharField()
    total_sales = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=14, decimal_places=2)


class SaleByPeriodSerializer(serializers.Serializer):
    period = serializers.CharField()
    total_sales = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=14, decimal_places=2)


class PurchaseReportSerializer(serializers.Serializer):
    total_purchases = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=14, decimal_places=2)
    average_purchase = serializers.DecimalField(max_digits=14, decimal_places=2)
    canceled_purchases = serializers.IntegerField()


class PurchaseBySupplierSerializer(serializers.Serializer):
    supplier_id = serializers.IntegerField()
    supplier_name = serializers.CharField()
    total_purchases = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=14, decimal_places=2)


class PurchaseByPeriodSerializer(serializers.Serializer):
    period = serializers.CharField()
    total_purchases = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=14, decimal_places=2)


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


class InventoryMovementReportSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    movement_type = serializers.CharField()
    quantity = serializers.IntegerField()
    user = serializers.CharField()
    created_at = serializers.DateTimeField()


class ProductReportSerializer(serializers.Serializer):
    top_selling = serializers.ListField()
    most_purchased = serializers.ListField()
    by_category = serializers.ListField()


class ProductTopSellingSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    category = serializers.CharField()
    total_quantity = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=14, decimal_places=2)


class ProductLowSellingSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    category = serializers.CharField()
    total_quantity = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=14, decimal_places=2)


class ProductMostPurchasedSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    category = serializers.CharField()
    total_quantity = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=14, decimal_places=2)


class ProductByCategorySerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    category_name = serializers.CharField()
    total_products = serializers.IntegerField()
    total_quantity_sold = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=14, decimal_places=2)


class CustomerReportSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    customer_name = serializers.CharField()
    total_purchases = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=14, decimal_places=2)


class CustomerTopSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    customer_name = serializers.CharField()
    total_purchases = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=14, decimal_places=2)


class InvoiceReportSerializer(serializers.Serializer):
    total_invoices = serializers.IntegerField()
    issued_invoices = serializers.IntegerField()
    canceled_invoices = serializers.IntegerField()
    pdf_generated = serializers.IntegerField()
