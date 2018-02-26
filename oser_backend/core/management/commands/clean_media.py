"""Clean unusued media files."""

import os
from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand
from django.db.models import FileField, Q
from markdownx.models import MarkdownxField
from core.management.file_utils import find_file, extract_md_file_refs


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
        db_files : set of filenames
        """
        all_models = apps.get_models()
        db_files = set()

        for model in all_models:
            file_fields = []
            filters = Q()

            # FileFields : only retrieve the models which have non-empty,
            # non-null file fields.
            for field in model._meta.fields:
                if isinstance(field, FileField):
                    file_fields.append(field.name)
                    is_null = {'{}__isnull'.format(field.name): True}
                    is_empty = {'{}__exact'.format(field.name): ''}
                    filters &= Q(**is_null) | Q(**is_empty)
            for field in file_fields:
                field_files = (model.objects.exclude(filters)
                               .values_list(field, flat=True)
                               .distinct())
                db_files.update(field_files)

            # MarkdownxFields can contain references to files in the form
            # of [](xxx) or ![](xxx).
            # NOTE: URLs may be included but they are not physical files
            # and won't be deleted (see handle()).
            model_markdown_fields = filter(
                lambda f: isinstance(f, MarkdownxField), model._meta.fields)
            for field in model_markdown_fields:
                for md in model.objects.values_list(field.name, flat=True):
                    db_files.update(extract_md_file_refs(md))

        return db_files

    def get_physical_files(self):
        """Retrieve the set of physical media files.

        Returns
        -------
        physical_files : set of filenames
        """
        physical_files = set()

        if not self.media_root:
            return physical_files

        # Get all files from the MEDIA_ROOT, recursively
        for dir_root, dirs, files in os.walk(self.media_root):
            for file_ in files:
                physical_files.add(file_)

        return physical_files

    def handle(self, *args, **options):
        """Find unused media files and delete them."""
        db_files = self.get_db_files()
        physical_files = self.get_physical_files()

        # Delete physical files that have no references in the DB.
        # NOTE: DB files that are not physical files will not be included.
        # This means that potential URLs detected in Markdown fields
        # are not considered as deletables.
        deletables = physical_files - db_files

        if deletables:
            self.stdout.write(
                self.style.NOTICE('Unused media files were detected:'))
            self.stdout.write('\n'.join(f_ for f_ in deletables))

            deleted = 0
            # Record files not found for safety measure.
            # Normally, all deletables should be existing files.
            not_found = 0

            # Delete files
            for file_ in deletables:
                try:
                    os.remove(find_file(file_, self.media_root))
                    deleted += 1
                except FileNotFoundError as e:
                    not_found += 1

            # Delete all empty folders, bottom-up
            walk = os.walk(self.media_root, topdown=False)
            for relative_root, dirs, files in walk:
                for dir_ in dirs:
                    if not os.listdir(os.path.join(relative_root, dir_)):
                        os.rmdir(os.path.join(relative_root, dir_))

            self.stdout.write(
                self.style.SUCCESS('Removed {} unused media file(s).'
                                   .format(deleted)))
            if not_found:
                self.stdout.write(self.style.ERROR(
                    '{} unused media file(s) failed to be deleted.'
                    .format(not_found)))
        else:
            self.stdout.write(self.style.SUCCESS(
                'No unused media files detected.'))
