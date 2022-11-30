from rest_framework import routers
from django.urls import path, include
from lead.views.api_views import *

app_name='lead'
router = routers.DefaultRouter()
router.register(r'', LeadViewSet, basename='lead')

urlpatterns = [
    path('', include(router.urls)),
]
