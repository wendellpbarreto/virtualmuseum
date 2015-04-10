#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Global name to project
PROJECT_NAME = 'virtualmuseum'
PROJECT_NAME_READABLE = 'Museu Virtual'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xow__e#dg_s2g&@tgp+ounvn*k$u1k8b#9f8pg)7bcic$jt^i*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli.dashboard',
    'grappelli',
    'redactor',
    'sorl.thumbnail',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'virtualmuseum.apps.core',
    'virtualmuseum.apps.accounts'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
)

ROOT_URLCONF = '%s.urls' % PROJECT_NAME

WSGI_APPLICATION = '%s.wsgi.application' % PROJECT_NAME


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': '%s_db' % PROJECT_NAME,                              
        'USER': '%s_admin' % PROJECT_NAME,
        'PASSWORD': 'q1IUilS14,747Qx',
        'HOST': 'localhost',                                
        'PORT': '',    
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LOCALE = 'pt_BR'

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Additional locations of template files

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, PROJECT_NAME, 'templates'),

)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Additional locations of static files

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, PROJECT_NAME, 'assets'),
)


# Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Media news files

MEDIA_PART_IMAGE_ROOT = os.path.join(MEDIA_ROOT, 'part', 'image')
MEDIA_PART_AUDIO_ROOT = os.path.join(MEDIA_ROOT, 'part', 'audio')
MEDIA_PART_VIDEO_ROOT = os.path.join(MEDIA_ROOT, 'part', 'video')
MEDIA_PART_DOCUMENT_ROOT = os.path.join(MEDIA_ROOT, 'part', 'document')
MEDIA_INTERVENTION_ROOT = os.path.join(MEDIA_ROOT, 'intervention')
MEDIA_SUBSCRIPTION_ROOT = os.path.join(MEDIA_ROOT, 'subscription')

# Admin tittle

GRAPPELLI_ADMIN_TITLE = u'Museu Virtual'


# Dashboard

GRAPPELLI_INDEX_DASHBOARD = 'fotec.dashboard.CustomIndexDashboard'


# Redactor config

REDACTOR_OPTIONS = {'lang': 'en'} 
REDACTOR_UPLOAD = os.path.join(MEDIA_ROOT, 'upload')


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '%s.apps.accounts' % PROJECT_NAME: {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
        '%s.apps.core' % PROJECT_NAME: {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
        '%s.apps.frontend' % PROJECT_NAME: {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}
