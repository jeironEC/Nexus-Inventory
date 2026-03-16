# Rest framework
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Category

# Serializers
from .user_read import UserReadSerializer


class CategorySerializer(serializers.ModelSerializer):
    created_by = UserReadSerializer(read_only=True)
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
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
        queryset = Category.objects.filter(name__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A Category with this name already exists."
            )
        return value
