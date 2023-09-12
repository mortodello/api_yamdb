from rest_framework import permissions
from users_yamdb.models import ADMIN, MODERATOR


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_superuser
                or (request.user.is_authenticated
                    and request.user.role == ADMIN))


class IsAdminOrReadOnly(IsAdmin):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.role == ADMIN
        )


class IsAuthorAdminModeratorOrReadOnly(IsAdminOrReadOnly):
    # этот метод необходим, анонимы - только смотреть,
    # зарегистрированные - смотреть и постить
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            super().has_object_permission(request, view, obj)
            or request.user.role == MODERATOR
            or obj.author == request.user
        )
