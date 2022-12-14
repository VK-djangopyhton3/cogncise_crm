from rest_framework import routers
from django.urls import path, include
from company.views.api_views import *

app_name='company'
router = routers.DefaultRouter()
router.register(r'', CompanyViewSet, basename='company')

urlpatterns = [
    path('statuses/', CompanyStatusListAPIView.as_view(), name='statuses'),
    path('', include(router.urls)),
]
