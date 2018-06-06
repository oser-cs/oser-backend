"""Profiles utilities tests."""

import datetime
from django.test import TestCase
from django.conf import settings
from profiles.utils import get_promotion_range


class TestGetPromotionRange(TestCase):
    """Test the get_promotion_range utility."""

    def make_date(self, year, months_after_arrival, days_after_arrival):
        return datetime.date(
            year,
            settings.NEW_PROMOTION_ARRIVAL_MONTH + months_after_arrival,
            settings.NEW_PROMOTION_ARRIVAL_DAY + days_after_arrival)

    def test_before_arrival_date(self):
        prom_range = get_promotion_range(self.make_date(2017, -1, 0))
        self.assertEqual(prom_range,
                         range(2019, 2019 - settings.NUMBER_OF_PROMOTIONS, -1))

    def test_on_arrival_date(self):
        prom_range = get_promotion_range(self.make_date(2017, 0, 0))
        self.assertEqual(prom_range,
                         range(2020, 2020 - settings.NUMBER_OF_PROMOTIONS, -1))

    def test_after_arrival_date(self):
        prom_range = get_promotion_range(self.make_date(2017, 0, 1))
        self.assertEqual(prom_range,
                         range(2020, 2020 - settings.NUMBER_OF_PROMOTIONS, -1))
