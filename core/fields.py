"""Core fields."""

from rest_framework import serializers

from .markdown import add_domain_to_image_files


class MarkdownField(serializers.Field):
    """Custom field for fields that contain Markdown text.

    Mainly ensures that image references contain a complete link
    including the server's host name.

    Should be used on markdownx.MarkdownxField fields.
    """

    def to_representation(self, obj):
        request = self.context['request']
        return add_domain_to_image_files(request, obj)

    def to_internal_value(self, data):
        return data
