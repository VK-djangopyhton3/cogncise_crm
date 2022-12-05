from common.common_serilizer_imports import *
from django.contrib.auth import get_user_model
from rest_flex_fields import FlexFieldsModelSerializer

from shared.serializers import AddressSerializer
from lead.models import LeadSource, LeadStatus, Lead
from company.serializers import OwnerSerializer

user = get_user_model()

class LeadSerializer(FlexFieldsModelSerializer):
    address = AddressSerializer(many=False)
    # owner = OwnerSerializer(many=False)

    class Meta:
        model   = Lead
        fields = "__all__"
    
        expandable_fields = {
            'owner': (OwnerSerializer, {'read_only': True})
            }

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


class LeadSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model   = LeadSource
        exclude = ['created_at', 'updated_at']


class LeadStatusSerializer(FlexFieldsModelSerializer):
    class Meta:
        model   = LeadStatus
        exclude = ['created_at', 'updated_at']
        expandable_fields = {
          'leads': (LeadSerializer, {'many': True, 'read_only': True, 'source': 'lead_status'})
        }
