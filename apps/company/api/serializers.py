from apps.company.models import Companies, CompanyUpdateRequests
from utils.dynamicfields import DynamicFieldsModelSerializer


class CompaniesSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Companies
        fields = ['company_name', 'company_address', 'ABN', 'created_on']


class CompanyUpdateRequestSerializer(DynamicFieldsModelSerializer):
    company = CompaniesSerializer(many=False, read_only=True)

    class Meta:
        model = CompanyUpdateRequests
        fields = ['id', 'company', 'requested_by', 'company_name', 'company_address', 'ABN', 'created_on', 'updated_on',
                  'is_approved']
