"""Production settings."""

import os
import django_heroku

from .dev import *

DEBUG = False
ALLOWED_HOSTS = ['florimondmanca.pythonanywhere.com', 'localhost',
                 '*.herokuapp.com']

# AWS S3 Storage config

# Use Amazon S3 storage for media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Also send static files to Amazon S3
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Credentials
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'oser-backend-files'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}


# Activate automatic Heroku settings configuration
django_heroku.settings(locals())
