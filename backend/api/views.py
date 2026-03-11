# Django
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

# DRF
from rest_framework import mixins, status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

# Serializers
from .serializers.empty import EmptySerializer
from .serializers.user_role import UserRoleSerializer
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
from .filters.inventory_movements import InventoryMovementFilter
from .filters.customer import CustomerFilter
from .filters.promotion import PromotionFilter
from .filters.customer_promotions import CustomerPromotionFilter

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

# Variables globales
LOW_STOCK_THRESHOLD = 5


def healthcheck(request):
    """
    Vista para mostrar el estado correcto de la API
    """
    return JsonResponse({"health": "ok"}, status=200)


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by("name")
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "description"]
    http_method_names = ["get", "post", "patch", "delete"]


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.filter(deleted_at__isnull=True)
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated, CanCreateUsers]
    throttle_classes = [UserRateThrottle]


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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "description"]
    http_method_names = ["get", "post", "patch", "delete"]

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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("name")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        "category",
        "state",
    ]

    search_fields = [
        "name",
        "description",
    ]
    http_method_names = ["get", "post", "patch", "delete"]

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


class InventoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Inventory.objects.select_related("product").all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["product"]
    search_fields = ["product__name"]

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


class InventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = InventoryMovement.objects.all().order_by("-created_at")
    serializer_class = InventoryMovementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = InventoryMovementFilter
    http_method_names = ["get"]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerFilter
    http_method_names = ["get", "post", "patch", "delete"]

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


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PromotionFilter
    http_method_names = ["get", "post", "patch", "delete"]


class CustomerPromotionViewSet(viewsets.ModelViewSet):
    queryset = CustomerPromotion.objects.select_related(
        "customer",
        "promotion",
    ).all()
    serializer_class = CustomerPromotionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerPromotionFilter
    http_method_names = ["get", "post", "patch", "delete"]

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
