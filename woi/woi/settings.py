"""
Django settings for woi project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

from django.contrib.messages import constants as messages

from .env_helper import Configuration


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

config = Configuration(BASE_DIR / '.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get(
    'SECRET_KEY',
    default='insecure-7i&o9yus94kagc*_z1t2q9v&*_lpp2sx4f0q%jurb=kqwf(((3'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get('DEBUG', default=False)

ALLOWED_HOSTS = config.get('ALLOWED_HOSTS', default=list)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
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

ROOT_URLCONF = 'woi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.processors.add_woi_variables',
            ],
        },
    },
]

WSGI_APPLICATION = 'woi.wsgi.application'

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = config.get('STATIC_ROOT', default=BASE_DIR / 'static')
STATIC_URL = config.get('STATIC_URL', default='static/')

MEDIA_ROOT = config.get('MEDIA_ROOT', default=BASE_DIR / 'media')
MEDIA_URL = config.get('MEDIA_URL', default='media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# WoI settings
WOI_TITLE = ''
WOI_SUBTITLE = ''
WOI_COMMENT_DELETED_MESSAGE = ''
WOI_FOOTER = True
WOI_FEEDS = True
WOI_PREVIEW_TIMEOUT_MS = 1000
WOI_CONTENT_LICENSE = {
    'url': 'https://creativecommons.org/licenses/by-nd/4.0/legalcode',
    'text': 'CC BY-ND 4.0',
}
WOI_GOOGLE_ANALYTICS_ID = config.get('WOI_GOOGLE_ANALYTICS_ID', default='')
