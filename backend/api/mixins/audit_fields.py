# DRF
from rest_framework import serializers

# Serializers
from api.serializers.user_read import UserReadSerializer


class AuditFieldsMixin(serializers.ModelSerializer):
    """
    Agrega los campos de auditoría en serializers marcados en read_only.
    """

    created_by = UserReadSerializer(read_only=True)
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)
