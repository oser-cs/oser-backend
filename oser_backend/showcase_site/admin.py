"""Showcase site admin panel configuration."""

from django.contrib import admin
from django.utils.html import format_html

from adminsortable2.admin import SortableAdminMixin

from .models import Article, Category, KeyFigure, Partner, Testimony


# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Article admin panel."""

    readonly_fields = ('slug', 'published',)

    list_display = ('title', 'published', 'pinned',)
    list_filter = ('published', 'pinned', 'categories')
    autocomplete_fields = ('categories',)
    # reorganize fields
    fields = ('title', 'slug', 'categories', 'pinned', 'image', 'content',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin panel."""

    list_display = ('title', 'get_num_articles',)
    search_fields = ('title',)

    def get_num_articles(self, obj):
        """Get number of articles in this category."""
        return obj.article_set.count()
    get_num_articles.short_description = "Nombre d'articles"


@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    """Testimony admin panel."""

    list_display = ('__str__', 'get_preview', 'created',)
    list_filter = ('created',)
    preview_length = 100
    preview_truncated_symbol = ' […]'

    def get_preview(self, obj):
        """Return a preview of the testimony.

        Max length of preview is preview_length.
        """
        if len(obj.content) > self.preview_length:
            return (obj.content[:self.preview_length] +
                    self.preview_truncated_symbol)
        return obj.content
    get_preview.short_description = 'Aperçu'


@admin.register(KeyFigure)
class KeyFigureAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Key figure admin panel.

    Key figures can be sorted through a drag'n'drop interface (thanks
    to django-admin-sortable2).
    """


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    """Partner admin panel."""

    list_display = ('__str__', 'thumbnail', 'get_website', 'premium', 'active')
    list_filter = ('active', 'premium',)

    def get_website(self, obj):
        """Return safe link to partner's website."""
        return format_html('<a target="_blank" href="{}">{}</a>',
                           obj.website, obj.website)
    get_website.short_description = 'Site internet'

    def thumbnail(self, obj):
        """Return thumbnail of partner's logo."""
        return format_html(
            '<img src="{}" alt="{}" style="max-width: 100px; height: auto;">',
            obj.logo.url, obj.name)
    thumbnail.short_description = 'Logo'
