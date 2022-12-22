from common.common_serilizer_imports import *

from appointment.models import WorkType, Appointment, ScheduleAppointment, TimeSlots

class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deleted_at', 'is_deleted']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deleted_at', 'is_deleted']

class TimeSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlots
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deleted_at', 'is_deleted']


class scheduleAppointmentSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotsSerializer(many=True)

    class Meta:
        model = ScheduleAppointment
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deleted_at', 'is_deleted']

    def create(self, validated_data):
        time_slots = validated_data.pop('time_slots')
        time_slots_serializer = self.fields.pop('time_slots')
        schedule_appointment = ScheduleAppointment.objects.create(**validated_data)
        for data in time_slots:
            TimeSlots.objects.create(schedule_appointment=schedule_appointment, **data)

        return schedule_appointment

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