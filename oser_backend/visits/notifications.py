"""Visits app notifications."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from mails import Notification

from .models import Visit

User = get_user_model()


class Abandon(Notification):

    args = ('user', 'user_email', 'visit', 'date', 'reason',)
    template_name = 'mails/visits/abandon.md'
    recipients = [settings.VISITS_TEAM_EMAIL]

    def get_subject(self):
        return f'Désistement à la sortie: {self.visit}'

    @classmethod
    def example(cls):
        return cls(user='John Doe', user_email='john.doe@example.com',
                   visit='Visite du Palais de la Découverte',
                   date=now(), reason='Je ne peux plus venir...')


class Participation(Notification):

    template_name = 'mails/visits/participation.md'
    args = ('user', 'visit',)
    accepted: bool

    def get_context(self):
        context = super().get_context()
        context['accepted'] = self.accepted
        return context

    def get_subject(self):
        return f'Participation à la sortie : {self.visit}'

    def get_recipients(self):
        return [self.user.email]

    @classmethod
    def example(cls):
        user = User(email='john.doe@example.com', first_name='John')
        visit = Visit(title='Visite du Palais de la Découverte', date=now())
        return cls(user=user, visit=visit)


class Accepted(Participation):

    accepted = True


class Rejected(Participation):

    accepted = False
