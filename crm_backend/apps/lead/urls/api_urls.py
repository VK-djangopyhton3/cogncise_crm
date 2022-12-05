from rest_framework import routers
from django.urls import path, include
from lead.views.api_views import *

app_name='lead'
router = routers.DefaultRouter()
router.register(r'', LeadViewSet, basename='lead')

urlpatterns = [
    path('sources/', LeadSourceListAPIView.as_view(), name='status'),
    path('statuses/', LeadStatusListAPIView.as_view(), name='statuses'),
    path('bulk-delete/', LeadsBulkDeleteAPIView.as_view(), name='delete_bulk_lead'),
    path('', include(router.urls))
]
