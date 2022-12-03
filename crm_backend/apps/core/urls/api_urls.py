from rest_framework import routers
from django.urls import path, include
from core.views.api_views import *

app_name='core'
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/', include(router.urls)),
    path('auth/login/', LoginAPIView.as_view(), name='auth_login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='auth_logout'),
    path('auth/roles/', RoleListView.as_view(), name='roles'),
    # path('auth/profile/', RetrieveUpdateProfileAPIView.as_view(), name='auth_profile'),
]
