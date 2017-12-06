"""Users utilities."""

import datetime
from django.conf import settings


def get_promotion_range(date=None):
    """Return the range of possible promotions.

    The new promotion arrival date (NPAD) is defined in settings by:
        NEW_PROMOTION_ARRIVAL_DAY
        NEW_PROMOTION_ARRIVAL_MONTH

    Before NPAD :
        - maximum promotion is 3 years ahead of today's year
        - minimum promotion is 2 years behind today's year
    After NPAD :
        - maximum promotion is 4 years ahead of today's year
        - minimum promotion is 1 year behind today's year

    Parameters
    ----------
    date : datetime.date or datetime.datetime, optional
        If not given, datetime.datetime.today() is used.
    """
    if date is None:
        date = datetime.datetime.today()
    year = date.year
    month, day = date.month, date.day
    if month >= settings.NEW_PROMOTION_ARRIVAL_MONTH:
        if day >= settings.NEW_PROMOTION_ARRIVAL_DAY:
            year += 1
    return range(year + 2, year + 2 - settings.NUMBER_OF_PROMOTIONS, -1)
