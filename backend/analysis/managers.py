from django.apps import apps
from django.db import models
from django.db.models import Q


class TranscriptManager(models.Manager):
    '''Custom querysets for Transcripts '''

    def need_converting(self):
        model = apps.get_model('analysis', 'Transcript')
        base = super().get_queryset()
        query = Q(status=model.CREATED) | Q(
            status=model.CONVERSION_FAILED)
        return base.filter(query)

    def need_parsing(self):
        model = apps.get_model('analysis', 'Transcript')
        base = super().get_queryset()
        query = Q(status=model.CONVERTED) | Q(
            status=model.PARSING_FAILED)
        return base.filter(query)
