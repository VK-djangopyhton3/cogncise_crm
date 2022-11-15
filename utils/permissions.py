from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission

from apps.users.models import StaffAssociation


class IsAdmin(BasePermission):
    my_safe_method = ['GET', 'PUT', 'POST', 'DELETE']

    def has_permission(self, request, view):
        user_role = request.user.userroles.role
        if request.method in self.my_safe_method:
            return user_role == 'admin'


class IsStaff(BasePermission):
    my_safe_method = ['GET', 'PUT', 'POST', 'DELETE']

    def has_permission(self, request, view):
        if request.method in ['PUT','POST','DELETE']:
            company = request.data['company_id']
        else:
            company = request.GET['company_id']
        if not StaffAssociation.objects.filter(user=request.user,company__id=company).exists() or request.user.is_admin:
            return False
        if request.method in self.my_safe_method:
            return request.user.is_staff


class IsManager(BasePermission):
    my_safe_method = ['GET', 'PUT', 'POST', 'DELETE']

    def has_permission(self, request, view):
        user_role = request.user.userroles.role
        if request.method in self.my_safe_method:
            return user_role == 'admin' or user_role == 'manager'
