"""Dynamic forms admin panels."""

from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin

from .models import Answer, File, Form, FormEntry, Question, Section
from .views import download_multiple_forms_entries


class SectionInline(SortableInlineAdminMixin, admin.StackedInline):
    """Inline for sections."""

    model = Section
    extra = 0


class QuestionInline(SortableInlineAdminMixin, admin.StackedInline):
    """Inline for questions."""

    model = Question
    extra = 0


class FileInline(admin.TabularInline):
    """Inline for form files."""

    model = File
    extra = 0


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    """Admin panel for forms."""

    list_display = ('title', 'created',)
    list_filter = ('created',)
    readonly_fields = ('slug', 'created',)
    search_fields = ('title',)
    inlines = (SectionInline, FileInline,)

    actions = ['download_csv']

    def download_csv(self, request, queryset):
        """Download entries of selected forms under a ZIP file."""
        return download_multiple_forms_entries(request, forms=queryset.all())

    download_csv.short_description = (
        'Télécharger les résponses des formulaires sélectionnés')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    """Admin panel for form sections."""

    list_display = ('title', 'form',)
    list_filter = ('form',)
    search_fields = ('title',)
    inlines = (QuestionInline,)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin panel for questions."""

    list_display = ('text', 'required', 'section', 'type',)
    list_filter = ('section__form',)
    search_fields = ('text', 'section__title, section__form__title',)


@admin.register(FormEntry)
class FormEntryAdmin(admin.ModelAdmin):
    """Admin panel for form entries."""

    list_display = ('form', 'submitted',)
    list_filter = ('form', 'submitted',)
    readonly_fields = ('submitted',)
    search_fields = ('form__title',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Admin panel for answers."""

    list_display = ('answer', 'question', 'entry')
    list_filter = ('entry__form',)
    search_fields = ('answer', 'question__text',)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    """Admin panel for form files."""

    list_display = ('name', 'file', 'form')
    list_filter = ('form',)
    search_fields = ('name',)
