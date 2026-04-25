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
        returns = list(
            qs.values(
                "id",
                "sale__id",
                "sale__customer__first_name",
                "sale__customer__last_name",
                "created_at",
                "total_amount",
                "state",
            )
        )

        return returns
