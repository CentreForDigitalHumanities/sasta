# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import (
    AnalysisRun,
    AssessmentMethod,
    Compound,
    CompoundFile,
    Corpus,
    MethodCategory,
    Transcript,
    UploadFile,
    Utterance,
)


class TranscriptInline(admin.TabularInline):
    model = Transcript


@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    model = Corpus
    inlines = (TranscriptInline,)
    list_display = ('name', 'user')


@admin.register(Utterance)
class UtteranceAdmin(admin.ModelAdmin):
    list_display = ('transcript', '__str__')
    model = Utterance


class UtteranceInline(admin.TabularInline):
    model = Utterance


@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    inlines = (UtteranceInline, )
    list_display = ('__str__', 'corpus', 'status', 'has_corrections')
    list_filter = ('status', 'corpus')
    model = Transcript

    def has_corrections(self, obj):
        return obj.corrections is not None


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    model = UploadFile


@admin.register(AssessmentMethod)
class AssessmentMethodAdmin(admin.ModelAdmin):
    model = AssessmentMethod
    readonly_fields = ('date_added',)
    list_display = ('category', 'name', 'queries')

    def queries(self, obj):
        if not obj.content:
            return 0
        return len(obj.to_sastadev().queries)

@admin.register(CompoundFile)
class CompoundFileAdmin(admin.ModelAdmin):
    model = CompoundFile


@admin.register(Compound)
class CompoundAdmin(admin.ModelAdmin):
    model = Compound


@admin.register(MethodCategory)
class MethodCategoryAdmin(admin.ModelAdmin):
    model = MethodCategory


@admin.register(AnalysisRun)
class AnalysisRunAdmin(admin.ModelAdmin):
    model = AnalysisRun
    list_display = ('__str__', 'created', 'method', 'is_manual_correction')
