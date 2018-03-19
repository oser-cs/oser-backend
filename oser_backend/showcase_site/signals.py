"""Showcase Site signals."""

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Article


# Create your signals here.

@receiver(pre_delete, sender=Article)
def clean_categories(sender, instance: Article, **kwargs):
    """Perform category cleanup just before an article is deleted.

    If no articles is tied to one of this article's categories,
    delete the category.
    """
    for category in instance.categories.all():
        # the article is still in the category's article_set
        if category.article_set.count() <= 1:
            category.delete()
