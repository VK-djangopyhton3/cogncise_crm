from common.common_serilizer_imports import *

from core.models import User
from shared.serializers import AddressSerializer, CompanyMixin

from customer.models import Customer

class CustomerSerializer(CompanyMixin, serializers.ModelSerializer):
    first_name    = serializers.CharField(required=True, max_length=100, source="user.first_name")
    last_name     = serializers.CharField(required=True, max_length=100, source="user.last_name")
    email         = serializers.EmailField(required=True, source="user.email")
    mobile_number = serializers.CharField(required=True, max_length=13, source="user.mobile_number")
    address       = AddressSerializer(many=False)

    class Meta:
        model   = Customer
        exclude = ['created_at', 'updated_at', 'user']
        read_only_fields = ['deleted_at', 'is_deleted']

    def create(self, validated_data):
        address = validated_data.pop('address')
        if self.company.owner is not None:
            owner = self.company.owner
            if owner.is_cogncise:
                validated_data['user'].update({ 'is_cogncise': True, 'company_id': self.company.id })
        user = User.create_customer(**validated_data)
        customer = Customer.objects.create(company=self.company, user=user)
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
        # update user
        if validated_data is not None:
            user_data = validated_data['user']
            User.objects.filter(id=instance.user_id).update(**user_data)

        return super().update(instance, {})

    def validate_email(self, value):
        if self.instance and User.objects.filter(email=value).exclude(id__in=[self.instance.user_id]).exists():
            raise serializers.ValidationError("This field must be unique.")

        if self.instance is None and User.objects.filter(email=value).exists():
                raise serializers.ValidationError("This field must be unique.")

        return value
