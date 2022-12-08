from common.common_view_imports import *

from shared.views import CrudViewSet
from customer.models import Customer
from customer.serializers import CustomerSerializer

class CustomerViewSet(CrudViewSet):
    swagger_tag = ["customers"]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
