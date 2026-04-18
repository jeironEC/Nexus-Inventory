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
        returns = list(
            qs.values(
                "id",
                "purchase__id",
                "purchase__supplier__name",
                "created_at",
                "total_amount",
                "state",
            )
        )

        return returns
