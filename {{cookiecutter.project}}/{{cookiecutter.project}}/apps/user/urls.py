from {{cookiecutter.project}}.apps.user import views
from rest_framework import routers
from django.conf.urls import url, include

router_v1 = routers.SimpleRouter()
router_v1.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'', include((router_v1.urls, "user"), namespace='v1')),
]
