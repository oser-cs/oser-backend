"""Showcase site admin panel configuration."""

from django.contrib import admin
from .models import Article
from .models import Category

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
