"""
Django settings for crystallake project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""


from pathlib import Path
from os import environ, path
from django.urls import reverse_lazy

import webpack_loader

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get("KEY")

# SECURITY WARNING: don't run with debug turned on in production!
if 'true' in environ.get("DEV", "false").lower():
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = [environ.get("CUSTOM_HOST", "localhost"), '192.168.1.57']


# Application definition

INSTALLED_APPS = [
    'webpack_loader',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polymorphic',
    'django_crontab',
    'apps.offer.apps.OfferConfig',
    'apps.room.apps.RoomConfig',
    'apps.service.apps.ServiceConfig',
    'apps.photo.apps.PhotoConfig',
    'apps.order.apps.OrderConfig',
    'apps.core.apps.CoreConfig',
    'apps.user.apps.UserConfig',
    'apps.tag.apps.TagConfig',
    'apps.client.apps.ClientConfig',
    'apps.worker.apps.WorkerConfig',
    'apps.group.apps.GroupConfig',
    'apps.client_profile.apps.ClientProfileConfig',
    'apps.worker_profile.apps.WorkerProfileConfig',
    'django_cleanup.apps.CleanupConfig',
]

AUTH_USER_MODEL = 'user.CustomUser'

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '',
        'STATS_FILE': path.join(BASE_DIR, 'frontend/webpack-stats.json'),
    },
}

CRONJOBS = [
    ('0 * * * *', 'apps.core.cron.clean_orders_job')
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crystallake.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'crystallake.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql',
        "NAME": environ.get("DB_NAME"),
        "USER": environ.get("DB_USER"),
        "PASSWORD": environ.get("DB_PASSWORD"),
        "HOST": "db",
        "PORT": "5432"
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Irkutsk'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []

MEDIA_URL = 'media/'
MEDIA_ROOT = path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTH SETTINGS
LOGOUT_REDIRECT_URL = reverse_lazy('index')
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend', 'django.contrib.auth.backends.AllowAllUsersModelBackend']

try:
    from .additional_settings.sms_settings import *
except ImportError:
    pass

try:
    from .additional_settings.rooms_settings import *
except ImportError:
    pass

try:
    from .additional_settings.pagination_settings import *
except ImportError:
    pass

