"""Showcase site admin panel configuration."""

from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Article
from .models import Category
from .models import Testimony
from .models import KeyFigure

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
        if len(obj.content) > self.preview_length:
            return (obj.content[:self.preview_length] +
                    self.preview_truncated_symbol)
        return obj.content
    get_preview.short_description = 'Aperçu'


@admin.register(KeyFigure)
class KeyFigureAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass
