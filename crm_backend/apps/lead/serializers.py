from common.common_serilizer_imports import *
from rest_flex_fields import FlexFieldsModelSerializer

from shared.serializers import AddressSerializer, CompanyMixin
from lead.models import LeadSource, LeadStatus, Lead
from company.serializers import OwnerSerializer

class LeadSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model   = LeadSource
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deleted_at', 'is_deleted']


class ILeadStatusSerializer(FlexFieldsModelSerializer):
    class Meta:
        model   = LeadStatus
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deleted_at', 'is_deleted']


class LeadSerializer(CompanyMixin, FlexFieldsModelSerializer):
    address = AddressSerializer(many=False)
    owner   = OwnerSerializer(read_only=True)

    class Meta:
        model = Lead
        fields = "__all__"
        read_only_fields = ['deleted_at', 'is_deleted']
        expandable_fields = {
          'status': (ILeadStatusSerializer, {'many': False, 'read_only': True}),
          'source': (LeadSourceSerializer, {'many': False, 'read_only': True})
        }

    def create(self, validated_data):
        address = validated_data.pop('address')
        lead = Lead.objects.create(company=self.company, owner=self.request_user, **validated_data)
        # create address
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


class LeadStatusSerializer(FlexFieldsModelSerializer):
    class Meta:
        model   = LeadStatus
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deleted_at', 'is_deleted']
        expandable_fields = {
          'leads': (LeadSerializer, {'many': True, 'read_only': True, 'source': 'lead_status'})
        }
