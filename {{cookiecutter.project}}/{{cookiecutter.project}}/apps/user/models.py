from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from {{cookiecutter.project}}.consts.user import Sex, OpenidType
from {{cookiecutter.project}}.models import BaseModel, OneToOneField, ForeignKey


class Profile(BaseModel):
    user = OneToOneField(get_user_model(), on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True, verbose_name="昵称")
    mobile = models.CharField(max_length=15, verbose_name="手机号", blank=True)
    real_name = models.CharField(max_length=150, blank=True, verbose_name="真实姓名")
    sex = models.IntegerField(choices=Sex.choices(), default=Sex.unknown, verbose_name="性别")
    country = models.CharField(max_length=50, blank=True, verbose_name="国家")
    province = models.CharField(max_length=50, blank=True, verbose_name="省份")
    city = models.CharField(max_length=50, blank=True, verbose_name="城市")
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")
    
    def __str__(self):
        return "%s-%s-%s" % (self.user.username, self.real_name, self.user.id)


@receiver(post_save, sender=get_user_model())
def save_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile()
        profile.user = kwargs['instance']
        profile.save()


class UserOpenid(BaseModel):
    user = ForeignKey(get_user_model(), on_delete=models.CASCADE)
    openid_id = models.CharField(max_length=512, verbose_name="OpenID")
    openid_type = models.IntegerField(choices=OpenidType.choices(), verbose_name="openid类型")
    is_valid = models.BooleanField(default=True, verbose_name="软删除标志")

    class Meta:
        unique_together = (('openid_type', 'openid_id'), )
