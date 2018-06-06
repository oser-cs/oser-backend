"""Test the mails app."""

from django.test import TestCase, override_settings
from tests.utils.mixins import SignalTestMixin
from mails.notifications import Notification
from mails.signals import delivered, app_disabled, notification_sent


class TestNotification(Notification):
    """A notification for testing purposes."""

    subject = 'Test'
    recipient_list = []

    def render(self):
        """Do not render a template, simply return a fake body."""
        return 'This is a test.'


class NotificationTest(SignalTestMixin, TestCase):
    """Test the notification class."""

    def setUp(self):
        self.notification = TestNotification()

    def test_sent_is_true_if_sent(self):
        self.assertIsNone(self.notification.sent)
        self.notification.send()
        self.assertTrue(self.notification.sent)

    def test_timestamp_is_set(self):
        self.assertIsNone(self.notification.timestamp)
        self.notification.send()
        self.assertIsNotNone(self.notification.timestamp)


class SignalsTest(SignalTestMixin, TestCase):
    """Test the mails signals."""

    def setUp(self):
        self.notification = TestNotification()

    @override_settings(MAILS_ENABLED=True)
    def test_delivered_called(self):
        with self.assertCalled(delivered):
            self.notification.send()

    @override_settings(MAILS_ENABLED=False)
    def test_app_disabled_called(self):
        with self.assertCalled(app_disabled):
            self.notification.send()

    def test_notification_sent_called(self):
        with self.assertCalled(notification_sent, sender=TestNotification):
            self.notification.send()
