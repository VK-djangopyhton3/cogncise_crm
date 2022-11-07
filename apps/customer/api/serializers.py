from apps.company.api.serializers import CompaniesSerializer
from apps.customer.models import CustomerInfo
from apps.users.api.serializers import UserSerializer
from utils.dynamicfields import DynamicFieldsModelSerializer


class CustomerInfoSerializer(DynamicFieldsModelSerializer):
    customer = UserSerializer(read_only=True, many=False, fields=['id', 'name', 'email', 'phone'])


    class Meta:
        model = CustomerInfo
        fields = ['id', 'customer', 'type', 'sms_consent', 'updated_on']
