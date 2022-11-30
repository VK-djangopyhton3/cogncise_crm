import django
from django import forms
from django.contrib.auth import (authenticate, get_user_model, password_validation)
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from django import forms

from core.models import UserDetails
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm


User = get_user_model()

