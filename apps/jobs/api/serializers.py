from apps.customer.api.serializers import CustomerInfoSerializer
from apps.jobs.models import WorkType, Jobs
from apps.properties.api.serializer import PropertySerializer
from apps.users.api.serializers import UserSerializer, UserRolesSerializer
from utils.dynamicfields import DynamicFieldsModelSerializer


class WorkTypeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = WorkType
        fields = ['id', 'work_type', 'is_active']


class JobSerializer(DynamicFieldsModelSerializer):
    customer = CustomerInfoSerializer(read_only=True, many=False)
    property_address = PropertySerializer(read_only=True, many=False)
    agent = UserRolesSerializer(read_only=True, many=False)

    class Meta:
        model = Jobs
        fields = ['id', 'customer', 'agent', 'property_address', 'job_status', 'created_on', 'updated_on']

