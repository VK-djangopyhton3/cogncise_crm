from common.common_view_imports import *

from shared.views import CrudViewSet
from job.models import Job, JobStatus
from job.serializers import JobSerializer, JobStatusSerializer

class JobStatusListAPIView(generics.ListAPIView):
    swagger_tag = ["appointment work types"]
    queryset = JobStatus.objects.all()
    serializer_class = JobStatusSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
class JobViewSet(CrudViewSet):
    swagger_tag = ["jobs"]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    search_fields = ['title', 'first_name', 'last_name', 'email', 'mobile_number', 'company__name', 'company__abn']
    filterset_fields = {
        'company': ['in', 'exact']
    }
