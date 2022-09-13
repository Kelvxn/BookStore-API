from rest_framework.permissions import BasePermission, SAFE_METHODS


class OnlyUser(BasePermission):
    """
    Only the user is permitted to make changes to the user object.
    Unauthorized users are granted read-only permissions.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj
