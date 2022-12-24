from common.common_serilizer_imports import *
from rest_flex_fields import FlexFieldsModelSerializer
from shared.serializers import AddressSerializer, CompanyMixin
from appointment.models import WorkType, Appointment, TimeSlots
from job.serializers import JobSerializer

class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deleted_at', 'is_deleted']


class AppointmentSerializer(CompanyMixin, FlexFieldsModelSerializer):
    class Meta:
        model = Appointment
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deleted_at', 'is_deleted']
    
    def create(self, validated_data):
        validated_data.update(company=self.company) 
        appointment = Appointment.objects.create(**validated_data)
        return appointment
    
        expandable_fields = {
            'job': (JobSerializer, {'many': False, 'read_only': True}),
            'work_type':(WorkTypeSerializer, {'many': False, 'read_only': True})
            }

class TimeSlotsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = TimeSlots
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deleted_at', 'is_deleted']


# class ScheduleAppointmentSerializer(serializers.ModelSerializer):
#     time_slots = TimeSlotsSerializer(many=True)

#     class Meta:
#         model = ScheduleAppointment
#         exclude = ['created_at', 'updated_at']
#         read_only_fields = ['deleted_at', 'is_deleted']

#     def create(self, validated_data):
#         time_slots = validated_data.pop('time_slots')
#         schedule_appointment = ScheduleAppointment.objects.create(**validated_data)
#         for data in time_slots:
#             TimeSlots.objects.create(schedule_appointment=schedule_appointment, **data)

#         return schedule_appointment

#     def update(self, instance, validated_data):
#         time_slots = validated_data.pop('time_slots', None)
#         # update time slots
#         if time_slots is not None:
#             for time_slot in time_slots:
#                 time_slot_id = time_slot.get('id')
#                 if time_slot_id is not None:
#                     TimeSlots.objects.filter(id=time_slot_id).update(**time_slot)
#                 else:
#                     TimeSlots.objects.create(schedule_appointment=instance, **time_slot)

#         return super().update(instance, validated_data)
