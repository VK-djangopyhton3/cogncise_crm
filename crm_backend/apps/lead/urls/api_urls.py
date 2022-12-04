from rest_framework import routers
from django.urls import path, include
from lead.views.api_views import *

app_name='lead'
router = routers.DefaultRouter()
router.register(r'', LeadViewSet, basename='lead')

urlpatterns = [
    path('sources/', LeadSourceListAPIView.as_view(), name='status'),
    path('statuses/', LeadStatusListAPIView.as_view(), name='statuses'),
    # path('lead/bulk/delete', BulkLeadViewSet.as_view({'post':'delete'}), name='bulk_delete'),
    path('', include(router.urls))
]
