from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
