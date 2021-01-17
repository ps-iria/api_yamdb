from rest_framework.permissions import (
    BasePermission, 
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS
)

from .models import UserRoles


class IsAdmin(BasePermission):
    """Проверка что пользователь является админом"""

    def has_permission(self, request, view):
        if (request.user.is_staff or
                request.user.is_superuser or
                request.user.is_admin):
            return True
        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return(request.user.is_staff or request.user.role == 'admin')


class IsAdminOrModeratorOrOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return bool(
            obj.author == request.user
            or request.method in SAFE_METHODS
            or request.auth and request.user.role == UserRoles.ADMIN
            or request.auth and request.user.role == UserRoles.MODERATOR
        )
        