from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    my_safe_method = ['GET', 'PUT', 'POST', 'DELETE']

    def has_permission(self, request, view):
        # print(request.user.)
        user_role = request.user.userroles.role
        if request.method in self.my_safe_method:
            return user_role == 'admin'

class IsStaffAdmin(BasePermission):
    my_safe_method = ['GET', 'PUT', 'POST', 'DELETE']

    def has_permission(self, request, view):
        if request.method in self.my_safe_method:
            return request.is_staff

