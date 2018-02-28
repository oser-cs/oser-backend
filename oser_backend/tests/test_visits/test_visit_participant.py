"""VisitParticipant model tests."""

from django.db.utils import IntegrityError
from visits.models import VisitParticipant
from tests.utils import ModelTestCase
from tests.factory import VisitFactory, UserFactory


class VisitParticipantTest(ModelTestCase):
    """Test the VisitParticipant model."""

    model = VisitParticipant
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
        }
    }
    model_tests = {
        'verbose_name': 'participant à la sortie',
        'verbose_name_plural': 'participants à la sortie',
        'unique_together': (('user', 'visit'),),
    }

    def create(self):
        return VisitParticipant.objects.create(user=self.user,
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

    def test_get_absolute_url(self):
        self.client.force_login(UserFactory.create())
        url = self.obj.get_absolute_url()
        expected = '/api/visit-participants/{}/'.format(self.obj.visit.pk)
        self.assertEqual(url, expected)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
