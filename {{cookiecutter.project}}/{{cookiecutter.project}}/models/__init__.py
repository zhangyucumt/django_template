from functools import partial
from django.db import models
from {{cookiecutter.project}}.utils import SimpleAesEncryption


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name="创建时间", auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name="更新时间", auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True


ForeignKey = partial(models.ForeignKey, db_constraint=False)
OneToOneField = partial(models.OneToOneField, db_constraint=False)
ManyToManyField = partial(models.ManyToManyField, db_constraint=False)


class PasswordField(models.CharField):
    def to_python(self, value):
        value = super(PasswordField, self).to_python(value)
        return SimpleAesEncryption().decrypt(value)

    def get_prep_value(self, value):
        value = super(PasswordField, self).get_prep_value(value)
        return SimpleAesEncryption().encrypt(value)
