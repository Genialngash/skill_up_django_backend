import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Application definition
CORE_DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_PACKAGES = [
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'django_filters',
    'storages',
    'corsheaders',
    'phonenumber_field',
    'django_extensions',
    'ckeditor'
]

VEETA_CUSTOM_APPS = [
    'users.apps.UsersConfig',
    'establishments.apps.EstablishmentsConfig',
    'jobs.apps.JobsConfig',
    'utils',
    'analytics',
    'jobseekers.apps.JobseekersConfig',
    'ratings',
    'payments',
    'profile_unlock.apps.ProfileUnlockConfig',
    'employers',
    'notifications'
]


INSTALLED_APPS = CORE_DJANGO_APPS + THIRD_PARTY_PACKAGES + VEETA_CUSTOM_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates",],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# allauth and dj-rest-auth global config
AUTH_USER_MODEL = 'users.User'
COMPANY_MODEL = 'establishments.Company'
JOB_CARD_MODEL = 'establishments.JobCard'
JOB_APPLICATION_MODEL = 'establishments.JobApplication'
JOBSEEKER_PROFILE_MODEL = 'users.JobseekerProfile'
JOB_BOOKMARK_MODEL = 'jobs.JobBookmark'
EMPLOYER_PROFILE_MODEL = 'users.EmployerProfile'


ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=1

# time(seconds) to wait before a request for resend confirmation email is sent again
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN=30

REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "users.serializers.CustomRegisterSerializer",
}

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "users.serializers.CustomUserDetailsSerializer",
    'LOGIN_SERIALIZER': 'users.serializers.CustomLoginSerializer',
}


from users.model_choices import MONTHS_OF_THE_YEAR

SPECTACULAR_SETTINGS = {
    'TITLE': 'Veeta Backend API',
    'DESCRIPTION': 'An backend API for veeta.co.uk',
    'VERSION': '1.0.0',
    # OTHER SETTINGS
    'COMPONENT_SPLIT_REQUEST': True,
    'ENUM_NAME_OVERRIDES': {
        'MonthEnum': MONTHS_OF_THE_YEAR.choices,
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240
BACKEND_DEV_EMAIL = 'developer@stephenkinyua.co.ke'
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

DJANGO_SUPERUSER_PASSWORD = 'veetaworkplace!@#'

CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        'skin': 'moono-lisa',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'styles', 'items': ['Format',]},
            {
                'name': 'paragraph',
                'items':  ['NumberedList', 'BulletedList']
            },
            {
                'name': 'basicstyles',
                'items': ['Bold', 'Underline', '-', 'RemoveFormat', 'Source']
            },

        ],
        'toolbar': 'YourCustomToolbarConfig',  # Put selected toolbar config here
        'tabSpaces': 0,
    }
}
