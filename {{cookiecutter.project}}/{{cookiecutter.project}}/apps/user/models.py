from django.db import models
from django.contrib.auth.models import AbstractUser
from {{cookiecutter.project}}.consts.user import Sex


class User(AbstractUser):
    username = models.CharField("账号", max_length=254, unique=True, error_messages={'unique': "用户名已存在"})
    email = models.EmailField(verbose_name="电子邮箱", blank=False, unique=True)
    phone = models.CharField(max_length=11, verbose_name="手机号", blank=False, unique=True)
    name = models.CharField(max_length=150, verbose_name="用户名")
    is_staff = models.BooleanField("管理员", default=False, help_text="是否可以登录管理站点")
    sex = models.IntegerField(choices=Sex.choices(), default=Sex.unknown, verbose_name="性别")
    avatar = models.ImageField(upload_to="user/avatars", null=True, blank=True, max_length=100, verbose_name="头像")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
