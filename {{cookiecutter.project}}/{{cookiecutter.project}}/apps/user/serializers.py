from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from django.contrib.auth import get_user_model


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class UserBaseSerializer(Serializer):
    username = serializers.CharField(max_length=20, required=False, help_text='用户名', label='uuuu')
    password = serializers.CharField(help_text='密码')
    email = serializers.EmailField(help_text="email")
