"""Tutoring models."""

from django.db import models
from django.shortcuts import reverse

# Create your models here.


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


class TutoringGroup(models.Model):
    """Represents a tutoring group to which tutors and students participate.

    Fields
    ------
    name : char
    students : n-1 with persons.Student
    tutors : n-n with persons.Tutor
    """

    name = models.CharField('nom', max_length=200)
    tutors = models.ManyToManyField('persons.Tutor',
                                    related_name='tutoring_groups',
                                    verbose_name='tuteurs',
                                    blank=True)
    # TODO add SchoolYear foreign key

    class Meta:  # noqa
        ordering = ('name',)
        verbose_name = 'groupe de tutorat'
        verbose_name_plural = 'groupes de tutorat'

    def get_absolute_url(self):
        return reverse('api:tutoringgroup-detail', args=[str(self.id)])

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
    students : n-1 with persons.Student
    staffmembers : n-1 with persons.SchoolStaffMember

    Meta
    ----
    ordering : by name
    """

    name = models.CharField('nom', max_length=200)

    # TODO add UAI code validation
    uai_code = models.CharField(
        'code UAI', max_length=8, primary_key=True,
        help_text=(
            "Code UAI (ex-RNE) de l'établissement. "
            "Celui-ci est composé de 7 chiffres et une lettre. "
            "Si vous ne le connaissez pas, consultez "
            "l'annuaire des établissements sur le site du "
            "ministère de l'Éducation Nationale."))

    # TODO convert to validated address field
    address = models.CharField('adresse', max_length=200)

    class Meta:  # noqa
        ordering = ('name',)
        verbose_name = 'lycée'

    def get_absolute_url(self):
        return reverse('api:school-detail', args=[str(self.uai_code)])
