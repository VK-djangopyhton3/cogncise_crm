from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.contrib.auth.models import Group as BaseGroup
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

from common.app_utils import profile_unique_upload
from core.managers import UserManager as CustomeUserManager
from core.abstract_models import BaseModel

class Role(BaseModel):
      
    CATEGORY_CHOICES = (
      (1, 'Cogncise'),
      (2, 'Company'),    
    )

    category = models.PositiveSmallIntegerField(_('role category'), choices=CATEGORY_CHOICES, default=1)
    name = models.CharField(_('name'), max_length=50)
    slug  = models.SlugField(max_length=50, unique=True, null=True, blank=True, editable=False)

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    @classmethod
    def company_admin(cls):
        return cls.objects.filter(slug='CompanyAdmin').last()

    def get_role_name(self):
        return f"{self.get_category_display()} {self.name}"

    def save(self, *args, **kwargs):
        super(Role, self).save(*args, **kwargs)
        if not self.slug:

            self.slug = f'{self.get_category_display().capitalize()}{self.name.capitalize()}'  # type: ignore
            self.save()

    def __str__(self):
        return f"{self.get_category_display()} {self.name}"  # type: ignore

    
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
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

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
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_role', null=True)
    mobile_number = PhoneNumberField(_('mobile number'), blank=True, null=True)

    is_company = models.BooleanField(_('Company User'), default=False, help_text=_('Designates whether this user should be treated as company user. '), )
    is_customer = models.BooleanField(_('Customer User'), default=False, help_text=_('Designates whether this user should be treated as customer user. '), )
    is_cogncise = models.BooleanField(_('Cogncise User'), default=False, help_text=_('Designates whether this user should be treated as cogncise staff user. '), )

    profile_pic = models.ImageField(upload_to=profile_unique_upload, null=True, blank=True)

    class Meta(AbstractCUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username
    
    @classmethod
    def create_company_admin(cls, **kwargs):
        user = cls.objects.filter(email = kwargs['email']).last()
        if user is not None: return user

        kwargs.update({ 'role': Role.company_admin(), 'is_company': True, 'username': kwargs['email'] })
        return cls.objects.create(**kwargs)


class Group(BaseGroup):
    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        proxy = True
