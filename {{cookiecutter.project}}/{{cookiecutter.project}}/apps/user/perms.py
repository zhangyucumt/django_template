from rest_framework.permissions import BasePermission


class UserViewPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action in ('login', 'logout'):
            return True
        else:
            return request.user and request.user.is_authenticated

