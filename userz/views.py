from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from userz.serializers import UserSerializer
from userz.models import CustomUser  # Assuming you have a CustomUser model defined
from django.http import HttpResponse
from django.core.mail import send_mail

from .serializers import (
    UserSerializer, ChangePasswordSerializer,
    ResetPasswordRequestSerializer, ResetPasswordConfirmSerializer,
    VerifyEmailSerializer
)

User = get_user_model()

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # Send verification email
        send_mail(
            subject="Verify your email",
            message=f"Use this token to verify: {user.email_verification_token}",
            from_email="noreply@petadoption.com",
            recipient_list=[user.email],
            fail_silently=True,
        )

class LoginView(APIView):
    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.validated_data["old_password"]):
            return Response({"detail": "Old password is incorrect"}, status=400)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"detail": "Password changed successfully"})


class ResetPasswordRequestView(APIView):
    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.validated_data["email"])
            # reuse email_verification_token for reset purpose
            send_mail(
                subject="Password reset",
                message=f"Use this token to reset password: {user.email_verification_token}",
                from_email="noreply@petadoption.com",
                recipient_list=[user.email],
                fail_silently=True,
            )
        except User.DoesNotExist:
            pass  # don't reveal email existence
        return Response({"detail": "If the email exists, a reset token has been sent"})


class ResetPasswordConfirmView(APIView):
    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email_verification_token=serializer.validated_data["token"])
            user.set_password(serializer.validated_data["new_password"])
            user.email_verification_token = None
            user.save()
            return Response({"detail": "Password reset successful"})
        except User.DoesNotExist:
            return Response({"detail": "Invalid token"}, status=400)


class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email_verification_token=serializer.validated_data["token"])
            user.mark_email_verified()
            return Response({"detail": "Email verified successfully"})
        except User.DoesNotExist:
            return Response({"detail": "Invalid token"}, status=400)


def home(request):
    return HttpResponse("Welcome to Pet Adoption API!")