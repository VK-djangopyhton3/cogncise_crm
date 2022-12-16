from rest_framework import routers
from django.urls import path, include

from users.views.api_views import *

app_name='users'
router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('bulk-delete/', UsersBulkDeleteAPIView.as_view(), name='delete_bulk_user'),
    path('', include(router.urls))
]
