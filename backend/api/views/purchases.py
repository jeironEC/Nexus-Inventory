from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from nexus_inventory_backend.db.models import (
    Purchase,
    PurchaseDetail,
)
from nexus_inventory_backend.db.models import Inventory
from nexus_inventory_backend.db.enums import OperationState

from api.serializers.empty import EmptySerializer
from api.serializers.purchase_read import PurchaseReadSerializer
from api.serializers.purchase_create import PurchaseCreateSerializer
from api.serializers.purchase_detail_read import PurchaseDetailReadSerializer

from api.filters.purchase import PurchaseAdminFilter, PurchaseFilter
from api.filters.purchase_detail import PurchaseDetailAdminFilter, PurchaseDetailFilter

from api.mixins.filter import StrictFilterMixin
from api.mixins.noput import NoPutMixin
from api.mixins.role_filter import RoleFilterMixin
from api.mixins.soft_delete_queryset import SoftDeleteQuerysetMixin
from api.mixins.audit_fields import AuditOperationUserMixin
from api.mixins.cancelable import CancelableMixin
from api.mixins.nested_detail import NestedDetailMixin


@extend_schema_view(
    list=extend_schema(tags=["Purchases"], summary="List purchases"),
    create=extend_schema(tags=["Purchases"], summary="Create purchase"),
    retrieve=extend_schema(tags=["Purchases"], summary="Get purchase"),
    update=extend_schema(tags=["Purchases"], summary="Update purchase"),
    partial_update=extend_schema(tags=["Purchases"], summary="Partial update purchase"),
    destroy=extend_schema(tags=["Purchases"], summary="Delete purchase"),
    cancel=extend_schema(tags=["Purchases"], summary="Cancel purchase"),
)
class PurchaseViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    NoPutMixin,
    AuditOperationUserMixin,
    SoftDeleteQuerysetMixin,
    CancelableMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona las compras del sistema.
    Permite cancelar compras mediante el endpoint /cancel.
    """

    permission_classes = [IsAuthenticated]
    admin_filterset_class = PurchaseAdminFilter
    user_filterset_class = PurchaseFilter

    queryset = (
        Purchase.objects.select_related(
            "supplier",
            "user",
            "updated_by",
            "deleted_by",
        )
        .all()
        .order_by("-created_at")
    )

    cancel_state = OperationState.CANCELED
    cancel_already_msg = "Purchase is already canceled."

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return PurchaseCreateSerializer
        if self.action == "cancel":
            return EmptySerializer
        return PurchaseReadSerializer

    def get_cancel_serializer(self, obj):
        return PurchaseReadSerializer(obj, context={"request": self.request})

    def on_cancel(self, obj):
        for detail in obj.details.select_related("product"):
            try:
                inventory = Inventory.objects.get(product=detail.product)
                inventory.quantity -= detail.quantity
                inventory.save()
            except Inventory.DoesNotExist:
                pass


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="purchases_pk", type=int, location=OpenApiParameter.PATH
            )
        ]
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter(
                name="purchases_pk", type=int, location=OpenApiParameter.PATH
            )
        ]
    ),
)
class PurchaseDetailViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    NestedDetailMixin,
    ListModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Gestiona los detalles de una compra.
    Al crear un detalle se genera automáticamente un InventoryMovement de tipo 'in'.
    """

    serializer_class = PurchaseDetailReadSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = PurchaseDetailAdminFilter
    user_filterset_class = PurchaseDetailFilter
    http_method_names = ["get"]

    parent_model = Purchase
    parent_lookup_kwarg = "purchases_pk"
    detail_model = PurchaseDetail
    detail_select_related = ("product", "product__category", "inventory_movement")
    detail_filter_field = "purchase__id"
    ordering = "created_at"
    not_found_msg = None
