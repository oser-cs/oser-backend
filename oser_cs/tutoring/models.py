"""Tutoring models."""

from datetime import datetime, timedelta
from django.db import models
from django.core import checks
from django.shortcuts import reverse
from django.template.defaulttags import date as date_tag
from dry_rest_permissions.generics import allow_staff_or_superuser

from utils import is_in_group, group_exists

from .conf import settings
from .validators import uai_code_validator

# Create your models here.


VP_TUTORAT_GROUP = 'VP Tutorat'


class SchoolYear(models.Model):
    """Represents a school year.

    If year is 2017, the school_year object represents the '2017-2018'
    school year.

    Fields
    ------
    year : int field
    """

    year = models.IntegerField('année', help_text=(
        "Année calendaire du début de l'année scolaire. "
        "Exemple : pour l'année scolaire 2017-2018, entrez 2017."
    ))

    class Meta:  # noqa
        verbose_name = 'année scolaire'
        verbose_name_plural = 'années scolaires'

    def __str__(self):
        return f'{self.year}-{self.year + 1}'


class TutoringGroupLeadership(models.Model):
    """Intermediate model for tutoring group and tutors n-n relationship."""

    tutoring_group = models.ForeignKey('TutoringGroup',
                                       on_delete=models.CASCADE)
    tutor = models.ForeignKey('users.Tutor', on_delete=models.CASCADE)
    is_leader = models.BooleanField(default=False)


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
                                    through='TutoringGroupLeadership')
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

    # System checks

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls._check_groups_exist(**kwargs))
        return errors

    @classmethod
    def _check_groups_exist(cls, **kwargs):
        errors = []
        if not group_exists(VP_TUTORAT_GROUP):
            errors.append(checks.Warning(
                'no group {} found'.format(VP_TUTORAT_GROUP),
                hint='Create the {} group'.format(VP_TUTORAT_GROUP),
                obj=cls,
            ))
        return errors

    # API permissions

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        """Can only be created or destroyed by admin or VP Tutorat."""
        return is_in_group(request.user, VP_TUTORAT_GROUP)

    @allow_staff_or_superuser
    def has_object_update_permission(self, request):
        """Can only be updated by admin, leader tutor or VP tutorat."""
        is_leader = (self.tutors
                     .filter(user_id=request.user.id, is_leader=True)
                     .exists())
        is_vp_tutorat = is_in_group(request.user, VP_TUTORAT_GROUP)
        return is_leader or is_vp_tutorat

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
    staffmembers : n-1 with users.SchoolStaffMember

    Meta
    ----
    ordering : by name
    """

    name = models.CharField('nom', max_length=200, help_text='Nom du lycée')

    # TODO add UAI code validation
    uai_code = models.CharField(
        'code UAI', max_length=8, primary_key=True,
        validators=[uai_code_validator],
        help_text=(
            "Code UAI (ex-RNE) de l'établissement. "
            "Celui-ci est composé de 7 chiffres et une lettre. "
            "Ce code est répertorié dans "
            "l'annuaire des établissements sur le site du "
            "ministère de l'Éducation Nationale."))

    # TODO convert to validated address field
    address = models.CharField('adresse', max_length=200,
                               help_text='Adresse complète du lycée')

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
        return f'{self.tutoring_group} ({date})'
