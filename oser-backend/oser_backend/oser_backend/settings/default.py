"""
Django settings for oser_backend project.

Base settings common to all environments.
"""

import os
import dj_database_url
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
dn = os.path.dirname
BASE_DIR = dn(dn(dn(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# One way to do this is to store it in an environment variable on the server
SECRET_KEY = 'odfuioTvdfvkdhvjeT9659dbnkcn2332fk564jvdf034'
DEBUG = False
ALLOWED_HOSTS = ['localhost']

ADMINS = (
    ('admin', 'admin@oser-cs.fr'),
)
ADMIN_INITIAL_PASSWORD = 'admin'  # to be changed after first login

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.forms',
]

THIRD_PARTY_APPS = [
    # Markdown integration
    'markdownx',
    # Django REST Framework (DRF)
    'rest_framework',
    'rest_framework.authtoken',
    # DRY REST permissions (rules-based API permissions)
    # https://github.com/dbkaplan/dry-rest-permissions
    'dry_rest_permissions',
    # CORS headers for Frontend integration
    'corsheaders',
    # Sortable models in Admin
    'adminsortable2',
    # Django Guardian: per object permissions
    # https://github.com/django-guardian/django-guardian
    'guardian',
]
PROJECT_APPS = [
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'tutoring.apps.TutoringConfig',
    'api.apps.ApiConfig',
    'showcase_site.apps.ShowcaseSiteConfig',
    'visits.apps.VisitsConfig',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'oser_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'oser_backend.wsgi.application'

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
        'rest_framework.authentication.TokenAuthentication',
        # v Enable session authentication in the browsable API
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DATE_FORMAT': '%d/%m/%Y',
    'DATE_INPUT_FORMATS': ['%d/%m/%Y'],
}

# Pymdown-extensions Emoji configuration
import pymdownx.emoji  # noqa

extension_configs = {
    'emoji_index': pymdownx.emoji.twemoji,
    'emoji_generator': pymdownx.emoji.to_png,
    'alt': 'short',
    'options': {
        'attributes': {
            'align': 'absmiddle',
            'height': '20px',
            'width': '20px'
        },
        'image_path': 'https://assets-cdn.github.com/images/icons/emoji/unicode/',
        'non_standard_image_path': 'https://assets-cdn.github.com/images/icons/emoji/'
    }
}

# Markdownx settings
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'pymdownx.emoji',
]
MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {
    'pymdownx.emoji': extension_configs,
}

# Database

DATABASES = {
    'default': dj_database_url.config(),
}

# Security: SSL and HTTPS
SECURE_SSL_REDIRECT = True  # redirect all to HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Authentication

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
]

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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_FILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# User-uploaded media files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
