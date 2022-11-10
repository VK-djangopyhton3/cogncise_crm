from apps.leads.models import WorkType
from utils.dynamicfields import DynamicFieldsModelSerializer


class WorkTypeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = WorkType
        fields = ['id', 'work_type', 'is_active']
