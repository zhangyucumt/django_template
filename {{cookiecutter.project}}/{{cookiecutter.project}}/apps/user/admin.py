from django.contrib import admin

from {{cookiecutter.project}}.apps.user import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'nickname')

    def user_id(self, obj):
        return obj.user.id

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

@admin.register(models.UserOpenid)
class UserOpenidAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'openid_type', 'openid_id')

    def user_id(self, obj):
        return obj.user.id
