from rest_framework import serializers
from .models import Pet

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            "id", "name", "age", "breed", "type", "health_status", 
            "photo", "available", "shelter"
        ]
        read_only_fields = ("id", "shelter","created_at")