from rest_framework import routers
from django.urls import path, include
from property.views.api_views import *

app_name='property'
router = routers.DefaultRouter()
router.register(r'', PropertyViewSet, basename='property')

urlpatterns = [
    path('', include(router.urls)),
]
