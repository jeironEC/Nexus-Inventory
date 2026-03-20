# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Invoice

# Serializers
from .sale_read import SaleReadSerializer


class InvoiceSerializer(serializers.ModelSerializer):
    sale = SaleReadSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "sale",
            "number_invoice",
            "pdf_generated",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "sale",
            "number_invoice",
            "pdf_generated",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
