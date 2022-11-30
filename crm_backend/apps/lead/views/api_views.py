from common.common_view_imports import *
from lead.models import Lead
from lead.serializers import LeadSerializer

class LeadViewSet(viewsets.ModelViewSet):
    """
    Leads Operation View

    Permitted User can perform CRUD operation on leads section.
    The data required are username, email, first_name, last_name, password, access_type.
    """

    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny(),]        
        return super(LeadViewSet, self).get_permissions()

    def get_queryset(self):
        self.queryset = self.queryset.filter()
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_class
        return self.serializer_class

    def create(self, request):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
                  
            serializer = serializer.save()
            # logger.info(data)
            return return_response(serializer.data, True, 'Successfully Created!', status.HTTP_200_OK)

        # logger.error(serializer.errors)
        return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)

    
    def list(self, request):
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.get_queryset(), many=True)

        # logger.info(serializer.data)
        return return_response(serializer.data, True, 'List Successfully Retrieved!', status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # logger.info(serializer.data)
        return return_response(serializer.data, True, ' Successfully Retrieved!', status.HTTP_200_OK)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.update(instance,validated_data=serializer.validated_data)
            
            # logger.info(serializer.data)
            return return_response(serializer.data, True, ' Successfully Updated!', status.HTTP_200_OK)

        # logger.error(serializer.errors)
        return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)

        # logger.info('Successfully Deleted!')
        return return_response({"detail":"object deleted"}, True, ' Successfully Deleted!', status.HTTP_200_OK)

