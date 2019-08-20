from {{cookiecutter.project}}.apps.user import views
from rest_framework import routers
from django.conf.urls import url, include

router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls))
]
