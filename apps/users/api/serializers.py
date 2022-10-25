from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.company.api.serializers import CompaniesSerializer
from apps.users.models import UserRoles
from utils.dynamicfields import DynamicFieldsModelSerializer

User = get_user_model()


class UserSerializer(DynamicFieldsModelSerializer):
    company = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'company', 'role', 'is_staff', 'is_active', 'is_verified']

    def get_company(self, obj):
        return obj.userroles.companies.company_name

    def get_role(self, obj):
        return obj.userroles.role


class UserRolesSerializer(DynamicFieldsModelSerializer):
    user = UserSerializer(many=False, read_only=True,
                          fields=['id', 'name', 'email', 'phone', 'is_active', 'is_verified', 'is_staff'])
    company = CompaniesSerializer(many=False, read_only=False)

    class Meta:
        model = UserRoles
        fields = ['user', 'company', 'role']
