"""Tutoring models."""

from datetime import datetime, timedelta

from django.db import models
from django.shortcuts import reverse
from django.template.defaulttags import date as date_tag
from dry_rest_permissions.generics import (allow_staff_or_superuser,
                                           authenticated_users)

from .conf import settings
from .validators import uai_code_validator


# Create your models here.


class TutorTutoringGroup(models.Model):
    """Intermediate model for tutoring group and tutors n-n relationship."""

    tutoring_group = models.ForeignKey(
        'TutoringGroup', on_delete=models.CASCADE,
        verbose_name='groupe de tutorat')
    tutor = models.ForeignKey(
        'users.Tutor', on_delete=models.CASCADE,
        verbose_name='Tuteur')
    is_leader = models.BooleanField(default=False, verbose_name='Responsable')

    class Meta:  # noqa
        verbose_name = 'membre du groupe de tutorat'
        verbose_name_plural = 'membres du groupe de tutorat'


class TutoringGroup(models.Model):
    """Represents a tutoring group to which tutors and students participate.

    Fields
    ------
    name : char
    tutors : n-n with users.Tutor
    school : 1-n with tutoring.School
        Deletion rule: SET_NULL

    Relationships
    -------------
    students : n-1 with users.Student
    """

    name = models.CharField('nom', max_length=200)
    tutors = models.ManyToManyField('users.Tutor',
                                    related_name='tutoring_groups',
                                    verbose_name='tuteurs',
                                    blank=True,
                                    through='TutorTutoringGroup')
    school = models.ForeignKey('School', on_delete=models.SET_NULL,
                               null=True,
                               related_name='tutoring_groups',
                               verbose_name='lycée')

    class Meta:  # noqa
        ordering = ('name',)
        verbose_name = 'groupe de tutorat'
        verbose_name_plural = 'groupes de tutorat'

    def get_absolute_url(self):
        return reverse('api:tutoring_group-detail', args=[str(self.id)])

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        """Can only be written by admin, leader tutor."""
        is_leader = (self.tutors
                     .filter(user_id=request.user.id,
                             tutortutoringgroup__is_leader=True)
                     .exists())
        return is_leader

    def __str__(self):
        return str(self.name)


class School(models.Model):
    """Represents a (high) school.

    Fields
    ------
    uai_code : char, primary key
        UAI code of the school.
    name : char
    address : char

    Relationships
    -------------
    students : n-1 with users.Student

    Meta
    ----
    ordering : by name
    """

    name = models.CharField('nom', max_length=200, help_text='Nom du lycée')

    # TODO add UAI code validation
    uai_code = models.CharField(
        'code UAI',
        max_length=8,
        primary_key=True,
        validators=[uai_code_validator],
        help_text=(
            "Code UAI (ex-RNE) de l'établissement qui sert à l'identifier. "
            "Celui-ci est composé de 7 chiffres et une lettre. "
            "Il est répertorié dans "
            "l'annuaire des établissements sur le site du "
            "ministère de l'Éducation Nationale."))

    address = models.ForeignKey(
        'core.Address', on_delete=models.SET_NULL, verbose_name='adresse',
        null=True, help_text='Adresse complète du lycée')

    class Meta:  # noqa
        ordering = ('name',)
        verbose_name = 'lycée'

    def save(self, *args, **kwargs):
        if self.pk is None:
            # ensure the letter in UAI code is always uppercase.
            # do only at object creation to prevent PK from changing while
            # object is alive.
            self.uai_code = self.uai_code.upper()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('api:school-detail', args=[str(self.uai_code)])

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @authenticated_users
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @authenticated_users
    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return True

    def __str__(self):
        return str(self.name)


def default_start_time():
    """Return the default tutoring session start time."""
    h, m = settings.DEFAULT_SESSION_START_TIME
    now = datetime.now()
    start = now.replace(hour=h, minute=m, second=0, microsecond=0)
    return (start if start > now else start + timedelta(days=1)).time()


def default_end_time():
    """Return the default tutoring session end time."""
    h, m = settings.DEFAULT_SESSION_END_TIME
    now = datetime.now()
    end = now.replace(hour=h, minute=m, second=0, microsecond=0)
    return (end if end > now else end + timedelta(days=1)).time()


class TutoringSession(models.Model):
    """Represents a tutoring session event.

    Fields
    ------
    date : date
    start_time : time
    end_time : time
    tutoring_group : 1-n with tutoring.TutoringGroup
        Deletion rule: CASCADE
    report : 1-1 with tutoring.TutoringReport

    Meta
    ----
    ordering : by date (upcoming sessions first)
    """

    date = models.DateField(default=datetime.now)
    start_time = models.TimeField('heure de début',
                                  default=default_start_time)
    end_time = models.TimeField('heure de fin',
                                default=default_end_time)
    tutoring_group = models.ForeignKey('TutoringGroup',
                                       on_delete=models.CASCADE,
                                       verbose_name='groupe de tutorat',
                                       related_name='tutoring_sessions')
    # TODO add report 1-1

    class Meta:  # noqa
        verbose_name = 'séance de tutorat'
        verbose_name_plural = 'séances de tutorat'
        ordering = ('date', 'start_time',)

    @property
    def school(self):
        return self.tutoring_group.school
    school.fget.short_description = 'lycée'

    def __str__(self):
        date = date_tag(self.date, 'SHORT_DATE_FORMAT')
        return '{} ({})'.format(self.tutoring_group, date)
