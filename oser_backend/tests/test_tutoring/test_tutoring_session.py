"""Tutoring session model tests."""

import tutoring.models
from tests.utils import ModelTestCase
from tests.factory import TutoringSessionFactory


class TutoringSessionTest(ModelTestCase):
    """Test the TutoringSession model."""

    model = tutoring.models.TutoringSession
    field_tests = {
        'date': {
            'verbose_name': 'date',
        },
        'start_time': {
            'verbose_name': 'heure de début',
        },
        'end_time': {
            'verbose_name': 'heure de fin',
        },
        'tutoring_group': {
            'verbose_name': 'groupe de tutorat',
        },
    }
    model_tests = {
        'verbose_name': 'séance de tutorat',
        'verbose_name_plural': 'séances de tutorat',
        'ordering': ('date', 'start_time'),
    }

    @classmethod
    def setUpTestData(self):
        self.obj = TutoringSessionFactory.create()

    def test_get_absolute_url(self):
        url = '/api/tutoring/sessions/{}/'.format(self.obj.pk)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_tutoring_group_one_to_many_relationship(self):
        self.assertEqual(tutoring.models.TutoringGroup.objects.get(),
                         self.obj.tutoring_group)
        self.assertIn(self.obj,
                      tutoring.models.TutoringGroup.objects.get()
                      .tutoring_sessions.all())
