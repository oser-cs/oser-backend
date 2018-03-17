import os
import django_heroku

from .default import *

DEBUG = True
ALLOWED_HOSTS = ['florimondmanca.pythonanywhere.com', 'localhost',
                 '*.herokuapp.com']

# Activate automatic Heroku settings configuration
django_heroku.settings(locals())
