from common.common_view_imports import *

from shared.views import CrudViewSet, BulkDeleteAPIView
from shared.serializers import BulkDeleteSerilizer

from customer.models import Customer
from customer.serializers import CustomerSerializer

class CustomerViewSet(CrudViewSet):
    swagger_tag = ["customers"]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ['first_name', 'last_name', 'email', 'mobile_number']
    
    def get_queryset(self):
        self.queryset = self.queryset.filter(companies=self.company)  # type: ignore
        return self.queryset


class CustomersBulkDeleteAPIView(BulkDeleteAPIView):
    swagger_tag = ["customers"]
    queryset = Customer.objects.all()
    serializer_class = BulkDeleteSerilizer
