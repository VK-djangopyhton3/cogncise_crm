from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    my_safe_method = ['GET', 'PUT', 'POST', 'DELETE']

    def has_permission(self, request, view):

        user_role = request.data.company.role  # taking token
        if request.method in self.my_safe_method:
            return user_role == 'admin'
