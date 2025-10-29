import functools
import logging
import os
import zipfile
from io import BytesIO
from itertools import chain
from typing import Dict, List, Optional, Tuple
from uuid import uuid4

from analysis.managers import SastaQueryManager
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from lxml import etree as ET
from sastadev.external_functions import form_map
from sastadev.methods import Method
from sastadev.query import Query
from sastadev.readmethod import read_method

logger = logging.getLogger('sasta')


class Compound(models.Model):
    HeadDiaNew = models.CharField(max_length=100)
    FlatClass = models.CharField(max_length=100)
    Class = models.CharField(max_length=100)

    def __str__(self):
        return self.HeadDiaNew


class CompoundFile(models.Model):
    content = models.FileField(
        upload_to=os.path.join('files', 'compoundfiles'))

    def __str__(self):
        return os.path.split(self.content.name)[1]


class MethodCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    zc_embeddings = models.BooleanField()
    levels = ArrayField(base_field=models.CharField(max_length=20, blank=True))
    marking_postcodes = ArrayField(base_field=models.CharField(
        max_length=20, blank=True), default=list)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'method categories'

    def get_form_function(self):
        try:
            return form_map.get(self.name)
        except KeyError:
            return None

    def has_form(self):
        return True if self.get_form_function() else False

    def get_current_method(self):
        return self.definitions.latest()


class AssessmentMethod(models.Model):
    def upload_path(self, filename):
        return os.path.join('files', 'TAMs', filename)

    name = models.CharField(max_length=50)
    date_added = models.DateField(auto_now_add=True)
    content = models.FileField(
        upload_to=upload_path, blank=True, null=True, max_length=500)
    category = models.ForeignKey(
        MethodCategory, related_name='definitions',
        blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('category', 'name'))
        get_latest_by = ('date_added', )

    def to_sastadev(self, variant: Optional[str] = None) -> Method:
        return read_method(
            methodname=self.category.name.lower(),
            methodfilename=self.content.path,
            variant=variant)


