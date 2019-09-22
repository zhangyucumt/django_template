from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    message = 'Adding Customer not allowed'

    # def has_permission(self, request, view):
    #     print(dir(view))
    #     print(view.name)
    #     return False

    # def has_object_permission(self, request, view, obj):
    #     return False
