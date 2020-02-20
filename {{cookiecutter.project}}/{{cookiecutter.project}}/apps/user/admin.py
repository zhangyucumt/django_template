from django.contrib import admin
from django.contrib.auth import get_user_model, models as auth_models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.unregister(auth_models.Group)


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    pass
