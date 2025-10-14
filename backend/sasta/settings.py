import os
# flake8: noqa: F403
from sasta.common_settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application settings
SECRET_KEY = 'kxreeb3bds$oibo7ex#f3bi5r+d(1x5zljo-#ms=i2%ih-!pvn'
DEBUG = True
ROOT_URLCONF = 'sasta.urls'

# Connectivity
WSGI_APPLICATION = 'sasta.wsgi.application'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(' ')
ALLOWED_HOSTS += ['localhost', '127.0.0.1']

# DRF
# Use defaults

# Alpino
ALPINO_HOST = os.environ.get('ALPINO_HOST', 'localhost')
ALPINO_PORT = 7001
CORPUS2ALPINO_LOG_DIR = '.logs'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("SQL_DATABASE", "sasta"),
        "USER": os.environ.get("SQL_USER", "sasta"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "sasta"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Auth
SITE_NAME = 'SASTA'
HOST = 'localhost:8000'
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Celery
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'django_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'when': 'd',
            'interval': 1,
            'backupCount': 0
        },
        'sasta_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'sasta.log'),
            'formatter': 'standard'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s\t%(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django_file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['django_file'],
            'level': 'INFO',
            'propagate': False
        },
        'sasta': {
            'handlers': ['sasta_file', 'console'],
            'level': 'INFO',
            'propagate': True
        },
        'sastadev': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False
        }
    },
}
