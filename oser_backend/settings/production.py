"""Production settings."""

import os

from aws.conf import *

from .common import *

# NOTE: `or False` ensures the value is  `False` (the boolean)
# if the value given in environment is false-y (e.g. empty string)
# Otherwise may lead to unexpected bugs.
# For example, SendGrid could send an empty string as the sandbox mode,
# leading to strange 400 Bad Request errors.
DEBUG = os.environ.get('DEBUG', False) or False

ALLOWED_HOSTS = [
    'localhost',
    'oser-backend.herokuapp.com',
    'oser-backend-dev.herokuapp.com',
    'oser-cs.fr',
]

# Security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# Mails
MAILS_ENABLED = True
MAILS_RAISE_EXCEPTIONS = os.environ.get('MAILS_RAISE_EXCEPTIONS', False)

# SendGrid
# Allow Sandbox if DEBUG is True (we're in prod anyway)
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
