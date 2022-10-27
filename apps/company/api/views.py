from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.company.api.serializers import CompanyUpdateRequestSerializer, CompaniesSerializer
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
