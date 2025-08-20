from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import get_user_model
from userz.serializers import UserSerializer
from userz.models import CustomUser  # Assuming you have a CustomUser model defined
from django.http import HttpResponse

User = get_user_model()

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
def home(request):
    return HttpResponse("Welcome to Pet Adoption API!")