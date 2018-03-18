"""Amazon S3 storage configuration.

See:
- http://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
- https://www.codingforentrepreneurs.com/blog/s3-static-media-files-for-django/
"""

import os

# Use S3 backends
DEFAULT_FILE_STORAGE = 'aws.backends.MediaBackend'
STATICFILES_STORAGE = 'aws.backends.StaticBackend'

# Credentials
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Name of the storage bucket
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# Region of the storage bucket (e.g. eu-west-1)
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')

# Misc
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
# Do not overwrite files with the same name
AWS_S3_FILE_OVERWRITE = False
AWS_S3_SIGNATURE_VERSION = 's3v4'

AWS_BASE_URL = (
    'https://{bucket}.s3.{region}.amazonaws.com/'
    .format(bucket=AWS_STORAGE_BUCKET_NAME, region=AWS_S3_REGION_NAME))

# Redefine media and static URLs to upload/retrieve to/from S3
MEDIA_URL = AWS_BASE_URL + 'media/'
STATIC_URL = AWS_BASE_URL + 'static/'

# Direct the MEDIA_ROOT and STATIC_ROOT to their directory
MEDIA_ROOT = 'media'
STATIC_ROOT = 'static'
