from common.common_serilizer_imports import *

from shared.serializers import AddressSerializer
from lead.models import LeadSource, LeadStatus, Lead

class LeadSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model   = LeadSource
        exclude = ['created_at', 'updated_at']


class LeadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model   = LeadStatus
        exclude = ['created_at', 'updated_at']


class LeadSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)

    class Meta:
        model   = Lead
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        address = validated_data.pop('address')
        lead = Lead.objects.create(**validated_data)
        if address is not None:
            lead.addresses.create(**address)

        return lead

    def update(self, instance, validated_data):
        address = validated_data.pop('address', None)
        # update address
        if address is not None:
            nested_serializer = self.fields['address']
            nested_instance = instance.address
            nested_serializer.update(nested_instance, address)

        return super().update(instance, validated_data)
