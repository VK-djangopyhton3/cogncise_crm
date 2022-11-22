from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.company.api.serializers import CompaniesSerializer
from apps.customer.models import CustomerInfo
from apps.users.models import UserRoles
from utils.dynamicfields import DynamicFieldsModelSerializer

User = get_user_model()


class UserSerializer(DynamicFieldsModelSerializer):
    userroles = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'password', 'userroles', 'customer', 'is_staff', 'is_active', 'is_verified']
        extra_kwargs = {'password': {'write_only': True}}

    def get_company(self, obj):
        user = UserRoles.objects.filter(user=obj)
        if not user.exists:
            return None
        return UserRolesSerializer(user, many=True, fields=['name', 'role', 'company']).data

    def get_customer(self, obj):
        user = CustomerInfo.objects.filter(customer=obj)
        if not user:
            return None
        user = user.first()
        customer = {
            "name": user.customer_name,
            "type": user.type,
        }
        if user.type == "business":
            customer["company_name"] = user.company_name
            customer["company_ABN"] = user.company_ABN
        return customer

    def create(self, validated_data):
        user = User(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserRolesSerializer(DynamicFieldsModelSerializer):
    user = UserSerializer(many=False, read_only=True,
                          fields=['id', 'email', 'phone', 'is_active', 'is_verified', 'is_staff'])
    company = CompaniesSerializer(many=False, read_only=True)

    class Meta:
        model = UserRoles
        fields = ['user', 'name', 'company', 'role']
