from rest_framework import routers
from django.urls import path, include
from appointment.views.api_views import *

app_name='appointment'
router = routers.DefaultRouter()
router.register(r'', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
]
