import os
from .default import *
from .default import REACT_APP_DIR

DEBUG = False
ALLOWED_HOSTS = ['oser-cs.fr', ]
STATICFILES_DIRS = (
    os.path.join(REACT_APP_DIR, 'build', 'static'),
)
