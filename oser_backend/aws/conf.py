"""Amazon S3 storage configuration.

See:
- http://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
- https://www.codingforentrepreneurs.com/blog/s3-static-media-files-for-django/
"""

import os

# Use S3 backends
DEFAULT_FILE_STORAGE = 'aws.backends.StaticRootS3BotoStorage'
STATICFILES_STORAGE = 'aws.backends.MediaRootS3BotoStorage'

# Credentials
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Name of the storage bucket
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

# Misc
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Redefine media and static URLs to upload/retrieve to/from S3
MEDIA_URL = (
    'https://{}.s3.amazonaws.com/media/'.format(AWS_STORAGE_BUCKET_NAME))
STATIC_URL = (
    'https://{}.s3.amazonaws.com/static/'.format(AWS_STORAGE_BUCKET_NAME))

MEDIA_ROOT = MEDIA_URL
STATIC_ROOT = STATIC_URL
