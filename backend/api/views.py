# Internal
import uuid
from hashlib import sha256

# Django
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.http.response import HttpResponse

# Weasyprint
from weasyprint import HTML

# DRF
from rest_framework import mixins, status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import NotFound

# DRF Spectacular
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

# Serializers
from .serializers.empty import EmptySerializer
from .serializers.user_role import RoleSerializer
from .serializers.user_read import UserReadSerializer
from .serializers.password_reset import (
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    PasswordResetConfirmSerializer,
)
from .serializers.company import CompanySerializer
from .serializers.user_create import UserCreateSerializer
from .serializers.user_update import UserUpdateSerializer
from .serializers.token_pair import EmailTokenObtainPairSerializer
from .serializers.category import CategorySerializer
from .serializers.product import ProductSerializer
from .serializers.inventory import InventorySerializer
from .serializers.inventory_movement import InventoryMovementSerializer
from .serializers.customer import CustomerSerializer
from .serializers.sale_read import SaleReadSerializer
from .serializers.sale_create import SaleCreateSerializer
from .serializers.sale_detail_read import SaleDetailReadSerializer
from .serializers.sale_return_read import SaleReturnReadSerializer
from .serializers.sale_return_create import SaleReturnCreateSerializer
from .serializers.sale_return_detail_read import SaleReturnDetailReadSerializer
from .serializers.invoice import InvoiceSerializer
from .serializers.supplier import SupplierSerializer
from .serializers.purchase_read import PurchaseReadSerializer
from .serializers.purchase_create import PurchaseCreateSerializer
from .serializers.purchase_detail_read import PurchaseDetailReadSerializer
from .serializers.purchase_return_read import PurchaseReturnReadSerializer
from .serializers.purchase_return_create import PurchaseReturnCreateSerializer
from .serializers.purchase_return_detail_read import PurchaseReturnDetailReadSerializer
from .serializers.reports import (
    SaleReportSerializer,
    SaleByCustomerSerializer,
    SaleByPaymentMethodSerializer,
    SaleByPeriodSerializer,
    PurchaseReportSerializer,
    PurchaseBySupplierSerializer,
    PurchaseByPeriodSerializer,
    InventoryReportSerializer,
    InventoryLowStockSerializer,
    InventoryMovementReportSerializer,
    ProductReportSerializer,
    ProductTopSellingSerializer,
    ProductLowSellingSerializer,
    ProductMostPurchasedSerializer,
    ProductByCategorySerializer,
    CustomerReportSerializer,
    CustomerTopSerializer,
    InvoiceReportSerializer,
    SaleReturnReportSerializer,
    PurchaseReturnReportSerializer,
)

# Filters
from .filters.user_role import RoleAdminFilter, RoleFilter
from .filters.user import UserAdminFilter, UserFilter
from .filters.company import CompanyAdminFilter, CompanyFilter
from .filters.category import CategoryAdminFilter, CategoryFilter
from .filters.product import ProductAdminFilter, ProductFilter
from .filters.inventory import InventoryAdminFilter, InventoryFilter
from .filters.inventory_movements import (
    InventoryMovementAdminFilter,
    InventoryMovementFilter,
)
from .filters.customer import CustomerAdminFilter, CustomerFilter
from .filters.sale import (
    SaleAdminFilter,
    SaleFilter,
)
from .filters.sale_detail import (
    SaleDetailAdminFilter,
    SaleDetailFilter,
)
from .filters.invoice import (
    InvoiceAdminFilter,
    InvoiceFilter,
)
from .filters.supplier import (
    SupplierAdminFilter,
    SupplierFilter,
)
from .filters.purchase import (
    PurchaseAdminFilter,
    PurchaseFilter,
)
from .filters.purchase_detail import (
    PurchaseDetailAdminFilter,
    PurchaseDetailFilter,
)
from .filters.sale_return import (
    SaleReturnAdminFilter,
    SaleReturnFilter,
)
from .filters.sale_return_detail import (
    SaleReturnDetailAdminFilter,
    SaleReturnDetailFilter,
)
from .filters.purchase_return import (
    PurchaseReturnAdminFilter,
    PurchaseReturnFilter,
)
from .filters.purchase_return_detail import (
    PurchaseReturnDetailAdminFilter,
    PurchaseReturnDetailFilter,
)
from .filters.reports import (
    SaleReportFilter,
    PurchaseReportFilter,
    InventoryReportFilter,
    ProductReportFilter,
    CustomerReportFilter,
    InvoiceReportFilter,
    SaleReturnReportFilter,
    PurchaseReturnReportFilter,
)

# Models
from nexus_inventory_backend.db.models import (
    Role,
    User,
    PasswordResetOTP,
    Company,
    Category,
    Product,
    Inventory,
    InventoryMovement,
    Customer,
    Sale,
    SaleDetail,
    Invoice,
    Supplier,
    Purchase,
    PurchaseDetail,
    SaleReturn,
    SaleReturnDetail,
    PurchaseReturn,
    PurchaseReturnDetail,
)

# Permissions
from .permissions import CanCreateUsers

# Mixins
from .mixins.filter import StrictFilterMixin
from .mixins.noput import NoPutMixin
from .mixins.role_filter import RoleFilterMixin
from .mixins.soft_delete_queryset import SoftDeleteQuerysetMixin
from .mixins.report_filter import ReportFilterMixin
from .mixins.audit_fields import AuditUserMixin, AuditOperationUserMixin
from .mixins.is_active import StateMixin

# Enums
from nexus_inventory_backend.db.enums import (
    OperationState,
    InvoiceState,
    InvoiceType,
)

# Services
from api.services.email_service import send_reset_password_email
from api.services.company_service import CompanyService
from api.services.reports.sale_report_service import SaleReportService
from api.services.reports.purchase_report_service import PurchaseReportService
from api.services.reports.inventory_report_service import InventoryReportService
from api.services.reports.product_report_service import ProductReportService
from api.services.reports.customer_report_service import CustomerReportService
from api.services.reports.invoice_report_service import InvoiceReportService
from api.services.reports.sale_return_report_service import SaleReturnReportService
from api.services.reports.purchase_return_report_service import (
    PurchaseReturnReportService,
)
from api.services.util_service import format_currency, generate_otp

# Utils
from api.utils import get_trunc_func

# Date
from datetime import timedelta


