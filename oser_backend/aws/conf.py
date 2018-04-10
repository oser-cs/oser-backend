"""Amazon S3 storage configuration.

See:
- http://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
- https://www.codingforentrepreneurs.com/blog/s3-static-media-files-for-django/
"""

import os

# Use S3 backends

DEFAULT_FILE_STORAGE = 'aws.backends.MediaBackend'

# Uncomment STATICFILES_STORAGE to store static files on AWS
# Beware that Heroku automatically calls 'manage.py collectstatic' for
# each deployment, and this backend does not support checking for pre-existing
# static files on AWS : all the static files will be uploaded on each
# deployment.
# It can be OK to set DISABLE_COLLECTSTATIC on Heroku, but then
# you'd have to run collectstatic manually on Heroku when necessary.
# Since static files on the backend should not change a lot, it seems OK
# to simply use the default file storage for static files.

# STATICFILES_STORAGE = 'aws.backends.StaticBackend'

# Credentials
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Name of the storage bucket
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# Region of the storage bucket (e.g. eu-west-1)
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')


# Do not overwrite files with the same name
AWS_S3_FILE_OVERWRITE = False

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
