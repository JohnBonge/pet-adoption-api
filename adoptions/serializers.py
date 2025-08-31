from rest_framework import serializers
from .models import AdoptionRequest

class AdoptionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionRequest
        fields = "__all__"
        read_only_fields = ['adopter', 'status', 'created_at']