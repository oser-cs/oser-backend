"""Showcase site models."""

from django.db import models
from django.shortcuts import reverse
from dry_rest_permissions.generics import authenticated_users

# Create your models here.


class Article(models.Model):
    """Represents a piece of news.

    Fields
    ------
    title : str
        Title of the news.
    slug : str
        A brief label identifying the article.
        It is generated from the title on creation.
        However, it is not used for the article's API URL.
    content : str
        Full content of the news.
    published : date
        Date the article was published. Today's date by default.
    image : Image
        An image to illustrate the article.
    pinned : bool
    """

    title = models.CharField('titre', max_length=300)
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField('contenu')  # TODO add Markdown support
    published = models.DateTimeField('date de publication', auto_now_add=True)
    image = models.ImageField('illustration', blank=True, null=True)
    pinned = models.BooleanField('épinglé', default=False, blank=True)
    # ^blank=True to allow True of False value (otherwise
    # validation would force pinned to be True)
    # see: https://docs.djangoproject.com/fr/2.0/ref/forms/fields/#booleanfield

    class Meta:  # noqa
        verbose_name = 'article'
        ordering = ('-published',)

    def get_absolute_url(self):
        """Return the article's absolute url."""
        return reverse('api:article-detail', args=[str(self.pk)])

    # Permissions

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True

    @authenticated_users
    def has_object_write_permission(self, request):
        return True

    def __str__(self):
        return str(self.title)
