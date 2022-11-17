from rest_framework.permissions import BasePermission

from apps.users.models import StaffAssociate


class IsAdmin(BasePermission):
    my_safe_method = ['GET', 'PUT', 'POST', 'DELETE']

    def has_permission(self, request, view):

        if not request.user.is_staff:
            user_role = request.user.userroles.role
            if request.method in self.my_safe_method:
                return user_role == 'admin'

        if request.method in ['PUT', 'POST', 'DELETE']:
            company = request.data['company_id']
        else:
            company = request.GET['company_id']

        if StaffAssociate.objects.filter(user=request.user, company__id=company).exists() or request.user.is_superuser:
            return request.user.is_verified


class IsStaff(BasePermission):
    my_safe_method = ['GET', 'PUT', 'POST', 'DELETE']

    def has_permission(self, request, view):
        print("staff")
        if request.method in ['PUT', 'POST', 'DELETE']:
            company = request.data['company_id']
        else:
            company = request.GET['company_id']
        if not StaffAssociate.objects.filter(user=request.user,
                                             company__id=company).exists() and not request.user.is_superuser:
            return False

        if request.method in self.my_safe_method:
            return request.user.is_staff


class IsSuper(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsManager(BasePermission):
    my_safe_method = ['GET', 'PUT', 'POST', 'DELETE']

    def has_permission(self, request, view):
        if request.method in ['PUT', 'POST', 'DELETE']:
            company = request.data['company_id']
        else:
            company = request.GET['company_id']

        if StaffAssociate.objects.filter(user=request.user, company__id=company).exists() or request.user.is_superuser:
            return request.user.is_verified

        if request.method in self.my_safe_method and request.user.is_verified and not request.user.is_staff:
            user_role = request.user.userroles.role
            return user_role == 'admin' or user_role == 'manager'
