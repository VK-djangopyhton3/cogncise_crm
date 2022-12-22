from common.common_serilizer_imports import *

from core.models import User
from shared.serializers import AddressSerializer, CompanyMixin

from customer.models import Customer

class CustomerSerializer(CompanyMixin, serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])
    mobile_number = serializers.CharField(max_length=13)
    address = AddressSerializer(many=False)

    class Meta:
        model   = Customer
        exclude = ['created_at', 'updated_at', 'username', 'password', 'last_login', 'is_staff', 'is_active', 'date_joined', 'is_company', 'is_customer', 'is_cogncise', 'is_superuser', 'companies', 'user_permissions', 'groups']
        read_only_fields = ['deleted_at', 'is_deleted']

    def create(self, validated_data):
        address = validated_data.pop('address')
        customer = Customer.create_record(**validated_data)
        customer.companies.add(self.company)
        # create address
        if address is not None:
            customer.addresses.create(**address)

        return customer

    def update(self, instance, validated_data):
        address = validated_data.pop('address', None)
        # update address
        if address is not None:
            nested_serializer = self.fields['address']
            nested_instance = instance.address
            nested_serializer.update(nested_instance, address)

        return super().update(instance, validated_data)
