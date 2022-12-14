from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.customer.models import CustomerInfo
from apps.properties.api.serializer import PropertyTypeSerializer, PropertySerializer, StreetTypeSerializer
from apps.properties.models import PropertyTypes, Property, StreetTypes
from utils.permissions import IsStaff, IsManager
from utils.responseformat import fail_response, success_response

User = get_user_model()


# Create your views here.

class PropertyTypeView(APIView):
    permission_classes = [IsStaff]

    def post(self):
        serializer = PropertyTypeSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, 'New property type created'))
        return Response(fail_response(serializer.errors, 'Could not be created', status.HTTP_400_BAD_REQUEST))

    def put(self):
        prop_type = PropertyTypes.objects.get(id=self.request.data['id'])
        serializer = PropertyTypeSerializer(prop_type, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, 'Update success full'))
        return Response(
            fail_response(serializer.errors, 'There were issues in the request', status.HTTP_400_BAD_REQUEST))

    def delete(self):
        property_type = PropertyTypes.objects.get(id=self.request.data['id'])
        property_type.is_active = False
        property_type.save()
        return Response(success_response(None, "Property type deleted"))


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


'''
Street types
'''


class StreetTypeViews(APIView):
    permission_classes = [IsStaff]

    def post(self):
        serializer = StreetTypeSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, 'New street type created'))
        return Response(fail_response(serializer.errors, 'Could not be created', status.HTTP_400_BAD_REQUEST))

    def put(self):
        street_type = StreetTypes.objects.get(id=self.request.data['id'])
        serializer = StreetTypeSerializer(street_type, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, 'Updated successfully'))
        return Response(
            fail_response(serializer.errors, 'There were issues in the request', status.HTTP_400_BAD_REQUEST))

    def delete(self):
        property_type = PropertyTypes.objects.get(id=self.request.data['id'])
        property_type.is_active = False
        property_type.save()
        return Response(success_response(None, "Property type deleted"))


class StreetTypeSearchList(ListAPIView):
    serializer_class = StreetTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = StreetTypes.objects.filter()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    message = "street type list"
    filter_backends = [SearchFilter]
    search_fields = ['type_name']


'''
Properties
'''


class PropertyView(APIView):
    permission_classes = [IsManager | IsStaff]

    def get_objects(self, pid):
        return Property.objects.get(id=pid)

    def post(self, request):
        customer = CustomerInfo.objects.get(customer__id=request.data['customer_id'])
        types = PropertyTypes.objects.get(id=request.data['property_type_id'])
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=customer, property_type=types)
            return Response(success_response(serializer.data, 'New property created'))
        return Response(fail_response(serializer.errors, 'Property could not be created', status.HTTP_400_BAD_REQUEST))

    def put(self, request):
        customer = CustomerInfo.objects.get(id=request.data['customer_id'])
        types = PropertyTypes.objects.get(id=request.data['property_type_id'])
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=customer, property_type=types)
            return Response(success_response(serializer.data, 'New property created'))
        return Response(fail_response(serializer.errors, 'Property could not be created', status.HTTP_400_BAD_REQUEST))

    def get(self, request):
        properties = self.get_objects(request.GET['property_id'])
        if properties:
            serializer = PropertySerializer(properties, many=False)
            return Response(success_response(serializer.data, "property details"))
        return Response(fail_response(None, "property details cannot be displayed", status.HTTP_400_BAD_REQUEST))


@api_view(["PUT"])
@permission_classes([IsManager])
def assign_billing_address(request):
    customer = request.user.id
    if request.user.is_staff:
        customer = request.data["user_id"]
    customer = CustomerInfo.objects.get(customer__id=request.data["user_id"], agency=request.data['company_id'])
    property_check = Property.objects.filter(customer=customer, is_billing_address=True)
    property_check.update(is_billing_address=False)
    property = Property.objects.filter(customer=customer, id=request.data['property_id']).update(is_billin_address=True)
    return Response(success_response(None, "Billing address updated"))


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


@api_view(["DELETE"])
@permission_classes([IsStaff])
def delete_property(request):
    customer_property = Property.objects.get(id=request.data['id'])
    customer_property.is_active = False
    customer_property.save()
    return Response(success_response(None, "Property deleted"))
