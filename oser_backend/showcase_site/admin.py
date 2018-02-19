"""Showcase site admin panel configuration."""

from django.contrib import admin
from .models import Article
from .models import Category
from .models import Testimony

# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Article admin panel."""
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('published',)

    list_display = ('title', 'published', 'pinned',)

    class Meta:  # noqa
        model = Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin panel."""

    list_display = ('title', 'get_num_articles',)

    def get_num_articles(self, obj):
        return obj.article_set.count()
    get_num_articles.short_description = "Nombre d'articles"

    class Meta:  # noqa
        model = Category


@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    """Testimony admin panel."""

    list_display = ('__str__', 'get_preview', 'created',)
    list_filter = ('created',)

    def get_preview(self, obj):
        if len(obj.content) > 100:
            return obj.content[:100] + ' […]'
        return obj.content
    get_preview.short_description = 'Aperçu'
