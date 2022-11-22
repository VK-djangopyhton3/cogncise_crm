from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.company.models import Companies
from apps.users.api.serializers import UserSerializer, UserRolesSerializer
from apps.users.models import UserRoles, StaffAssociate
from utils.permissions import IsAdmin, IsSuper, IsManager, IsStaff, IsViewOnly
from utils.responseformat import success_response, fail_response

User = get_user_model()


# Create your views here.

class UserViews(APIView, mixins.CreateModelMixin):
    permission_classes = [IsViewOnly | IsManager | IsAdmin | IsStaff]

    def get_objects(self, user_id):

        user = User.objects.filter(id=user_id)
        company_id = None
        if not user.first() == self.request.user:
            roles = ['admin', 'manager', 'field_worker', 'auditor']
            if self.request.user.is_staff and user_id is not self.request.user.id:
                company_id = self.request.data['company_id']
            elif self.request.user.userroles.role in roles and user_id is not self.request.user.id:
                company_id = self.request.user.userroles.company.id
        if company_id is not None:
            user = user.filter(Q(userroles__company__id=company_id) | Q(customerinfo__agency__id=company_id))
        else:
            user = user.filter()
        return user.first()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_superuser and 'staff' in request.data:
                serializer.save(is_staff=request.data['is_staff'], is_superuser=request.data['is_superuser'])
            else:
                serializer.save()
            return Response(success_response(serializer.data, 'New user added'))
        return Response(fail_response(serializer.errors, 'New user could not be added'))

    def get(self, request):

        if 'user_id' in request.GET:
            uid = request.GET['user_id']
        else:
            uid = request.user.id
        user = self.get_objects(uid)
        if user:
            serializer = UserSerializer(user, many=False)
            return Response(success_response(serializer.data, 'user details'))
        return Response(fail_response(None, 'user does not exist', status.HTTP_404_NOT_FOUND))

    def put(self, request):
        if 'is_active' in request.data:
            return Response(fail_response(None, 'Unauthorised', status.HTTP_401_UNAUTHORIZED))
        user = self.get_objects(request.data['user_id'])
        if user:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(success_response(serializer.data, "user details updated"))
            return Response(fail_response(None, 'User could not be deleted', status.HTTP_400_BAD_REQUEST))
        return Response(fail_response(None, 'User not found', status.HTTP_404_NOT_FOUND))

    def delete(self):
        user = self.get_objects(self.request.data["user_id"])
        serializer = UserSerializer(user, data={"is_active": False}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, "user deleted"))
        return Response(fail_response(None, 'User could not be deleted', status.HTTP_400_BAD_REQUEST))


class UserSearchList(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter()
        if user.is_staff:
            queryset = queryset.filter(Q(userroles__company__id=self.request.data['company_id']) |
                                       Q(customerinfo__agency__id=self.request.data['company_id']))
        if not user.is_staff and user.userroles.role not in ['auditor', 'field_worker']:
            company = user.userroles.company
            queryset = queryset.filter(Q(userroles__company=company) | Q(customerinfo__agency=company))
        return queryset.order_by('id')

    message = "User list"
    filter_backends = [SearchFilter, DjangoFilterBackend]
    ordering = ['id', ]
    filters = ['id', 'email', 'phone', 'company_role', 'company__company__company_name', 'company__company__ABN']
    filterset_fields = filters
    search_fields = filters


class UserRolesViews(APIView):
    permission_classes = [IsAdmin | IsStaff]

    def get_objects(self, uid):
        if not self.request.is_staff:
            company = self.request.user.userroles.company
        else:
            company = Companies.objects.get(id=self.request.data['company_id'])
        roles = UserRoles.objects.filter(user__id=uid, company=company)
        return roles.first()

    def post(self, request):
        if not request.user.is_staff:
            company = request.user.userroles.company
        else:
            company = Companies.objects.get(id=request.data['company_id'])

        user = User.objects.get(id=request.data['user_id'])
        serializer = UserRolesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=company, user=user)
            return Response(success_response(serializer.data, 'New roles and company assigned'))
        return Response(
            fail_response(serializer.errors, "User could not be assigned a role", status.HTTP_400_BAD_REQUEST))

    def put(self):
        role = self.get_objects(self.request.data["user_id"])
        if not role:
            return Response(fail_response(None, "User does not exist", status.HTTP_404_NOT_FOUND))
        serializer = UserRolesSerializer(role, data={"role": self.request.data["role"]}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, "User role updated"))
        return Response(fail_response(None, "User role could not be updated"))


@api_view(['PUT'])
@permission_classes([IsSuper])
def assign_companies(request):
    user = User.objects.get(id=request.data['user_id'])
    [StaffAssociate(company=Companies.objects.get(id=cid), user=user).save() for cid in request.data['company_id_list']]
    return Response(success_response(None, "Staff has been assigned"))
