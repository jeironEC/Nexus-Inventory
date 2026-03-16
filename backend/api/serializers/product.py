# Rest framework
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Category, Product

# Serializers
from .user_read import UserReadSerializer
from .category import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    created_by = UserReadSerializer(read_only=True)
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)

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

    def validate_name(self, value):
        queryset = Product.objects.filter(name__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A Product with this name already exists."
            )
        return value

    def validate_sale_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Sale price must be greater than 0.")
        return value

    def validate_purchase_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Purchase price must be greater than 0.")
        return value
