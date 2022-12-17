from rest_framework import routers
from django.urls import path, include

from appointment.views.api_views import *

app_name='appointment'
router = routers.DefaultRouter()
router.register(r'', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('work-types/', WorkTypeListAPIView.as_view(), name='appointment_work_types'),
    path('', include(router.urls)),
]
