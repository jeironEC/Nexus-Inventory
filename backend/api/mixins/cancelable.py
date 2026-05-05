from typing import Any, ClassVar

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers.empty import EmptySerializer


class CancelableMixin:
    """
    Mixin que proporciona la lógica común para cancelar operaciones.

    Las subclases deben definir:
        cancel_state: El estado de cancelación (ej: OperationState.CANCELED)
        cancel_already_msg: Mensaje cuando ya está cancelado
        get_cancel_serializer(obj): Retorna el serializer para la respuesta

    Opcionalmente pueden sobrescribir:
        on_cancel(obj): Hook para lógica post-cancelación (ej: restaurar inventario)
    """

    cancel_state: ClassVar[Any] = None
    cancel_already_msg: ClassVar[str] = "This item is already canceled."

    def on_cancel(self, obj):
        """Hook ejecutado después de marcar como cancelado. Por defecto no hace nada."""
        pass

    def get_cancel_serializer(self, obj):
        """Retorna el serializer para la respuesta post-cancelación."""
        raise NotImplementedError

    @transaction.atomic
    @action(
        detail=True,
        methods=["patch"],
        url_name="cancel",
        serializer_class=EmptySerializer,
    )
    def cancel(self, request, pk=None):
        obj = self.get_object()

        if obj.state == self.cancel_state:
            return Response(
                {"detail": self.cancel_already_msg},
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj.state = self.cancel_state
        obj.updated_by = request.user
        obj.save(update_fields=["state", "updated_by", "updated_at"])

        self.on_cancel(obj)

        serializer = self.get_cancel_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
