from rest_framework.permissions import BasePermission


class CanCreateUsers(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == "admin"
