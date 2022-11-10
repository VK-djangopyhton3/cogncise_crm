from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.customer.models import CustomerInfo
from apps.properties.api.serializer import PropertyTypeSerializer, PropertySerializer, StreetTypeSerializer
from apps.properties.models import PropertyTypes, Property, StreetTypes
from utils.permissions import IsStaff, IsManager
from utils.responseformat import fail_response, success_response

User = get_user_model()


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
    prop_type = PropertyTypes.objects.get(id=request.data['id'])
    serializer = PropertyTypeSerializer(prop_type, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(success_response(serializer.data, 'Update success full'))
    return Response(fail_response(serializer.errors, 'There were issues in the request', status.HTTP_400_BAD_REQUEST))


class PropertyTypeSearchList(ListAPIView):
    serializer_class = PropertyTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = PropertyTypes.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    message = "Property type list"
    filter_backends = [SearchFilter]
    search_fields = ['type_name']


@api_view(["DELETE"])
@permission_classes([IsStaff])
def delete_property_type(request):
    # print(request.data['id'])
    property_type = PropertyTypes.objects.get(id=request.data['id'])
    property_type.is_active = False
    property_type.save()
    return Response(success_response(None, "Property type deleted"))


'''
Street types
'''


@api_view(['POST'])
@permission_classes([IsStaff])
def create_street_type(request):
    serializer = StreetTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(success_response(serializer.data, 'New street type created'))
    return Response(fail_response(serializer.errors, 'Street type could not be created', status.HTTP_400_BAD_REQUEST))


@api_view(['PUT'])
@permission_classes([IsStaff])
def update_street_type(request):
    prop_type = StreetTypes.objects.get(id=request.data['id'])
    serializer = StreetTypeSerializer(prop_type, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(success_response(serializer.data, 'Update success full'))
    return Response(fail_response(serializer.errors, 'There were issues in the request', status.HTTP_400_BAD_REQUEST))


class StreetTypeSearchList(ListAPIView):
    serializer_class = StreetTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = StreetTypes.objects.filter()
        print(queryset.count())
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    message = "street type list"
    filter_backends = [SearchFilter]
    search_fields = ['type_name']


@api_view(["DELETE"])
@permission_classes([IsStaff])
def delete_street_type(request):
    # print(request.data['id'])
    street_type = StreetTypes.objects.get(id=request.data['id'])
    street_type.is_active = False
    street_type.save()
    return Response(success_response(None, "Street type deleted"))


'''
Properties
'''


def unassign_billing_address(customer):
    property_check = Property.objects.filter(customer=customer, is_billing_address=True)
    property_check.update(is_billing_address=False)
    return True


@api_view(["POST"])
@permission_classes([IsManager])
def property_add(request):
    customer = CustomerInfo.objects.get(customer__id=request.data['customer_id'])
    types = PropertyTypes.objects.get(id=request.data['property_type_id'])
    if "is_billing_address" in request.data:
        if request.data['is_billing_address']:
            unassign_billing_address(customer)
    serializer = PropertySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(customer=customer, property_type=types)
        return Response(success_response(serializer.data, 'New property created'))
    return Response(fail_response(serializer.errors, 'Property could not be created', status.HTTP_400_BAD_REQUEST))


@api_view(["GET"])
@permission_classes([IsManager])
def property_details(request):
    properties = Property.objects.filter(id=request.GET['id'])
    if properties.exists():
        serializer = PropertySerializer(properties, many=True)
        return Response(success_response(serializer.data, "property details"))
    return Response(
        fail_response(None, "property details cannot be displayed or does not exist", status.HTTP_400_BAD_REQUEST))


class PropertySearchList(ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsManager]
    message = "property list"

    def get_queryset(self):
        queryset = Property.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        if "customer_id" in self.request.GET:
            queryset = queryset.filter(customer__customer__id=self.request.GET['customer_id'])
        return queryset

    filter_backends = [SearchFilter]
    search_fields = ['customer__customer__name', 'property_type__type_name', 'building_name', 'street_name', 'suburb',
                     'postcode', 'state']


@api_view(['PUT'])
@permission_classes([IsManager])
def update_property(request):
    properties = Property.objects.get(id=request.data['id'])
    property_type = properties.property_type
    street_type = properties.street_type

    if "is_active" in request.data:
        return Response(
            fail_response(request.data, "You are not authorized delete a property", status.HTTP_401_UNAUTHORIZED))

    if "is_billing_address" in request.data:
        if request.data['is_billing_address']:
            unassign_billing_address(properties.customer)

    if "property_type_id" in request.data:
        property_type = PropertyTypes.objects.get(id=request.data["property_type_id"])

    if "street_type_id" in request.data:
        street_type = StreetTypes.objects.get(id=request.data["street_type_id"])

    serializer = PropertySerializer(properties, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(property_type=property_type, street_type=street_type)
        return Response(success_response(serializer.data, 'Update success full'))
    return Response(fail_response(serializer.errors, 'There were issues in the request', status.HTTP_400_BAD_REQUEST))


@api_view(["DELETE"])
@permission_classes([IsStaff])
def delete_property(request):
    customer_property = Property.objects.get(id=request.data['id'])
    customer_property.is_active = False
    customer_property.save()
    return Response(success_response(None, "Property deleted"))
