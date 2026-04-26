# Django
from django.db.models import Count, Sum, Q

# Enums
from nexus_inventory_backend.db.enums import OperationState


class SaleReturnReportService:

    @staticmethod
    def get_summary(qs):
        result = qs.aggregate(
            total_returns=Count("id"),
            completed_returns=Count("id", filter=Q(state=OperationState.COMPLETED)),
            canceled_returns=Count("id", filter=Q(state=OperationState.CANCELED)),
            total_refund_amount=Sum(
                "total_amount", filter=Q(state=OperationState.COMPLETED)
            ),
        )

        return result

    @staticmethod
    def format_returns(qs):
        returns_data = qs.values(
            "id",
            "sale__id",
            "sale__customer__first_name",
            "sale__customer__last_name",
            "reason",
            "created_at",
            "total_amount",
            "state",
        )

        return [
            {
                "id": r["id"],
                "sale_id": r["sale__id"],
                "customer_name": f"{r['sale__customer__first_name'] or ''} {r['sale__customer__last_name'] or ''}".strip()
                or "Anonymous",
                "reason": r["reason"],
                "created_at": r["created_at"],
                "total_amount": r["total_amount"],
                "state": r["state"],
            }
            for r in returns_data
        ]
