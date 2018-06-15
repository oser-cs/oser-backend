"""Dynamic forms admin panels."""

from django.contrib import admin
from .models import Form, Section, Question, FormEntry, Answer, File


class SectionInline(admin.StackedInline):
    """Inline for sections."""

    model = Section
    extra = 0


class QuestionInline(admin.StackedInline):
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
    readonly_fields = ('slug',)
    search_fields = ('title',)
    inlines = (SectionInline, FileInline,)


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
