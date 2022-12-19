from common.common_serilizer_imports import *
from rest_flex_fields import FlexFieldsModelSerializer

from core.models import User
from shared.serializers import AddressSerializer
from company.models import CompanyStatus, Company

class OwnerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'mobile_number', 'is_company', 'is_cogncise', 'role']
        read_only_fields = ['deleted_at', 'is_deleted']


class CompanyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model   = CompanyStatus
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deleted_at', 'is_deleted']


class CompanySerializer(FlexFieldsModelSerializer):
    address = AddressSerializer(many=False, allow_null=True, required=False)
    owner   = OwnerSerializer(many=False, required = False)

    class Meta:
        model   = Company
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deleted_at', 'is_deleted']
        expandable_fields = {
            'status': (CompanyStatusSerializer, {'many': False, 'read_only': True})
        }

    def create(self, validated_data):
        address = validated_data.pop('address')
        owner_data = validated_data.pop('owner')
        company = None
        if owner_data is not None:
            owner = User.create_company_admin(**owner_data)
            company = Company.objects.create(owner=owner, **validated_data)
            owner.company = company
            owner.save()
        if address is not None:
            company.addresses.create(**address) # type: ignore

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
