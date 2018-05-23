"""Test the participation abandon endpoint."""

from django.test import override_settings
from rest_framework.test import APITestCase

from users.factory import UserFactory
from visits.factory import VisitFactory


@override_settings(MAILS_ENABLED=False)
class AbandonTest(APITestCase):
    """Test endpoint to notify a user does not participate to visit anymore."""

    def setUp(self):
        self.user = UserFactory.create()
        self.visit = VisitFactory.create()
        self.reason = (
            "Désolé, je ne peux plus venir à cause d'un rendez-vous médical.")

    def perform(self):
        data = {
            'user': self.user.pk,
            'visit': self.visit.pk,
            'reason': self.reason,
        }
        response = self.client.post('/api/participations/abandon/', data=data,
                                    format='json')
        return response

    def test(self):
        self.client.force_login(self.user)
        response = self.perform()
        self.assertEqual(response.status_code, 201, response.data)
