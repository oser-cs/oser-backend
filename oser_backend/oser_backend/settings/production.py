"""Production settings."""

import os

from .dev import *
from aws.conf import *

DEBUG = os.environ.get('DEBUG', False)
ALLOWED_HOSTS = [
    'florimondmanca.pythonanywhere.com',
    'localhost',
    'oser-backend-production.herokuapp.com',
    'oser-cs.fr',
]
