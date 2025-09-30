# Almacen/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    GET/HEAD/OPTIONS: requiere estar autenticado.
    POST/PUT/PATCH/DELETE: solo admin (is_superuser).
    """
    def has_permission(self, request, view):
        user = request.user
        if request.method in SAFE_METHODS:
            return bool(user and user.is_authenticated)
        return bool(user and user.is_authenticated and user.is_superuser)
