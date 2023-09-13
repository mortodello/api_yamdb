from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_superuser
                or (request.user.is_authenticated
                    and request.user.is_admin))


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
            or request.user.is_admin
        )


class IsAuthorAdminModeratorOrReadOnly(IsAuthenticatedOrReadOnly,
                                       IsAdminOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (
            super().has_object_permission(request, view, obj)
            or request.user.is_moderator
            or obj.author == request.user
        )
