# DRF
from rest_framework.decorators import action
from rest_framework.response import Response

# Serializers
from api.serializers.empty import EmptySerializer


class UserStateMixin:
    """Mixin para viewsets que usan el campo 'is_active' (como User)."""

    @action(detail=False, methods=["get"])
    def active(self, request):
        qs = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def inactive(self, request):
        qs = self.get_queryset().filter(is_active=False)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], serializer_class=EmptySerializer)
    def activate(self, request, pk=None):
        obj = self.get_object()
        obj.is_active = True
        obj.save(update_fields=["is_active"])
        return Response({"id": obj.id, "is_active": obj.is_active})

    @action(detail=True, methods=["patch"], serializer_class=EmptySerializer)
    def deactivate(self, request, pk=None):
        obj = self.get_object()
        obj.is_active = False
        obj.save(update_fields=["is_active"])
        return Response({"id": obj.id, "is_active": obj.is_active})
