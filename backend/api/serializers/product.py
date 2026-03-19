# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Category, Product

# Serializers
from .category import CategorySerializer

# Mixins
from api.mixins.audit_fields import AuditFieldsMixin


class ProductSerializer(AuditFieldsMixin):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_id",
            "name",
            "description",
            "unique_code",
            "sale_price",
            "purchase_price",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        ]
        read_only_fields = [
            "id",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def validate(self, data):
        name = data.get("name")

        if name:
            qs = Product.objects.filter(name__iexact=name)

            if self.instance:
                qs = qs.exclude(id=self.instance.id)

            if qs.exists():
                raise serializers.ValidationError({"name": "Already exists"})

        sale_price = data.get("sale_price")
        purchase_price = data.get("purchase_price")

        if sale_price is not None and sale_price < 0:
            raise serializers.ValidationError(
                {"sale_price": "Sale price must be >= 0."}
            )

        if purchase_price is not None and purchase_price < 0:
            raise serializers.ValidationError(
                {"purchase_price": "Purchase price must be >= 0."}
            )

        if (
            sale_price is not None
            and purchase_price is not None
            and purchase_price > sale_price
        ):
            raise serializers.ValidationError(
                {"purchase_price": "Purchase price cannot exceed sale price."}
            )

        return data
