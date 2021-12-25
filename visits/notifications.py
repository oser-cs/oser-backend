"""Visits app notifications."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from mails import Notification

from .models import Visit, Participation

User = get_user_model()


class ParticipationCancelled(Notification):

    args = ('user', 'visit', 'reason',)
    template_name = 'visits/participation_cancelled.md'
    recipients = [settings.VISITS_TEAM_EMAIL]

    def get_subject(self):
        return f'Désistement à la sortie: {self.visit}'

    @classmethod
    def example(cls):
        user = User(email='john.doe@example.com', first_name='John')
        visit = Visit(title='Visite du Palais de la Découverte', date=now())
        return cls(user=user, visit=visit, reason='Je ne peux plus venir...')


class ConfirmParticipation(Notification):
    """ConfirmParticipation whether a user can participate to a visit."""

    template_name = 'visits/confirm_participation.md'
    args = ('participation',)

    def get_subject(self):
        return f'Participation à la sortie : {self.participation.visit}'

    def get_recipients(self):
        return [self.participation.user.email]

    @classmethod
    def example(cls):
        user = User(email='john.doe@example.com', first_name='John')
        visit = Visit(title='Visite du Palais de la Découverte', date=now())
        participation = Participation(
            user=user, visit=visit, accepted=True, submitted=now())
        return cls(participation=participation)