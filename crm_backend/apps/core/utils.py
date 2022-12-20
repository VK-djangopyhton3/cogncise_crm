from django.contrib.auth import login, logout, user_logged_in, user_logged_out
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from core.models import OTPVerify
import pyotp


def login_user(request, user):
    token, _ = Token.objects.get_or_create(user=user)
    login(request, user)
    user_logged_in.send(sender=user.__class__, request=request, user=user)


def logout_user(request):
    Token.objects.filter(user=request.user).delete()
    user_logged_out.send(
        sender=request.user.__class__, request=request, user=request.user
    )
    logout(request)

def get_otp_instance(data):
    kwargs = {}
    user_data = {}

    if 'email' in data:
        kwargs = {'email': data.get('email')}
        user_data.update({'email': data.get('email')})
    
    if 'mobile_number' in data:
        kwargs = {'mobile_number': data.get('mobile_number')}
        user_data.update({'mobile_number': data.get('mobile_number')})

    otp_instance = None

    try:
        otp_instance = OTPVerify.objects.get(**kwargs)
        # logger.info(f'')
    except ObjectDoesNotExist:
        """if charge id does not exist then create user otp """
        user_data['email_mfa_secret'] = pyotp.random_base32()
        user_data['mobile_mfa_secret'] = pyotp.random_base32()
        otp_instance = OTPVerify.objects.create(**user_data)

    return otp_instance

