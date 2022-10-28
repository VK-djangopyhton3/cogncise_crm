from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.api.serializers import UserSerializer, UserRolesSerializer
from apps.users.models import UserRoles
from utils.permissions import IsAdmin
from utils.responseformat import success_response, fail_response

User = get_user_model()


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_user(request):
    user = request.user
    company = UserRoles.objects.get(user=request.user).company_name
    if 'id' in request.GET and (request.user.userrole.company.company_name == company or request.user.is_staff == True):
        user = User.objects.get(id=request.GET['id'])
    serializer = UserSerializer(user, many=False)
    return Response(success_response(serializer.data, 'user deleted'))


@api_view(['UPDATE'])
@permission_classes([IsAdmin])
def user_details_update(request):
    user = User.objects.get(id=request.data['id'])
    if not request.is_staff:
        user = user.filter(userroles__company=request.user.userrole.company)
    serializer = UserSerializer(user, many=False, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return success_response(serializer.data, 'user details updated')
    return fail_response(serializer.errors, "details could not be updated", status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    company = UserRoles.objects.get(user=request.user).company_name
    if 'id' in request.GET and (request.user.userrole.company.company_name == company or request.user.is_staff == True):
        user = User.objects.get(id=request.GET['id'])
    user.is_active = False
    user.save()
    return Response(success_response(None, 'user deleted'))


@api_view(['POST'])
@permission_classes([IsAdmin])
def add_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        if request.user.is_staff and 'staff' in request.data['staff']:
            serializer.save(is_active=True, is_staff=request.data[
                'staff'])  # is_active default=True not working, is_staff incase cg admin creates a user
        else:
            serializer.save(is_active=True)  # is_active default=True not working
        return Response(success_response(serializer.data, 'New user added'))
    return Response(fail_response(serializer.errors, 'New user could not be added'))


class UserSearchList(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        company = user.userroles.company
        queryset = User.objects.filter()
        if not user.is_staff and user.userroles.role not in ['auditor', 'field_worker']:
            queryset = queryset.filter(userroles__company=company)
        return queryset

    message = "User list"
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name', 'email', 'phone', 'is_staff', 'is_active', 'userroles__role',
                     'userroles__company__company_name', 'userroles__company__ABN']


@api_view(['POST'])
@permission_classes([IsAdmin])
def assign_role(request):
    company = request.user.userroles.company
    user = User.objects.get(id=request.data['user_id'])
    serializer = UserRolesSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(company=company, user=user)
        return Response(success_response(serializer.data, 'New roles and company assigned'))
    return Response(
        fail_response((serializer.errors, 'User could not be assigned a role', status.HTTP_400_BAD_REQUEST)))
