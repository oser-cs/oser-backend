"""Showcase site models."""

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from dry_rest_permissions.generics import authenticated_users

from markdownx.models import MarkdownxField


# Create your models here.


class Category(models.Model):
    """Represents a group of articles."""

    title = models.CharField('titre', max_length=100, unique=True)

    @property
    def articles_count(self):
        """Return the number of articles in this category."""
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
    slug = models.SlugField(
        max_length=100, unique=True,
        help_text=(
            "Un court identifiant généré après la création de l'article."
        ))
    content = MarkdownxField(
        'contenu',
        help_text="Contenu complet de l'article")
    published = models.DateTimeField('date de publication', auto_now_add=True)
    image = models.ImageField('illustration', blank=True, null=True,
                              upload_to='articles/')
    pinned = models.BooleanField('épinglé', default=False, blank=True)
    # ^blank=True to allow True of False value (otherwise
    # validation would force pinned to be True)
    # see: https://docs.djangoproject.com/fr/2.0/ref/forms/fields/#booleanfield
    categories = models.ManyToManyField(
        'Category', blank=True,
        help_text="Catégories auxquelles rattacher l'article",
        verbose_name='catégories')

    def save(self, *args, **kwargs):
        """Assign a slug on article creation."""
        if self.pk is None and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:  # noqa
        verbose_name = 'article'
        ordering = ('-pinned', '-published',)

    def get_absolute_url(self):
        """Return the article's absolute url."""
        return reverse('api:article-detail', args=[str(self.pk)])

    # Permissions

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    def __str__(self):
        return str(self.title)


class Action(models.Model):
    """Represents a key action point the association pursues."""

    title = models.CharField('titre', max_length=30)
    thumbnail = models.ImageField(
        'illustration', null=True, blank=True, upload_to='actions/',
        help_text=(
            "Une petite image représentant l'action. "
            "Format recommandé : 200x200"
        )
    )
    description = MarkdownxField()
    key_figure = models.TextField(
        'chiffre clé',
        default='', blank=True,
        help_text=(
            "Enoncer un chiffre clé à propos de cette action. "
            "Exemple : "
            "'En 2018, 18 sorties ont été organisées dans des lieux tels que…'"
        )
    )
    highlight = models.BooleanField(
        "mettre en avant", default=True,
        help_text=(
            "Cochez pour afficher cette action sur la page d'accueil. "
            "Pour un affichage optimal, assurez-vous alors d'avoir renseigné "
            "une illustration."
        )
    )
    order = models.PositiveIntegerField('ordre', default=0)

    class Meta:  # noqa
        verbose_name = 'action clé'
        verbose_name_plural = 'actions clés'
        ordering = ('order',)

    def __str__(self):
        return str(self.title)


class Testimony(models.Model):
    """Represents a testimony of a person on the association."""

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


class KeyFigure(models.Model):
    """A key figure about the association."""

    figure = models.PositiveIntegerField(
        'chiffre',
        help_text='Un nombre entier positif. Exemple : 60')
    description = models.CharField(
        max_length=100,
        help_text=(
            "Une courte description du chiffre "
            "(sera convertie en minuscules). "
            "Exemple : millions d'amis."))
    order = models.PositiveIntegerField('ordre', default=0)

    class Meta:  # noqa
        verbose_name = 'chiffre clé'
        verbose_name_plural = 'chiffres clés'
        ordering = ('order',)

    def save(self, *args, **kwargs):
        # Always save description as lowercase
        self.description = self.description.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.figure, self.description)


class Partner(models.Model):
    """Represents a partner of the association.

    Basic model but could be extended to store further
    information about the partnership.
    """

    name = models.CharField('nom', max_length=200)
    website = models.URLField('site internet', null=True)
    logo = models.ImageField(
        help_text=(
            "Image PNG avec arrière-plan transparent. "
            "Dimensions recommandées : hauteur = 320px. "
        ),
        null=True,
        upload_to='partners/',
    )
    premium = models.BooleanField(
        'partenaire privilégié', default=False,
        help_text=(
            "Cocher si ce partenaire est un partenaire privilégié. Il "
            "sera davantage mis en avant sur le site. Exemple : les "
            "organismes de subventions peuvent être des partenaires "
            "secondaires et les entreprises des partenaires principaux."
        )
    )
    active = models.BooleanField(
        'actif', default=True,
        help_text=(
            "Cocher si le partenariat est actif. Les partenariats inactifs "
            "ne seront pas affichés sur le site."
        )
    )
    start_date = models.DateField(
        'début du partenariat', default=now, blank=True, null=True,
        help_text=(
            "Laisser vide si inconnu. "
            "(Cette information est stockée pour historique uniquement.)"
        ))

    class Meta:  # noqa
        verbose_name = 'partenaire'
        ordering = ('-active', '-premium', '-start_date', 'name',)

    def __str__(self):
        return str(self.name)
