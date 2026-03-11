from rest_framework.permissions import BasePermission
from shared.exceptions.custom_exceptions import PermissionDeniedException

class IsAdminRole(BasePermission):
    message = "Acesso restrito a administradores."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')