@extend_schema(tags=["Health"])
class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes: list[str] = []
    serializer_class = EmptySerializer

    def get(self, request):
        return Response(
            {
                "status": "ok",
                "version": "1.0.0",
                "timestamp": timezone.now().date().isoformat(),
            }
        )


@extend_schema_view(
    list=extend_schema(tags=["Roles"], summary="List roles"),
    create=extend_schema(tags=["Roles"], summary="Create role"),
    retrieve=extend_schema(tags=["Roles"], summary="Get role"),
    partial_update=extend_schema(tags=["Roles"], summary="Partial update role"),
    destroy=extend_schema(tags=["Roles"], summary="Delete role"),
    activate=extend_schema(tags=["Roles"], summary="Activate role"),
    deactivate=extend_schema(tags=["Roles"], summary="Deactivate role"),
)
class UserRoleViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona los roles de usuario del sistema.
    Solo los administradores pueden gestionar todo el sistema.
    """

    queryset = Role.objects.all().order_by("name")
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = RoleAdminFilter
    user_filterset_class = RoleFilter


@extend_schema_view(
    list=extend_schema(tags=["Users"], summary="List users"),
    create=extend_schema(tags=["Users"], summary="Create user"),
    activate=extend_schema(tags=["Users"], summary="Activate user"),
    deactivate=extend_schema(tags=["Users"], summary="Deactivate user"),
)
class UserViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    AuditUserMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Gestiona los usuarios del sistema.
    Solo permite creación y listado. La edición y eliminación se hace desde /me.
    """

    queryset = (
        User.objects.select_related("created_by", "updated_by", "deleted_by")
        .filter(deleted_at__isnull=True)
        .order_by("created_at")
    )
    permission_classes = [IsAuthenticated, CanCreateUsers]
    admin_filterset_class = UserAdminFilter
    user_filterset_class = UserFilter

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserReadSerializer


