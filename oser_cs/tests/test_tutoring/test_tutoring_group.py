"""Tutoring group model tests."""

import tutoring.models
from tests.utils import ModelTestCase
from tests.factory import TutoringGroupFactory, TutorTutoringGroupFactory


class TutoringGroupTest(ModelTestCase):
    """Test the TutoringGroup model."""

    model = tutoring.models.TutoringGroup
    field_tests = {
        'name': {
            'verbose_name': 'nom',
            'max_length': 200,
        },
        'tutors': {
            'verbose_name': 'tuteurs',
            'blank': True,
        },
    }
    # TODO implement
    model_tests = {
        'verbose_name': 'groupe de tutorat',
        'verbose_name_plural': 'groupes de tutorat',
        'ordering': ('name',),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = TutoringGroupFactory.create()

    def test_get_absolute_url(self):
        response = self.client.get(f'/api/tutoring/groups/{self.obj.pk}/')
        self.assertEqual(200, response.status_code)

    def test_tutors_many_to_many_relationship(self):
        membership = TutorTutoringGroupFactory.create(
            tutoring_group=self.obj,
        )
        tutor = membership.tutor
        self.assertIn(tutor, self.obj.tutors.all())
        self.assertIn(self.obj, tutor.tutoring_groups.all())
