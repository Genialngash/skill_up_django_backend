import os
from datetime import timedelta

from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('RDS_DB_NAME'), 
        'USER': os.getenv('RDS_DB_MASTER_USERNAME'),
        'PASSWORD': os.getenv('RDS_DB_PASS'),
        'HOST': os.getenv('RDS_HOST'), 
        'PORT': 5432,
    }
}

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
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
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
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=45),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
}

# Stripe
STRIPE_PUBLISHABLE_KEY = os.environ.get('VEETA_STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.environ.get('VEETA_STRIPE_SECRET_KEY')
STRIPE_ENDPOINT_SECRET = os.environ.get('STRIPE_ENDPOINT_SECRET')
STRIPE_FRONTEND_DOMAIN_URL = 'https://veeta.co.uk'

#base url aka the frontend url => linked to the frontend
FRONTEND_DOMAIN_URL='veeta.co.uk'
PROTOCOL='https' #
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BROKER', 'redis://redis:6379/0')

CSRF_TRUSTED_ORIGINS=['https://api.veeta.co.uk']

# static files and media settings
# basic conf
AWS_ACCESS_KEY_ID = os.getenv('DJANGO_AWS_ACCESS_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

# Set the London Region
AWS_S3_REGION_NAME = "eu-west-2"

# s3 static settings
AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
STATICFILES_STORAGE = 'core.storage_backends.StaticStorage'

# public media
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'core.storage_backends.PublicMediaStorage'

# s3 private media settings
PRIVATE_MEDIA_LOCATION = 'private'
PRIVATE_FILE_STORAGE = 'core.storage_backends.PrivateMediaStorage'

# imagekit storage
IMAGEKIT_DEFAULT_FILE_STORAGE = 'core.storage_backends.PublicMediaStorage'

ALLOWED_HOSTS = [
    'api.veeta.co.uk',
    'www.api.veeta.co.uk',
    'backend',
    '10.0.13.30'
]

# CORS
CORS_ALLOWED_ORIGINS = [
    "https://veeta.co.uk",
    "https://www.veeta.co.uk",
]

CORS_ALLOW_CREDENTIALS = True

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
    "access-control-allow-origin",
    'access-control-allow-headers',
    'x-forwarded-proto',  # elb
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# https://stackoverflow.com/questions/32500073/request-header-field-access-control-allow-headers-is-not-allowed-by-itself-in-pr

# Mail Settings
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = os.getenv('SG_API_KEY')
FAIL_SILENTLY = True
DEFAULT_FROM_EMAIL='Veeta <no-reply@veeta.co.uk>'

# Toggle sandbox mode (when running in DEBUG mode)
SENDGRID_SANDBOX_MODE_IN_DEBUG = False

# echo to stdout or any other file-like object that is passed to the backend via the stream kwarg.
SENDGRID_ECHO_TO_STDOUT = False

# TWILIO
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SERVICE_ID = os.getenv('TWILIO_VERIFY_SERVICE_ID')
TESTING = False

SERVER_ALIAS = 'Production Server'