class UserMeViewSet(SoftDeleteQuerysetMixin, viewsets.GenericViewSet):
    """
    Expone el perfil del usuario autenticado.
    Permite consultar, actualizar parcialmente y eliminar (soft delete) su propia cuenta.
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UserUpdateSerializer
        return UserReadSerializer

    @action(
        detail=False, methods=["get", "patch", "delete"], url_path="me", url_name="me"
    )
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer_class()(request.user)
            return Response(serializer.data)

        if request.method == "PATCH":
            serializer = self.get_serializer_class()(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        if request.method == "DELETE":
            request.user.soft_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class EmailTokenObtainPairViewSet(TokenObtainPairView):
    """
    Autenticación mediante email y contraseña.
    Retorna un par de tokens JWT (access y refresh).
    """

    serializer_class = EmailTokenObtainPairSerializer


class PasswordResetViewSet(viewsets.ViewSet):
    """
    Recuperación de contraseña mediante email.
    Envia un correo con un código OTP y retorna un mensaje de seguridad.
    Valida el código y retorna un token de recuperación.
    Valida el token y permite cambiar la contraseña.
    """

    permission_classes = [IsAuthenticated, CanCreateUsers]

    def get_serializer_class(self):
        if self.action == "request":
            return PasswordResetRequestSerializer
        elif self.action == "verify":
            return PasswordResetVerifySerializer
        elif self.action == "confirm":
            return PasswordResetConfirmSerializer
        return None

    @action(detail=False, methods=["post"])
    def request(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "If the email address exists, you will receive a code."},
                status=status.HTTP_200_OK,
            )

        PasswordResetOTP.objects.filter(email=email, is_used=False).update(is_used=True)

        otp = generate_otp()
        otp_hash = sha256(otp.encode()).hexdigest()

        PasswordResetOTP.objects.create(user=user, email=email, otp_hash=otp_hash)

        send_reset_password_email(email, otp, user)

        return Response(
            {"detail": "If the email address exists, you will receive a code."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def verify(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        record = PasswordResetOTP.objects.filter(email=email, is_used=False).first()

        if not record:
            return Response(
                {"detail": "Invalid or expired code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if timezone.now() - record.created_at > timedelta(minutes=5):
            return Response(
                {"detail": "Expired code."}, status=status.HTTP_400_BAD_REQUEST
            )

        if sha256(otp.encode()).hexdigest() != record.otp_hash:
            return Response(
                {"detail": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST
            )

        record.reset_token = uuid.uuid4()
        record.save(update_fields=["reset_token"])

        return Response(
            {"reset_token": str(record.reset_token)}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"])
    def confirm(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_token = serializer.validated_data["reset_token"]
        new_password = serializer.validated_data["new_password"]

        record = PasswordResetOTP.objects.filter(
            reset_token=reset_token, is_used=False
        ).first()

        if not record:
            return Response(
                {"detail": "Invalid or expired reset token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=record.email).first()

        if not user:
            return Response(
                {"detail": "Invalid user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        record.is_used = True
        record.reset_token = None
        record.save(update_fields=["is_used", "reset_token"])

        return Response(
            {"detail": "Password updated successfully"},
            status=status.HTTP_200_OK,
        )


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
        .all()
        .order_by("-created_at")
    )
    serializer_class = InventoryMovementSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = InventoryMovementAdminFilter
    user_filterset_class = InventoryMovementFilter


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


@extend_schema_view(
    list=extend_schema(tags=["Sales"], summary="List sales"),
    create=extend_schema(tags=["Sales"], summary="Create sale"),
    retrieve=extend_schema(tags=["Sales"], summary="Get sale"),
    update=extend_schema(tags=["Sales"], summary="Update sale"),
    partial_update=extend_schema(tags=["Sales"], summary="Partial update sale"),
    destroy=extend_schema(tags=["Sales"], summary="Delete sale"),
    cancel=extend_schema(tags=["Sales"], summary="Cancel sale"),
)
class SaleViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    NoPutMixin,
    AuditOperationUserMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona las ventas del sistema.
    Permite cancelar ventas mediante el endpoint /cancel.
    """

    permission_classes = [IsAuthenticated]
    admin_filterset_class = SaleAdminFilter
    user_filterset_class = SaleFilter

    queryset = (
        Sale.objects.select_related(
            "customer",
            "user",
            "updated_by",
            "deleted_by",
        )
        .all()
        .order_by("-created_at")
    )

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return SaleCreateSerializer
        if self.action == "cancel":
            return EmptySerializer
        return SaleReadSerializer

    @action(
        detail=True,
        methods=["patch"],
        url_name="cancel",
        serializer_class=EmptySerializer,
    )
    def cancel(self, request, pk=None):
        sale = self.get_object()

        if sale.state == OperationState.CANCELED:
            return Response(
                {"detail": "Sale is already canceled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sale.state = OperationState.CANCELED
        sale.updated_by = request.user
        sale.save(update_fields=["state", "updated_by", "updated_at"])

        serializer = SaleReadSerializer(sale, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(name="sales_pk", type=int, location=OpenApiParameter.PATH)
        ]
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter(name="sales_pk", type=int, location=OpenApiParameter.PATH)
        ]
    ),
)
class SaleDetailViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona los detalles de una venta.
    Al crear un detalle se genera automáticamente un InventoryMovement de tipo 'out' y su respectiva factura.
    """

    serializer_class = SaleDetailReadSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = SaleDetailAdminFilter
    user_filterset_class = SaleDetailFilter
    http_method_names = ["get"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return SaleDetail.objects.none()

        sale_pk = self.kwargs.get("sales_pk")
        if not Sale.objects.filter(pk=sale_pk).exists():
            raise NotFound(f"Sale {sale_pk} not found.")

        return (
            SaleDetail.objects.select_related(
                "product",
                "product__category",
                "inventory_movement",
            )
            .filter(sale__id=sale_pk)
            .order_by("created_at")
        )


@extend_schema_view(
    list=extend_schema(tags=["Invoices"], summary="List invoices"),
    retrieve=extend_schema(tags=["Invoices"], summary="Get invoice"),
    cancel=extend_schema(tags=["Invoices"], summary="Cancel invoice"),
)
class InvoiceViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ReadOnlyModelViewSet,
):
    """
    Gestiona las facturas del sistema.
    Las facturas se generan automáticamente al crear una venta.
    Permite cancelar facturas mediante el endpoint /cancel.
    """

    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = InvoiceAdminFilter
    user_filterset_class = InvoiceFilter

    queryset = (
        Invoice.objects.select_related(
            "sale",
            "sale__customer",
            "sale__user",
            "sale__updated_by",
            "sale__deleted_by",
        )
        .all()
        .order_by("-created_at")
    )

    def get_serializer_class(self):
        if self.action == "cancel":
            return EmptySerializer
        return InvoiceSerializer

    @action(
        detail=True,
        methods=["patch"],
        url_name="cancel",
        serializer_class=EmptySerializer,
    )
    def cancel(self, request, pk=None):
        invoice = self.get_object()

        if invoice.state == InvoiceState.CANCELED:
            return Response(
                {"detail": "Invoice is already canceled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invoice.state = InvoiceState.CANCELED
        invoice.updated_by = request.user
        invoice.save(update_fields=["state", "updated_by", "updated_at"])

        serializer = InvoiceSerializer(invoice, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        url_name="pdf",
        url_path="pdf",
        serializer_class=EmptySerializer,
    )
    def pdf(self, request, pk=None):
        invoice = get_object_or_404(
            Invoice.objects.select_related(
                "sale",
                "sale__customer",
                "sale__user",
                "purchase",
                "purchase__supplier",
                "purchase__user",
            ),
            pk=pk,
        )
        company = CompanyService.get_active_company()

        template = (
            "pdf/invoice_sale.html"
            if invoice.invoice_type == "SALE"
            else "pdf/invoice_puchase.html"
        )

        html_content = render_to_string(
            template,
            {
                "invoice": invoice,
                "company": company,
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="factura_{invoice.number_invoice}.pdf"'
        )

        return response


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

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return PurchaseCreateSerializer
        if self.action == "cancel":
            return EmptySerializer
        return PurchaseReadSerializer

    @action(
        detail=True,
        methods=["patch"],
        url_name="cancel",
        serializer_class=EmptySerializer,
    )
    def cancel(self, request, pk=None):
        purchase = self.get_object()

        if purchase.state == OperationState.CANCELED:
            return Response(
                {"detail": "Purchase is already canceled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        purchase.state = OperationState.CANCELED
        purchase.updated_by = request.user
        purchase.save(update_fields=["state", "updated_by", "updated_at"])

        serializer = PurchaseReadSerializer(purchase, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    viewsets.ModelViewSet,
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

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return PurchaseDetail.objects.none()

        purchase_pk = self.kwargs.get("purchases_pk")
        if not Purchase.objects.filter(pk=purchase_pk).exists():
            raise NotFound(f"Purchase {purchase_pk} not found.")

        return (
            PurchaseDetail.objects.select_related(
                "product",
                "product__category",
                "inventory_movement",
            )
            .filter(purchase__id=purchase_pk)
            .order_by("created_at")
        )


@extend_schema_view(
    list=extend_schema(tags=["Sale Returns"], summary="List sale returns"),
    create=extend_schema(tags=["Sale Returns"], summary="Create sale return"),
    retrieve=extend_schema(tags=["Sale Returns"], summary="Get sale return"),
    partial_update=extend_schema(
        tags=["Sale Returns"], summary="Partial update sale return"
    ),
    destroy=extend_schema(tags=["Sale Returns"], summary="Delete sale return"),
    cancel=extend_schema(tags=["Sale Returns"], summary="Cancel sale return"),
)
class SaleReturnViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    NoPutMixin,
    AuditOperationUserMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona las devoluciones de ventas del sistema.
    Permite cancelar devoluciones mediante el endpoint /cancel.
    """

    permission_classes = [IsAuthenticated]
    admin_filterset_class = SaleReturnAdminFilter
    user_filterset_class = SaleReturnFilter

    queryset = (
        SaleReturn.objects.select_related(
            "sale",
            "sale__customer",
            "user",
            "updated_by",
            "deleted_by",
        )
        .all()
        .order_by("-created_at")
    )

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return SaleReturnCreateSerializer
        if self.action == "cancel":
            return EmptySerializer
        return SaleReturnReadSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "create":
            context["sale_id"] = self.request.data.get("sale_id")
        return context

    @action(
        detail=True,
        methods=["patch"],
        url_name="cancel",
        serializer_class=EmptySerializer,
    )
    def cancel(self, request, pk=None):
        sale_return = self.get_object()

        if sale_return.state == OperationState.CANCELED:
            return Response(
                {"detail": "Sale return is already canceled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sale_return.state = OperationState.CANCELED
        sale_return.updated_by = request.user
        sale_return.save(update_fields=["state", "updated_by", "updated_at"])

        serializer = SaleReturnReadSerializer(sale_return, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="sale_returns_pk", type=int, location=OpenApiParameter.PATH
            )
        ]
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter(
                name="sale_returns_pk", type=int, location=OpenApiParameter.PATH
            )
        ]
    ),
)
class SaleReturnDetailViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona los detalles de una devolución de venta.
    """

    serializer_class = SaleReturnDetailReadSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = SaleReturnDetailAdminFilter
    user_filterset_class = SaleReturnDetailFilter
    http_method_names = ["get"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return SaleReturnDetail.objects.none()

        sale_return_pk = self.kwargs.get("sale_returns_pk")
        if not SaleReturn.objects.filter(pk=sale_return_pk).exists():
            raise NotFound(f"SaleReturn {sale_return_pk} not found.")

        return (
            SaleReturnDetail.objects.select_related(
                "product",
                "product__category",
                "inventory_movement",
            )
            .filter(sale_return__id=sale_return_pk)
            .order_by("created_at")
        )


@extend_schema_view(
    list=extend_schema(tags=["Purchase Returns"], summary="List purchase returns"),
    create=extend_schema(tags=["Purchase Returns"], summary="Create purchase return"),
    retrieve=extend_schema(tags=["Purchase Returns"], summary="Get purchase return"),
    partial_update=extend_schema(
        tags=["Purchase Returns"], summary="Partial update purchase return"
    ),
    destroy=extend_schema(tags=["Purchase Returns"], summary="Delete purchase return"),
    cancel=extend_schema(tags=["Purchase Returns"], summary="Cancel purchase return"),
)
class PurchaseReturnViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    NoPutMixin,
    AuditOperationUserMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona las devoluciones de compras del sistema.
    Permite cancelar devoluciones mediante el endpoint /cancel.
    """

    permission_classes = [IsAuthenticated]
    admin_filterset_class = PurchaseReturnAdminFilter
    user_filterset_class = PurchaseReturnFilter

    queryset = (
        PurchaseReturn.objects.select_related(
            "purchase",
            "purchase__supplier",
            "user",
            "updated_by",
            "deleted_by",
        )
        .all()
        .order_by("-created_at")
    )

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return PurchaseReturnCreateSerializer
        if self.action == "cancel":
            return EmptySerializer
        return PurchaseReturnReadSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "create":
            context["purchase_id"] = self.request.data.get("purchase_id")
        return context

    @action(
        detail=True,
        methods=["patch"],
        url_name="cancel",
        serializer_class=EmptySerializer,
    )
    def cancel(self, request, pk=None):
        purchase_return = self.get_object()

        if purchase_return.state == OperationState.CANCELED:
            return Response(
                {"detail": "Purchase return is already canceled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        purchase_return.state = OperationState.CANCELED
        purchase_return.updated_by = request.user
        purchase_return.save(update_fields=["state", "updated_by", "updated_at"])

        serializer = PurchaseReturnReadSerializer(
            purchase_return, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="purchase_returns_pk", type=int, location=OpenApiParameter.PATH
            )
        ]
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter(
                name="purchase_returns_pk", type=int, location=OpenApiParameter.PATH
            )
        ]
    ),
)
class PurchaseReturnDetailViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona los detalles de una devolución de compra.
    """

    serializer_class = PurchaseReturnDetailReadSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = PurchaseReturnDetailAdminFilter
    user_filterset_class = PurchaseReturnDetailFilter
    http_method_names = ["get"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return PurchaseReturnDetail.objects.none()

        purchase_return_pk = self.kwargs.get("purchase_returns_pk")
        if not PurchaseReturn.objects.filter(pk=purchase_return_pk).exists():
            raise NotFound(f"PurchaseReturn {purchase_return_pk} not found.")

        return (
            PurchaseReturnDetail.objects.select_related(
                "product",
                "product__category",
                "inventory_movement",
            )
            .filter(purchase_return__id=purchase_return_pk)
            .order_by("created_at")
        )


class SaleReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las ventas del sistema.
    Incluye resumen general, agrupación por cliente, método de pago y periodo (day, week, month).
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=SaleReportSerializer)
    @action(detail=False, methods=["get"], url_path="sales")
    def sales(self, request):
        qs = self.get_filtered_queryset(Sale.objects.all(), SaleReportFilter)
        data = SaleReportService.get_summary(qs)
        serializer = SaleReportSerializer(data)
        return Response(serializer.data)

    @extend_schema(responses=SaleByCustomerSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="sales/by-customer")
    def sales_by_customer(self, request):
        qs = self.get_filtered_queryset(
            Sale.objects.filter(state=OperationState.COMPLETED), SaleReportFilter
        )
        result = SaleReportService.get_by_customer(qs)
        serializer = SaleByCustomerSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=SaleByPaymentMethodSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="sales/by-payment-method")
    def sales_by_payment_method(self, request):
        qs = self.get_filtered_queryset(
            Sale.objects.filter(state=OperationState.COMPLETED), SaleReportFilter
        )
        result = SaleReportService.get_by_payment_method(qs)
        serializer = SaleByPaymentMethodSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=SaleByPeriodSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="sales/by-period")
    def sales_by_period(self, request):
        period = request.query_params.get("period", "month")
        trunc_func = get_trunc_func(period)
        qs = self.get_filtered_queryset(
            Sale.objects.filter(state=OperationState.COMPLETED), SaleReportFilter
        )
        result = SaleReportService.get_by_period(qs, trunc_func)
        serializer = SaleByPeriodSerializer(result, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="sales/pdf",
    )
    def sales_pdf(self, request):
        qs = self.get_filtered_queryset(
            Sale.objects.select_related("customer", "user").all(), SaleReportFilter
        )

        data = SaleReportService.build_sales_pdf(qs)

        company = CompanyService.get_active_company()

        for sale in data["sales"]:
            sale["subtotal"] = format_currency(sale.get("subtotal"))
            sale["tax_amount"] = format_currency(sale.get("tax_amount"))
            sale["total_amount"] = format_currency(sale.get("total_amount"))

        data["summary"]["total_revenue"] = format_currency(
            data["summary"].get("total_revenue")
        )
        data["summary"]["total_tax"] = format_currency(data["summary"].get("total_tax"))
        data["summary"]["average_ticket"] = format_currency(
            data["summary"].get("average_ticket")
        )

        html_content = render_to_string(
            "pdf/sales_report.html",
            {
                "data": data["summary"],
                "sales": data["sales"],
                "company": company,
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_ventas.pdf"'
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="sales/by-customer/pdf",
    )
    def sales_by_customer_pdf(self, request):
        qs = self.get_filtered_queryset(
            Sale.objects.filter(state=OperationState.COMPLETED), SaleReportFilter
        )
        result = SaleReportService.get_by_customer(qs)
        totals = SaleReportService.get_totals_from_list(result)

        total_sales = totals["total_sales"]
        total_revenue = totals["total_revenue"]

        company = CompanyService.get_active_company()

        for item in result:
            item["total_revenue"] = format_currency(item["total_revenue"])

        html_content = render_to_string(
            "pdf/sales_by_customer_report.html",
            {
                "data": result,
                "company": company,
                "total_sales": total_sales,
                "total_revenue": format_currency(total_revenue),
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_ventas_por_cliente.pdf"'
        )
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="sales/by-payment-method/pdf",
    )
    def sales_by_payment_method_pdf(self, request):
        qs = self.get_filtered_queryset(
            Sale.objects.filter(state=OperationState.COMPLETED), SaleReportFilter
        )
        result = SaleReportService.get_by_payment_method(qs)
        totals = SaleReportService.get_totals_from_list(result)

        total_sales = totals["total_sales"]
        total_revenue = totals["total_revenue"]

        company = CompanyService.get_active_company()

        for item in result:
            item["total_revenue"] = format_currency(item["total_revenue"])

        html_content = render_to_string(
            "pdf/sales_by_payment_method_report.html",
            {
                "data": result,
                "company": company,
                "total_sales": total_sales,
                "total_revenue": format_currency(total_revenue),
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_ventas_por_metodo_pago.pdf"'
        )
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="sales/by-period/pdf",
    )
    def sales_by_period_pdf(self, request):
        period_type = request.query_params.get("period_type", "month")
        qs = self.get_filtered_queryset(
            Sale.objects.filter(state=OperationState.COMPLETED), SaleReportFilter
        )
        result = SaleReportService.get_by_period(qs, period_type)
        totals = SaleReportService.get_totals_from_list(result)

        total_sales = totals["total_sales"]
        total_revenue = totals["total_revenue"]

        company = CompanyService.get_active_company()

        for item in result:
            item["total_revenue"] = format_currency(item["total_revenue"])

        html_content = render_to_string(
            "pdf/sales_by_period_report.html",
            {
                "data": result,
                "company": company,
                "total_sales": total_sales,
                "total_revenue": format_currency(total_revenue),
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_ventas_por_periodo.pdf"'
        )
        return response


class PurchaseReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las compras del sistema.
    Incluye resumen general, agrupación por proveedor y periodo (day, week, month).
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=PurchaseReportSerializer)
    @action(detail=False, methods=["get"], url_path="purchases")
    def purchases(self, request):
        qs = self.get_filtered_queryset(Purchase.objects.all(), PurchaseReportFilter)
        data = PurchaseReportService.get_summary(qs)
        serializer = PurchaseReportSerializer(data)
        return Response(serializer.data)

    @extend_schema(responses=PurchaseBySupplierSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="purchases/by-supplier")
    def purchases_by_supplier(self, request):
        qs = self.get_filtered_queryset(
            Purchase.objects.filter(state=OperationState.COMPLETED),
            PurchaseReportFilter,
        )
        result = PurchaseReportService.get_by_supplier(qs)
        serializer = PurchaseBySupplierSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=PurchaseByPeriodSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="purchases/by-period")
    def purchases_by_period(self, request):
        period = request.query_params.get("period", "month")
        trunc_func = get_trunc_func(period)
        qs = self.get_filtered_queryset(
            Purchase.objects.filter(state=OperationState.COMPLETED),
            PurchaseReportFilter,
        )
        result = PurchaseReportService.get_by_period(qs, trunc_func)
        serializer = PurchaseByPeriodSerializer(result, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="purchases/pdf",
    )
    def purchases_pdf(self, request):
        qs = self.get_filtered_queryset(
            Purchase.objects.select_related("supplier", "user").all(),
            PurchaseReportFilter,
        )

        data = PurchaseReportService.build_purchase_pdf_data(qs)

        company = CompanyService.get_active_company()

        for purchase in data["purchases"]:
            purchase["total_amount"] = format_currency(purchase.get("total_amount"))

        data["summary"]["total_spent"] = format_currency(
            data["summary"].get("total_spent")
        )
        data["summary"]["average_purchase"] = format_currency(
            data["summary"].get("average_purchase")
        )

        html_content = render_to_string(
            "pdf/purchases_report.html",
            {
                "data": data["summary"],
                "purchases": data["purchases"],
                "company": company,
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_compras.pdf"'
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="purchases/by-supplier/pdf",
    )
    def purchases_by_supplier_pdf(self, request):
        qs = self.get_filtered_queryset(
            Purchase.objects.filter(state=OperationState.COMPLETED),
            PurchaseReportFilter,
        )
        result = PurchaseReportService.get_by_supplier(qs)

        totals = PurchaseReportService.get_totals_from_list(result)
        total_purchases = totals["total_purchases"]
        total_spent = totals["total_spent"]

        company = CompanyService.get_active_company()

        for item in result:
            item["total_spent"] = format_currency(item["total_spent"])

        html_content = render_to_string(
            "pdf/purchases_by_supplier_report.html",
            {
                "data": result,
                "company": company,
                "total_purchases": total_purchases,
                "total_spent": format_currency(total_spent),
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_compras_por_proveedor.pdf"'
        )
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="purchases/by-period/pdf",
    )
    def purchases_by_period_pdf(self, request):
        period = request.query_params.get("period", "month")
        trunc_func = get_trunc_func(period)
        qs = self.get_filtered_queryset(
            Purchase.objects.filter(state=OperationState.COMPLETED),
            PurchaseReportFilter,
        )
        result = PurchaseReportService.get_by_period(qs, trunc_func)

        company = CompanyService.get_active_company()

        for item in result:
            item["total_spent"] = format_currency(item["total_spent"])

        html_content = render_to_string(
            "pdf/purchases_by_period_report.html", {"data": result, "company": company}
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_compras_por_periodo.pdf"'
        )
        return response


class InventoryReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con el inventario del sistema.
    Incluye stock actual por producto, productos con stock bajo un umbral configurable
    y historial de movimientos de inventario (entradas y salidas).
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=InventoryReportSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="inventory")
    def inventory(self, request):
        qs = self.get_filtered_queryset(
            Inventory.objects.select_related("product", "product__category").all(),
            InventoryReportFilter,
        )
        result = [InventoryReportService.map_inventory(inv) for inv in qs]
        serializer = InventoryReportSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=InventoryLowStockSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="inventory/low-stock")
    def low_stock(self, request):
        threshold = int(
            request.query_params.get(
                "low_stock_threshold", settings.LOW_STOCK_THRESHOLD
            )
        )
        qs = self.get_filtered_queryset(
            Inventory.objects.select_related("product", "product__category").filter(
                quantity__lte=threshold
            ),
            InventoryReportFilter,
        )
        result = [InventoryReportService.map_low_stock(inv, threshold) for inv in qs]
        serializer = InventoryLowStockSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=InventoryMovementReportSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="inventory/movements")
    def movements(self, request):
        qs = self.get_filtered_queryset(
            InventoryMovement.objects.select_related("product", "user").all(),
            InventoryReportFilter,
        )
        result = [InventoryReportService.map_movement(m) for m in qs]
        serializer = InventoryMovementReportSerializer(result, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="inventory/pdf",
    )
    def inventory_pdf(self, request):
        qs = self.get_filtered_queryset(
            Inventory.objects.select_related("product", "product__category").all(),
            InventoryReportFilter,
        )
        result = [InventoryReportService.map_inventory(inv) for inv in qs]

        totals = InventoryReportService.get_totals_for_inventory(result)
        total_quantity = totals["total_quantity"]
        total_sale_price = totals["total_sale_price"]
        total_stock_value = totals["total_stock_value"]

        company = CompanyService.get_active_company()

        for item in result:
            item["sale_price"] = format_currency(item["sale_price"])
            item["stock_value"] = format_currency(item["stock_value"])

        html_content = render_to_string(
            "pdf/inventory_report.html",
            {
                "inventory": result,
                "company": company,
                "total_quantity": total_quantity,
                "total_sale_price": format_currency(total_sale_price),
                "total_stock_value": format_currency(total_stock_value),
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_inventario.pdf"'
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="inventory/low-stock/pdf",
    )
    def low_stock_pdf(self, request):
        threshold = int(
            request.query_params.get(
                "low_stock_threshold", settings.LOW_STOCK_THRESHOLD
            )
        )
        qs = self.get_filtered_queryset(
            Inventory.objects.select_related("product", "product__category").filter(
                quantity__lte=threshold
            ),
            InventoryReportFilter,
        )
        result = [InventoryReportService.map_low_stock(inv, threshold) for inv in qs]

        company = CompanyService.get_active_company()

        html_content = render_to_string(
            "pdf/inventory_low_stock_report.html",
            {"data": result, "threshold": threshold, "company": company},
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_bajo_stock.pdf"'
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="inventory/movements/pdf",
    )
    def movements_pdf(self, request):
        qs = self.get_filtered_queryset(
            InventoryMovement.objects.select_related("product", "user").all(),
            InventoryReportFilter,
        )
        result = [InventoryReportService.map_movement(m) for m in qs]

        company = CompanyService.get_active_company()

        totals = InventoryReportService.get_totals_for_movements(result)
        total_in = totals["total_in"]
        total_out = totals["total_out"]

        html_content = render_to_string(
            "pdf/inventory_movements_report.html",
            {
                "data": result,
                "company": company,
                "total_in": total_in,
                "total_out": total_out,
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_movimientos_inventario.pdf"'
        )
        return response


class ProductReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con los productos del sistema.
    Incluye productos más vendidos, menos vendidos, más comprados a proveedores
    y agrupación de ventas por categoría.
    """

    permission_classes = [IsAuthenticated]

    def _base_sale_detail_qs(self):
        return self.get_filtered_queryset(
            SaleDetail.objects.select_related(
                "product", "product__category", "sale"
            ).filter(sale__state=OperationState.COMPLETED),
            ProductReportFilter,
        )

    @extend_schema(responses=ProductReportSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="products")
    def products(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))

        sale_qs = self._base_sale_detail_qs()

        purchase_qs = self.get_filtered_queryset(
            PurchaseDetail.objects.select_related(
                "product", "product__category", "purchase"
            ).filter(purchase__state=OperationState.COMPLETED),
            ProductReportFilter,
        )

        data = ProductReportService.build_report_products(sale_qs, purchase_qs, limit)

        serializer = ProductReportSerializer(data)
        return Response(serializer.data)

    @extend_schema(responses=ProductTopSellingSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="products/top-selling")
    def top_selling(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        result = ProductReportService.get_products_report(
            qs=self._base_sale_detail_qs(),
            order_by="-total_quantity",
            limit=limit,
        )
        serializer = ProductTopSellingSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=ProductLowSellingSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="products/low-selling")
    def low_selling(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        result = ProductReportService.get_products_report(
            qs=self._base_sale_detail_qs(),
            order_by="total_quantity",
            limit=limit,
        )
        serializer = ProductLowSellingSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=ProductMostPurchasedSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="products/most-purchased")
    def most_purchased(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        qs = self.get_filtered_queryset(
            PurchaseDetail.objects.select_related(
                "product", "product__category", "purchase"
            ).filter(purchase__state=OperationState.COMPLETED),
            ProductReportFilter,
        )
        result = ProductReportService.get_products_report(
            qs=qs,
            order_by="-total_quantity",
            limit=limit,
        )
        serializer = ProductMostPurchasedSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=ProductByCategorySerializer(many=True))
    @action(detail=False, methods=["get"], url_path="products/by-category")
    def by_category(self, request):
        result = ProductReportService.get_products_by_category(
            self._base_sale_detail_qs(),
        )
        serializer = ProductByCategorySerializer(result, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="products/pdf",
    )
    def products_pdf(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))

        sale_qs = self._base_sale_detail_qs()

        purchase_qs = self.get_filtered_queryset(
            PurchaseDetail.objects.select_related(
                "product", "product__category", "purchase"
            ).filter(purchase__state=OperationState.COMPLETED),
            ProductReportFilter,
        )

        data = ProductReportService.build_report_products(sale_qs, purchase_qs, limit)

        company = CompanyService.get_active_company()

        for section in ["top_selling", "most_purchased", "by_category"]:
            if section == "by_category":
                for cat in data.get(section, []):
                    cat["total_revenue"] = format_currency(cat.get("total_revenue"))
            else:
                for item in data.get(section, []):
                    item["total_amount"] = format_currency(item.get("total_amount"))
                    item["total_revenue"] = format_currency(item.get("total_revenue"))
                    item["total_spent"] = format_currency(item.get("total_spent"))

        html_content = render_to_string(
            "pdf/products_report.html", {"data": data, "company": company}
        )

        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="products/top-selling/pdf",
    )
    def top_selling_pdf(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        result = ProductReportService.get_products_report(
            qs=self._base_sale_detail_qs(),
            order_by="-total_quantity",
            limit=limit,
        )

        totals = ProductReportService.get_totals_from_report(result)
        total_quantity = totals["total_quantity"]
        total_revenue = totals["total_revenue"]

        company = CompanyService.get_active_company()

        for item in result:
            item["total_amount"] = format_currency(item.get("total_amount"))

        html_content = render_to_string(
            "pdf/products_top_selling.html",
            {
                "data": result,
                "company": company,
                "total_quantity": total_quantity,
                "total_revenue": format_currency(total_revenue),
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_productos_mas_vendidos.pdf"'
        )
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="products/low-selling/pdf",
    )
    def low_selling_pdf(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        result = ProductReportService.get_products_report(
            qs=self._base_sale_detail_qs(),
            order_by="total_quantity",
            limit=limit,
        )

        totals = ProductReportService.get_totals_from_report(result)
        total_quantity = totals["total_quantity"]
        total_revenue = totals["total_revenue"]

        company = CompanyService.get_active_company()

        for item in result:
            item["total_amount"] = format_currency(item.get("total_amount"))

        html_content = render_to_string(
            "pdf/products_low_selling_report.html",
            {
                "data": result,
                "company": company,
                "total_quantity": total_quantity,
                "total_revenue": format_currency(total_revenue),
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_productos_menos_vendidos.pdf"'
        )
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="products/most-purchased/pdf",
    )
    def most_purchased_pdf(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        qs = self.get_filtered_queryset(
            PurchaseDetail.objects.select_related(
                "product", "product__category", "purchase"
            ).filter(purchase__state=OperationState.COMPLETED),
            ProductReportFilter,
        )
        result = ProductReportService.get_products_report(
            qs=qs,
            order_by="-total_quantity",
            limit=limit,
        )

        totals = ProductReportService.get_totals_from_report(
            result, amount_field="total_spent"
        )
        total_quantity = totals["total_quantity"]
        total_spent = totals["total_spent"]

        company = CompanyService.get_active_company()

        for item in result:
            item["total_amount"] = format_currency(item.get("total_amount"))
            item["total_spent"] = format_currency(item.get("total_spent"))

        html_content = render_to_string(
            "pdf/products_most_purchased_report.html",
            {
                "data": result,
                "company": company,
                "total_quantity": total_quantity,
                "total_spent": format_currency(total_spent),
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_productos_mas_comprados.pdf"'
        )
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="products/by-category/pdf",
    )
    def by_category_pdf(self, request):
        result = ProductReportService.get_products_by_category(
            self._base_sale_detail_qs(),
        )

        totals = ProductReportService.get_totals_by_category(result)
        total_quantity = totals["total_quantity"]
        total_revenue = totals["total_revenue"]

        company = CompanyService.get_active_company()

        for item in result:
            item["total_revenue"] = format_currency(item.get("total_revenue"))

        html_content = render_to_string(
            "pdf/products_by_category_report.html",
            {
                "data": result,
                "company": company,
                "total_quantity": total_quantity,
                "total_revenue": format_currency(total_revenue),
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_productos_por_categoria.pdf"'
        )
        return response


class CustomerReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con los clientes del sistema.
    Incluye ranking de clientes por gasto total y uso de promociones por cliente.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=CustomerReportSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="customers")
    def customers(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        qs = self.get_filtered_queryset(
            Customer.objects.filter(sales__state=OperationState.COMPLETED),
            CustomerReportFilter,
        )
        result = CustomerReportService.get_summary(qs, limit)

        serializer = CustomerReportSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=CustomerTopSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="customers/top")
    def top_customers(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        qs = self.get_filtered_queryset(
            Customer.objects.filter(sales__state=OperationState.COMPLETED),
            CustomerReportFilter,
        )
        result = CustomerReportService.get_summary(qs, limit)
        serializer = CustomerTopSerializer(result, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="customers/pdf",
    )
    def customers_pdf(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))

        qs = self.get_filtered_queryset(
            Customer.objects.filter(sales__state=OperationState.COMPLETED),
            CustomerReportFilter,
        )
        result = CustomerReportService.get_summary(qs, limit)

        totals = CustomerReportService.get_totals_from_summary(result)
        total_purchases = totals["total_purchases"]
        total_spent = totals["total_spent"]

        company = CompanyService.get_active_company()

        for item in result:
            item["total_spent"] = format_currency(item["total_spent"])

        html_content = render_to_string(
            "pdf/customers_report.html",
            {
                "data": result,
                "company": company,
                "total_purchases": total_purchases,
                "total_spent": format_currency(total_spent),
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_clientes.pdf"'
        return response

    @action(detail=False, methods=["get"], url_path="customers/top/pdf")
    def top_customers_pdf(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        qs = self.get_filtered_queryset(
            Customer.objects.filter(sales__state=OperationState.COMPLETED),
            CustomerReportFilter,
        )
        result = CustomerReportService.get_summary(qs, limit)

        totals = CustomerReportService.get_totals_from_summary(result)
        total_customers = totals["total_customers"]
        total_purchases = totals["total_purchases"]
        total_spent = totals["total_spent"]

        company = CompanyService.get_active_company()

        for item in result:
            item["total_spent"] = format_currency(item["total_spent"])

        html_content = render_to_string(
            "pdf/customers_top_report.html",
            {
                "data": result,
                "company": company,
                "total_customers": total_customers,
                "total_purchases": total_purchases,
                "total_spent": format_currency(total_spent),
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_clientes_top.pdf"'
        return response


class InvoiceReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las facturas del sistema.
    Incluye resumen de facturas emitidas, canceladas y con PDF generado.
    Incluye reportes específicos de facturas de ventas y compras.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=InvoiceReportSerializer)
    @action(detail=False, methods=["get"], url_path="invoices")
    def invoices(self, request):
        qs = self.get_filtered_queryset(Invoice.objects.all(), InvoiceReportFilter)
        data = InvoiceReportService.get_summary(qs)
        serializer = InvoiceReportSerializer(data)
        return Response(serializer.data)

    @extend_schema(responses=InvoiceReportSerializer)
    @action(detail=False, methods=["get"], url_path="invoices/sales")
    def invoices_sales(self, request):
        qs = self.get_filtered_queryset(
            Invoice.objects.filter(invoice_type=InvoiceType.SALE), InvoiceReportFilter
        )
        data = InvoiceReportService.get_summary(qs)
        serializer = InvoiceReportSerializer(data)
        return Response(serializer.data)

    @extend_schema(responses=InvoiceReportSerializer)
    @action(detail=False, methods=["get"], url_path="invoices/purchases")
    def invoices_purchases(self, request):
        qs = self.get_filtered_queryset(
            Invoice.objects.filter(invoice_type=InvoiceType.PURCHASE),
            InvoiceReportFilter,
        )
        data = InvoiceReportService.get_summary(qs)
        serializer = InvoiceReportSerializer(data)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="invoices/pdf",
    )
    def invoices_pdf(self, request):
        qs = self.get_filtered_queryset(
            Invoice.objects.select_related(
                "sale", "sale__customer", "purchase", "purchase__supplier"
            ).all(),
            InvoiceReportFilter,
        )

        data = InvoiceReportService.get_summary(qs)

        invoices = list(
            qs.values(
                "id",
                "number_invoice",
                "created_at",
                "sale__customer__first_name",
                "sale__customer__last_name",
                "purchase__supplier__name",
                "sale__total_amount",
                "purchase__total_amount",
                "state",
                "pdf_generated",
            )
        )

        company = CompanyService.get_active_company()

        for inv in invoices:
            if inv.get("sale__total_amount"):
                inv["sale__total_amount"] = format_currency(inv["sale__total_amount"])
            if inv.get("purchase__total_amount"):
                inv["purchase__total_amount"] = format_currency(
                    inv["purchase__total_amount"]
                )

        html_content = render_to_string(
            "pdf/invoices_report.html",
            {
                "data": data,
                "invoices": invoices,
                "company": company,
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_facturas.pdf"'
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="invoices/sales/pdf",
    )
    def invoices_sales_pdf(self, request):
        qs = self.get_filtered_queryset(
            Invoice.objects.select_related("sale", "sale__customer").filter(
                invoice_type=InvoiceType.SALE
            ),
            InvoiceReportFilter,
        )
        invoices = InvoiceReportService.build_sales_invoices(qs)

        data = InvoiceReportService.get_summary(qs)

        company = CompanyService.get_active_company()

        for inv in invoices:
            inv["sale__total_amount"] = format_currency(inv.get("sale__total_amount"))

        html_content = render_to_string(
            "pdf/invoices_sales_report.html",
            {
                "data": data,
                "invoices": invoices,
                "company": company,
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_facturas_ventas.pdf"'
        )
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="invoices/purchases/pdf",
    )
    def invoices_purchases_pdf(self, request):
        qs = self.get_filtered_queryset(
            Invoice.objects.select_related("purchase", "purchase__supplier").filter(
                invoice_type=InvoiceType.PURCHASE
            ),
            InvoiceReportFilter,
        )
        invoices = InvoiceReportService.build_purchase_invoices(qs)
        data = InvoiceReportService.get_summary(qs)

        company = CompanyService.get_active_company()

        for inv in invoices:
            inv["purchase__total_amount"] = format_currency(
                inv.get("purchase__total_amount")
            )

        html_content = render_to_string(
            "pdf/invoices_purchases_report.html",
            {
                "data": data,
                "invoices": invoices,
                "company": company,
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_facturas_compras.pdf"'
        )
        return response


class SaleReturnReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las devoluciones de ventas.
    Incluye resumen general, devoluciones canceladas y completadas.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=SaleReturnReportSerializer)
    @action(detail=False, methods=["get"], url_path="sale-returns")
    def sale_returns(self, request):
        qs = self.get_filtered_queryset(
            SaleReturn.objects.all(), SaleReturnReportFilter
        )
        data = SaleReturnReportService.get_summary(qs)
        serializer = SaleReturnReportSerializer(data)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="sale-returns/pdf",
    )
    def sale_returns_pdf(self, request):
        qs = self.get_filtered_queryset(
            SaleReturn.objects.select_related("sale", "sale__customer").all(),
            SaleReturnReportFilter,
        )

        data = SaleReturnReportService.get_summary(qs)
        data["total_refund_amount"] = format_currency(data.get("total_refund_amount"))

        sales_returns = SaleReturnReportService.format_returns(qs)

        company = CompanyService.get_active_company()

        for ret in sales_returns:
            ret["total_amount"] = format_currency(ret.get("total_amount"))

        html_content = render_to_string(
            "pdf/sale_returns_report.html",
            {"data": data, "sales_returns": sales_returns, "company": company},
        )

        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_devoluciones_ventas.pdf"'
        )
        return response


class PurchaseReturnReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las devoluciones de compras.
    Incluye resumen general, devoluciones canceladas y completadas.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=PurchaseReturnReportSerializer)
    @action(detail=False, methods=["get"], url_path="purchase-returns")
    def purchase_returns(self, request):
        qs = self.get_filtered_queryset(
            PurchaseReturn.objects.all(), PurchaseReturnReportFilter
        )
        data = PurchaseReturnReportService.get_summary(qs)
        serializer = PurchaseReturnReportSerializer(data)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="purchase-returns/pdf",
    )
    def purchase_returns_pdf(self, request):
        qs = self.get_filtered_queryset(
            PurchaseReturn.objects.select_related(
                "purchase", "purchase__supplier"
            ).all(),
            PurchaseReturnReportFilter,
        )

        data = PurchaseReturnReportService.get_summary(qs)
        data["total_refund_amount"] = format_currency(data.get("total_refund_amount"))

        purchases_returns = PurchaseReturnReportService.format_returns(qs)

        company = CompanyService.get_active_company()

        for ret in purchases_returns:
            ret["total_amount"] = format_currency(ret.get("total_amount"))

        html_content = render_to_string(
            "pdf/purchase_returns_report.html",
            {"data": data, "purchases_returns": purchases_returns, "company": company},
        )

        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            'inline; filename="reporte_devoluciones_compras.pdf"'
        )
        return response
