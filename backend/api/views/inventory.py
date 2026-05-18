from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Case, CharField, Exists, OuterRef, Value, When
from drf_spectacular.utils import extend_schema, extend_schema_view

from nexus_inventory_backend.db.models import (
    Inventory,
    InventoryMovement,
    PurchaseDetail,
    PurchaseReturnDetail,
    SaleDetail,
    SaleReturnDetail,
)

from api.serializers.inventory import InventorySerializer
from api.serializers.inventory_movement import InventoryMovementSerializer

from api.filters.inventory import InventoryAdminFilter, InventoryFilter
from api.filters.inventory_movements import (
    InventoryMovementAdminFilter,
    InventoryMovementFilter,
)

from api.mixins.filter import StrictFilterMixin
from api.mixins.role_filter import RoleFilterMixin
from api.mixins.soft_delete_queryset import SoftDeleteQuerysetMixin
from api.mixins.audit_fields import AuditUserMixin


@extend_schema_view(
    list=extend_schema(tags=["Inventory"], summary="List inventory"),
    get_by_product=extend_schema(
        tags=["Inventory"], summary="Get inventory by product"
    ),
    low_stock=extend_schema(tags=["Inventory"], summary="List low stock inventory"),
)
class InventoryViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    SoftDeleteQuerysetMixin,
    AuditUserMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Expone el inventario actual de productos en modo lectura.
    Incluye endpoints para consultar por producto y detectar stock bajo.
    """

    queryset = (
        Inventory.objects.select_related(
            "product", "created_by", "updated_by", "deleted_by"
        )
        .all()
        .order_by("product__name")
    )
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = InventoryAdminFilter
    user_filterset_class = InventoryFilter

    @action(detail=False, methods=["get"], url_path=r"product/(?P<product_id>\d+)")
    def get_by_product(self, request, product_id=None):
        inventory = get_object_or_404(self.get_queryset(), product_id=product_id)
        serializer = self.get_serializer(inventory)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="low-stock")
    def low_stock(self, request):
        inventory = self.get_queryset().filter(
            quantity__lte=settings.LOW_STOCK_THRESHOLD
        )
        serializer = self.get_serializer(inventory, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        tags=["Inventory Movements"], summary="List inventory movements"
    ),
    retrieve=extend_schema(
        tags=["Inventory Movements"], summary="Get inventory movement"
    ),
)
class InventoryMovementViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Expone los movimientos de inventario en modo lectura.
    Los movimientos son generados por el sistema, no se crean ni modifican manualmente.
    """

    queryset = (
        InventoryMovement.objects.select_related("product", "user")
        .annotate(
            source=Case(
                When(
                    Exists(
                        SaleDetail.objects.filter(inventory_movement=OuterRef("pk"))
                    ),
                    then=Value("VENTA"),
                ),
                When(
                    Exists(
                        PurchaseDetail.objects.filter(inventory_movement=OuterRef("pk"))
                    ),
                    then=Value("COMPRA"),
                ),
                When(
                    Exists(
                        SaleReturnDetail.objects.filter(
                            inventory_movement=OuterRef("pk")
                        )
                    ),
                    then=Value("DEVOLUCION_VENTA"),
                ),
                When(
                    Exists(
                        PurchaseReturnDetail.objects.filter(
                            inventory_movement=OuterRef("pk")
                        )
                    ),
                    then=Value("DEVOLUCION_COMPRA"),
                ),
                default=Value("MANUAL"),
                output_field=CharField(),
            )
        )
        .all()
        .order_by("-created_at")
    )
    serializer_class = InventoryMovementSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = InventoryMovementAdminFilter
    user_filterset_class = InventoryMovementFilter
