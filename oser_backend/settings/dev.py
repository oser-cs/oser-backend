"""Development settings"""

import os
from .common import *
from .common import BASE_DIR

DEBUG = True
ALLOWED_HOSTS = ['localhost','127.0.0.1']

# Static files (CSS, JavaScript, Images) and media files (user-uploaded)

# In development, static and media files are tied to the local filesystem.
# In production, media files cannot be stored on Heroku and need
# to be hosted elsewhere (e.g. AWS S3).

# Static files config
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]

# Media files config
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Mails config

# However emails won't be delivered by SendGrid (use dev_sendgrid settings)
MAILS_ENABLED = True
