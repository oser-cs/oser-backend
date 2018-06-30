"""Amazon S3 storage configuration.

See:
- http://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
- https://www.codingforentrepreneurs.com/blog/s3-static-media-files-for-django/
"""

import os
import warnings

# Use S3 backends
DEFAULT_FILE_STORAGE = 'aws.backends.MediaBackend'

# Credentials
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Name of the storage bucket
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

# Region of the storage bucket (e.g. eu-west-1)
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')

# Warn if any of the above is not set
if not AWS_ACCESS_KEY_ID:
    warnings.warn('AWS_ACCESS_KEY_ID not set')
if not AWS_SECRET_ACCESS_KEY:
    warnings.warn('AWS_SECRET_ACCESS_KEY not set')
if not AWS_STORAGE_BUCKET_NAME:
    warnings.warn('AWS_STORAGE_BUCKET_NAME not set')
if not AWS_S3_REGION_NAME:
    warnings.warn('AWS_S3_REGION_NAME not set')

# Overwrite files with the same name
AWS_S3_FILE_OVERWRITE = True

# Use the new signature version
AWS_S3_SIGNATURE_VERSION = 's3v4'

# Misc
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_S3_CUSTOM_DOMAIN = (
    '{bucket}.s3.amazonaws.com'
    .format(bucket=AWS_STORAGE_BUCKET_NAME))

# Redefine media URL to upload/retrieve to/from S3
MEDIA_URL = 'https://' + AWS_S3_CUSTOM_DOMAIN + 'media/'

# Direct the MEDIA_ROOT to the media/ directory inside the bucket
MEDIA_ROOT = 'media'
