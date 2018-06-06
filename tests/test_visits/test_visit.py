"""Visit model tests."""
from django.test import TestCase

from tests.utils import ModelTestCase
from users.factory import UserFactory
from visits.factory import (VisitFactory, VisitWithClosedRegistrationsFactory,
                            VisitWithOpenRegistrationsFactory)
from visits.models import Visit, VisitQuerySet


class VisitTest(ModelTestCase):
    """Test the Visit model."""

    model = Visit
    field_tests = {
        'title': {
            'verbose_name': 'titre',
            'max_length': 100,
        },
        'summary': {
            'verbose_name': 'résumé',
            'max_length': 300,
            'default': '',
            'blank': True,
        },
        'description': {
            'default': '',
            'blank': True,
        },
        'place': {
            'verbose_name': 'lieu',
        },
        'start_time': {
            'verbose_name': 'heure de début',
        },
        'end_time': {
            'verbose_name': 'heure de fin',
        },
        'meeting': {
            'verbose_name': 'lieu de rendez-vous',
            'max_length': 100,
            'default': '',
        },
        'deadline': {
            'verbose_name': "date limite d'inscription",
        },
        'image': {
            'verbose_name': 'illustration',
            'blank': True,
            'null': True,
        },
        'fact_sheet': {
            'verbose_name': 'fiche sortie',
            'blank': True,
            'null': True,
        },
        'permission': {
            'verbose_name': 'autorisation de sortie',
            'blank': True,
            'null': True,
        },
    }
    model_tests = {
        'verbose_name': 'sortie',
        'ordering': ('date',),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = VisitFactory.create()

    def test_get_absolute_url(self):
        self.client.force_login(UserFactory.create())
        url = self.obj.get_absolute_url()
        expected = '/api/visits/{}/'.format(self.obj.pk)
        self.assertEqual(url, expected)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_registrations_open(self):
        visit = VisitWithOpenRegistrationsFactory.create()
        self.assertTrue(visit.registrations_open)

    def test_registrations_closed(self):
        visit = VisitWithClosedRegistrationsFactory.create()
        self.assertFalse(visit.registrations_open)

    def test_organizers(self):
        self.assertEqual(0, self.obj.organizers.count())

    def test_str_is_title(self):
        self.assertEqual(str(self.obj), str(self.obj.title))


class VisitQuerySetTest(TestCase):
    """Test the custom Visit QuerySet."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        VisitWithOpenRegistrationsFactory.create_batch(5)
        VisitWithClosedRegistrationsFactory.create_batch(3)
        cls.qs = VisitQuerySet(model=Visit)

    def test_registrations_open(self):
        qs = self.qs.registrations_open(True)
        self.assertEqual(qs.count(), 5)

    def test_registrations_closed(self):
        qs = self.qs.registrations_open(False)
        self.assertEqual(qs.count(), 3)

    def test_state_required(self):
        with self.assertRaises(TypeError):
            self.qs.registrations_open()
