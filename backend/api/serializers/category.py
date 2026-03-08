# Rest framework
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "state",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "state",
            "created_at",
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
