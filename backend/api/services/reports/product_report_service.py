# Django
from django.db.models import Count, Sum

# Services
from api.services.util_service import get_raw_value


class ProductReportService:
    @staticmethod
    def get_totals_from_report(result, amount_field="total_amount"):
        if amount_field == "total_spent":
            return {
                "total_quantity": sum(item["total_quantity"] or 0 for item in result),
                "total_spent": sum(
                    get_raw_value(item.get("total_spent", 0)) for item in result
                ),
            }

        return {
            "total_quantity": sum(item["total_quantity"] or 0 for item in result),
            "total_revenue": sum(get_raw_value(item[amount_field]) for item in result),
        }

    @staticmethod
    def get_totals_by_category(result):
        return {
            "total_quantity": sum(item["total_quantity_sold"] or 0 for item in result),
            "total_revenue": sum(
                get_raw_value(item["total_revenue"]) for item in result
            ),
        }

    @staticmethod
    def build_report_products(sale_qs, purchase_qs, limit):
        return {
            "top_selling": ProductReportService.get_products_report(
                sale_qs,
                order_by="-total_quantity",
                limit=limit,
            ),
            "most_purchased": ProductReportService.get_products_report(
                purchase_qs,
                order_by="-total_quantity",
                limit=limit,
            ),
            "by_category": ProductReportService.get_products_by_category(sale_qs),
        }

    @staticmethod
    def get_products_report(qs, order_by, limit=None):
        data = (
            qs.values(
                "product__id",
                "product__name",
                "product__category__name",
            )
            .annotate(
                total_quantity=Sum("quantity"),
                total_amount=Sum("subtotal"),
            )
            .order_by(order_by)
        )

        if limit:
            data = data[:limit]

        return [
            {
                "product_id": r["product__id"],
                "product_name": r["product__name"],
                "category": r["product__category__name"],
                "total_quantity": r["total_quantity"],
                "total_amount": r["total_amount"],
                "total_quantity_sold": r["total_quantity"],
                "total_revenue": r["total_amount"],
                "total_quantity_purchased": r["total_quantity"],
                "total_spent": r["total_amount"],
            }
            for r in data
        ]

    @staticmethod
    def get_products_by_category(qs):
        data = (
            qs.values(
                "product__category__id",
                "product__category__name",
            )
            .annotate(
                total_products=Count("product__id", distinct=True),
                total_quantity_sold=Sum("quantity"),
                total_revenue=Sum("subtotal"),
            )
            .order_by("-total_revenue")
        )

        return [
            {
                "category_id": r["product__category__id"],
                "category_name": r["product__category__name"],
                "total_products": r["total_products"],
                "total_quantity_sold": r["total_quantity_sold"],
                "total_revenue": r["total_revenue"],
            }
            for r in data
        ]

    @staticmethod
    def get_products_by_supplier(qs):
        data = (
            qs.values(
                "purchase__supplier__id",
                "purchase__supplier__name",
            )
            .annotate(
                total_products=Count("product__id", distinct=True),
                total_quantity_purchased=Sum("quantity"),
                total_spent=Sum("subtotal"),
            )
            .order_by("-total_spent")
        )
        return [
            {
                "supplier_id": r["purchase__supplier__id"],
                "supplier_name": r["purchase__supplier__name"],
                "total_products": r["total_products"],
                "total_quantity_purchased": r["total_quantity_purchased"],
                "total_spent": r["total_spent"],
            }
            for r in data
        ]
