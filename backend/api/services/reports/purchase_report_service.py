# Django
from django.db.models import Count, Sum, Avg, Q

# Enums
from nexus_inventory_backend.db.enums import OperationState

# Services
from api.services.util_service import get_raw_value


class PurchaseReportService:

    @staticmethod
    def get_totals_from_list(result):
        return {
            "total_purchases": sum(item["total_purchases"] or 0 for item in result),
            "total_spent": sum(get_raw_value(item["total_spent"]) for item in result),
        }

    @staticmethod
    def get_summary(qs):
        return qs.aggregate(
            total_purchases=Count("id", filter=Q(state=OperationState.COMPLETED)),
            total_spent=Sum("total_amount", filter=Q(state=OperationState.COMPLETED)),
            average_purchase=Avg(
                "total_amount", filter=Q(state=OperationState.COMPLETED)
            ),
            canceled_purchases=Count("id", filter=Q(state=OperationState.CANCELED)),
        )

    @staticmethod
    def build_purchase_pdf_data(qs):
        purchases = []

        for purchase in qs:

            purchases.append(
                {
                    "id": purchase.id,
                    "created_at": purchase.created_at,
                    "supplier__name": purchase.supplier.name,
                    "total_amount": purchase.total_amount,
                    "state": purchase.state,
                }
            )

        summary = PurchaseReportService.get_summary(qs)

        return {
            "purchases": purchases,
            "summary": {
                "total_purchases": summary.get("total_purchases") or 0,
                "total_spent": summary.get("total_spent"),
                "average_purchase": summary.get("average_purchase"),
            },
        }

    @staticmethod
    def get_by_supplier(qs):
        data = (
            qs.values("supplier__id", "supplier__name")
            .annotate(
                total_purchases=Count("id"),
                total_spent=Sum("total_amount"),
            )
            .order_by("-total_spent")
        )

        return [
            {
                "supplier_id": r["supplier__id"],
                "supplier_name": r["supplier__name"],
                "total_purchases": r["total_purchases"],
                "total_spent": r["total_spent"],
            }
            for r in data
        ]

    @staticmethod
    def get_by_period(qs, trunc_func):
        data = (
            qs.annotate(period=trunc_func("created_at"))
            .values("period")
            .annotate(
                total_purchases=Count("id"),
                total_spent=Sum("total_amount"),
            )
            .order_by("period")
        )

        return [
            {
                "period": r["period"].strftime("%Y-%m-%d") if r["period"] else None,
                "total_purchases": r["total_purchases"],
                "total_spent": r["total_spent"],
            }
            for r in data
        ]
