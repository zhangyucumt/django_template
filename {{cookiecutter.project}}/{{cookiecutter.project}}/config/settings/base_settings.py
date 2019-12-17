"""
Django settings for {{cookiecutter.project}} project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from kombu import Queue, Exchange

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mh&z3_bcs%i#2l$s-6kdk#+6j#wc*&o@j9b#8hbqr5v5$=4vba'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_celery_results',
    'corsheaders',
    "rest_framework",
    "django_celery_beat",
    "rest_framework_swagger",
    "django_filters",
]

LOCAL_APPS = [
    '{{cookiecutter.project}}.apps.user.apps.UserConfig'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    '{{cookiecutter.project}}.middleware.logging.LoggingMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = '{{cookiecutter.project}}.config.urls'

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

WSGI_APPLICATION = '{{cookiecutter.project}}.config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': '{{cookiecutter.project}}.paginations.PageNumberPagination',
    'PAGE_SIZE': 20,
    'UNICODE_JSON': False,
    'COERCE_DECIMAL_TO_STRING': False,
    'EXCEPTION_HANDLER': '{{cookiecutter.project}}.exception.handler.exception_handler',
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_SCHEMA_CLASS': '{{cookiecutter.project}}.schema.CustomerSchema',
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/second',
        'user': '30/second'
    }
}

SWAGGER_SETTINGS = {
    'is_authenticated': True
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = 'Y-m-d'

DATETIME_FORMAT = 'Y-m-d H:i:s'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

# [celery]
CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = "amqp://admin:admin@localhost:5672/ci"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = "django-db"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 28800}

# QUEUE related
CELERY_QUEUES = [
    # Queue('default', exchange=Exchange('default', type='direct'), routing_key='default'),
    Queue('{{cookiecutter.project}}', exchange=Exchange('topic', type='topic'), routing_key='{{cookiecutter.project}}.#'),
]
CELERY_TASK_DEFAULT_QUEUE = '{{cookiecutter.project}}'
CELERY_TASK_DEFAULT_EXCHANGE = 'topic'
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_TASK_DEFAULT_ROUTING_KEY = '{{cookiecutter.project}}.#'


# task route
def route_task(name, *args, **kwargs):
    return {'exchange': 'topic', 'exchange_type': 'topic', 'routing_key': '{{cookiecutter.project}}.default'}


CELERY_ROUTES = route_task
