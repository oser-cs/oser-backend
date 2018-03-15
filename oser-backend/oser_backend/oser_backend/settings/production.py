import os
import django_heroku

from .default import *

DEBUG = True
ALLOWED_HOSTS = ['florimondmanca.pythonanywhere.com', 'localhost',
                 'lit-dusk-75348.herokuapp.com']

django_heroku.settings(locals())
