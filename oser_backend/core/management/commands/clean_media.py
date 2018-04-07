"""Clean unusued media files."""

import os.path

from django.apps import apps
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management import BaseCommand
from django.db.models import FileField, Q

from core.file_utils import walk as os_walk
from core.markdown import extract_md_file_refs
from markdownx.models import MarkdownxField


class Command(BaseCommand):
    """Management command to delete all unused media files.

    Inspired by
    -----------
    https://www.algotech.solutions/blog/python/deleting-unused-django-media-files/
    """

    help = "Delete all unused media files."
    media_root = getattr(settings, 'MEDIA_ROOT', '')
    top = ''

    def add_arguments(self, parser):
        parser.add_argument(
            '--top',
            dest='top',
            help='Top directory in which to look for unused media files.',
        )

    def get_db_files(self):
        """Retrieve all references to files in the database.

        Returns
        -------
        db_files : set of file paths relative to the MEDIA_ROOT
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

            def get_file_fields(field):
                for obj in model.objects.exclude(filters):
                    yield getattr(obj, field)

            for field in file_fields:
                # field_file.name is the path relative to the media root
                file_paths = [field_file.name
                              for field_file in get_file_fields(field)]
                db_files.update(file_paths)

            # MarkdownxFields can contain references to files in the form
            # of [](xxx) or ![](xxx).
            # NOTE: URLs may be included but they are not physical files
            # and won't be deleted (see handle()).
            model_markdown_fields = filter(
                lambda f: isinstance(f, MarkdownxField), model._meta.fields)
            for field in model_markdown_fields:
                for md in model.objects.values_list(field.name, flat=True):
                    file_refs = extract_md_file_refs(md)
                    db_files.update(ref.filename for ref in file_refs)

        return db_files

    def get_storage_files(self, location):
        """Retrieve the set of media files stored in default_storage.

        Parameters
        ----------
        location : str
            Directory where to look for unused media files, relative
            to the media_root.

        Returns
        -------
        storage_files : set of file paths relative to the MEDIA_ROOT
        """
        storage_files = set()

        if not self.media_root:
            return storage_files

        def onerror(e):
            self.stdout.write(self.style.ERROR(str(e)))

        # Get all files from location, recursively
        for dir_root, dirs, files in os_walk(default_storage, location,
                                             onerror=onerror):
            # dir_root is the absolute path except the filename
            # files contains filenames
            dir_relative_to_media_root = dir_root.replace(self.media_root, '')
            # remove leading slash
            dir_relative_to_media_root = dir_relative_to_media_root.lstrip('/')
            for file_ in files:
                file_path = os.path.join(dir_relative_to_media_root, file_)
                storage_files.add(file_path)

        return storage_files

    def clean_files(self, deletables):
        """Remove a list of files from default_storage."""
        deleted = 0
        # Record files not found for safety measure.
        # Normally, all deletables should be existing files.
        not_found = 0

        # Delete files
        for file_ in deletables:
            try:
                default_storage.delete(file_)
                deleted += 1
            except FileNotFoundError as e:
                not_found += 1

        # Delete all empty folders
        for dir_root, dirs, files in os_walk(default_storage, self.media_root,
                                             topdown=False):
            for dir_ in dirs:
                # build the path relative to the media_root
                dir_path = os.path.join(dir_root, dir_)
                dir_path = dir_path.replace(self.media_root, '').lstrip('/')
                # check the contents of the directory
                dirs_here, non_dirs_here = default_storage.listdir(dir_path)
                if not dirs_here and not non_dirs_here:
                    default_storage.delete(dir_path)

        return deleted, not_found

    def handle(self, *args, **options):
        """Find unused media files and delete them."""
        location = options.get('top') or ''

        db_files = self.get_db_files()
        storage_files = self.get_storage_files(location=location)

        # Delete physical files that have no references in the DB.
        # NOTE: DB files that are not physical files will not be included.
        # This means that potential URLs detected in Markdown fields
        # are not considered as deletables, which is an expected behavior.
        deletables = storage_files - db_files

        self.stdout.write(f'DB files: {db_files}')
        self.stdout.write(f'Storage files: {storage_files}')
        self.stdout.write(f'Deletables: {deletables}')

        if deletables:
            self.stdout.write(
                self.style.NOTICE('Unused media files were detected:'))
            self.stdout.write('\n'.join(f_ for f_ in deletables))

            deleted, not_found = self.clean_files(deletables)

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
