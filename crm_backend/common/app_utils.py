from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import requests, json, uuid, secrets, random
import urllib.request
import urllib.parse


def unique_media_upload(instance, filename):
    ext = filename.split('.').pop()
    return f"images/{instance._meta.model_name}/{uuid.uuid4().hex[:6]}.{ext}"


def profile_unique_upload(instance, filename):
    ext = filename.split('.').pop()
    return f"images/profiles/{instance._meta.model_name}/{uuid.uuid4().hex[:6]}.{ext}"
