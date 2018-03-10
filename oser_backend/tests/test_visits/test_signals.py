"""Test visits signals."""

from django.contrib.auth.models import Group
from django.test import TestCase
from guardian.shortcuts import get_group_perms

from visits.factory import VisitFactory


class OrganizersGroupSignalsTest(TestCase):
    """Test the post_save create_organizers_group signal."""

    def test_creates_group_using_organizers_group_name_property(self):
        visit = VisitFactory.create()
        self.assertTrue(Group.objects
                        .filter(name=visit.organizers_group_name)
                        .exists())

    def test_organizers_group_can_manage_visit(self):
        visit = VisitFactory.create()
        group = visit.organizers_group
        self.assertTrue('manage_visit' in get_group_perms(group, visit))

    def test_visit_save_updates_group_name(self):
        visit = VisitFactory.create()
        initial_name = visit.organizers_group.name
        visit.title = 'Look, another title!'
        visit.save()  # should trigger update of organizers_group.name
        self.assertNotEqual(visit.organizers_group_name, initial_name)
        self.assertEqual(visit.organizers_group.name,
                         visit.organizers_group_name)

    def test_group_is_deleted_after_visit_is_deleted(self):
        visit = VisitFactory.create()
        visit.delete()
        self.assertFalse(
            Group.objects.filter(name=visit.organizers_group_name).exists())
