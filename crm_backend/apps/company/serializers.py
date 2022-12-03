from common.common_serilizer_imports import *

from core.models import User
from core.serializers import UserSerializer
from shared.serializers import AddressSerializer
from company.models import Company

class OwnerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'mobile_number', 'is_company', 'role']

class CompanySerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)
    owner   = OwnerSerializer(many=False)

    class Meta:
        model   = Company
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        address = validated_data.pop('address')
        owner_data = validated_data.pop('owner')
        owner = User.create_company_admin(**owner_data)
        validated_data.update({'owner': owner })
        company = Company.objects.create(**validated_data)
        if address is not None:
            company.addresses.create(**address)

        return company

    def update(self, instance, validated_data):
        address = validated_data.pop('address', None)
        owner = validated_data.pop('owner', None)
        # update owner
        if owner is not None:
            nested_serializer = self.fields['owner']
            nested_instance = instance.owner
            nested_serializer.update(nested_instance, owner)
        # update address
        if address is not None:
            nested_serializer = self.fields['address']
            nested_instance = instance.address
            nested_serializer.update(nested_instance, address)

        return super().update(instance, validated_data)
