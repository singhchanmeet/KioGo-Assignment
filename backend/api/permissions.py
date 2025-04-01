
from rest_framework import permissions

class IsAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        return request.user is not None and hasattr(request.user, 'id')