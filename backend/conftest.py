import glob
from collections import Counter
from os import path as op
import os
from typing import Optional

import pytest
from analysis.convert.convert import convert
from analysis.models import AssessmentMethod, Corpus, MethodCategory, Transcript
from django.conf import settings
from django.core.files import File
from sastadev.allresults import AllResults
from sastadev.conf import settings as sd_settings
from django.contrib.auth.models import User

from lxml import etree

from parse.parse_utils import create_utterance_objects


def _get_transcript_filenames(name: str, dir: Optional[str] = None):
    fns = {
        'chat': f'{name}.cha',
        'parsed': f'{name}.xml',
        'corrected': f'{name}_corrected.xml'
    }
    if dir:
        fns = {k: op.join(dir, v) for k, v in fns.items()}
    return fns


def _make_transcript(corpus: Corpus, name: str, dir: str):
    filenames = _get_transcript_filenames(name)

    obj = Transcript.objects.create(
        name=name,
        status=Transcript.PARSED,
        corpus=corpus
    )

    with open(op.join(dir, filenames['chat']), 'rb') as f:
        obj.content.save(filenames['chat'], File(f))

    convert(obj)

    with open(op.join(dir, filenames['parsed']), 'rb') as f:
        obj.parsed_content.save(filenames['parsed'], File(f))
    with open(op.join(dir, filenames['corrected']), 'rb') as f:
        obj.corrected_content.save(filenames['corrected'], File(f))

    create_utterance_objects(obj)

    obj.save()
    return obj


def _make_method_transcripts(corpus: Corpus, testfiles_dir):
    method_name = corpus.method_category.name
    method_dir = op.join(testfiles_dir, method_name)
    transcript_dirs = os.listdir(method_dir)

    for name in transcript_dirs:
        _make_transcript(corpus, name, op.join(method_dir, name))

    transcripts = corpus.transcripts.all()
    assert transcripts.count() == len(transcript_dirs)
    return transcripts


@pytest.fixture
def testfiles_dir():
    return op.join(settings.BASE_DIR, 'test_files')


@pytest.fixture
def normal_user():
    new_user = User.objects.create(
        username='new_user',
        password='secret'
    )
    return new_user

@pytest.fixture
def tarsp_category(db):
    return MethodCategory.objects.create(
        name='TARSP', zc_embeddings=True,
        levels=['Sz', 'Zc', 'Wg', 'VVW'],
        marking_postcodes=['[+ G]'])


@pytest.fixture
def tarsp_corpus(db, admin_user, tarsp_method, tarsp_category):
    obj = Corpus.objects.create(
        user=admin_user,
        name='tarsp_test_corpus',
        default_method=tarsp_method,
        method_category=tarsp_category
    )
    return obj


@pytest.fixture
def stap_category(db):
    obj = MethodCategory.objects.create(
        name='STAP', zc_embeddings=False,
        levels=['Complexiteit', 'Grammaticale fout'],
        marking_postcodes=['[+ G]', '[+ VU]'])
    return obj


@pytest.fixture
def asta_category(db):
    return MethodCategory.objects.create(
        name='ASTA', zc_embeddings=False, levels=[
            "Samplegrootte",
            "MLU",
            "Taalmaat",
            "Foutenanalyse",
            "Lemma"
        ], marking_postcodes=["[+ G]"])


@pytest.fixture
def asta_corpus(db, admin_user, asta_method, asta_category):
    obj = Corpus.objects.create(
        user=admin_user,
        name='asta_test_corpus',
        default_method=asta_method,
        method_category=asta_category
    )
    yield obj
    obj.delete()


@pytest.fixture
def method_dir():
    return op.join(sd_settings.SD_DIR, 'data', 'methods')


@pytest.fixture
def tarsp_method(db, tarsp_category, method_dir):
    file = glob.glob(f'{method_dir}/TARSP_Index_Current.xlsx')[0]
    with open(file, 'rb') as f:
        wrapped_file = File(f)
        instance = AssessmentMethod(
            name='tarsp_test_method', category=tarsp_category)
        instance.content.save(op.basename(file), wrapped_file)
    yield instance
    instance.delete()


