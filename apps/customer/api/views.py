from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.customer.api.serializers import CustomerInfoSerializer
from apps.customer.models import CustomerInfo
from apps.users.api.serializers import UserSerializer
from utils.permissions import IsManager, IsStaff
from utils.responseformat import success_response, fail_response

User = get_user_model()


# Create your views here.

class CustomerViews(APIView):
    permission_classes = [IsManager]

    def get_object(self, uid, cid):
        customer = CustomerInfo.objects.filter(customer__id=uid, agency__id=cid)
        return customer.first()

    def post(self, request):
        # user_info = request.data['user_info']
        # user = UserSerializer(data=user_info, many=False)
        # if not user.is_valid():
        #     return Response(user.errors, "User could not be created")
        # user_id = user.save().data.id

        user = User.objects.get(id=request.data['user_id'])
        agency = request.user.userroles.company
        if request.data["type"] == "business":
            cname, abn = request.data["company_name"], request.data["company_ABN"]  # just to force a check on api
        serializer = CustomerInfoSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save(customer=user, assigned_to=request.user.userroles, agency=agency)
            return Response(success_response(serializer.data, "created new customer"))
        return Response(fail_response(serializer.errors, 'Customer could not be created', status.HTTP_400_BAD_REQUEST))

    def put(self, request):
        customer = self.get_object(request.data['user_id'],
                                   request.data['company_id'])  # if customer try updating own data
        if customer:
            serializer = CustomerInfoSerializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(success_response(serializer.data, "Customer details updated"))
            return Response(
                fail_response(serializer.errors, "customer info could not be updated", status.HTTP_400_BAD_REQUEST))
        return fail_response(None, "No customer with this information")


class CustomerListSearch(ListAPIView):
    serializer_class = CustomerInfoSerializer
    permission_classes = [IsManager]
    queryset = CustomerInfo.objects.filter()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filters = ['id', 'customer_name', 'type', 'company_name', 'company_ABN', 'lead_status']
    filterset_fields = filters
    search_fields = filters
