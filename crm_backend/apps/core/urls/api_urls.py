from rest_framework import routers
from django.urls import path, include
from core.views.api_views import *

app_name='core'
router = routers.DefaultRouter()

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='auth_login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='auth_logout'),
    path('auth/roles/', RoleListView.as_view(), name='roles'),
    path('auth/', include(router.urls)),
    path('auth/otp/login/', OTPLoginAPIView.as_view(), name='otp_login'),
    path('auth/send-otp/', SendOTPView.as_view(), name='auth_send_otp'),
]
