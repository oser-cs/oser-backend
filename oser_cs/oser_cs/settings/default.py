"""
Django settings for oserwebsite project.

Base settings common to all environments.
"""

import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
dn = os.path.dirname
BASE_DIR = dn(dn(dn(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# One way to do this is to store it in an environment variable on the server
SECRET_KEY = 'i^08u==e5++$g(9a#^b46i@xsstxnf9j2rn(%g5nbe@#xu*5#c'

DEBUG = False

ALLOWED_HOSTS = ['localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Django REST Framework (DRF)
    'rest_framework',
    # DRF Swagger (API documentation generator)
    'rest_framework_swagger',
    # Site apps
    'users.apps.UsersConfig',
    'persons.apps.PersonsConfig',
    'tutoring.apps.TutoringConfig',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'oser_cs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./oser_cs/templates'],
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

WSGI_APPLICATION = 'oser_cs.wsgi.application'

# Flash messages classes
MESSAGE_TAGS = {
    messages.INFO: 'alert alert-info alert-dismissible fade show',
    messages.SUCCESS: 'alert alert-success alert-dismissible fade show',
    messages.WARNING: 'alert alert-warning alert-dismissible fade show',
    messages.ERROR: 'alert alert-danger alert-dismissible fade show',
}

# Django rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication'
    ]
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Date and time formats

SHORT_DATE_FORMAT = '%d/%m/%Y'
DATE_INPUT_FORMATS = [
    '%d/%m/%Y',  # 24/05/2006
]
REST_FRAMEWORK = {
    'DATE_FORMAT': SHORT_DATE_FORMAT,
    'DATE_INPUT_FORMATS': DATE_INPUT_FORMATS,
}

# Authentication


AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# LOGIN_URL = '/accounts/login'
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/'

# Promotion settings
NUMBER_OF_PROMOTIONS = 10
NEW_PROMOTION_ARRIVAL_MONTH = 9
NEW_PROMOTION_ARRIVAL_DAY = 1

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
