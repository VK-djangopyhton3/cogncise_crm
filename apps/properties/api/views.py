from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.properties.models import Property
from utils.permissions import IsManager
from utils.responseformat import success_response, fail_response


# Create your views here.
@api_view(["GET"])
@permission_classes([IsManager])
def property_details(request):
    properties = Property.objects.filter(id=request.GET['id'])
    if property_details.exists():
        serializer = PropertySerializer(properties, many=True)
        return Response(success_response(serializer.data, "property details"))
    return Response(
        fail_response(None, "property details cannot be displayed or does not exist", status.HTTP_400_BAD_REQUEST))
