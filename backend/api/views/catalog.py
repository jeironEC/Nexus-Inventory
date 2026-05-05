from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from nexus_inventory_backend.db.models import (
    Company,
    Category,
    Product,
    Supplier,
    Customer,
)

from api.serializers.company import CompanySerializer
from api.serializers.category import CategorySerializer
from api.serializers.product import ProductSerializer
from api.serializers.supplier import SupplierSerializer
from api.serializers.customer import CustomerSerializer

from api.filters.company import CompanyAdminFilter, CompanyFilter
from api.filters.category import CategoryAdminFilter, CategoryFilter
from api.filters.product import ProductAdminFilter, ProductFilter
from api.filters.supplier import SupplierAdminFilter, SupplierFilter
from api.filters.customer import CustomerAdminFilter, CustomerFilter

from api.mixins.filter import StrictFilterMixin
from api.mixins.noput import NoPutMixin
from api.mixins.role_filter import RoleFilterMixin
from api.mixins.soft_delete_queryset import SoftDeleteQuerysetMixin
from api.mixins.audit_fields import AuditUserMixin
from api.mixins.is_active import StateMixin


@extend_schema_view(
    list=extend_schema(tags=["Companies"], summary="List companies"),
    create=extend_schema(tags=["Companies"], summary="Create company"),
    retrieve=extend_schema(tags=["Companies"], summary="Get company"),
    partial_update=extend_schema(tags=["Companies"], summary="Partial update company"),
    destroy=extend_schema(tags=["Companies"], summary="Delete company"),
    activate=extend_schema(tags=["Companies"], summary="Activate company"),
    deactivate=extend_schema(tags=["Companies"], summary="Deactivate company"),
)
class CompanyViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    AuditUserMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona las compañias del sistema.
    Permite activar y desactivar compañias mediante los endpoints /activate y /deactivate.
    """

    queryset = (
        Company.objects.select_related("created_by", "updated_by", "deleted_by")
        .all()
        .order_by("name")
    )
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = CompanyAdminFilter
    user_filterset_class = CompanyFilter


@extend_schema_view(
    list=extend_schema(tags=["Categories"], summary="List categories"),
    create=extend_schema(tags=["Categories"], summary="Create category"),
    retrieve=extend_schema(tags=["Categories"], summary="Get category"),
    partial_update=extend_schema(
        tags=["Categories"], summary="Partial update category"
    ),
    destroy=extend_schema(tags=["Categories"], summary="Delete category"),
    activate=extend_schema(tags=["Categories"], summary="Activate category"),
    deactivate=extend_schema(tags=["Categories"], summary="Deactivate category"),
)
class CategoryViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    AuditUserMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona las categorías de productos.
    Permite activar y desactivar categorías mediante los endpoints /activate y /deactivate.
    """

    queryset = (
        Category.objects.select_related("created_by", "updated_by", "deleted_by")
        .all()
        .order_by("name")
    )
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = CategoryAdminFilter
    user_filterset_class = CategoryFilter


@extend_schema_view(
    list=extend_schema(tags=["Products"], summary="List products"),
    create=extend_schema(tags=["Products"], summary="Create product"),
    retrieve=extend_schema(tags=["Products"], summary="Get product"),
    partial_update=extend_schema(tags=["Products"], summary="Partial update product"),
    destroy=extend_schema(tags=["Products"], summary="Delete product"),
    activate=extend_schema(tags=["Products"], summary="Activate product"),
    deactivate=extend_schema(tags=["Products"], summary="Deactivate product"),
)
class ProductViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    AuditUserMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona los productos del sistema.
    Permite activar y desactivar productos mediante los endpoints /activate y /deactivate.
    """

    queryset = (
        Product.objects.select_related(
            "category", "created_by", "updated_by", "deleted_by"
        )
        .all()
        .order_by("name")
    )
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = ProductAdminFilter
    user_filterset_class = ProductFilter

    @action(detail=False, methods=["get"], url_path="by-supplier/<int:supplier_id>")
    def by_supplier(self, request, supplier_id):
        """Listar productos comprados a un proveedor específico."""
        products = (
            Product.objects.filter(purchase_details__purchase__supplier_id=supplier_id)
            .select_related("category")
            .distinct()
            .order_by("name")
        )

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(tags=["Suppliers"], summary="List suppliers"),
    create=extend_schema(tags=["Suppliers"], summary="Create supplier"),
    retrieve=extend_schema(tags=["Suppliers"], summary="Get supplier"),
    partial_update=extend_schema(tags=["Suppliers"], summary="Partial update supplier"),
    destroy=extend_schema(tags=["Suppliers"], summary="Delete supplier"),
    activate=extend_schema(tags=["Suppliers"], summary="Activate supplier"),
    deactivate=extend_schema(tags=["Suppliers"], summary="Deactivate supplier"),
)
class SupplierViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    AuditUserMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona los suplidores del sistema.
    """

    queryset = (
        Supplier.objects.select_related("created_by", "updated_by", "deleted_by")
        .all()
        .order_by("name")
    )
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = SupplierAdminFilter
    user_filterset_class = SupplierFilter


@extend_schema_view(
    list=extend_schema(tags=["Customers"], summary="List customers"),
    create=extend_schema(tags=["Customers"], summary="Create customer"),
    retrieve=extend_schema(tags=["Customers"], summary="Get customer"),
    partial_update=extend_schema(tags=["Customers"], summary="Partial update customer"),
    destroy=extend_schema(tags=["Customers"], summary="Delete customer"),
    activate=extend_schema(tags=["Customers"], summary="Activate customer"),
    deactivate=extend_schema(tags=["Customers"], summary="Deactivate customer"),
)
class CustomerViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    AuditUserMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona los clientes del sistema.
    Permite consultar las promociones asignadas a un cliente específico.
    """

    queryset = (
        Customer.objects.select_related("created_by", "updated_by", "deleted_by")
        .all()
        .order_by("first_name")
    )
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = CustomerAdminFilter
    user_filterset_class = CustomerFilter
