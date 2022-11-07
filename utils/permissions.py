from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    my_safe_method = ['GET', 'PUT', 'POST', 'DELETE']

    def has_permission(self, request, view):
        user_role = request.user.userroles.role
        if request.method in self.my_safe_method:
            return user_role == 'admin'


class IsStaff(BasePermission):
    my_safe_method = ['GET', 'PUT', 'POST', 'DELETE']

    def has_permission(self, request, view):
        if request.method in self.my_safe_method:
            return request.user.is_staff


class IsManager(BasePermission):
    my_safe_method = ['GET', 'PUT', 'POST', 'DELETE']

    def has_permission(self, request, view):
        user_role = request.user.userroles.role
        if request.method in self.my_safe_method:
            return user_role == 'admin' or user_role == 'manager'
