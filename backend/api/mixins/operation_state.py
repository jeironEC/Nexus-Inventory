# DRF
from rest_framework.decorators import action
from rest_framework.response import Response

# Enums
from nexus_inventory_backend.db.enums import OperationState


class OperationStateMixin:
    """Mixin para viewsets que manejan el campo 'state' de compras y ventas (COMPLETED/CANCELED)."""

    @action(detail=False, methods=["get"])
    def completed(self, request):
        qs = self.get_queryset().filter(state=OperationState.COMPLETED)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def canceled(self, request):
        qs = self.get_queryset().filter(state=OperationState.CANCELED)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
