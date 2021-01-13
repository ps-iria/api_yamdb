from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Проверка что пользователь является админом"""

    def has_permission(self, request, view):
        if (request.user.is_staff or
                request.user.is_superuser or
                request.user.is_admin):
            return True
        return False


class IsOwnerOrReadOnly(BasePermission):
  

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user