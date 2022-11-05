from apps.properties.models import PropertyTypes
from utils.dynamicfields import DynamicFieldsModelSerializer


class PropertyType(DynamicFieldsModelSerializer):
    class Meta:
        model = PropertyTypes
        fields = ['unit_type']

