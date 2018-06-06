"""Define AWS storage backends for static and media files.

We do this to make sure static and media files are stored in different
directories in the S3 bucket (defined by the 'location' below).
"""

from storages.backends.s3boto3 import S3Boto3Storage


# uncomment and update aws/conf.py to use for storing static files on AWS
# def StaticBackend():
#     """Static storage backend."""
#     return S3Boto3Storage(location='static')


def MediaBackend():
    """Media storage backend."""
    return S3Boto3Storage(location='media')
