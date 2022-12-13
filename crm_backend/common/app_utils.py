import datetime, uuid
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import requests, json, pyotp, uuid, secrets, random
import urllib.request
import urllib.parse

# timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def unique_media_upload(instance, filename):
    ext = filename.split('.').pop()
    return f"images/{instance._meta.model_name}/{uuid.uuid4().hex[:6]}.{ext}"


def profile_unique_upload(instance, filename):
    ext = filename.split('.').pop()
    return f"images/profiles/{instance._meta.model_name}/{uuid.uuid4().hex[:6]}.{ext}"


def logo_media_upload(instance, filename):
    ext = filename.split('.').pop()
    return f"images/{instance._meta.model_name}/{instance.abn}.{ext}"


def send_email(email, title, context, email_html_message, email_plaintext_message):
    email_html_message = render_to_string(email_html_message, context)
    email_plaintext_message = render_to_string(email_plaintext_message, context)
    msg = EmailMultiAlternatives(
        # title:
        title,
        # message:
        email_plaintext_message,
        # from:
        settings.DEFAULT_FROM_EMAIL,
        # to:
        [email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


"""This method is used to send sms when send otp. """
def send_sms(apikey, numbers, sender, message):
    response = {}
    try:
        params ={'apikey': apikey, 'numbers': numbers, 'message' : message, 'sender': sender}
        url = 'https://api.textlocal.in/send/?'
        response = requests.post(url+urllib.parse.urlencode(params))

        return response.json()
    except Exception as e:
        response['sms_response'] = {'errors': str(e)}
        return response


def send_otp(instance,  email_otp, mobile_otp, otp_type):
    print(email_otp)
    print(mobile_otp)
    is_sent = False
    data = {}
    try:
        expire_time_in_minute = int(settings.OTP_EXPIRATION_TIME_IN_SECONDS/60)

        if instance.mobile_number:
            sender = 'FINZIP'
            otp_transaction_type = {1:"Login", 2:"SignUp", 3:"Other"}

            if otp_type:
                transaction_type = otp_transaction_type[otp_type]
            else:
                transaction_type = 'Login'


            message = f'Welcome to Finzip!%nOTP for {transaction_type} Transaction is {mobile_otp} and valid for {expire_time_in_minute} minutes. Do not share this OTP to anyone for security reasons. -Finzip'

            # message = f'{otp} is your one time password to proceed on FinZip. It is valid for {expire_time_in_minute} minutes. Do not share your OTP with anyone for security reasons. -Finzip'

            data['sms_response'] = send_sms(settings.API_KEY_TEXT_LOCAL, instance.mobile_number.as_e164, sender, message)

            is_sent = True
            if 'errors' in  data['sms_response']:
                is_sent = False

        if instance.email:
            email_html_message = "email/otp_email.html"
            email_plaintext_message = "email/otp_email.txt"
            title = f'OTP from FinZip'
            context = {"user": instance, "otp" : email_otp, "expire_time_in_minute" : expire_time_in_minute}
            send_email(instance.email, title, context, email_html_message, email_plaintext_message)
            data.update({'source':"email"})
            is_sent = True


    except Exception as e:
        # to do integrate logger
        pass

    data.update({"is_sent": is_sent})
    return data


