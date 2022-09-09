from rest_framework.permissions import BasePermission, SAFE_METHODS


class OnlyUserOrAdmin(BasePermission):
    """
    Only the user and admin users are permitted to make changes to the user object.
    Unauthorized users are granted read-only permissions.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj or request.user.is_staff

