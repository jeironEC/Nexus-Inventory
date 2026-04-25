# Django
from django.db.models import Count, Sum, Q

# Services
from api.services.util_service import get_raw_value


class CustomerReportService:

    @staticmethod
    def get_totals_from_summary(result):
        return {
            "total_customers": len(result),
            "total_purchases": sum(item["total_purchases"] or 0 for item in result),
            "total_spent": sum(get_raw_value(item["total_spent"]) for item in result),
        }

    @staticmethod
    def get_totals_from_promotions(result):
        return {
            "total_customers": len(result),
            "total_promotions": sum(item["total_promotions"] or 0 for item in result),
            "total_applied": sum(item["applied_promotions"] or 0 for item in result),
        }

    @staticmethod
    def get_summary(qs, limit):
        data = (
            qs.values("id", "first_name", "last_name")
            .annotate(
                total_purchases=Count("sales__id", distinct=True),
                total_spent=Sum("sales__total_amount"),
            )
            .order_by("-total_spent")[:limit]
        )

        return [
            {
                "customer_id": r["id"],
                "customer_name": f"{r['first_name']} {r['last_name']}",
                "total_purchases": r["total_purchases"],
                "total_spent": r["total_spent"],
            }
            for r in data
        ]

    @staticmethod
    def get_customer_promotions(qs):
        data = (
            qs.values("customer__id", "customer__first_name", "customer__last_name")
            .annotate(
                total_promotions=Count("id"),
                applied_promotions=Count("id", filter=Q(applied=True)),
            )
            .order_by("-total_promotions")
        )

        return [
            {
                "customer_id": r["customer__id"],
                "customer_name": f"{r['customer__first_name']} {r['customer__last_name']}",
                "total_promotions": r["total_promotions"],
                "applied_promotions": r["applied_promotions"],
            }
            for r in data
        ]
