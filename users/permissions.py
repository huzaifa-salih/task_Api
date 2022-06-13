from rest_framework import permissions


class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    """
    Custom permissions for userViewset to only allow user edit their own USER Ptherwis, get and POST only
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_anonymous:
            return request.user == obj

        return False


class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permissions for userViewset to only allow user edit their own PROFILE Ptherwis, get and POST only
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return request.user == obj
        return False
