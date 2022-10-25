from apps.company.models import Companies
from utils.dynamicfields import DynamicFieldsModelSerializer


class CompaniesSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Companies
        fields = ['company_name','company_address','ABN']
