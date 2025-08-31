from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from .models import AdoptionRequest
from .serializers import AdoptionRequestSerializer
from pets.models import Pet
from django.utils.timezone import now

class AdoptionRequestViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = AdoptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = AdoptionRequest.objects.all()  # Ensure queryset is defined

    def get_queryset(self):
        # Short-circuit for Swagger schema generation
        if getattr(self, "swagger_fake_view", False):
            return AdoptionRequest.objects.none()

        user = self.request.user
        if user.is_authenticated:
            # Shelter sees requests for their pets
            if getattr(user, "is_authenticated", False) and getattr(user, "is_shelter", False):
                return AdoptionRequest.objects.select_related("pet", "user").filter(pet__shelter=user)
            # Adopter sees their own requests
            return AdoptionRequest.objects.select_related("pet", "user").filter(user=user)
        return AdoptionRequest.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if getattr(user, "is_shelter", False):
            return Response({"detail": "Shelters cannot adopt pets."}, status=status.HTTP_403_FORBIDDEN)
        
        pet_id = self.request.data.get("pet")
        pet = get_object_or_404(Pet, pk=pet_id)
        serializer.save(user=user, pet=pet)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        # Only shelter can update status for their own pets
        if not getattr(user, "is_shelter", False) or instance.pet.shelter != user:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        status_val = request.data.get("status")
        if status_val not in ["Approved", "Rejected", "Pending"]:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = status_val
        instance.decision_at = now()
        instance.save()
        return Response(self.get_serializer(instance).data)