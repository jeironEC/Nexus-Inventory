# Django
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

# DRF
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

# Serializers
from .serializers.empty import EmptySerializer
from .serializers.user_role import RoleSerializer
from .serializers.user_read import UserReadSerializer
from .serializers.user_create import UserCreateSerializer
from .serializers.user_update import UserUpdateSerializer
from .serializers.token_pair import EmailTokenObtainPairSerializer
from .serializers.category import CategorySerializer
from .serializers.product import ProductSerializer
from .serializers.inventory import InventorySerializer
from .serializers.inventory_movement import InventoryMovementSerializer
from .serializers.customer import CustomerSerializer
from .serializers.promotion import PromotionSerializer
from .serializers.customer_promotion import (
    CustomerPromotionSerializer,
    CustomerPromotionCreateSerializer,
)

# Filters
from .filters.user_role import RoleAdminFilter, RoleFilter
from .filters.user import UserAdminFilter, UserFilter
from .filters.category import CategoryAdminFilter, CategoryFilter
from .filters.product import ProductAdminFilter, ProductFilter
from .filters.inventory import InventoryAdminFilter, InventoryFilter
from .filters.inventory_movements import (
    InventoryMovementAdminFilter,
    InventoryMovementFilter,
)
from .filters.customer import CustomerAdminFilter, CustomerFilter
from .filters.promotion import PromotionAdminFilter, PromotionFilter
from .filters.customer_promotions import (
    CustomerPromotionAdminFilter,
    CustomerPromotionFilter,
)

# Models
from nexus_inventory_backend.db.models import (
    Role,
    User,
    Category,
    Product,
    Inventory,
    InventoryMovement,
    Customer,
    Promotion,
    CustomerPromotion,
)

# Permissions
from .permissions import CanCreateUsers

# Enums
from nexus_inventory_backend.db.enums import State

# Mixins
from .mixins import StrictFilterMixin

# Variables globales
LOW_STOCK_THRESHOLD = 5


def healthcheck(request):
    """
    Vista para mostrar el estado correcto de la API
    """
    return JsonResponse({"health": "ok"}, status=200)


