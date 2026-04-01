# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from io import BytesIO, StringIO
from operator import is_

from analysis.query.run import annotate_transcript
from analysis.tasks import analyse_transcript_task
from analysis.utils import create_analysis_run
from annotations.reader import read_saf
from annotations.writers.querycounts import querycounts_to_xlsx
from annotations.writers.saf_chat import enrich_chat
from annotations.writers.saf_xlsx import SAFWriter
from celery import group
from convert.chat_writer import ChatWriter
from django.db.models import Q
from django.http import HttpResponse
from openpyxl import load_workbook
from parse.parse_utils import parse_and_create
from parse.tasks import parse_transcript_task
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from parse.views import CeleryTaskView

from .convert.convert import convert
from .models import (AnalysisRun, AssessmentMethod, Corpus, MethodCategory,
                     Transcript, UploadFile)
from .permissions import IsCorpusChildOwner, IsCorpusOwner
from .serializers import (AssessmentMethodSerializer, CorpusDetailsSerializer,
                          CorpusListSerializer, MethodCategorySerializer,
                          TranscriptDetailsSerializer,
                          TranscriptListSerializer, UploadFileSerializer)

logger = logging.getLogger('sasta')

# flake8: noqa: E501
SPREADSHEET_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


class UploadFileViewSet(viewsets.ModelViewSet):
    queryset = UploadFile.objects.all()
    serializer_class = UploadFileSerializer
    permission_classes = (IsCorpusChildOwner, )

    def get_queryset(self):
        return self.queryset.filter(corpus__user=self.request.user)


