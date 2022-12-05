from common.common_serilizer_imports import *

from core.models import User
from core.serializers import UserSerializer
from shared.serializers import AddressSerializer
from customer.models import Customer
from company.serializers import OwnerSerializer


class CustomerSerializer(serializers.ModelSerializer):

    address = AddressSerializer(many=False)
    user = OwnerSerializer(many=False)

    class Meta:
        model   = Customer
        exclude = ['created_at', 'updated_at']
        depth = 1

    def create(self, validated_data):
        address = validated_data.pop('address')
        user = User.create_customer(**validated_data)
        customer = Customer.objects.create(user=user)
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
        if validated_data is not None:
            nested_serializer = self.fields['user']
            nested_instance = instance.user
            nested_serializer.update(nested_instance, validated_data)

        return super().update(instance, {})