class UserRoleViewSet(StrictFilterMixin, viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by("name")
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_filterset_class(self):
        if self.request.user.role == "ADMIN":
            return RoleAdminFilter
        return RoleFilter


class UserViewSet(
    StrictFilterMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    queryset = User.objects.filter(deleted_at__isnull=True)
    permission_classes = [IsAuthenticated, CanCreateUsers]
    throttle_classes = [UserRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserAdminFilter

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserReadSerializer

    def get_filterset_class(self):
        if self.request.user.role == "ADMIN":
            return UserAdminFilter
        return UserFilter


class UserMeViewSet(viewsets.GenericViewSet):
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
    ViewSet que permite obtener token usando el email
    """

    serializer_class = EmailTokenObtainPairSerializer


class CategoryViewSet(StrictFilterMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryAdminFilter
    http_method_names = ["get", "post", "patch", "delete"]

    def get_filterset_class(self):
        if self.request.user.role == "ADMIN":
            return CategoryAdminFilter
        return CategoryFilter

    @action(detail=False, methods=["get"])
    def active(self, request):
        categories = Category.objects.filter(state=State.ACTIVE)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def inactive(self, request):
        categories = Category.objects.filter(state=State.INACTIVE)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], serializer_class=EmptySerializer)
    def activate(self, request, pk=None):
        category = self.get_object()
        category.state = State.ACTIVE
        category.save()

        return Response(
            {"id": category.id, "state": category.state}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["patch"], serializer_class=EmptySerializer)
    def deactivate(self, request, pk=None):
        category = self.get_object()
        category.state = State.INACTIVE
        category.save()

        return Response(
            {"id": category.id, "state": category.state}, status=status.HTTP_200_OK
        )


class ProductViewSet(StrictFilterMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("name")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductAdminFilter
    http_method_names = ["get", "post", "patch", "delete"]

    def get_filterset_class(self):
        if self.request.user.role == "ADMIN":
            return ProductAdminFilter
        return ProductFilter

    @action(detail=False, methods=["get"])
    def active(self, request):
        products = Product.objects.filter(state=State.ACTIVE)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def inactive(self, request):
        products = Product.objects.filter(state=State.INACTIVE)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], serializer_class=EmptySerializer)
    def activate(self, request, pk=None):
        product = self.get_object()
        product.state = State.ACTIVE
        product.save()

        return Response(
            {"id": product.id, "state": product.state}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["patch"], serializer_class=EmptySerializer)
    def deactivate(self, request, pk=None):
        product = self.get_object()
        product.state = State.INACTIVE
        product.save()

        return Response(
            {"id": product.id, "state": product.state}, status=status.HTTP_200_OK
        )


class InventoryViewSet(
    StrictFilterMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Inventory.objects.select_related("product").all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = InventoryAdminFilter

    def get_filterset_class(self):
        if self.request.user.role == "ADMIN":
            return InventoryAdminFilter
        return InventoryFilter

    @action(detail=False, methods=["get"], url_path="product/<int:product_id>")
    def get_by_product(self, request, product_id=None):
        try:
            inventory = Inventory.objects.get(product_id=product_id)
        except Inventory.DoesNotExist:
            return Response(
                {"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(inventory)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="low-stock")
    def low_stock(self, request):
        inventory = Inventory.objects.filter(quantity__lte=LOW_STOCK_THRESHOLD)
        serializer = self.get_serializer(inventory, many=True)
        return Response(serializer.data)


class InventoryMovementViewSet(StrictFilterMixin, viewsets.ModelViewSet):
    queryset = InventoryMovement.objects.all().order_by("-created_at")
    serializer_class = InventoryMovementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = InventoryMovementAdminFilter
    http_method_names = ["get"]

    def get_filterset_class(self):
        if self.request.user.role == "ADMIN":
            return InventoryMovementAdminFilter
        return InventoryMovementFilter


class CustomerViewSet(StrictFilterMixin, viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerAdminFilter
    http_method_names = ["get", "post", "patch", "delete"]

    def get_filterset_class(self):
        if self.request.user.role == "ADMIN":
            return CustomerAdminFilter
        return CustomerFilter

    @action(
        detail=True,
        methods=["get"],
        url_path="list_promotions",
        serializer_class=EmptySerializer,
    )
    def list_promotions(self, request, pk=None):
        customer = self.get_object()

        promotions = CustomerPromotion.objects.filter(customer=customer).select_related(
            "promotion"
        )

        serializer = CustomerPromotionSerializer(promotions, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="promotions",
        serializer_class=CustomerPromotionCreateSerializer,
    )
    def add_promotion(self, request, pk=None):
        customer = self.get_object()

        promotion_id = request.data.get("promotion")

        promotion = get_object_or_404(Promotion, id=promotion_id)

        customer_promotion, created = CustomerPromotion.objects.get_or_create(
            customer=customer, promotion=promotion
        )

        if not created:
            return Response(
                {"detail": "Promotion already assigned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CustomerPromotionSerializer(customer_promotion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PromotionViewSet(StrictFilterMixin, viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PromotionAdminFilter
    http_method_names = ["get", "post", "patch", "delete"]

    def get_filterset_class(self):
        if self.request.user.role == "ADMIN":
            return PromotionAdminFilter
        return PromotionFilter


class CustomerPromotionViewSet(StrictFilterMixin, viewsets.ModelViewSet):
    queryset = CustomerPromotion.objects.select_related(
        "customer",
        "promotion",
    ).all()
    serializer_class = CustomerPromotionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerPromotionAdminFilter
    http_method_names = ["get", "post", "patch", "delete"]

    def get_filterset_class(self):
        if self.request.user.role == "ADMIN":
            return CustomerPromotionAdminFilter
        return CustomerPromotionFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = serializer.validated_data["customer"]
        promotion = serializer.validated_data["promotion"]

        obj, created = CustomerPromotion.objects.get_or_create(
            customer=customer, promotion=promotion
        )

        if not created:
            return Response(
                {"detail": "Promotion already assigned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
