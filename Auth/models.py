import datetime
import hashlib
import random
import re
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):

        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=False,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)

        user.set_password(password)

        user.email = "%s" % (user.email)

        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        user = self._create_user(email, password, False, False, **extra_fields)
        user.is_active = True

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password,)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.is_active = True

        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    NONE = 'NO'
    ATT = 'AT'
    VERIZON = 'VE'
    SPRINT = 'SP'
    TMOBILE = 'TM'
    VIRGIN = 'VM'
    CINGULAR = 'CI'
    CARRIER_CHOICES = (
        (NONE, 'None'),
        (ATT, 'AT&T'),
        (VERIZON, 'Verizon'),
        (SPRINT, 'Sprint'),
        (TMOBILE, 'T-Mobile'),
        (VIRGIN, 'Virgin-Mobile'),
        (CINGULAR, 'Cingular'),
    )

    username  = models.CharField(max_length=254, unique=False)
    email     = models.EmailField(blank=True, unique=True)
    cell      = models.CharField(max_length=20, unique=False, blank=True, verbose_name='(Optional) Cell #')
    verified  = models.BooleanField(default=False)
    carrier = models.CharField(max_length=2, choices=CARRIER_CHOICES, default='NONE', verbose_name='(Optional) Carrier')
    alias   = models.CharField(max_length=15, unique=False, blank=True, verbose_name='(Optional) Alias')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    date_updated = models.DateField(default=timezone.now)
    is_active   = models.BooleanField(default=True)
    is_admin    = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)
    

    def get_short_name(self):
        "Returns the short name for the user."
        return self.alias
    

    def get_full_name(self):
            return "%s" % ( self.email )
        

    def __unicode__(self):
        email = "No email set for this account"
        
        if hasattr(self, 'email'):
            email = self.email
            
        return email
    

    def __unicode__(self):
        email = "No email set for this account"
        
        if hasattr(self, 'email'):
            email = self.email
            
        return email
    

    def update_user_settings(self):
        threshold = datetime.timedelta(days=30)
            
                
    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
        


