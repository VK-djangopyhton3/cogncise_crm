from rest_framework import routers
from django.urls import path, include
from job.views.api_views import *

app_name='job'
router = routers.DefaultRouter()
router.register(r'', JobViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
]
