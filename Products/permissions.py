from rest_framework import permissions


class BuyerPermission(permissions.BasePermission):
    """
    Custom permission to allow buyers read-only access to product lists.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class AdminPermission(permissions.BasePermission):
    """
    Custom permission to allow admins full access to product CRUD operations.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_admin
