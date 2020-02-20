import logging

from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from {{cookiecutter.project}}.apps.user import serializers, perms, handler
from {{cookiecutter.project}}.exception import ValidationError, AuthenticationFailed

from {{cookiecutter.project}}.decorators import parse_request_with


logger = logging.getLogger(__name__)


class UserViewSet(GenericViewSet):
    serializer_class = serializers.UserModelSerializer
    permission_classes = [perms.UserViewPermission, ]
    queryset = get_user_model().objects.filter(is_active=True)

    @action(detail=False, methods=['POST'])
    @parse_request_with(serializers.UserBaseLoginSerializer)
    def login(self, request, *args, validate_data, **kwargs):
        """登录"""
        user = authenticate(username=validate_data['username'], password=validate_data['password'])
        if user is not None:
            login(request, user)
            return Response(self.get_serializer(user, many=False).data)
        else:
            logout(request)
            raise AuthenticationFailed()

    @action(detail=False, methods=['GET'])
    def user_info(self, request, *args, **kwargs):
        """
        获取用户信息
        ```json
        {
          "id": 4, # id
          "username": "zhangsan", # 账号
          "name": "haoda",        # 用户名
          "phone": "17600719912", # 手机
          "email": "zhangyucumt@foxmail.com",  # 邮箱
          "avatar": "http://127.0.0.1:{{cookiecutter.port}}/media/user/avatars/%E4%B8%8B%E8%BD%BD_kyJzAAT.png"  # 头像
        }
        ```
        """
        user = request.user
        return Response(self.get_serializer(user, many=False).data)

    @action(detail=False, methods=['POST'])
    def logout(self, request, *args, **kwargs):
        """退出登录"""
        logout(request)
        return Response({})
