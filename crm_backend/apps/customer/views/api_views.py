from common.common_view_imports import *

from shared.views import CrudViewSet
from customer.models import Customer
from customer.serializers import CustomerSerializer
from shared.serializers import BulkDeleteSerilizer
from shared.views import CrudViewSet, BulkDeleteAPIView

# class CustomerViewSet(CrudViewSet):
#     swagger_tag = ["customers"]
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer


class CustomerViewSet(CrudViewSet):
    swagger_tag = ["customers"]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'user__mobile_number']
    filterset_fields = {
        'company':  ['in', 'exact'],
        'user': ['in', 'exact'],
    }


class CustomersBulkDeleteAPIView(BulkDeleteAPIView):
    swagger_tag = ["customers"]
    queryset = Customer.objects.all()
    serializer_class = BulkDeleteSerilizer
