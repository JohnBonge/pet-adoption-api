"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pets.views import PetViewSet
from adoptions.views import AdoptionRequestViewSet
from userz.views import RegisterView, LoginView, ProfileView, home

# JWT views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# DRF Router
router = DefaultRouter()
router.register(r"pets", PetViewSet, basename="pets")
router.register(r"adoptions", AdoptionRequestViewSet, basename="adoptions")

urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API routes
    path("api/", include(router.urls)),

    # Root
    path("", home, name="home"),

    path("api/profile/", ProfileView.as_view(), name="profile"),
]