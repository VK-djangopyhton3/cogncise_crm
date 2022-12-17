from rest_framework import filters, serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from common.common_view_imports import *
from core.permissions import IsCompany
from company.models import Company

class CrudViewSet(viewsets.ModelViewSet):
    queryset = Q()
    serializer_class = serializers.ModelSerializer()
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsCompany]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    company_id = None
    company = None
    search_fields = []
    filterset_fields = {
        'id':  ['in', 'exact']
    }
    ordering_fields = '__all__'

    # init viewset
    def dispatch(self, request, *args, **kwargs):
        self.set_request_company()
        return super().dispatch(request, *args, **kwargs)

    # set request company
    def set_request_company(self):
        self.company_id = self.kwargs.get('company_id')
        self.company = Company.objects.filter(id=self.company_id).last()
        return self.company

    # scope queryset on befalh of company
    def get_queryset(self):
        self.queryset = self.queryset.filter(company=self.company)  # type: ignore
        return self.queryset

    # add/update context with company information
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'company_id': self.company_id, 'company': self.company})
        return context

    # create new object
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return return_response(serializer.data, True, 'Successfully Created!', status.HTTP_200_OK)
        
        return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)

    # list all object
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return return_response(serializer.data, True, 'List Successfully Retrieved!', status.HTTP_200_OK)

    # fetch requested object
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return return_response(serializer.data, True, 'Successfully Retrieved!', status.HTTP_200_OK)

    # update requested object
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return return_response(serializer.data, True, 'Successfully Updated!', status.HTTP_200_OK)

        return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)

    # delete requested object
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return return_response({'detail': 'object deleted'}, True, 'Successfully Deleted!', status.HTTP_200_OK)


class BulkDeleteAPIView(generics.GenericAPIView):
    queryset = Q()
    permission_classes = [IsAuthenticated,]
    serializer_class = serializers.ModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # self.queryset.filter(id__in=serializer.data['ids']).update(is_deleted=True)  # type: ignore
            return return_response({ 'detail': 'objects deleted' }, True, 'Records successfully Deleted!', status.HTTP_200_OK)
        return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)


class BulkRestoreAPIView(generics.GenericAPIView):
    queryset = Q()
    permission_classes = [IsAuthenticated,]
    serializer_class = serializers.ModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.queryset.filter(id__in=serializer.data['ids']).update(is_deleted=False)  # type: ignore
            return return_response({ 'detail': 'objects restored' }, True, 'Records successfully Restored!', status.HTTP_200_OK)
        return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)
