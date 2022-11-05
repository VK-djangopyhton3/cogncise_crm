from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.properties.api.serializer import PropertyTypeSerializer, PropertySerializer
from apps.properties.models import PropertyTypes, Property
from utils.permissions import IsStaff, IsManager
from utils.responseformat import fail_response, success_response


# Create your views here.
@api_view(['POST'])
@permission_classes([IsStaff])
def create_property_type(request):
    serializer = PropertyTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(success_response(serializer.data, 'New property type created'))
    return Response(fail_response(serializer.errors, 'Property type could not be created', status.HTTP_400_BAD_REQUEST))


@api_view(['PUT'])
@permission_classes([IsStaff])
def update_property_type(request):
    user = request.user
    company = PropertyTypes.objects.get(id=request.data["id"])
    serializer = PropertyTypeSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(company=company, requested_by=user)
        return Response(success_response(serializer.data, 'Update success full'))
    return Response(fail_response(serializer.errors, 'There were issues in the request', status.HTTP_400_BAD_REQUEST))


class CompanySearchList(ListAPIView):
    serializer_class = PropertyTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = PropertyTypes.objects.all()
    message = "Property type list"
    filter_backends = [SearchFilter]
    search_fields = ['type_name']


@api_view(["DELETE"])
@permission_classes([IsStaff])
def delete_property_type(request):
    property_type = PropertyTypes.objects.get(id=request.data['id'])
    property_type.is_active = False
    property_type.save()
    return Response(success_response(None, "Property type deleted"))


# @api_view(["GET"])
# @permission_classes([IsManager])
# def property_details(request):
#     properties = Property.objects.filter(id=request.GET['id'])
#     if property_details.exists():
#         serializer = PropertySerializer(properties, many=True)
#         return Response(success_response(serializer.data, "property details"))
#     return Response(
#         fail_response(None, "property details cannot be displayed or does not exist", status.HTTP_400_BAD_REQUEST))

