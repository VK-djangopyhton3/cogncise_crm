from rest_framework import routers
from django.urls import path, include
from customer.views.api_views import *

app_name='customer'
router = routers.DefaultRouter()
router.register(r'', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
]
