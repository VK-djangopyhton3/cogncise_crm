from common.common_serilizer_imports import *
from job.models import Job


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = "__all__"

