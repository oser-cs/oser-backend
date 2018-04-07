"""Development settings"""

import os
from .common import *
from .common import BASE_DIR

DEBUG = True
ALLOWED_HOSTS = ['localhost']

# Static files (CSS, JavaScript, Images) and media files (user-uploaded)

# In development, static and media files are tied to the local filesystem.
# In production, media files cannot be stored on Heroku and need
# to be hosted elsewhere (e.g. AWS S3).

# Static files config
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files config
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
