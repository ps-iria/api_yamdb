from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Проверка что пользователь является админом"""

    def has_permission(self, request, view):
        if (request.user.is_staff or
                request.user.is_superuser or
                request.user.is_admin):
            return True
        return False