# DRF
from rest_framework.decorators import action
from rest_framework.response import Response

# Serializers
from api.serializers.empty import EmptySerializer

# Enums
from nexus_inventory_backend.db.enums import State


class StateMixin:
    """Mixin para viewsets que manejan un campo 'state' (ACTIVE/INACTIVE)."""

    @action(detail=False, methods=["get"])
    def active(self, request):
        qs = self.get_queryset().filter(state=State.ACTIVE)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def inactive(self, request):
        qs = self.get_queryset().filter(state=State.INACTIVE)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

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
