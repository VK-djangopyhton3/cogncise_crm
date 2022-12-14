from common.common_view_imports import *

from company.models import CompanyStatus, Company
from company.serializers import CompanyStatusSerializer, CompanySerializer
from shared.views import CrudViewSet

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
    
    def get_queryset(self):
        if self.request.user.is_cogncise is False:  # type: ignore
            self.queryset = self.queryset.filter(id=self.request.user.company_id)  # type: ignore
        return self.queryset
