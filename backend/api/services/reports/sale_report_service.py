# Django
from django.db.models import Count, Sum, Avg, Q
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear

# Enums
from nexus_inventory_backend.db.enums import OperationState

# Services
from api.services.util_service import get_raw_value


class SaleReportService:

    @staticmethod
    def get_totals_from_list(result):
        return {
            "total_sales": sum(item["total_sales"] or 0 for item in result),
            "total_revenue": sum(
                get_raw_value(item["total_revenue"]) for item in result
            ),
        }

    @staticmethod
    def get_summary(qs):
        return qs.aggregate(
            total_sales=Count("id", filter=Q(state=OperationState.COMPLETED)),
            total_revenue=Sum("total_amount", filter=Q(state=OperationState.COMPLETED)),
            total_tax=Sum("tax_amount", filter=Q(state=OperationState.COMPLETED)),
            average_ticket=Avg(
                "total_amount", filter=Q(state=OperationState.COMPLETED)
            ),
            canceled_sales=Count("id", filter=Q(state=OperationState.CANCELED)),
        )

    @staticmethod
    def build_sales_pdf(qs):
        sales = list(
            qs.values(
                "id",
                "created_at",
                "customer__first_name",
                "customer__last_name",
                "payment_method",
                "subtotal",
                "tax_amount",
                "total_amount",
                "state",
            )
        )

        summary = SaleReportService.get_summary(qs)

        return {
            "sales": sales,
            "summary": {
                "total_sales": summary.get("total_sales") or 0,
                "total_revenue": summary.get("total_revenue"),
                "total_tax": summary.get("total_tax"),
                "average_ticket": summary.get("average_ticket"),
            },
        }

    @staticmethod
    def get_by_customer(qs):
        data = (
            qs.values("customer__id", "customer__first_name", "customer__last_name")
            .annotate(
                total_sales=Count("id"),
                total_revenue=Sum("total_amount"),
            )
            .order_by("-total_revenue")
        )

        return [
            {
                "customer_id": r["customer__id"],
                "customer_name": f"{r['customer__first_name'] or ''} {r['customer__last_name'] or ''}".strip()
                or "Anonymous",
                "total_sales": r["total_sales"],
                "total_revenue": r["total_revenue"],
            }
            for r in data
        ]

    @staticmethod
    def get_by_payment_method(qs):
        data = (
            qs.values("payment_method")
            .annotate(
                total_sales=Count("id"),
                total_revenue=Sum("total_amount"),
            )
            .order_by("-total_revenue")
        )

        return [
            {
                "payment_method": r["payment_method"],
                "total_sales": r["total_sales"],
                "total_revenue": r["total_revenue"],
            }
            for r in data
        ]

    @staticmethod
    def get_by_period(qs, period_type):

        trunc_map = {
            "day": TruncDay,
            "week": TruncWeek,
            "month": TruncMonth,
            "year": TruncYear,
        }

        trunc_func = trunc_map.get(period_type, TruncMonth)

        data = (
            qs.annotate(period=trunc_func("created_at"))
            .values("period")
            .annotate(
                total_sales=Count("id"),
                total_revenue=Sum("total_amount"),
            )
            .order_by("period")
        )

        return [
            {
                "period": r["period"].strftime("%Y-%m-%d") if r["period"] else None,
                "total_sales": r["total_sales"],
                "total_revenue": r["total_revenue"],
            }
            for r in data
        ]