@pytest.fixture
def asta_method(db, asta_category, method_dir):
    file = glob.glob(f'{method_dir}/ASTA_Index_Current.xlsx')[0]
    with open(file, 'rb') as f:
        wrapped_file = File(f)
        instance = AssessmentMethod(
            name='asta_test_method', category=asta_category)
        instance.content.save(op.basename(file), wrapped_file)
    yield instance
    instance.delete()


@pytest.fixture()
def asta_transcripts(db, asta_corpus, testfiles_dir):
    return _make_method_transcripts(asta_corpus, testfiles_dir)


@pytest.fixture()
def tarsp_transcripts(db, tarsp_corpus, testfiles_dir):
    return _make_method_transcripts(tarsp_corpus, testfiles_dir)


@pytest.fixture
def single_utt_transcript(db, asta_corpus, single_utt):
    transcript = Transcript.objects.create(
        corpus=asta_corpus,
        name=single_utt['name'],
        status=Transcript.CREATED,
    )
    yield transcript
    transcript.delete()


@pytest.fixture()
def single_utt(testfiles_dir, single_utt_allresults):
    dir = op.join(testfiles_dir, 'ASTA', 'single_utt', 'single_utt')
    name = 'single_utt'
    fns = _get_transcript_filenames(dir, name)
    return {**fns,
            'name': name,
            'allresults': single_utt_allresults
            }


@pytest.fixture
def single_utt_allresults(testfiles_dir):
    parsed = etree.parse(
        op.join(testfiles_dir, 'ASTA', 'single_utt', 'single_utt_corrected.xml'))
    utts = parsed.xpath('alpino_ds')

    return AllResults(
        uttcount=2,
        coreresults={('A029', 'A029'): Counter({'1': 1}), ('A045', 'A045'): Counter({'1': 1}),
                     ('A001', 'A001'): Counter({'1': 1}), ('A003', 'A003'): Counter({'1': 2}),
                     ('A013', 'A013'): Counter({'1': 1}), ('A018', 'A018'): Counter({'1': 2}),
                     ('A021', 'A021'): Counter({'1': 2}), ('A024', 'A024'): Counter({'1': 2}),
                     ('A051', 'beet'): Counter({'1': 1}), ('A051', 'vertellen'): Counter({'1': 1}),
                     ('A051', 'ongeluk'): Counter({'1': 1}), ('A051', 'hebben'): Counter({'1': 1})},

        exactresults={('A029', 'A029'): [('1', 1)], ('A045', 'A045'): [('1', 2)],
                      ('A001', 'A001'): [('1', 7)], ('A003', 'A003'): [('1', 8), ('1', 13)],
                      ('A013', 'A013'): [('1', 4)], ('A018', 'A018'): [('1', 12), ('1', 18)],
                      ('A021', 'A021'): [('1', 6), ('1', 17)], ('A024', 'A024'): [('1', 4), ('1', 15)],
                      ('A051', 'beet'): [('1', 6)], ('A051', 'vertellen'): [('1', 12)],
                      ('A051', 'ongeluk'): [('1', 17)], ('A051', 'hebben'): [('1', 18)],
                      },
        postresults={'A046': Counter({('beet', '1'): 1, ('ongeluk', '1'): 1}),
                     'A049': Counter({('vertellen', '1'): 1, ('hebben', '1'): 1})},
        allmatches=None,  # Not provided in this fixture
        filename='single_utt',
        analysedtrees=[(n + 1, tree) for n, tree in enumerate(utts)],
        annotationinput=True,
        allutts={'1': ['ja', 'uh', 'ik', 'vind', 'het', 'beetje', 'moeilijk',
                     'om', 'het', 'goed', 'te', 'vertellen', 'want', 'ik',
                     'heb', 'een', 'ongeluk', 'gehad']}
    )


@pytest.fixture
def all_transcripts(asta_transcripts, tarsp_transcripts):
    return Transcript.objects.all()
