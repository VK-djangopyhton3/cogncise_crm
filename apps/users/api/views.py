from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.company.models import Companies
from apps.customer.models import CustomerInfo
from apps.users.api.serializers import UserSerializer, UserRolesSerializer
from utils.permissions import IsAdmin, IsSuper
from utils.responseformat import success_response, fail_response

User = get_user_model()


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_user(request):
    user = request.user
    info = CustomerInfo.objects.filter(customer=user)

    if 'user_id' in request.GET:
        user = User.objects.filter(id=request.GET['user_id'])
    else:
        serializer = UserSerializer(user, many=False)
        return Response(success_response(serializer.data, 'user details'))

    if not info.exists() and not request.user.is_staff:
        user = user.filter(customerinfo__agency=request.user.userroles.company)
    if request.user.is_staff and not request.user.is_superuser:
        user = user.filter(customerinfo__agency__user=request.user)
    if not user.exists():
        return Response(fail_response(None, 'User does not exist'))

    serializer = UserSerializer(user.first(), many=False)
    return Response(success_response(serializer.data, 'user details'))


@api_view(['PUT'])
@permission_classes([IsAdmin])
def update_user_details(request):
    user = User.objects.filter(id=request.data['user_id'])
    if not request.user.is_staff:
        user = user.filter(Q(userroles__company=request.user.userroles.company) |
                           Q(customerinfo__agency=request.user.userroles.company))
    else:
        user = user.filter(Q(userroles__company__id=request.data['company_id']) |
                           Q(customerinfo__agency__id=request.data['company_id']))

    if user:
        serializer = UserSerializer(user.first(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, "user details updated"))
        return Response(fail_response(None, 'User could not be deleted', status.HTTP_400_BAD_REQUEST))
    return Response(fail_response(None, 'User not found', status.HTTP_404_NOT_FOUND))


@api_view(['DELETE'])
@permission_classes([IsAdmin])
def delete_user(request):
    user = User.objects.filter(id=request.data['user_id'])
    if not request.user.is_staff:
        user = user.filter(Q(userroles__company=request.user.userroles.company) |
                           Q(customerinfo__agency=request.user.userroles.company))
    else:
        user = user.filter(Q(userroles__company__id=request.data['company_id']) |
                           Q(customerinfo__agency__id=request.data['company_id']))
    if user:
        user.update(is_active=False)
        return Response(success_response(None, 'User deleted'))
    return Response(fail_response(None, 'User not found', status.HTTP_404_NOT_FOUND))


@api_view(['POST'])
@permission_classes([IsAdmin])
def add_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        if request.user.is_superuser and 'staff' in request.data:
            serializer.save(is_staff=request.data['is_staff'], is_superuser=request.data['is_superuser'])
        else:
            serializer.save()
        return Response(success_response(serializer.data, 'New user added'))
    return Response(fail_response(serializer.errors, 'New user could not be added'))


class UserSearchList(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter()
        if user.is_staff:
            queryset = queryset.filter(userroles__company__id=self.request.GET['company_id'])
        if not user.is_staff and user.userroles.role not in ['auditor', 'field_worker']:
            company = user.userroles.company
            queryset = queryset.filter(userroles__company=company)
        return queryset.order_by('id')

    message = "User list"
    filter_backends = [SearchFilter, DjangoFilterBackend]
    ordering = ['id', ]
    filters = ['id', 'email', 'phone', 'userroles__role', 'userroles__company__company_name', 'userroles__company__ABN']
    filterset_fields = filters
    search_fields = filters


@api_view(['POST'])
@permission_classes([IsAdmin])
def assign_role(request):
    if not request.is_staff:
        company = request.user.userroles.company
    else:
        company = Companies.objects.get(id=request.data['company_id'])
    user = User.objects.get(id=request.data['user_id'], userroles__company=company)
    serializer = UserRolesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(company=company, user=user)
        return Response(success_response(serializer.data, 'New roles and company assigned'))
    return Response(
        fail_response((serializer.errors, 'User could not be assigned a role', status.HTTP_400_BAD_REQUEST)))


@api_view(['PUT'])
@permission_classes([IsSuper])
def assign_companies(request):
    user = User.objects.get(id=request.data['user_id'])
    companies = [Companies(company__id=cid) for cid in request.data['company_id_list']]
    associates = Companies.objects.bulk_create(companies)
    associates.update(user=user)
    return Response()
