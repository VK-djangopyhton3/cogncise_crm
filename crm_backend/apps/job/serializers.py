from common.common_serilizer_imports import *

from core.serializers import AddressSerializer
from job.models import Job

# Job Serializer
class JobSerializer(serializers.ModelSerializer):
    business_address = AddressSerializer(many=False)
    property_address = AddressSerializer(many=False)

    class Meta:
        model = Job
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        business_address = validated_data.pop('business_address')
        property_address = validated_data.pop('property_address')
        job = Job.objects.create(**validated_data)
        if business_address:
            business_address.update({ 'purpose': 'business' })
            job.addresses.create(**business_address)
        if property_address:
            property_address.update({ 'purpose': 'property' })
            job.addresses.create(**property_address)

        return job

    def update(self, instance, validated_data):
        business_address = validated_data.pop('business_address', None)
        property_address = validated_data.pop('property_address', None)
        # update business address
        if business_address is not None:
            nested_serializer = self.fields['business_address']
            nested_instance = instance.business_address
            nested_serializer.update(nested_instance, business_address)
        # update property address
        if property_address is not None:
            nested_serializer = self.fields['property_address']
            nested_instance = instance.property_address
            nested_serializer.update(nested_instance, property_address)

        return super().update(instance, validated_data)
