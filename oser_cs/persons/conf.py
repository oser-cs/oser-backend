"""Persons settings."""

from django.conf import settings
from utils import setdefault


# Tutor.promotion field settings
setdefault(settings, 'NUMBER_OF_PROMOTIONS', 10)
setdefault(settings, 'NEW_PROMOTION_ARRIVAL_MONTH', 9)
setdefault(settings, 'NEW_PROMOTION_ARRIVAL_DAY', 1)
