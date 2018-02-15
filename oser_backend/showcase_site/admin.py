"""Showcase site admin panel configuration."""

from django.contrib import admin
from .models import Article

# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Article admin panel."""
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('published',)

    list_display = ('title', 'published', 'pinned')

    class Meta:  # noqa
        model = Article
