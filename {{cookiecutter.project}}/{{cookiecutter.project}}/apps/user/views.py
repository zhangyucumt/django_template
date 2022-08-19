import logging

from django.contrib.auth import get_user_model, authenticate, login, logout
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from {{cookiecutter.project}}.apps.user import serializers, perms, handler
from {{cookiecutter.project}}.exception import ValidationError, AuthenticationFailed


logger = logging.getLogger(__name__)


class UserViewSet(GenericViewSet):
    # serializer_class = serializers.UserModelSerializer
    permission_classes = [perms.UserViewPermission, ]
    queryset = get_user_model().objects.filter(is_active=True)
    pagination_class = None
    filter_backends = []

    def get_serializer_class(self):
        if self.action == "login":
            return serializers.UserBaseLoginSerializer
        elif self.action == "logout":
            return None
        else:
            return serializers.UserModelSerializer

    @action(detail=False, methods=['POST'])
    @swagger_auto_schema(responses={200: serializers.UserModelSerializer(many=False)})
    def login(self, request):
        """登录"""
        serializer = serializers.UserBaseLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
        if user is not None:
            login(request, user)
            return Response(serializers.UserModelSerializer(user, many=False).data)
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
          "avatar": "http://127.0.0.1:8061/media/user/avatars/%E4%B8%8B%E8%BD%BD_kyJzAAT.png"  # 头像
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
