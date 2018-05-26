"""Example of notification definition and usage."""

from django.contrib.auth import get_user_model
from django.utils.timezone import now

from .notifications import Notification

User = get_user_model()


class Today(Notification):

    template_name = 'mails/myapp/today.md'
    args = ('user', 'date',)
    subject = "What's the date today?"

    def get_recipients(self):
        return [self.user.email]

    @classmethod
    def example(cls):
        user = User(first_name='John', email='john.doe@example.com')
        return cls(user=user, date=now())
