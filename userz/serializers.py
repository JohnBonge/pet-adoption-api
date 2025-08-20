from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ("username","email","password","is_shelter","location")

    def create(self, validated_data):
        pwd = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(pwd)
        user.save()
        return user