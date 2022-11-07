from apps.customer.api.serializers import CustomerInfoSerializer
from apps.properties.models import PropertyTypes, Property
from utils.dynamicfields import DynamicFieldsModelSerializer


class PropertyTypeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = PropertyTypes
        fields = ['id', 'type_name', 'is_active']


class PropertySerializer(DynamicFieldsModelSerializer):
    customer = CustomerInfoSerializer(read_only=True, many=False)
    property_type = PropertyTypeSerializer(read_only=True,many=False)

    class Meta:
        model = Property
        fields = ['id', 'customer', 'property_type', 'level_no', 'unit_no', 'lot_no', 'street_name', 'street_type', 'suffix', 'suburb',
                  'postcode',
                  'state', 'is_active']
