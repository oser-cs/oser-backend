"""Define AWS storage backends for static and media files."""

from storages.backends.s3boto3 import S3Boto3Storage


def StaticRootS3BotoStorage():
    """Static storage backend."""
    return S3Boto3Storage(location='static')


def MediaRootS3BotoStorage():
    """Media storage backend."""
    return S3Boto3Storage(location='media')
