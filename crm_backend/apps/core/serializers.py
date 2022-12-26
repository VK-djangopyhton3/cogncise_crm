from django.db.models import Q
from common.common_serilizer_imports import *
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from core.models import Group, ROLE_TYPES

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    role = serializers.IntegerField()


    # def validate_password(self, value: str) -> str:
    #     """
    #     Hash value passed by user.

    #     :param value: password of a user
    #     :return: a hashed version of the password
    #     """
    #     return make_password(value)

    class Meta:
        model = User
        fields = ["username", "role", "email", "first_name", "last_name", "mobile_number", "password", "is_company", "is_customer", "is_cogncise"]
        read_only_fields = ['deleted_at', 'is_deleted']
        extra_kwargs = {"role": {"required": True}}


    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        # group = Group.get_group_obj(role)
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.groups.add(role)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    # username = serializers.CharField(required=False)
    password = serializers.CharField(required=True, style={"input_type": "password"})
    
    class Meta:
        model = User
        fields = ["email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "mobile_number", "first_name", "last_name", "profile_pic", "role_name", "last_login"]
        read_only_fields = ["id", "username", "email", "role_name", "last_login", 'deleted_at', 'is_deleted']


class ShowUserSerializer(serializers.ModelSerializer):
    """
    UserShowSerializer is a model serializer which shows the attributes
    of a user.
    """

    # mobile_number = PhoneNumberField(region="IN")

    class Meta:
        """Passing model metadata"""
        model = User
        fields = ["id", "username", "email", "mobile_number", "first_name", "last_name", "profile_pic", "role_name", "role_type", "last_login", "auth_token", "is_cogncise", "is_customer", "is_company", "company_id"]
        read_only_fields = ["id", "username", "email", "auth_token"]


class CheckUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["email", "username"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "slug", "role_name"]


class OTPLoginSerializer(serializers.Serializer):
    role_type = serializers.ChoiceField(required=True, choices=(('customer', 'customer'), ('field_worker', 'field_worker')))
    email = serializers.EmailField(required=False)
    mobile_number = PhoneNumberField(region="AU", required=False)
    otp = serializers.CharField(required=True, min_length=6, max_length=6)

    def validate(self, data):
        email = data.get("email", None)
        mobile_number = data.get("mobile_number", None)
        if not email and not mobile_number:
            raise serializers.ValidationError("Either email or mobile must be required field.")

        user = self.get_model_object(data)

        if not user:
            raise serializers.ValidationError("User does not exist with that mobile or email, please register now!")

        return data
    
    def get_model_object(self, data):
        return User.objects.filter(Q(role_type=data.get('role_type', None)) and (Q(mobile_number=data.get('mobile_number', None)) | Q(email__iexact=data.get('email')))).first()

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile_number = PhoneNumberField(region="IN", required=False)
    otp_type = serializers.ChoiceField(required=True, choices=((1, 'Login'), (2, 'SignUp')))


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile_number = PhoneNumberField(region="IN", required=False)
    email_otp = serializers.CharField(required=True, min_length=6, max_length=6)
    mobile_otp = serializers.CharField(required=True, min_length=6, max_length=6)

    def validate(self, data):
        email = data.get("email", None)
        mobile_number = data.get("mobile_number", None)
        if not email and not mobile_number :
            raise serializers.ValidationError("Either email or mobile must be required field.")
        return data
