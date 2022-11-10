from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.leads.api.serializers import WorkTypeSerializer
from apps.leads.models import WorkType
from utils.permissions import IsStaff, IsManager
from utils.responseformat import fail_response, success_response


# Create your views here.
@api_view(['POST'])
@permission_classes([IsStaff])
def create_work_type(request):
    serializer = WorkTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(success_response(serializer.data, 'New work type created'))
    return Response(fail_response(serializer.errors, 'Work type could not be created', status.HTTP_400_BAD_REQUEST))


@api_view(['PUT'])
@permission_classes([IsStaff])
def update_work_type(request):
    work_type = WorkType.objects.get(id=request.data['id'])
    serializer = WorkTypeSerializer(work_type, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(success_response(serializer.data, 'Update success full'))
    return Response(fail_response(serializer.errors, 'There were issues in the request', status.HTTP_400_BAD_REQUEST))


class WorkTypeSearchList(ListAPIView):
    serializer_class = WorkTypeSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        queryset = WorkType.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    message = "work type list"
    filter_backends = [SearchFilter]
    search_fields = ['work_type']


@api_view(["DELETE"])
@permission_classes([IsStaff])
def delete_work_type(request):

    work_type = WorkType.objects.get(id=request.data['id'])
    work_type.is_active = False
    work_type.save()
    return Response(success_response(None, "Work type deleted"))


