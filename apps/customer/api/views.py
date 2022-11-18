from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.customer.api.serializers import CustomerInfoSerializer
from apps.customer.models import CustomerInfo
from utils.permissions import IsManager
from utils.responseformat import success_response, fail_response

User = get_user_model()


# Create your views here.
@api_view(['POST'])
@permission_classes([IsManager])
def add_customer(request):
    user = User.objects.get(id=request.data['customer_id'])
    agency = request.user.userroles.company
    serializer = CustomerInfoSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(customer=user, created_by=request.user, agency=agency)
        return Response(success_response(serializer.data, "created new customer"))
    return Response(fail_response(serializer.errors, 'Customer could not be created', status.HTTP_400_BAD_REQUEST))


class CustomerListSearch(ListAPIView):
    serializer_class = CustomerInfoSerializer
    permission_classes = [IsManager]
    queryset = CustomerInfo.objects.filter()
    filter_backends = [SearchFilter]
    search_fields = ['id', 'customer__name', 'type', 'customer__phone', 'customer__email', ]


@api_view(["PUT"])
@permission_classes([IsManager])
def sms_consent_update(request):
    customer = CustomerInfo.objects.get(customer__id=request.data['user_id'], agency=request.user.userroles.company)
    customer.sms_consent = request.data['sms_consent']
    customer.save()
    return Response(success_response({'sms_consent': request.data['sms_consent']}, "sms consent updated"))

@api_view(['PUT'])
@permission_classes([IsManager])
def update_job_status(request):
    lead = CustomerInfo.objects.get(id=request.data['customer_id'])
    serializer = CustomerInfoSerializer(lead, data={'lead_status': request.data['job_status']})
    if serializer.is_valid():
        serializer.save()
        return Response(success_response(serializer.data, "Job status updated"))
    return Response(fail_response(serializer.errors, 'job status could not be update'))