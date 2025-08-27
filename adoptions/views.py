from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from .models import AdoptionRequest
from .serializers import AdoptionRequestSerializer
from pets.models import Pet
from django.utils.timezone import now
# Create your views here.
class AdoptionRequestViewSet(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = AdoptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Shelter sees requests for their pets; adopter sees their own
        if user.is_shelter:
            return AdoptionRequest.objects.select_related("pet","user").filter(pet__shelter=user)
        return AdoptionRequest.objects.select_related("pet","user").filter(user=user)

    def perform_create(self, serializer):
        if self.request.user.is_shelter:
            raise PermissionError("Shelters cannot adopt pets.")
        pet = Pet.objects.get(pk=self.request.data.get("pet"))
        # Prevent self-applying by shelters (optional)
        serializer.save(user=self.request.user, pet=pet)

    def partial_update(self, request, *args, **kwargs):
        # Shelter updates status only if request belongs to their pet
        instance = self.get_object()
        if not request.user.is_shelter or instance.pet.shelter != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        status_val = request.data.get("status")
        if status_val not in ["Approved","Rejected","Pending"]:
            return Response({"detail":"Invalid status"}, status=400)
        instance.status = status_val
        instance.decision_at = now()
        instance.save()
        return Response(self.get_serializer(instance).data)