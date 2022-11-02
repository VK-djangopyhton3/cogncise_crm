from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.company.api.serializers import CompanyUpdateRequestSerializer, CompaniesSerializer
from apps.company.models import CompanyUpdateRequests, Companies
from utils.permissions import IsAdmin, IsStaff
from utils.responseformat import success_response, fail_response


# Create your views here.

@api_view(['POST'])
@permission_classes([IsStaff])
def create_company(request):
    serializer = CompaniesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(success_response(serializer.data, 'New company created'))
    return Response(fail_response(serializer.errors, 'Company could not be created', status.HTTP_400_BAD_REQUEST))


@api_view(['POST'])
@permission_classes([IsAdmin])
def update_request(request):
    user = request.user
    company = user.userroles.company
    serializer = CompanyUpdateRequestSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(company=company, requested_by=user)
        return Response(success_response(serializer.data, 'Update request has been sent'))
    return Response(fail_response(serializer.errors, 'There were issues in the request', status.HTTP_400_BAD_REQUEST))


def update_info(company, updates):
    if updates.company_name is not None:
        company.company_name = updates.company_name
    if updates.company_address is not None:
        company.company_address = updates.company_address
    if updates.ABN is not None:
        company.ABN = updates.ABN

    company.save()
    return True


@api_view(['POST'])
@permission_classes([IsStaff])
def update_company_info(request):
    request_qs = CompanyUpdateRequests.objects.filter(id=request.data["request_id"], is_approved=None)
    serializer = CompanyUpdateRequestSerializer(request_qs[0], data=request.data, partial=True)
    approved = request.data['is_approved']
    if serializer.is_valid():
        if approved:
            update_info(request_qs[0].company, request_qs[0])
        serializer.save()
        return Response(success_response(serializer.data, 'Approval granted = ' + str(request.data['is_approved'])))
    return Response(fail_response(serializer.errors, 'There were issues in the request', status.HTTP_400_BAD_REQUEST))

class CompanySearchList(ListAPIView):
    serializer_class = CompaniesSerializer
    permission_classes = [IsStaff]
    queryset = Companies.objects.all()
    message = "Company list"
    filter_backends = [SearchFilter]
    search_fields = ['id', 'company_name', 'ABN']