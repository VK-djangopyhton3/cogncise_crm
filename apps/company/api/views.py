from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.company.api.serializers import CompanyUpdateRequestSerializer, CompaniesSerializer
from apps.company.models import CompanyUpdateRequests, Companies
from utils.permissions import IsAdmin, IsStaff, IsManager, IsSuper
from utils.responseformat import success_response, fail_response

User = get_user_model()


# Create your views here.

@api_view(['POST'])
@permission_classes([IsSuper])
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


@api_view(['PUT'])
@permission_classes([IsStaff])
def update_company_info(request):
    request_qs = CompanyUpdateRequests.objects.filter(id=request.data["request_id"], is_approved=None,
                                                      company__id=request.data['company_id'])
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Companies.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(staffassociation__user=self.request.user)
        return queryset

    message = "Company list"
    filter_backends = [SearchFilter]
    search_fields = ['id', 'company_name', 'ABN']


@api_view(["PUT"])
@permission_classes([IsStaff])
def delete_company(request):
    company = Companies.objects.get(id=request.data['company_id'])
    company.is_active = False
    company.save()
    users = User.objects.filter(userroles__company=company)
    users.update(is_active=False)
    return Response(success_response(None, "Company deleted"))


@api_view(["GET"])
@permission_classes([IsManager])
def company_details(request):
    company = Companies.objects.filter(id=request.GET['company_id'])
    if not request.user.is_staff:
        company = company.filter(company_name=request.user.userroles.company.company_name)
    if company.exists():
        serializer = CompaniesSerializer(company[0], many=False)
        return Response(success_response(serializer.data, "company details"))
    return Response(
        fail_response(None, "company details cannot be displayed or does not exist", status.HTTP_400_BAD_REQUEST))
