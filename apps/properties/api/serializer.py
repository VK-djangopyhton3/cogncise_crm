from apps.properties.models import PropertyTypes, Property
from utils.dynamicfields import DynamicFieldsModelSerializer


class PropertyTypeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = PropertyTypes
        fields = ['id', 'type_name']


class PropertySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'level_no', 'unit_no', 'lot_no', 'street_name', 'street_type', 'suffix', 'suburb', 'postcode',
                  'state']
