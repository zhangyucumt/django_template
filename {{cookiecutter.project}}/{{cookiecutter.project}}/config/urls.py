"""{{cookiecutter.project}} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view

schema_view = get_swagger_view(title='API DOC')

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'apidocs/', schema_view),
    path(r'user/', include('{{cookiecutter.project}}.apps.user.urls')),
    path(r'openapi/', get_schema_view(
        title="Your Project",
        description="API for all things …"
    ), name='openapi-schema'),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
