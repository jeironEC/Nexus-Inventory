from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from nexus_inventory_backend.db.models import Role, User

from api.serializers.user_role import RoleSerializer
from api.serializers.user_read import UserReadSerializer
from api.serializers.user_create import UserCreateSerializer
from api.serializers.user_update import UserUpdateSerializer

from api.filters.user_role import RoleAdminFilter, RoleFilter
from api.filters.user import UserAdminFilter, UserFilter
from api.permissions import CanCreateUsers
from api.mixins.filter import StrictFilterMixin
from api.mixins.noput import NoPutMixin
from api.mixins.role_filter import RoleFilterMixin
from api.mixins.soft_delete_queryset import SoftDeleteQuerysetMixin
from api.mixins.audit_fields import AuditUserMixin
from api.mixins.is_active import StateMixin


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
    retrieve=extend_schema(tags=["Users"], summary="Get user"),
    partial_update=extend_schema(tags=["Users"], summary="Partial update user"),
    activate=extend_schema(tags=["Users"], summary="Activate user"),
    deactivate=extend_schema(tags=["Users"], summary="Deactivate user"),
)
class UserViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    AuditUserMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
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
        elif self.action == "partial_update":
            return UserUpdateSerializer
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
