# Django
from django.db.models import Count, Q

# Enums
from nexus_inventory_backend.db.enums import InvoiceState


class InvoiceReportService:

    @staticmethod
    def get_summary(qs):
        return qs.aggregate(
            total_invoices=Count("id"),
            issued_invoices=Count("id", filter=Q(state=InvoiceState.ISSUED)),
            canceled_invoices=Count("id", filter=Q(state=InvoiceState.CANCELED)),
            pdf_generated=Count("id", filter=Q(pdf_generated=True)),
        )

    @staticmethod
    def build_sales_invoices(qs):
        return list(
            qs.values(
                "id",
                "number_invoice",
                "created_at",
                "sale__customer__first_name",
                "sale__customer__last_name",
                "sale__total_amount",
                "state",
                "pdf_generated",
            )
        )

    @staticmethod
    def build_purchase_invoices(qs):
        return list(
            qs.values(
                "id",
                "number_invoice",
                "created_at",
                "purchase__supplier__name",
                "purchase__total_amount",
                "state",
                "pdf_generated",
            )
        )
