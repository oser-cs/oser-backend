"""Test the visits app signals."""

from django.test import TestCase
from tests.utils.mixins import SignalTestMixin

from mails.signals import notification_sent
from users.factory import UserFactory
from visits.factory import ParticipationFactory, VisitFactory
from visits.notifications import Accepted, Rejected
from visits.signals import accepted_changed


class NotifyParticipationTest(SignalTestMixin, TestCase):
    """Test the notify_participation signal handler."""

    def setUp(self):
        VisitFactory.create()
        user = UserFactory.create()
        self.obj = ParticipationFactory.create(user=user, accepted=None)

    def change(self, accepted=True):
        self.obj.accepted = accepted
        self.obj.save()

    def test_accepted_changed_called(self):
        with self.assertCalled(accepted_changed):
            self.change()

    def test_notification_sent_called_by_accepted(self):
        with self.assertCalled(notification_sent, sender=Accepted):
            self.change(accepted=True)

    def test_notification_sent_called_by_rejected(self):
        with self.assertCalled(notification_sent, sender=Rejected):
            self.change(accepted=False)
