# DRF
from rest_framework.decorators import action
from rest_framework.response import Response

# Serializers
from api.serializers.empty import EmptySerializer

# Enums
from nexus_inventory_backend.db.enums import State


class StateMixin:
    """Mixin para viewsets que manejan el campo 'state' (ACTIVE/INACTIVE)."""

    @action(detail=True, methods=["patch"], serializer_class=EmptySerializer)
    def activate(self, request, pk=None):
        obj = self.get_object()
        obj.state = State.ACTIVE
        obj.save(update_fields=["state"])
        return Response({"id": obj.id, "state": obj.state})

    @action(detail=True, methods=["patch"], serializer_class=EmptySerializer)
    def deactivate(self, request, pk=None):
        obj = self.get_object()
        obj.state = State.INACTIVE
        obj.save(update_fields=["state"])
        return Response({"id": obj.id, "state": obj.state})
