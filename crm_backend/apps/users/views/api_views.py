from common.common_view_imports import *
from django.contrib.auth import get_user_model

from shared.serializers import BulkDeleteSerilizer
from shared.views import CrudViewSet, BulkDeleteAPIView
from users.serializers import UserSerializer

User = get_user_model()

class UserViewSet(CrudViewSet):
    swagger_tag = ['users']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['username', 'first_name', 'last_name', 'email', 'mobile_number']
    ordering_fields = ['username', 'first_name', 'last_name', 'email', 'mobile_number']
    filterset_fields = ['is_company', 'is_customer', 'is_cogncise']
    
    def get_queryset(self):
        self.queryset = self.queryset.filter(companies=self.company)  # type: ignore
        return self.queryset


class UsersBulkDeleteAPIView(BulkDeleteAPIView):
    swagger_tag = ['users']
    queryset = User.objects.all()
    serializer_class = BulkDeleteSerilizer
