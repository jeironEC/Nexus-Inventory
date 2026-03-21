# DRF
from rest_framework import serializers

# Serializers
from api.serializers.user_read import UserReadSerializer

# Django
from django.utils import timezone


class AuditFieldsMixin(serializers.ModelSerializer):
    """
    Agrega los campos de auditoría en serializers marcados en read_only.
    """

    created_by = UserReadSerializer(read_only=True)
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)


class AuditUserMixin:
    """
    Asignar el usuario que crea, actualiza o elimina un registro en las tablas que tienen los campos de auditoria.
    """

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_by", "deleted_at", "updated_at"])
