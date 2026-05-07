"""
URL configuration for core project.
"""

from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Swagger imports
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


# ---------------- SWAGGER SETUP ---------------- #

schema_view = get_schema_view(
    openapi.Info(
        title="SubGuard API",
        default_version="v1",
        description="Subscription tracking, billing simulation, and risk analysis API",
        contact=openapi.Contact(email="support@subguard.local"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# ---------------- URLS ---------------- #

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API (versioned)
    path('api/v1/', include('apps.subscriptions.urls')),
    path('api/v1/users/', include('apps.users.urls')),

    # JWT auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger UI
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='swagger-ui'
    ),

    # Redoc UI
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='redoc'
    ),

    # DRF browsable API login (optional dev tool)
    path('api-auth/', include('rest_framework.urls')),
]