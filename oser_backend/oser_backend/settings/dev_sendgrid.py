"""Development settings to use SendGrid email backend locally."""

from .dev import *

# Allow to send emails with SendGrid while in DEBUG mode.
# See: https://github.com/sklarsa/django-sendgrid-v5#other-settings
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
