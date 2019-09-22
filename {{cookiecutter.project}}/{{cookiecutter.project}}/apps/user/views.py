import logging

from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse

from {{cookiecutter.project}}.apps.user.models import Profile
from {{cookiecutter.project}}.apps.user import serializers
from {{cookiecutter.project}}.apps.user.perms import MyPermission
from {{cookiecutter.project}}.exception import raise_invalid_param, BaseApiException, ValidationError, ErrorCode
from {{cookiecutter.project}}.apps.user.filters import UserFilter
from {{cookiecutter.project}}.decorators import parse_request_with, allows_filters

logger = logging.getLogger(__name__)


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserModelSerializer
    # permission_classes = [IsAuthenticated, ]
    queryset = get_user_model().objects.all()
    filterset_class = UserFilter
    search_fields = ('username', )
    ordering = 'pk'

    @action(detail=False, methods=['POST'])
    @parse_request_with(serializers.UserBaseSerializer)
    def test(self, request, *args, **kwargs):
        return Response(kwargs)

    @action(detail=False)
    @allows_filters
    def statistics(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_name='user_new')
    def new(self, request, pk=None):
        """
        aaa
        :param request:
        :param pk:
        :return:
        """
        obj = self.get_object()
        raise ValidationError

    @new.mapping.delete
    def delete_new(self, request, pk=None):
        raise_invalid_param()

