"""
Django settings for esoe_oop_judge project.
Generated by 'django-admin startproject' using Django 1.9.2.
For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config

from django.contrib.messages import constants as messages


# Django's own debug mode (here, we let it be the same as config.DEBUG)
DEBUG = config.DEBUG


# Web base directory
BASE_DIR = config.WEB_DIR


# Deployment
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
SECRET_KEY = config.WEB_SECRET_KEY
ALLOWED_HOSTS = config.WEB_ALLOWED_HOSTS


# Application settings
INSTALLED_APPS = [
    'judge.apps.JudgeConfig',
    'widget_tweaks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'esoe_oop_judge.urls'

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

WSGI_APPLICATION = 'esoe_oop_judge.wsgi.application'


# Database settings
# See https://docs.djangoproject.com/en/1.9/ref/settings/#databases
if config.DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(config.WEB_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config.DB_NAME,
            'USER': config.DB_USER,
            'PASSWORD': config.DB_PASSWORD,
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

DATETIME_FORMAT='Y-m-d H:i:s'

USE_I18N = False
USE_L10N = False
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(config.WEB_HTDOCS_DIR, 'static')

STATICFILES_DIRS = [config.JUDGE_STATIC_DIR]


# Miscellaneous settings
LOGIN_URL = 'judge:login'
LOGIN_REDIRECT_URL = 'judge:index'
LOGOUT_URL = 'judge:logout'

MESSAGE_TAGS = {
    messages.SUCCESS: 'alert-success',
    messages.ERROR: 'alert-danger',
}
