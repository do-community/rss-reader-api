"""rss_reader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as authviews
from rest_framework.schemas import get_schema_view
import os

urlpatterns = [
    path("admin", admin.site.urls),
    path("", include("rss.urls")),
    path(
        "login",
        authviews.obtain_auth_token,
        name="login",
    ),
    path(
        "openapi",
        get_schema_view(
            title="RSS Reader", description="API for RSS aggregation", version="1.0.0"
        ),
        name="openapi-schema",
    ),
]
