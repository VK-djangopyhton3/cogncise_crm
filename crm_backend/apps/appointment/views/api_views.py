from common.common_view_imports import *

from shared.views import CrudViewSet
from appointment.models import WorkType, Appointment, ScheduleAppointment
from appointment.serializers import WorkTypeSerializer, AppointmentSerializer, ScheduleAppointmentSerializer

class WorkTypeListAPIView(generics.ListAPIView):
    swagger_tag = ["appointment work types"]
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class AppointmentViewSet(CrudViewSet):
    swagger_tag = ["appointments"]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class SechduleAppointmentViewSet(CrudViewSet):
    queryset = ScheduleAppointment.objects.all()
    serializer_class = ScheduleAppointmentSerializer

    def get_queryset(self):
        self.queryset = self.queryset.all()  # type: ignore
        return self.queryset
