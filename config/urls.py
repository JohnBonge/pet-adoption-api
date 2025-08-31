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
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions

# Views
from pets.views import PetViewSet
from adoptions.views import AdoptionRequestViewSet
from userz.views import RegisterView, LoginView, ProfileView, home, ChangePasswordView, ResetPasswordRequestView, ResetPasswordConfirmView, VerifyEmailView

# JWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# DRF Router
router = DefaultRouter()
router.register(r"pets", PetViewSet, basename="pets")
router.register(r"adoptions", AdoptionRequestViewSet, basename="adoptions")

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Pet Adoption API",
        default_version='v1',
        description="API documentation for Pet Adoption API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Authentication
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Django’s auth views
    path('accounts/', include('django.contrib.auth.urls')),

    # API
    path("api/", include(router.urls)),

    # Profile
    path("api/profile/", ProfileView.as_view(), name="profile"),

    # Root
    path("", home, name="home"),

    # Swagger / OpenAPI
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Password & email verification
    path("api/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("api/reset-password/request/", ResetPasswordRequestView.as_view(), name="reset-password-request"),
    path("api/reset-password/confirm/", ResetPasswordConfirmView.as_view(), name="reset-password-confirm"),
    path("api/verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]