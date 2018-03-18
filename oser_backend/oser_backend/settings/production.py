"""Production settings."""

import os
# import django_heroku

from .dev import *
from aws.conf import *

DEBUG = os.environ.get('DEBUG', False)
ALLOWED_HOSTS = [
    'florimondmanca.pythonanywhere.com',
    'localhost',
    'oser-backend-production.herokuapp.com',
    'oser-cs.fr',
]


# Activate automatic Heroku settings configuration
# django_heroku.settings(locals())