class Corpus(models.Model):
    user = models.ForeignKey(
        User, related_name='corpora', on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    uuid = models.UUIDField(default=uuid4)
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    default_method = models.ForeignKey(AssessmentMethod,
                                       on_delete=models.SET_NULL,
                                       related_name='corpora',
                                       blank=True, null=True)
    method_category = models.ForeignKey(
        MethodCategory, on_delete=models.SET_DEFAULT,
        default=1, related_name='corpora')

    share_permission = models.BooleanField(
        verbose_name='Permission to share data',
        default=False
    )

    def __str__(self):
        return self.name

    def download_as_zip(self):
        stream = BytesIO()
        files = [t.get_filepaths() for t in self.transcripts.all()]
        files = list(chain.from_iterable(files))
        zipf = zipfile.ZipFile(stream, "w")
        for f in files:
            arcname = os.path.split(f)[1]
            zipf.write(f, arcname)
        zipf.close()
        return stream

    class Meta:
        verbose_name_plural = 'corpora'


class Transcript(models.Model):
    UNKNOWN = 0
    CREATED = 1
    CONVERTING, CONVERTED, CONVERSION_FAILED = 2, 3, 4
    PARSING, PARSED, PARSING_FAILED = 5, 6, 7

    STATUS_CHOICES = (
        (UNKNOWN, 'unknown'),
        (CREATED, 'created'),
        (CONVERTING, 'converting'),
        (CONVERTED, 'converted'),
        (CONVERSION_FAILED, 'conversion-failed'),
        (PARSING, 'parsing'),
        (PARSED, 'parsed'),
        (PARSING_FAILED, 'parsing-failed'),
    )

    def upload_path(self, filename):
        return os.path.join('files', f'{self.corpus.uuid}',
                            'transcripts', filename)

    def upload_path_parsed(self, filename):
        return os.path.join('files', f'{self.corpus.uuid}',
                            'parsed', filename)

    name = models.CharField(max_length=255)
    status = models.PositiveIntegerField(
        choices=STATUS_CHOICES, default=UNKNOWN)
    # status = models.CharField(max_length=50)
    corpus = models.ForeignKey(
        Corpus, related_name='transcripts', on_delete=models.CASCADE)
    content = models.FileField(
        upload_to=upload_path, blank=True, null=True, max_length=500)
    parsed_content = models.FileField(
        upload_to=upload_path_parsed, blank=True, null=True, max_length=500)
    corrected_content = models.FileField(
        upload_to=upload_path_parsed, blank=True, null=True, max_length=500)
    extracted_filename = models.CharField(
        max_length=500, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    corrections = models.JSONField(blank=True, null=True)

    # objects = TranscriptManager()
    target_speakers = models.CharField(max_length=500, blank=True)
    target_ids = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def target_speakers_list(self):
        return self.target_speakers.split(',')

    def get_utterance_by_id(self, utt_id: int):
        try:
            return self.utterances.get(utt_id=utt_id)
        except Exception:
            raise

    def get_filepaths(self) -> Tuple:
        if self.corrected_content:
            return (self.content.path,
                    self.parsed_content.path,
                    self.corrected_content.path)
        return (self.content.path, self.parsed_content.path)

    @property
    def best_available_treebank(self):
        if not self.corrected_content:
            return self.parsed_content
        return self.corrected_content

    def convertable(self):
        return self.status in (self.CREATED, self.CONVERSION_FAILED)

    def parseable(self):
        return self.status in (self.CONVERTED, self.PARSING_FAILED)

    @property
    def latest_run(self):
        try:
            return self.analysisruns.latest()
        except AnalysisRun.DoesNotExist:
            return None


class Utterance(models.Model):
    sentence = models.CharField(max_length=500)
    speaker = models.CharField(max_length=50)
    uttno = models.IntegerField()
    utt_id = models.IntegerField(blank=True, null=True)
    xsid = models.IntegerField(blank=True, null=True)
    parse_tree = models.TextField(blank=True)
    transcript = models.ForeignKey(
        Transcript, related_name='utterances', on_delete=models.CASCADE)

    @property
    def syntree(self):
        if self.parse_tree:
            return ET.fromstring(self.parse_tree)
        return None

    @property
    def for_analysis(self):
        """ Utterance should be analysed if:
        - Speaker is in target list
            - If target xsids, utt should also have xsid
        OR
        - Utterance has xsid
        """
        if self.speaker in self.transcript.target_speakers_list:
            if self.transcript.target_ids:
                return self.xsid is not None
            return True
        return self.xsid is not None

    @property
    @functools.lru_cache(maxsize=128)
    def word_elements(self) -> List[ET._Element]:
        '''List of word elements, sorted by word (begin, end)'''
        word_elements = self.syntree.findall('.//node[@word]')
        return sorted(word_elements, key=lambda x: (int(x.attrib.get('begin')),
                                                    int(x.attrib.get('end'))))

    @property
    @functools.lru_cache(maxsize=128)
    def word_position_mapping(self) -> List[Dict]:
        ''' List of dictionaries (begin, end) for each word in the utterance
            starts with { begin:None, end:None } to represent unaligned
        '''
        mapping = [{'begin': int(el.attrib.get('begin')),
                    'end': int(el.attrib.get('end'))}
                   for el in self.word_elements]
        return [{'begin': None, 'end': None}] + mapping

    @property
    @functools.lru_cache(maxsize=128)
    def word_list(self) -> List[str]:
        '''List of words in the utterance'''
        return [el.attrib.get('word') for el in self.word_elements]

    def __str__(self):
        return f'{self.uttno}\t|\t{self.speaker}:\t{self.sentence}'


class UploadFile(models.Model):
    def upload_path(self, filename):
        return os.path.join('files', f'{self.corpus.uuid}',
                            'uploads', filename)

    name = models.CharField(max_length=255)
    content = models.FileField(upload_to=upload_path, max_length=500)
    corpus = models.ForeignKey(
        Corpus, related_name='files', on_delete=models.CASCADE,
        null=True, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AssessmentQuery(models.Model):
    method = models.ForeignKey(AssessmentMethod, related_name='queries',
                               on_delete=models.CASCADE)

    query_id = models.CharField(max_length=4)
    cat = models.CharField(max_length=50, blank=True, default='')
    subcat = models.CharField(max_length=50, blank=True, default='')
    level = models.CharField(max_length=50, blank=True, default='')
    item = models.CharField(max_length=50, blank=True, default='')
    altitems = ArrayField(
        base_field=models.CharField(max_length=50, blank=True),
        default=list)
    implies = ArrayField(
        base_field=models.CharField(max_length=50, blank=True),
        default=list, null=True, blank=True)
    original = models.BooleanField()
    pages = models.CharField(max_length=50, blank=True, default='')
    fase = models.IntegerField(blank=True, null=True)
    query = models.CharField(max_length=5000, blank=True, default='')
    inform = models.CharField(max_length=20, blank=True, default='')
    screening = models.CharField(max_length=20, blank=True, default=True)
    process = models.IntegerField(blank=True, null=True)
    literal = models.CharField(max_length=200, blank=True, default='')
    stars = models.CharField(max_length=50, blank=True, default='')
    filter = models.CharField(max_length=200, blank=True, default='')
    variants = ArrayField(
        base_field=models.CharField(max_length=200, blank=True), default=list, null=True, blank=True)
    unused1 = models.CharField(max_length=50, blank=True, default='')
    unused2 = models.CharField(max_length=50, blank=True, default='')
    comments = models.TextField(blank=True, default='')

    # Manager
    objects = SastaQueryManager()

    def __str__(self):
        return self.query_id

    def get_items_list(self, str, sep, lower=True):
        rawresult = str.split(sep)
        if lower:
            cleanresult = [w.strip().lower() for w in rawresult]
        else:
            cleanresult = [w.strip() for w in rawresult]
        if cleanresult == ['']:
            return []
        return cleanresult

    def to_sastadev(self) -> Query:
        sastadev_mapping = {'query_id': 'id'}
        processes = ['pre', 'core', 'post', 'form']
        relevant_fields = [f for f in self._meta.fields
                           if f.get_internal_type()
                           not in ('AutoField', 'ForeignKey', 'id')]
        values = {f.name: getattr(self, f.name) for f in relevant_fields}
        # Convert process back to string
        values['process'] = processes[values.pop('process')]

        for k, v in list(values.items()):
            if k in sastadev_mapping:
                values[sastadev_mapping.get(k)] = values.pop(k)

        return Query(**values)

    class Meta:
        unique_together = ('method', 'query_id')


class AnalysisRun(models.Model):
    def upload_path(self, filename):
        return os.path.join('files', f'{self.transcript.corpus.uuid}',
                            'analysis_files', filename)

    transcript = models.ForeignKey(
        Transcript, related_name='analysisruns', on_delete=models.CASCADE)
    method = models.ForeignKey(
        AssessmentMethod, related_name='analysisruns',
        on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    query_file = models.FileField(upload_to=upload_path, max_length=500)
    annotation_file = models.FileField(upload_to=upload_path, max_length=500)
    is_manual_correction = models.BooleanField(
        default=False,
        help_text='this run was generated by parsing a user-uploaded SAF-file')

    class Meta:
        get_latest_by = "created"

    def __str__(self):
        return f'{self.transcript.name}'
