"""Development settings with AWS file uploads.

See aws/conf.py for environment variables that must be defined.
"""

import os
from .common import *
from aws.conf import *

DEBUG = True
ALLOWED_HOSTS = ['localhost']
