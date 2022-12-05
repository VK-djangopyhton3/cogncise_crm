from rest_framework import filters
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from common.common_view_imports import *

from lead.models import LeadSource, LeadStatus, Lead
from lead.serializers import LeadSourceSerializer, LeadStatusSerializer, LeadSerializer
from shared.serializers import BulkDeleteSerilizer

class LeadSourceListAPIView(generics.ListAPIView):
    queryset = LeadSource.objects.all()
    serializer_class = LeadSourceSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class LeadStatusListAPIView(generics.ListAPIView):
    queryset = LeadStatus.objects.all()
    serializer_class = LeadStatusSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'email', 'mobile_number', 'company__name', 'company__abn']
    filterset_fields = ['company', 'source', 'status', 'owner', 'customer']
    ordering_fields = '__all__'

    
    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return return_response(serializer.data, True, 'Successfully Created!', status.HTTP_200_OK)
        
        return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return return_response(serializer.data, True, 'List Successfully Retrieved!', status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return return_response(serializer.data, True, 'Successfully Retrieved!', status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return return_response(serializer.data, True, 'Successfully Updated!', status.HTTP_200_OK)

        return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return return_response({'detail': 'object deleted'}, True, 'Successfully Deleted!', status.HTTP_200_OK)

class LeadsBulkDeleteAPIView(generics.GenericAPIView):

    """
    User bulk delete Operation View

    User can perform Bulk delete operation to the system.
    The data required are ids = [1,2,3].
    """

    queryset = Lead.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = BulkDeleteSerilizer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.queryset.filter(id__in=serializer.data['ids']).update(is_deleted=True)
            return return_response({'detail': 'objects deleted'}, True, 'Leads successfully Deleted!', status.HTTP_200_OK)
        return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)