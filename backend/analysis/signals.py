import csv
import logging
import os
import shutil
from typing import Union

from django.conf import settings
from django.db.models.fields.files import FieldFile
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import (AnalysisRun, AssessmentMethod, AssessmentQuery, Compound,
                     CompoundFile, Corpus, Transcript, UploadFile)
from .utils import extract, read_TAM

logger = logging.getLogger('sasta')


@receiver(post_save, sender=CompoundFile)
def save_compounds(sender, instance, **kwargs):
    Compound.objects.all().delete()
    with open(instance.content.path) as f:
        data = csv.reader(f, delimiter='\\')
        compounds = []
        for i, row in enumerate(data):
            compounds.append(
                Compound(HeadDiaNew=row[1], FlatClass=row[0], Class=row[2]))
        Compound.objects.bulk_create(compounds)


@receiver(post_delete, sender=Corpus)
def corpus_delete(sender, instance, **kwargs):
    corpus_dir = os.path.join(settings.MEDIA_ROOT, 'files', str(instance.uuid))
    shutil.rmtree(corpus_dir, ignore_errors=True)


@receiver(post_delete, sender=Transcript)
def transcript_delete(sender, instance, **kwargs):
    _attempt_file_delete(instance.content)
    _attempt_file_delete(instance.parsed_content)
    _attempt_file_delete(instance.corrected_content)
    _attempt_file_delete(instance.extracted_filename)


@receiver(post_save, sender=UploadFile)
def extract_upload_file(sender, instance, created, **kwargs):
    if created:
        try:
            extract(instance)
        except Exception as error:
            logger.exception(error)


@receiver(post_delete, sender=UploadFile)
@receiver(post_delete, sender=AssessmentMethod)
@receiver(post_delete, sender=CompoundFile)
def file_delete(sender, instance, **kwargs):
    try:
        instance.content.delete(False)
    except FileNotFoundError:
        pass


@receiver(post_save, sender=AssessmentMethod)
def read_method_file(sender, instance, created, **kwargs):
    if not created:
        # on update: delete all queries related to this method
        AssessmentQuery.objects.filter(method=instance).delete()
    try:
        read_TAM(instance)
    except Exception as error:
        logger.exception(error)
        print(f'error in read_tam_file:\t{error}')


@receiver(post_delete, sender=AnalysisRun)
def delete_annotation_files(sender, instance, **kwargs):
    try:
        instance.annotation_file.delete(False)
        instance.query_file.delete(False)
    except FileNotFoundError:
        pass


@receiver(post_save, sender=Corpus)
def initial_default_method(sender, instance, created, **kwargs):
    if created:
        try:
            instance.default_method = instance.method_category.definitions.latest()
            instance.save()
        except Exception as error:
            logger.exception(error)


def _attempt_file_delete(field: Union[FieldFile, str]) -> None:
    '''Helper function to attempt deletion of a file field.
    Also deletes the file at storage location if it exists.
    Works for both FileField and CharField.'''
    try:
        if isinstance(field, FieldFile):
            if field.storage.exists(field.name):
                field.storage.delete(field.name)
            field.delete(save=False)
        elif isinstance(field, str):
            if os.path.exists(field):
                os.remove(field)
    except FileNotFoundError:
        pass
    except Exception as error:
        logger.exception(error)
