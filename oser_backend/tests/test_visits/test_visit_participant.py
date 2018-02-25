"""VisitParticipant model tests."""

from django.db.utils import IntegrityError
from visits.models import VisitParticipant
from tests.utils import ModelTestCase
from tests.factory import StudentFactory, VisitFactory, UserFactory


class VisitParticipantTest(ModelTestCase):
    """Test the VisitParticipant model."""

    model = VisitParticipant
    field_tests = {
        'student': {
            'verbose_name': 'lycéen',
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
        'unique_together': (('student', 'visit'),),
    }

    def create(self):
        return VisitParticipant.objects.create(student=self.student,
                                               visit=self.visit)

    def setUp(self):
        self.student = StudentFactory.create()
        self.visit = VisitFactory.create()
        self.obj = self.create()

    def test_student_cannot_participate_more_than_once(self):
        with self.assertRaises(IntegrityError):
            self.create()

    def test_str_contains_student(self):
        self.assertIn(str(self.student), str(self.obj))

    def test_str_contains_visit(self):
        self.assertIn(str(self.visit), str(self.obj))

    def test_get_absolute_url(self):
        self.client.force_login(UserFactory.create())
        url = self.obj.get_absolute_url()
        expected = '/api/visit-participants/{}/'.format(self.obj.visit.pk)
        self.assertEqual(url, expected)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
