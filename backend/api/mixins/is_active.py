# DRF
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


class StateMixin:
    """Mixin para viewsets que usan el campo 'is_active' (como User)."""

    @extend_schema(
        request=None,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "is_active": {"type": "boolean"},
                },
            }
        },
    )
    @action(detail=True, methods=["patch"])
    def activate(self, request, pk=None):
        obj = self.get_object()
        obj.is_active = True
        obj.save(update_fields=["is_active"])
        return Response({"id": obj.id, "is_active": obj.is_active})

    @extend_schema(
        request=None,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "is_active": {"type": "boolean"},
                },
            }
        },
    )
    @action(detail=True, methods=["patch"])
    def deactivate(self, request, pk=None):
        obj = self.get_object()
        obj.is_active = False
        obj.save(update_fields=["is_active"])
        return Response({"id": obj.id, "is_active": obj.is_active})
