# Django
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend

# Rest framework
from rest_framework import mixins, status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated

# Serializers
from .serializers.user_role import UserRoleSerializer
from .serializers.user_read import UserReadSerializer
from .serializers.user_create import UserCreateSerializer
from .serializers.user_update import UserUpdateSerializer
from .serializers.token_pair import EmailTokenObtainPairSerializer
from .serializers.category import CategorySerializer
from .serializers.product import ProductSerializer

# Models
from nexus_inventory_backend.db.models import Role, User, Category, Product

# Permissions
from .permissions import CanCreateUsers

# Rest framework
from rest_framework_simplejwt.views import TokenObtainPairView

# Enums
from nexus_inventory_backend.db.enums import State


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
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated, CanCreateUsers]
    throttle_classes = [UserRateThrottle]
    queryset = User.objects.filter(deleted_at__isnull=True)


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

    @action(detail=True, methods=["patch"], serializer_class=None)
    def activate(self, request, pk=None):
        category = self.get_object()
        category.state = State.ACTIVE
        category.save()

        return Response(
            {"id": category.id, "state": category.state}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["patch"], serializer_class=None)
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

    @action(detail=True, methods=["patch"], serializer_class=None)
    def activate(self, request, pk=None):
        product = self.get_object()
        product.state = State.ACTIVE
        product.save()

        return Response(
            {"id": product.id, "state": product.state}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["patch"], serializer_class=None)
    def deactivate(self, request, pk=None):
        product = self.get_object()
        product.state = State.INACTIVE
        product.save()

        return Response(
            {"id": product.id, "state": product.state}, status=status.HTTP_200_OK
        )
