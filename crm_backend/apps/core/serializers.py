from common.common_serilizer_imports import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)


    # def validate_password(self, value: str) -> str:
    #     """
    #     Hash value passed by user.

    #     :param value: password of a user
    #     :return: a hashed version of the password
    #     """
    #     return make_password(value)

    class Meta:
        model = User
        fields = ['username', 'role', 'email', 'first_name', 'last_name', 'mobile_number', 'password']

        extra_kwargs = {'role': {'required': True}} 


class LoginSerializer(serializers.ModelSerializer):
    # email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=True, style={"input_type": "password"})
    
    class Meta:
        model = User
        fields = ["username", "password"]


class ShowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "auth_token", "profile_pic"]
        read_only_fields = ["id", "username", "email", "auth_token"]

class UserProfileSerializer(serializers.ModelSerializer):
    """
    UserShowSerializer is a model serializer which shows the attributes
    of a user.
    """

    # mobile_number = PhoneNumberField(region="IN")

    class Meta:
        """Passing model metadata"""
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "auth_token", "profile_pic"]
        read_only_fields = ["id", "username", "email", "auth_token"]



class CheckUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["email", "username"]