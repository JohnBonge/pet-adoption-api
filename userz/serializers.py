from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ("username","email","password","is_shelter","location", "phone_number", "is_email_verified")
        read_only_fields = ("is_email_verified",)

    def create(self, validated_data):
        pwd = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(pwd)
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField()


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.UUIDField()