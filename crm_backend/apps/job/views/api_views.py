from common.common_view_imports import *

from shared.views import CrudViewSet
from job.models import Job
from job.serializers import JobSerializer

class JobViewSet(CrudViewSet):
    swagger_tag = ["jobs"]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    search_fields = ['title', 'first_name', 'last_name', 'email', 'mobile_number', 'company__name', 'company__abn']
    filterset_fields = {
        'company': ['in', 'exact']
    }
