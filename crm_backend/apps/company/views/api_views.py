from common.common_view_imports import *

from shared.views import CrudViewSet, BulkDeleteAPIView
from shared.serializers import BulkDeleteSerilizer

from company.models import CompanyStatus, Company
from company.serializers import CompanyStatusSerializer, CompanySerializer

class CompanyStatusListAPIView(generics.ListAPIView):
    queryset = CompanyStatus.objects.all()
    serializer_class = CompanyStatusSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class CompanyViewSet(CrudViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'abn', 'email', 'mobile_number']
    filterset_fields = {
        'status':     ['in', 'exact']
    }

    
    def get_queryset(self):
        if self.request.user.is_cogncise is False:  # type: ignore
            self.queryset = self.queryset.filter(id=self.request.user.company_id)  # type: ignore
        return self.queryset


class CompanyBulkDeleteAPIView(BulkDeleteAPIView):
    swagger_tag = ['companies']
    queryset = Company.objects.all()
    serializer_class = BulkDeleteSerilizer
