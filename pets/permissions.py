from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsShelter(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_shelter)

class IsShelterOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_shelter and obj.shelter == request.user)