from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model


class UserModelSerializer(ModelSerializer):
    phone = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = "__all__"


class UserBaseLoginSerializer(Serializer):
    username = serializers.CharField(max_length=254, required=True, help_text='账号')
    password = serializers.CharField(help_text='密码')

