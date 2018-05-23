"""Participation model tests."""

from django.db.utils import IntegrityError
from tests.utils import ModelTestCase

from users.factory import UserFactory
from visits.factory import VisitFactory
from visits.models import Participation


class ParticipationTest(ModelTestCase):
    """Test the Participation model."""

    model = Participation
    field_tests = {
        'user': {
            'verbose_name': 'utilisateur',
        },
        'visit': {
            'verbose_name': 'sortie',
        },
        'present': {
            'verbose_name': 'présent',
            'null': True,
        },
        'accepted': {
            'verbose_name': 'accepté',
            'null': True,
        },
    }
    model_tests = {
        'verbose_name': 'participation',
        'unique_together': (('user', 'visit'),),
    }

    def create(self):
        return Participation.objects.create(user=self.user,
                                            visit=self.visit)

    def setUp(self):
        self.user = UserFactory.create()
        self.visit = VisitFactory.create()
        self.obj = self.create()

    def test_user_cannot_participate_more_than_once(self):
        with self.assertRaises(IntegrityError):
            self.create()

    def test_str_contains_user(self):
        self.assertIn(str(self.user), str(self.obj))

    def test_str_contains_visit(self):
        self.assertIn(str(self.visit), str(self.obj))
