from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from .models import Pet
from .serializers import PetSerializer
from .permissions import IsShelter, IsShelterOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.filter(available=True).select_related("shelter")
    serializer_class = PetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["type","breed","age","shelter__location"]
    search_fields = ["name","breed","type"]
    ordering_fields = ["created_at","age"]

    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            return [AllowAny()]
        if self.action in ["create","update","partial_update","destroy"]:
            return [IsShelterOwnerOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        # shelter creating their own pet
        assert self.request.user.is_shelter, "Only shelters can create pets"
        serializer.save(shelter=self.request.user)