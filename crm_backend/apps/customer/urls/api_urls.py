from rest_framework import routers
from django.urls import path, include
from customer.views.api_views import *

app_name='customer'
router = routers.DefaultRouter()
router.register(r'', CustomerViewSet, basename='customer')

urlpatterns = [
    path('bulk-delete/', CustomersBulkDeleteAPIView.as_view(), name='delete_bulk_customer'),
    path('', include(router.urls)),
]
