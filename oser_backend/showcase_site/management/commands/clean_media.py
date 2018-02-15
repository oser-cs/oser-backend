import os

from django.apps import apps
from django.db.models import Q
from django.db.models import FileField
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Management command to delete all unused media files.

    Inspired by
    -----------
    https://www.algotech.solutions/blog/python/deleting-unused-django-media-files/
    """

    help = "Delete all unused media files."
    media_root = getattr(settings, 'MEDIA_ROOT', None)

    def get_db_files(self):
        """Retrieve all references to files in the database.

        Returns
        -------
        db_files : set
        """
        all_models = apps.get_models()
        db_files = set()

        for model in all_models:
            file_fields = []
            filters = Q()
            for field in model._meta.fields:
                if isinstance(field, FileField):
                    file_fields.append(field.name)
                    is_null = {'{}__isnull'.format(field.name): True}
                    is_empty = {'{}__exact'.format(field.name): ''}
                    filters &= Q(**is_null) | Q(**is_empty)
            # only retrieve the models which have non-empty, non-null file
            # fields
            if file_fields:
                files = (model.objects.exclude(filters)
                         .values_list(*file_fields, flat=True)
                         .distinct())
                db_files.update(files)

        return db_files

    def get_physical_files(self):
        """Retrieve the set of physical media files.

        Returns
        -------
        physical_files : set
        """
        physical_files = set()

        if not self.media_root:
            return physical_files

        # Get all files from the MEDIA_ROOT, recursively
        for relative_root, dirs, files in os.walk(self.media_root):
            for file_ in files:
                physical_files.add(file_)

        return physical_files

    def handle(self, *args, **options):
        """Find unused media files and delete them."""
        db_files = self.get_db_files()
        physical_files = self.get_physical_files()

        # delete physical files that have no references in the DB
        deletables = physical_files - db_files

        if deletables:
            unused = len(deletables)
            self.stdout.write('Unused media files were detected:')
            self.stdout.write('\n'.join(f_ for f_ in deletables))

            for file_ in deletables:
                os.remove(os.path.join(self.media_root, file_))

            # Delete all empty folders, bottom-up
            walk = os.walk(self.media_root, topdown=False)
            for relative_root, dirs, files in walk:
                for dir_ in dirs:
                    if not os.listdir(os.path.join(relative_root, dir_)):
                        os.rmdir(os.path.join(relative_root, dir_))
            self.stdout.write(
                self.style.SUCCESS('Removed {} unused media file(s).'
                                   .format(unused)))
        else:
            self.stdout.write(self.style.SUCCESS(
                'No unused media files detected.'))
