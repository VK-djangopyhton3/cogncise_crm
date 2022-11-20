from rest_framework import serializers

from apps.customer.api.serializers import CustomerInfoSerializer
from apps.jobs.models import WorkType, Jobs, JobTransferHistory
from apps.properties.api.serializer import PropertySerializer
from apps.users.api.serializers import UserSerializer
from utils.dynamicfields import DynamicFieldsModelSerializer


class WorkTypeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = WorkType
        fields = ['id', 'work_type', 'is_active']


class JobSerializer(DynamicFieldsModelSerializer):
    customer = CustomerInfoSerializer(read_only=True, many=False)
    property_address = PropertySerializer(read_only=True, many=False)
    work_type = WorkTypeSerializer(read_only=True, many=False)
    agent = UserSerializer(read_only=True, many=False)
    agency_transfer_history = serializers.SerializerMethodField()

    class Meta:
        model = Jobs
        fields = ['id', 'customer', 'agent', 'property_address', 'work_type', 'job_status', 'created_on', 'updated_on',
                  'agency_transfer_history']

    def get_agency_transfer_history(self, obj):
        jt = JobTransferHistory.objects.filter(job=obj)
        return JobTransferHistorySerializer(jt, many=True).data

    # def save(self, request, obj, form, change):
    #     obj.save()
    #     form.save_m2m()
    #     # your custom stuff goes here
    #     if not obj.name:
    #         obj.name = obj.__str__()
    #         obj.save()


class JobTransferHistorySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = JobTransferHistory
        fields = ['job', 'agency', 'transfer_count', 'assigned_on', 'is_current_assignee']
