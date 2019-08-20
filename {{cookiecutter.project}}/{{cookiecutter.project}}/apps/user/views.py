from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
import logging
from {{cookiecutter.project}}.apps.user.models import Profile
from {{cookiecutter.project}}.apps.user import serializers as serializer
from rest_framework.decorators import list_route
from rest_framework.response import Response

from {{cookiecutter.project}}.exception import raise_invalid_param, BaseApiException, ValidationError, ErrorCode

logger = logging.getLogger('django.server')

class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializer.UserModelSerializer

    @list_route(methods=['post'])
    def new(self, request):
        data = request.data
        return Response(data)

