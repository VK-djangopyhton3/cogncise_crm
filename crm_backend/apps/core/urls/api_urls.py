from rest_framework import routers
from django.urls import path, include
from core.views.api_views import *

app_name='core'
router = routers.DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='auth_login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='auth_logout'),
    path('auth/roles/', RoleListView.as_view(), name='roles'),
    # path('auth/users/bulk-delete/', UsersBulkDeleteAPIView.as_view(), name='delete_bulk_user'),
    path('auth/', include(router.urls)),
    # path('auth/profile/', RetrieveUpdateProfileAPIView.as_view(), name='auth_profile'),
]
