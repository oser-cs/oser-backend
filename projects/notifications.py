"""Projects notifications."""


from mails import Notification
from django.utils.timezone import now
from users.models import User
from .models import Edition, Project


class _BaseParticipationNotification(Notification):
    """Base notification for project participations."""

    args = ('user', 'edition',)

    @classmethod
    def example(cls):
        """Example notification."""
        user = User(email='john.doe@example.com', first_name='John')
        project = Project(title='Focus Europe')
        edition = Edition(project=project, year=now().year)
        return cls(user=user, edition=edition)


class _NotifyOrgnizers(_BaseParticipationNotification):
    """Notify the edition organizers a participation has changed."""

    title: str

    def get_subject(self):
        return f'{self.title}: {self.edition}'

    def get_recipients(self):
        """Return the email of each organizer."""
        edition = self.kwargs['edition']
        # TODO add the project team's email
        return list(edition.organizers.values_list('email', flat=True))


class _NotifyUser(_BaseParticipationNotification):
    """Notify a user their participation state has changed."""

    verb: str

    def get_subject(self):
        return f'Dossier {self.verb}: {self.edition}'

    def get_recipients(self):
        return [self.kwargs['user'].email]


class OrganizersReceived(_NotifyOrgnizers):
    """Notify the edition organizers that a new participation was created."""

    title = 'Nouvelle participation'
    template_name = 'projects/organizers_participation_received.md'


class UserReceived(_NotifyUser):
    """Notify a user their participation was well received."""

    verb = 'en attente'
    template_name = 'projects/participation_received.md'


class UserValid(_NotifyUser):
    """Notify a user their participation was marked as valid."""

    verb = 'validé'
    template_name = 'projects/participation_valid.md'


class UserAccepted(_NotifyUser):
    """Notify a user their participation was marked as accepted."""

    verb = 'accepté'
    template_name = 'projects/participation_accepted.md'


class UserRejected(_NotifyUser):
    """Notify a user their participation was marked as rejected."""

    verb = 'rejeté'
    template_name = 'projects/participation_rejected.md'


class UserCancelled(_NotifyUser):
    """Notify a user their participation was correctly cancelled."""

    verb = 'annulé'
    template_name = 'projects/participation_cancelled.md'


class UserDeleted(_NotifyUser):
    """Notify a user their participation was correctly deleted."""

    verb = 'supprimé'
    template_name = 'projects/participation_deleted.md'


class OrganizersCancelled(_NotifyOrgnizers):
    """Notify organizers that a user has cancelled their participation."""

    title = 'Participation annulée'
    template_name = 'projects/organizers_participation_cancelled.md'


class OrganizersDeleted(_NotifyOrgnizers):
    """Notify organizers a user has deleted their participation."""

    title = 'Participation supprimée'
    template_name = 'projects/organizers_participation_deleted.md'
