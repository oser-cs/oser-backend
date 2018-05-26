"""Test the visits app signals."""

from django.test import TestCase
from tests.utils.mixins import SignalTestMixin

from mails.signals import notification_sent
from users.factory import UserFactory
from visits.factory import ParticipationFactory, VisitFactory
from visits.notifications import Confirm
from visits.signals import accepted_changed


class NotifyParticipationTest(SignalTestMixin, TestCase):
    """Test the notify_participation signal handler."""

    def setUp(self):
        VisitFactory.create_batch(5)
        self.obj = ParticipationFactory.create(accepted=None)

    def change(self, accepted=True):
        self.obj.accepted = accepted
        self.obj.save()

    def test_accepted_changed_called(self):
        with self.assertCalled(accepted_changed):
            self.change()

    def test_accepted_changed_called_when_creating_accepted_partipant(self):
        with self.assertCalled(accepted_changed):
            ParticipationFactory.create(accepted=True)

    def test_notification_sent_is_called_by_confirm(self):
        with self.assertCalled(notification_sent, sender=Confirm):
            self.change(accepted=True)

    def test_notification_sent_is_called_by_confirm(self):
        with self.assertCalled(notification_sent, sender=Confirm):
            self.change(accepted=False)
