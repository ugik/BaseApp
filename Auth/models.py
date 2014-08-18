from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """ Creates and saves a user with the given email/password
        """
        now = str(datetime.now().time())
        if not email:
            raise ValueError('Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

class CustomUser(AbstractBaseUser):
    NONE = 'NO'
    ATT = 'AT'
    VERIZON = 'VE'
    SPRINT = 'SP'
    TMOBILE = 'TM'
    CARRIER_CHOICES = (
        (NONE, 'None'),
        (ATT, 'AT&T'),
        (VERIZON, 'Verizon'),
        (SPRINT, 'Sprint'),
        (TMOBILE, 'T-Mobile'),
    )

    username  = models.CharField(max_length=254, unique=False)
    email     = models.EmailField(blank=True, unique=True)
    cell      = models.CharField(max_length=20, unique=False, blank=True, verbose_name='(Optional) Cell # eg.6171231234')
    verified  = models.BooleanField(default=False)
    carrier = models.CharField(max_length=2, choices=CARRIER_CHOICES, default='NONE', verbose_name='(Optional) Carrier')
    alias   = models.CharField(max_length=15, unique=False, blank=True, verbose_name='(Optional) Alias')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])


