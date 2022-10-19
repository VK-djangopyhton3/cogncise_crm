from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['company'] ={}
        # Add custom claims
        token['name'] = user.name
        token['company']['name'] = user.userroles.company.company_name
        token['company']['role'] = user.userroles.role
        token['email'] = user.email
        token['phone'] = user.phone
        token['is_verified'] = user.is_verified
        token['is_staff'] = user.is_staff

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
