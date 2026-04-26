# Django
from django.db.models import Count, Sum, Q

# Enums
from nexus_inventory_backend.db.enums import OperationState


class PurchaseReturnReportService:

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
            "purchase__id",
            "purchase__supplier__name",
            "reason",
            "created_at",
            "total_amount",
            "state",
        )

        return [
            {
                "id": r["id"],
                "purchase_id": r["purchase__id"],
                "supplier_name": r["purchase__supplier__name"] or "N/A",
                "reason": r["reason"],
                "created_at": r["created_at"],
                "total_amount": r["total_amount"],
                "state": r["state"],
            }
            for r in returns_data
        ]
