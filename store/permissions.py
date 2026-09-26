from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access for any user,
    but write operations (POST, PUT, PATCH, DELETE) only for admin/staff users.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsOrderOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow users to access only their own orders.
    Staff/admins can access any order.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user
