from rest_framework import permissions


class CustomUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.id == request.user
            or request.user.is_staff
            or request.user.is_superuser
        )
