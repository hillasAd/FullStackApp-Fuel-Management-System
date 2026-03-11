from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    message = "Apenas gestores podem realizar esta acção."

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == "MANAGER")
        

class IsOperator(BasePermission):
    message = "Apenas Operadores podem realizar esta acção."
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == "OPERATOR")
