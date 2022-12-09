from common.common_view_imports import *

from lead.models import LeadSource, LeadStatus, Lead
from lead.serializers import LeadSourceSerializer, LeadStatusSerializer, LeadSerializer
from shared.serializers import BulkDeleteSerilizer
from shared.views import CrudViewSet, BulkDeleteAPIView

class LeadSourceListAPIView(generics.ListAPIView):
    swagger_tag = ["lead sources"]
    queryset = LeadSource.objects.all()
    serializer_class = LeadSourceSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class LeadStatusListAPIView(generics.ListAPIView):
    swagger_tag = ["lead statuses"]
    queryset = LeadStatus.objects.all()
    serializer_class = LeadStatusSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class LeadViewSet(CrudViewSet):
    swagger_tag = ["leads"]
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    search_fields = ['first_name', 'last_name', 'email', 'mobile_number', 'company__name', 'company__abn']
    filterset_fields = {
        'company':  ['in', 'exact'],
        'source':   ['in', 'exact'],
        'customer': ['in', 'exact'],
        'owner':    ['in', 'exact'],
        'status':   ['in', 'exact']
    }


class LeadsBulkDeleteAPIView(BulkDeleteAPIView):
    swagger_tag = ["leads"]
    queryset = Lead.objects.all()
    serializer_class = BulkDeleteSerilizer
