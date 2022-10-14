import os
from datetime import timedelta

from .base import *

SECRET_KEY = 'Ec?Xz5n@%L@jZs_ZpS7VyZfn+h!&2KkT-t8DsqS#H+p4Hcxj^C_euNw-nKLLxse@jpN?=+b?p%uJ^!Y8'

DEBUG = True

if DEBUG:
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
    INSTALLED_APPS = ["debug_toolbar"] + INSTALLED_APPS

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static",]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_prod')

# dj-rest-auth and allauth config
ACCOUNT_AUTHENTICATION_METHOD='email'
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_EMAIL_VERIFICATION='mandatory'
ACCOUNT_ADAPTER='users.adapters.CustomAccountAdapter'
SITE_ID = 1
ACCOUNT_LOGOUT_ON_GET = False
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False

AUTHENTICATION_BACKENDS = [
    # needed to login by username in Django admin, regardless of allauth
    'django.contrib.auth.backends.ModelBackend',
    # allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# rest framework config
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
     'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'EXCEPTION_HANDLER': 'utils.custom_exception_response.handler'
}


REST_USE_JWT = True
JWT_AUTH_COOKIE = 'access'
JWT_AUTH_REFRESH_COOKIE = 'refresh'


# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
}

#email config
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Stripe
STRIPE_PUBLISHABLE_KEY = os.environ.get('VEETA_STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.environ.get('VEETA_STRIPE_SECRET_KEY')
STRIPE_ENDPOINT_SECRET = os.environ.get('STRIPE_ENDPOINT_SECRET')
STRIPE_FRONTEND_DOMAIN_URL = 'http://localhost:3000/'
STRIPE_LIVE_MODE = False  # Change to True in production

# celery
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

PROTOCOL='http'
FRONTEND_DOMAIN_URL='localhost:3000'
ADMIN_EMAIL=['mazindev.tech@mail.com']
DEFAULT_FROM_EMAIL='Veeta <no-reply@veeta.co.uk>'

# CORS
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "content-disposition",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "access-control-allow-origin"
]

FAIL_SILENTLY = False
DEFAULT_FROM_EMAIL='Veeta <no-reply@veeta.co.uk>'

# TWILIO
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SERVICE_ID = os.getenv('TWILIO_VERIFY_SERVICE_ID')

# Sites Framework
SITE_ID = 1

# Set testing mode
TESTING = True
SERVER_ALIAS = 'Testing Environment Server'

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}
