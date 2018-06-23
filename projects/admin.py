"""Projects admin configuration."""

from django.contrib import admin

from dynamicforms.views import download_multiple_forms_entries
from dynamicforms.models import Form
from .models import Edition, Participation, Project, EditionForm


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin panel for projects."""

    list_display = ('__str__', 'logo', 'num_editions', 'last_edition',
                    'total_accepted_participations')

    def num_editions(self, obj: Project) -> int:
        """Return the number of editions."""
        return obj.editions.count()
    num_editions.short_description = "Éditions"

    def last_edition(self, obj: Project) -> int:
        """Return the year of the last edition."""
        return obj.editions.latest().year
    last_edition.short_description = 'Année de la dernière édition'

    def total_accepted_participations(self, obj: Project) -> int:
        """Return total number of accepted participations."""
        return obj.total_participations(state=Participation.STATE_ACCEPTED)
    total_accepted_participations.short_description = 'Participations totales'


class OrganizersInline(admin.TabularInline):
    """Inline for edition organizers."""

    model = Edition.organizers.through
    extra = 0


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    """Admin panel for editions."""

    list_display = ('project', 'year',
                    'num_pending', 'num_validated', 'num_accepted',
                    'num_rejected', 'num_cancelled')
    list_filter = ('project', 'year',)
    inlines = (OrganizersInline,)

    def num_pending(self, obj: Edition) -> int:
        """Return number of pending participations."""
        return obj.participations.pending().count()
    num_pending.short_description = 'En attente'

    def num_validated(self, obj: Edition) -> int:
        """Return number of validated participations."""
        return obj.participations.validated().count()
    num_validated.short_description = 'Validés'

    def num_accepted(self, obj: Edition) -> int:
        """Return number of accepted participations."""
        return obj.participations.accepted().count()
    num_accepted.short_description = 'Acceptés'

    def num_rejected(self, obj: Edition) -> int:
        """Return number of rejected participations."""
        return obj.participations.rejected().count()
    num_rejected.short_description = 'Refusés'

    def num_cancelled(self, obj: Edition) -> int:
        """Return number of cancelled participations."""
        return obj.participations.cancelled().count()
    num_cancelled.short_description = 'Annulés'


@admin.register(EditionForm)
class EditionFormAdmin(admin.ModelAdmin):
    """Admin panel for edition forms."""

    list_display = ('form', 'deadline', 'recipient',)
    list_filter = ('edition', 'deadline',)

    actions = ['download_csv']

    def download_csv(self, request, queryset):
        """Download entries of selected edition forms under a ZIP file."""
        form_ids = queryset.values_list('form__id', flat=True)
        forms = Form.objects.filter(id__in=form_ids)
        return download_multiple_forms_entries(request, forms=forms)

    download_csv.short_description = (
        'Télécharger les résponses des formulaires sélectionnés')


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    """Participation admin panel."""

    list_display = ('user', 'edition', 'submitted', 'state')
    list_filter = ('edition', 'submitted', 'state',)
    readonly_fields = ('submitted',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email',)
