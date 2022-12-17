from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.contrib.auth.models import Group as BaseGroup
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.template.defaultfilters import slugify
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
import pyotp, random
from datetime import timedelta

from common.app_utils import profile_unique_upload
from core.managers import UserManager as CustomeUserManager
from core.abstract_models import BaseModel

BaseGroup.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))
BaseGroup.add_to_class('slug', models.SlugField(max_length=50, unique=True, null=True, editable=False))

class Group(BaseGroup):

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        proxy = True


    @classmethod
    def company_admin(cls):
        return cls.objects.filter(slug='company-admin').last()

    @classmethod
    def customer(cls):
        return cls.objects.filter(slug='customer').last()

    @classmethod
    def get_group_obj(cls, group_id):
        return cls.objects.filter(id=group_id).last()

    @property
    def role_name(self):
        return self.__str__()

    # def save(self, *args, **kwargs):
    #     super(Group, self).save(*args, **kwargs)
    #     if not self.slug:
    #         self.slug = slugify(self.name)  # type: ignore
    #         self.save()

    def __str__(self):
        return self.name


class AbstractCUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Email and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },  
    )

    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomeUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

        is_company = self.is_company    # type: ignore
        is_cogncise = self.is_cogncise  # type: ignore
        is_customer = self.is_customer  # type: ignore
        
        if not self.is_superuser:
            if (is_company and is_customer):
                raise ValidationError(_("Not acceptable multiple types of user selection, needs to single selection."))
            
            if (not is_company and not is_customer and not is_cogncise):
                raise ValidationError(_("Either is_company, is_cogncise or is_customer must be checked."))

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractCUser, BaseModel):
    """
    Users within the Django authentication system are represented by this
    model.

    Password and email are required. Other fields are optional.
    """
    created_by = models.ForeignKey('self', on_delete=models.CASCADE, related_name='user_created_by', null=True, blank=True)
    mobile_number = PhoneNumberField(_('mobile number'), blank=True, null=True)

    is_company = models.BooleanField(_('Company User'), default=False, help_text=_('Designates whether this user should be treated as company user. '), )
    is_customer = models.BooleanField(_('Customer User'), default=False, help_text=_('Designates whether this user should be treated as customer user. '), )
    is_cogncise = models.BooleanField(_('Cogncise User'), default=False, help_text=_('Designates whether this user should be treated as cogncise staff user. '), )

    profile_pic = models.ImageField(upload_to=profile_unique_upload, null=True, blank=True)
    
    company   = models.ForeignKey('company.Company', related_name="user_company", on_delete=models.CASCADE, null=True, blank=True)

    class Meta(AbstractCUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    @property
    def role(self):
        return self.groups.last() and self.groups.last().id
    
    @property
    def role_obj(self):
        return self.groups.last() and self.groups.last()

    @property
    def role_name(self):
        return self.groups.last() and self.groups.last().name

    @classmethod
    def create_company_admin(cls, **kwargs):
        kwargs.update({ 'is_company':True})
        user = cls.objects.filter(email = kwargs['email']).last()
        if user is not None: 
            return user
        if 'username' not in kwargs:
            kwargs.update({ 'username': kwargs['email'] })
        owner = cls.objects.create(**kwargs)
        role = Group.company_admin() and Group.company_admin().id
        owner.groups.add(role)
        owner.save()
            
        return owner


    @classmethod
    def create_customer(cls, **kwargs):
        kwargs.update(kwargs.get('user', None))
        kwargs.pop('user', None)
        kwargs.update({'is_company': True, 'is_customer': True })
        if 'username' not in kwargs:
            kwargs.update({ 'username': kwargs['email'] })
        customer = cls.objects.create(**kwargs)
        role = Group.customer() and Group.customer().id
        customer.groups.add(role)
        customer.save()
            
        return customer


class OTPVerify(BaseModel):
    user = models.OneToOneField( User, on_delete=models.CASCADE, editable=False, related_name='user_otp', null=True, blank=True)

    email = models.EmailField(
        _('email address'),
        unique=True, blank=True, null=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )

    mobile_number = PhoneNumberField(_('mobile number'), error_messages={ 'unique': _("A user with that mobile number already exists."),}, blank=True, null=True, unique=True)
    # otp = models.CharField(editable=False, default=False, max_length=6) #storing otp
    mobile_counter_secret = models.IntegerField(editable=False, default=0) # storing counter
    email_counter_secret = models.IntegerField(editable=False, default=0) # storing counter
    email_mfa_secret = models.CharField(_('email mfa secret'), editable=False, max_length=40, default=pyotp.random_base32())
    mobile_mfa_secret = models.CharField(_('mobile mfa secret'), editable=False, max_length=40, default=pyotp.random_base32())
    is_used = models.BooleanField(default=False) #default is True when not using otp is used
    is_verified = models.BooleanField(default=False) #default is True when not using otp email or mobile verification
    is_registered = models.BooleanField(default=False) #default is True when not using otp email or mobile verification
    otp_created_at = models.DateTimeField(auto_now=True, db_index=True)

    sms_api_response = models.JSONField(null=True)
    is_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email or self.mobile_number.as_e164


    # Generating and sending OTP
    def generate_and_send_otp(self, otp_type):
        # set interval(time of the otp expiration) according to your need in seconds.
        # totp = pyotp.TOTP(mfa_secret, interval=settings.OTP_EXPIRATION_TIME_IN_SECONDS)

        email_counter_secret = random.randint(1000 , 9999)
        # email otp
        hotp = pyotp.HOTP(self.email_mfa_secret)
        email_otp = hotp.at(email_counter_secret)
        
        #mobile otp
        mobile_counter_secret = random.randint(1000 , 9999)
        hotp = pyotp.HOTP(self.mobile_mfa_secret)
        mobile_otp = hotp.at(mobile_counter_secret)
        # Saving otp in db
        # self.otp = otp
        self.mobile_counter_secret = mobile_counter_secret
        self.email_counter_secret = email_counter_secret
        self.is_used = False
        self.is_verified = False

        # Sending OTP on email or mobile
        response = send_otp(self, email_otp, mobile_otp, otp_type)

        if response['is_sent']:
            self.is_sent = response['is_sent']
            self.sms_api_response = response
        else:
            self.is_sent = response['is_sent']
            self.sms_api_response = response

        self.save()
        
        return self


    # verifying OTP
    def verify_otp(self, email_otp, mobile_otp, otp_instance):
        email_hotp = pyotp.HOTP(otp_instance.email_mfa_secret)
        mobile_hotp = pyotp.HOTP(otp_instance.mobile_mfa_secret)
        answer = email_hotp.verify(email_otp, otp_instance.email_counter_secret)
        answer = mobile_hotp.verify(mobile_otp, otp_instance.mobile_counter_secret)

        if self.is_otp_expired()['is_expired']:
            answer = False

        # Saving otp in db
        self.is_used = True
        self.save()
        return answer


    # otp checker if otp expired or not
    def is_otp_expired(self):
        data = {}
        time_elapsed = timezone.now() - self.otp_created_at
        left_time = timedelta(seconds=settings.OTP_EXPIRATION_TIME_IN_SECONDS) - time_elapsed

        is_expired = False
        if left_time < timedelta(seconds=0):
            is_expired = True
            data.update({'message':"OTP is expired!"})
            
        data.update({'is_expired': is_expired})

        return data

