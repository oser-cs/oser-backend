"""Tutoring group model tests."""

from tests.utils import ModelTestCase
from tutoring.factory import TutoringGroupFactory, TutorTutoringGroupFactory
from tutoring.models import TutoringGroup
from users.factory import UserFactory, TutorFactory


class TutoringGroupTest(ModelTestCase):
    """Test the TutoringGroup model."""

    model = TutoringGroup
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
    model_tests = {
        'verbose_name': 'groupe de tutorat',
        'verbose_name_plural': 'groupes de tutorat',
        'ordering': ('name',),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = TutoringGroupFactory.create()

    def test_get_absolute_url(self):
        self.client.force_login(UserFactory.create())
        response = self.client.get(
            '/api/tutoring/groups/{}/'.format(self.obj.pk))
        self.assertEqual(200, response.status_code)

    def test_tutors_many_to_many_relationship(self):
        tutor = TutorFactory.create()
        membership = TutorTutoringGroupFactory.create(
            tutor=tutor,
            tutoring_group=self.obj)
        tutor = membership.tutor
        self.assertIn(tutor, self.obj.tutors.all())
        self.assertIn(self.obj, tutor.tutoring_groups.all())
