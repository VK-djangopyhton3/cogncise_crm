from common.common_serilizer_imports import *

from appointment.models import Appointment, SechduleAppointment, TimeSlots

# Appointment Serializer
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        exclude = ['created_at', 'updated_at']

class TimeSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlots
        exclude = ['created_at', 'updated_at']


class SechduleAppointmentSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotsSerializer()

    class Meta:
        model = SechduleAppointment
        exclude = ['created_at', 'updated_at']

    # def create(self, validated_data):
    #     business_address = validated_data.pop('business_address')
    #     property_address = validated_data.pop('property_address')
    #     SechduleAppointment = SechduleAppointment.objects.create(**validated_data)
    #     if business_address:
    #         business_address.update({ 'purpose': 'business' })
    #         SechduleAppointment.addresses.create(**business_address)
    #     if property_address:
    #         property_address.update({ 'purpose': 'property' })
    #         SechduleAppointment.addresses.create(**property_address)

    #     return SechduleAppointment

    # def update(self, instance, validated_data):
    #     business_address = validated_data.pop('business_address', None)
    #     property_address = validated_data.pop('property_address', None)
    #     # update business address
    #     if business_address is not None:
    #         nested_serializer = self.fields['business_address']
    #         nested_instance = instance.business_address
    #         nested_serializer.update(nested_instance, business_address)
    #     # update property address
    #     if property_address is not None:
    #         nested_serializer = self.fields['property_address']
    #         nested_instance = instance.property_address
    #         nested_serializer.update(nested_instance, property_address)

    #     return super().update(instance, validated_data)