class TranscriptViewSet(viewsets.ModelViewSet):
    queryset = Transcript.objects.all()
    permission_classes = (IsCorpusChildOwner,)

    def get_serializer_class(self):
        if self.action == 'list':
            return TranscriptListSerializer
        return TranscriptDetailsSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(corpus__user=self.request.user)

    @action(detail=True, methods=['POST'], name='Score transcript')
    def query(self, request, *args, **kwargs):
        transcript = self.get_object()
        method_id = request.data.get('method')
        method = AssessmentMethod.objects.get(pk=method_id)

        response = HttpResponse(
            content_type=SPREADSHEET_MIMETYPE)
        response['Content-Disposition'] = "attachment; filename=matches_output.xlsx"

        allresults = annotate_transcript(transcript, method)

        spreadsheet = querycounts_to_xlsx(allresults, method)
        spreadsheet.save(response)

        return response

    @action(detail=True, methods=['POST'], name='Annotate')
    def annotate(self, request, *args, **kwargs):
        # Retrieve objects
        transcript = self.get_object()
        method_id = request.data.get('method')
        method = AssessmentMethod.objects.get(pk=method_id)

        # Perform the actual querying
        allresults = annotate_transcript(transcript, method)

        # Always create an XLSX file for AnalysisRun purposes
        writer = SAFWriter(method.to_sastadev(), allresults)
        spreadsheet = writer.workbook
        create_analysis_run(transcript, method, spreadsheet)

        # Adapt output to requested format
        format = request.data.get('format', 'xlsx')

        if format == 'xlsx':
            response = HttpResponse(
                content_type=SPREADSHEET_MIMETYPE)
            response['Content-Disposition'] = "attachment; filename=saf_output.xlsx"
            spreadsheet.save(response)

            return response

        if format == 'cha':
            enriched = enrich_chat(transcript, allresults, method)
            output = StringIO()
            writer = ChatWriter(enriched, target=output)
            writer.write()
            output.seek(0)

            response = HttpResponse(
                output.getvalue(), content_type='text/plain')
            response['Content-Disposition'] = "attachment; filename=annotated.cha"

            return response

    @action(detail=True, methods=['POST'], name='Annotate (async)')
    def analyse_async(self, request, *args, **kwargs):
        # Retrieve objects
        transcript = self.get_object()
        transcript_id = transcript.pk
        method_id = request.data.get('method')
        method = AssessmentMethod.objects.get(pk=method_id)

        # create an AnalysisRun without annotations file to attach the task id to
        run = AnalysisRun.objects.create(transcript=transcript, method=method,
                                         is_manual_correction=False)

        # create the async task
        task = analyse_transcript_task.s(
            transcript_id, method_id, run.pk).delay()

        # attach task id to analysisrun without results
        run.task_id = task.id
        run.save()

        # return task_id
        return Response(task.id)

    @action(detail=True, methods=['GET'], name='Download latest annotation', url_path='annotations/latest')
    def latest_annotations(self, request, *args, **kwargs):
        obj = self.get_object()
        run = AnalysisRun.objects.filter(transcript=obj).latest()

        filename = run.annotation_file.name.split('/')[-1]
        response = HttpResponse(run.annotation_file,
                                content_type=SPREADSHEET_MIMETYPE)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

    @action(detail=True, methods=['GET'], name='Reset annotations', url_path='annotations/reset')
    def reset_annotations(self, request, *args, **kwargs):
        obj = self.get_object()
        all_runs = AnalysisRun.objects.filter(transcript=obj)
        all_runs.delete()
        return Response('Success', status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], name='Upload annotations', url_path='annotations/upload')
    def upload_annotations(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            latest_run = AnalysisRun.objects.filter(transcript=obj).latest()
        except AnalysisRun.DoesNotExist:
            return Response('No previous annotations found for this transcript. Run regular annotating at least once before providing corrected input.',
                            status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['content'].file

        new_run = create_analysis_run(
            obj, latest_run.method, file, is_manual=True)

        try:
            read_saf(new_run.annotation_file.path,
                     latest_run.method.to_sastadev())
        except Exception as e:
            new_run.delete()
            logger.exception(e)
            return Response(str(e), status.HTTP_400_BAD_REQUEST)

        return Response('Success', status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], name='Generate form')
    def generateform(self, request, *args, **kwargs):
        # Retrieve objects
        transcript = self.get_object()
        method_id = request.data.get('method')
        method = AssessmentMethod.objects.get(pk=method_id)

        # Find the form function for this method
        form_func = method.category.get_form_function()
        if not form_func:
            raise ParseError(detail='No form definition for this method.')

        allresults = annotate_transcript(transcript, method)

        form = form_func(allresults, None, in_memory=True)

        form.seek(0)

        # Weird hack to prevent Excel warning about corrupted files: copying the whole workbook to a new bytestream
        # TODO: Find out why openpyxl corrupts only the STAP forms (probably to do with copying of exisitng xlsx file)
        if method.category.name == 'STAP':
            new_target = BytesIO()
            wb = load_workbook(form)
            wb.save(new_target)
            new_target.seek(0)
        else:
            new_target = form

        response = HttpResponse(
            new_target,
            content_type=SPREADSHEET_MIMETYPE)
        response['Content-Disposition'] = f"attachment; filename={transcript.name}_{method.category.name}_form.xlsx"

        return response

    @action(detail=True, methods=['GET'], name='convert')
    def convert(self, request, *args, **kwargs):
        transcript = self.get_object()
        if transcript.status == Transcript.CONVERTED:
            return Response(self.get_serializer(transcript).data)
        result = convert(transcript)
        if result:
            return Response(self.get_serializer(result).data)
        return Response(None, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], name='parse')
    def parse(self, request, *args, **kwargs):
        transcript = self.get_object()
        if transcript.status in (Transcript.CONVERTED, Transcript.PARSING_FAILED):
            result = parse_and_create(transcript)
            if result:
                return Response(self.get_serializer(result).data)
        if transcript.status == Transcript.PARSED:
            return Response(self.get_serializer(transcript).data)

        return Response(None, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], name='parse_async')
    def parse_async(self, request, *args, **kwargs):
        transcript = self.get_object()
        if not transcript.parseable():
            return Response('Transcript not parseable', status.HTTP_400_BAD_REQUEST)

        task = parse_transcript_task.s(transcript.id).delay()
        if not task:
            return Response('Failed to create task', status.HTTP_400_BAD_REQUEST)
        return Response(task.id)

    @action(detail=True, methods=['POST'], name='results', url_name='results', url_path='results')
    def get_results(self, request, *args, **kwargs):
        '''Use existing AnalysisRun to get results for a transcript and method, without re-running sastacore'''
        transcript = self.get_object()
        run = AnalysisRun.objects.filter(transcript=transcript).latest()
        method = run.method

        format = request.data.get('format', 'xlsx')

        # format: xlsx
        if format == 'xlsx':
            filename = run.annotation_file.name.split('/')[-1]
            response = HttpResponse(run.annotation_file,
                                    content_type=SPREADSHEET_MIMETYPE)
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response

        # format: cha
        # return enriched chat based on analysisrun.allresults
        if format == 'cha':
            enriched = enrich_chat(transcript, run.allresults, method)
            output = StringIO()
            writer = ChatWriter(enriched, target=output)
            writer.write()
            output.seek(0)

            response = HttpResponse(
                output.getvalue(), content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename={transcript.name}_{method.category.name}_annotated.cha'

            return response

        # format: form
        # return form based on analysisrun.allresults
        if format == 'form':
            form_func = method.category.get_form_function()
            if not form_func:
                raise ParseError(detail='No form definition for this method.')

            form = form_func(run.allresults, None, in_memory=True)

            form.seek(0)

            # Weird hack to prevent Excel warning about corrupted files: copying the whole workbook to a new bytestream
            # TODO: Find out why openpyxl corrupts only the STAP forms (probably to do with copying of exisitng xlsx file)
            if method.category.name == 'STAP':
                new_target = BytesIO()
                wb = load_workbook(form)
                wb.save(new_target)
                new_target.seek(0)
            else:
                new_target = form

            response = HttpResponse(
                new_target,
                content_type=SPREADSHEET_MIMETYPE)
            response['Content-Disposition'] = f"attachment; filename={transcript.name}_{method.category.name}_form.xlsx"

            return response



class CorpusViewSet(viewsets.ModelViewSet):
    queryset = Corpus.objects.all()
    permission_classes = (IsCorpusOwner, )

    def get_serializer_class(self):
        if self.action == 'list':
            return CorpusListSerializer
        return CorpusDetailsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=['GET'], name='convert_all')
    def convert_all(self, request, *args, **kwargs):
        corpus = self.get_object()
        transcripts = Transcript.objects.filter(
            Q(corpus=corpus),
            Q(status=Transcript.CREATED) | Q(status=Transcript.CONVERSION_FAILED))

        for t in transcripts:
            res = convert(t)
            if not res:
                return Response('Failed', status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(corpus).data)

    @action(detail=True, methods=['GET'], name='parse_all')
    def parse_all(self, request, *args, **kwargs):
        corpus = self.get_object()
        transcripts = Transcript.objects.filter(
            Q(corpus=corpus),
            Q(status=Transcript.CONVERTED) | Q(status=Transcript.PARSING_FAILED))
        for t in transcripts:
            res = parse_and_create(t)
            if not res:
                return Response('Failed', status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(corpus).data)

    @action(detail=True, methods=['GET'], name='parse_all_async')
    def parse_all_async(self, request, *args, **kwargs):
        corpus = self.get_object()
        transcripts = Transcript.objects.filter(
            Q(corpus=corpus), Q(status=Transcript.CONVERTED) | Q(
                status=Transcript.PARSING_FAILED)
        )

        # If in DEBUG mode and celery not running, parse synchronously
        # TODO: fix
        # if settings.DEBUG and get_celery_worker_status():
        #     logger.info('Bypassing Celery')
        #     return self.parse_all()

        task = group(parse_transcript_task.s(t.id)
                     for t in transcripts).delay()

        if not task:
            return Response('Failed to create task', status.HTTP_400_BAD_REQUEST)
        return Response(task.id)

    @action(detail=True, methods=['POST'], name='download')
    def download(self, request, *args, **kwargs):
        corpus = self.get_object()
        stream = corpus.download_as_zip()
        response = HttpResponse(
            stream.getvalue(), content_type='application/x-zip-compressed')
        response['Content-Disposition'] = f'attachment; filename={corpus.name}.zip'

        return response

    @action(detail=True, methods=['POST'], name='setdefaultmethod')
    def defaultmethod(self, request, *args, **kwargs):
        corpus = self.get_object()
        method_id = request.data.get('method')
        if method_id == 'null':
            method = None
        else:
            method = AssessmentMethod.objects.get(pk=method_id)
        corpus.default_method = method
        corpus.save()
        return Response('Succes')


class AssessmentMethodViewSet(viewsets.ModelViewSet):
    queryset = AssessmentMethod.objects.all()
    serializer_class = AssessmentMethodSerializer


class MethodCategoryViewSet(viewsets.ModelViewSet):
    queryset = MethodCategory.objects.all()
    serializer_class = MethodCategorySerializer


class AnalysisTaskView(CeleryTaskView):
    '''View for starting analysis tasks
    For now, only implements parent functionality of CeleryTaskView,
    but can be extended with analysis-specific functionality if needed'''
    pass
