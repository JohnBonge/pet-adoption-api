from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, permissions
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework.exceptions import PermissionDenied
from .models import Pet
from .serializers import PetSerializer
from .permissions import IsShelterOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class IsShelterUser(BasePermission):
    """Custom permission: only authenticated shelter users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "is_shelter", False)


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["type", "breed", "age", "shelter__location"]
    search_fields = ["name", "breed", "type"]
    ordering_fields = ["created_at", "age"]

    def get_queryset(self):
        # Short-circuit for Swagger schema generation
        if getattr(self, "swagger_fake_view", False):
            return Pet.objects.none()

        user = self.request.user
        if getattr(user, "is_authenticated", False) and getattr(user, "is_shelter", False):
            # Shelter sees only their own pets
            return Pet.objects.filter(shelter=user)
        # Non-shelter users or anonymous users see all pets
        return Pet.objects.all()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsShelterOwnerOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user
        if not getattr(user, "is_shelter", False):
            raise PermissionDenied("Only shelter users can add pets.")
        serializer.save(shelter=user)