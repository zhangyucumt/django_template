from functools import partial
import json

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


class SecretField(models.CharField):
    def to_python(self, value):
        value = super(SecretField, self).to_python(value)
        return SimpleAesEncryption().decrypt(value)

    def get_prep_value(self, value):
        value = super(SecretField, self).get_prep_value(value)
        return SimpleAesEncryption().encrypt(value)


class ListField(models.CharField):

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if value is None:
            return []
        try:
            return json.loads(value)
        except Exception:
            return []

    def get_prep_value(self, value):
        return json.dumps(value)
