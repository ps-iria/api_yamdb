<<<<<<< HEAD
from rest_framework.permissions import BasePermission
from rest_framework import permissions
=======
from rest_framework.permissions import (
    BasePermission, 
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS
)

from .models import UserRoles
>>>>>>> correcting and getting one review on title


class IsAdmin(BasePermission):
    """Проверка что пользователь является админом"""

    def has_permission(self, request, view):
        if (request.user.is_staff or
                request.user.is_superuser or
                request.user.is_admin):
            return True
        return False


<<<<<<< HEAD
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return(request.user.is_staff or request.user.role == 'admin')

=======
class IsAdminOrModeratorOrOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
  

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.author == request.user
            or request.method in SAFE_METHODS
            or request.auth and request.user.role == UserRoles.ADMIN
            or request.auth and request.user.role == UserRoles.MODERATOR
        )
>>>>>>> correcting and getting one review on title
