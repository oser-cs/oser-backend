"""Showcase site models."""

from django.utils.text import slugify
from django.db import models
from django.shortcuts import reverse
from dry_rest_permissions.generics import authenticated_users

# Create your models here.


class Category(models.Model):
    """Represents a group of articles."""

    title = models.CharField('titre', max_length=100, unique=True)

    @property
    def articles_count(self):
        return self.article_set.count()

    class Meta:  # noqa
        verbose_name = 'catégorie'
        ordering = ('title',)

    def __str__(self):
        return str(self.title)


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

    title = models.CharField('titre', max_length=300,
                             help_text="Titre de l'article")
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField(
        'contenu',
        help_text="Contenu complet de l'article")  # TODO add Markdown support
    published = models.DateTimeField('date de publication', auto_now_add=True)
    image = models.ImageField('illustration', blank=True, null=True)
    pinned = models.BooleanField('épinglé', default=False, blank=True)
    # ^blank=True to allow True of False value (otherwise
    # validation would force pinned to be True)
    # see: https://docs.djangoproject.com/fr/2.0/ref/forms/fields/#booleanfield
    categories = models.ManyToManyField(
        'Category', blank=True,
        help_text="Catégories auxquelles rattacher l'article")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.title and not self.slug:
            self.slug = slugify(self.title)

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


class Testimony(models.Model):

    content = models.TextField('contenu')
    author_name = models.CharField('auteur', max_length=300,
                                   help_text="Nom de l'auteur")
    author_position = models.CharField(
        'position',
        max_length=300,
        help_text="Position de l'auteur (lycéen, professeur…)")
    created = models.DateField('date de création', auto_now_add=True)

    @property
    def author(self):
        return ('{}, {}'
                .format(self.author_name, self.author_position.lower()))
    author.fget.short_description = 'auteur'

    class Meta:  # noqa
        verbose_name = 'témoignage'
        ordering = ('-created', 'author_name',)

    def __str__(self):
        return self.author
