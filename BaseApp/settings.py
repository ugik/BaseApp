"""
Django settings for BaseApp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ni%88vb-9ne_++$dwm)v@g!jum^*tv^@2uva*6vzx21act$fq)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Template directories
TEMPLATE_DIRS = (
	BASE_DIR+'/templates',
	BASE_DIR+'/Auth/templates',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap_toolkit',
    'Auth',
)

AUTH_USER_MODEL = "Auth.CustomUser"
AUTHENTICATION_BACKENDS = ("Auth.backends.CustomUserAuth",)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'BaseApp.urls'

WSGI_APPLICATION = 'BaseApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# grab email pw from parent directory (not in repo)
# this is work-around until figure out how to set env vars on EC2 instance
PARENT_DIR = os.path.abspath(os.path.dirname(__file__) + "/../../")
fname = PARENT_DIR+'/.email'
if os.path.isfile(fname):
	EMAIL_HOST_PASSWORD = open(fname, 'r').read()[:16]
else:
	EMAIL_HOST_PASSWORD = ""

# gmail SMTP setup
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ugikma@gmail.com'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# Media files
MEDIA_ROOT = BASE_DIR+'/static'

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = ''
STATIC_URL = '/static/'

try:
    from local_settings import *
except ImportError:
    pass

