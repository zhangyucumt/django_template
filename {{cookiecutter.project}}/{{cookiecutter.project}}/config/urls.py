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
from django.conf import settings


admin.site.site_title = '后台管理系统'
admin.site.site_header = '后台管理系统'
admin.site.index_title = '后台管理系统'


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'user/', include('{{cookiecutter.project}}.apps.user.urls')),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path(r'oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]


if settings.DEBUG:
    from rest_framework_swagger.views import get_swagger_view
    schema_view = get_swagger_view(title='API DOC')
    urlpatterns.append(path(r'apidocs/', schema_view))
