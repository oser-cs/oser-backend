"""Test the projects app signals."""

from django.test import TestCase
from django.utils.timezone import now
from tests.utils.mixins import SignalTestMixin

from dynamicforms.models import Form
from profiles.factory import TutorFactory
from projects.factory import (EditionFactory, ParticipationFactory,
                              ProjectFactory)
from projects.models import EditionForm, Participation, EditionOrganizer
from projects.signals import (accepted, cancelled, deleted, pending, rejected,
                              valid)


class NotifyParticipationTest(SignalTestMixin, TestCase):
    """Test project participation signal handlers."""

    def setUp(self):
        # Create all objects that need to exist for rendering emails
        project = ProjectFactory.create(name='Focus Europe')
        recipient = TutorFactory.create()
        self.edition = EditionFactory.create(project=project, year=2018)
        EditionOrganizer.objects.create(
            user=recipient.user,
            edition=self.edition)
        form = Form.objects.create(title=f'Inscriptions à {self.edition}')
        EditionForm.objects.create(
            edition=self.edition,
            form=form,
            recipient=recipient,
            deadline=now(),
        )
        self.obj = self.create_obj()

    def create_obj(self):
        return ParticipationFactory.create(edition=self.edition)

    def change(self, state):
        self.obj.state = state
        self.obj.save()

    def test_create_participation_pending_called(self):
        with self.assertCalled(pending):
            self.create_obj()

    def test_save_without_changing_state_not_called(self):
        with self.assertNotCalled(pending):
            self.obj.save()

    def test_valid_called(self):
        with self.assertCalled(valid):
            self.change(Participation.STATE_VALIDATED)

    def test_accepted_called(self):
        with self.assertCalled(accepted):
            self.change(Participation.STATE_ACCEPTED)

    def test_rejected_called(self):
        with self.assertCalled(rejected):
            self.change(Participation.STATE_REJECTED)

    def test_cancelled_called(self):
        with self.assertCalled(cancelled):
            self.change(Participation.STATE_CANCELLED)

    def test_deleted_called(self):
        with self.assertCalled(deleted):
            self.obj.delete()
