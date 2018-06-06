"""
Django settings for oser_backend project.

Common settings suitable for all environmebts.
"""

import os

import dj_database_url
import pymdownx.emoji

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
dn = os.path.dirname
BASE_DIR = dn(dn(dn(os.path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!
# One way to do this is to store it in an environment variable on the server
SECRET_KEY = os.environ.get('SECRET_KEY',
                            'odfuioTvdfvkdhvjeT9659dbnkcn2332fk564jvdf034')

# Admin generation settings
ADMINS = (
    ('Secteur Geek', 'oser.geek@gmail.com'),
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
    # Extra Django file storage backends
    'storages',
    # Country fields
    'django_countries',
]
PROJECT_APPS = [
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'profiles.apps.ProfilesConfig',
    'tutoring.apps.TutoringConfig',
    'visits.apps.VisitsConfig',
    'register.apps.RegisterConfig',
    'api.apps.ApiConfig',
    'mails.apps.MailsConfig',
    'projects.apps.ProjectsConfig',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
                'django.template.context_processors.i18n',
            ],
        },
    },
]
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'oser_backend.wsgi.application'

# Django rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # v Enable session authentication in the browsable API
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# Security
CORS_ORIGIN_REGEX_WHITELIST = (
    # Allow local hosts on any port
    r'^(https?://)?localhost(:\d+)?$',
    r'^(https?://)?127\.0\.0\.1(:\d+)?$',
    # Allow hosts such as:
    # - https://oser-cs.herokuapp.com
    # - https://oser-frontend-dev.herokuapp.com
    # (but also https://unknown.herokuapp.com...)
    # Essentially allows any frontend hosted on Heroku to send CORS requests.
    r'^(https?://)?(.+\.)?herokuapp\.com$',
    # Allow any app hosted on *oser-cs.fr
    r'^(https?://)?(.+\.)?oser-cs\.fr$',
)
X_FRAME_OPTIONS = 'DENY'  # refuse to serve in an <iframe>

# Pymdown-extensions Emoji configuration
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

# Config be retrieved through the DATABASE_URL environment variable
# DATABASE_URL format: postgres://USERNAME:PASSWORD@HOST:PORT/NAME
DATABASES = {
    'default': dj_database_url.config(
        # Provide a default for dev environment
        default='postgres://postgres:postgres@localhost:5432/oser_backend_db'),
}


# Authentication

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
]

# Password validation
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


# Logging

# NOTE: all loggers within this project should be named 'web.<logger_name>'
# so that the same configuration is applied to them.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'web': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}


# Email configuration

EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

# Mails app config

MAILS_ENABLED = True
MAILS_NOTIFICATIONS_ADDRESS = 'notifications@oser-cs.fr'
MAILS_RAISE_EXCEPTIONS = True

# Visits app config
VISITS_TEAM_EMAIL = os.environ.get('VISITS_TEAM_EMAIL',
                                   'florimond.manca@gmail.com')

# Internationalization

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) and media files (user-uploaded)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Celery settings

CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ('application/json',)
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
