import io
import logging
import os
from types import SimpleNamespace
from typing import Optional

from analysis.models import Transcript, Utterance
from bs4 import BeautifulSoup
from corpus2alpino.annotators.alpino import AlpinoAnnotator
from corpus2alpino.collectors.filesystem import FilesystemCollector
from corpus2alpino.converter import Converter
from corpus2alpino.targets.filesystem import FilesystemTarget
from corpus2alpino.targets.memory import MemoryTarget
from corpus2alpino.writers.lassy import LassyWriter
from django.conf import settings
from django.core.files import File
from lxml import etree
from sastadev.correctionparameters import CorrectionParameters
from sastadev.correcttreebank import correcttreebank, corrn
from sastadev.sastatypes import ErrorDict, Treebank
from sastadev.targets import get_targets

logger = logging.getLogger('sasta')

# Parser setup
ALPINO = AlpinoAnnotator(
    settings.ALPINO_HOST,
    settings.ALPINO_PORT
)


def parse_and_create(transcript):
    try:
        output_path = transcript.content.path.replace(
            '/transcripts', '/parsed')
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        result = parse_transcript(transcript, output_path)
        create_utterance_objects(transcript)
        return result
    except Exception:
        logger.exception(f'ERROR parsing {transcript.name}')


def parse_transcript(transcript, output_path):
    transcript.status = Transcript.PARSING
    transcript.save()

    output_path = output_path.replace('.cha', '.xml')

    try:
        logger.info(f'Parsing:\t{transcript.name}...')
        parsed_filename = initial_parse(transcript.content.path, output_path)
        logger.info(f'Succesfully parsed:\t{transcript.name}')
        transcript.save()

        # Saving parsed file
        transcript.parsed_content.name = transcript.upload_path_parsed(
            parsed_filename)
        transcript.save()

        # Correcting and reparsing
        correct_transcript(transcript)
        transcript.status = Transcript.PARSED
        transcript.save()
        return transcript

    except Exception:
        logger.exception(
            f'ERROR parsing {transcript.name}')
        transcript.status = Transcript.PARSING_FAILED
        transcript.save()


def initial_parse(in_path: str, out_path: str,
                  annotator: AlpinoAnnotator = ALPINO,
                  in_memory: bool = False) -> Optional[str]:

    target = MemoryTarget() if in_memory else FilesystemTarget(out_path, merge_files=True)
    converter = Converter(
        collector=FilesystemCollector([in_path]),
        annotators=[annotator],
        target=target,
        writer=LassyWriter(merge_treebanks=True),
    )
    # actual parsing
    next(converter.convert())
    return None if in_memory else out_path


def correct_transcript(transcript: Transcript) -> str:
    logger.info(f'Correcting:\t{transcript.name}...')
    try:
        corrected, error_dict, _origandalts = correct_treebank(transcript)
        save_corrected_treebank(transcript, corrected, error_dict)
        logger.info(
            f'Successfully corrected:\t{transcript.name}, {len(error_dict)} corrections.')
        return transcript.corrected_content.path

    except Exception as err:
        transcript.corrections = {'error': str(err)}
        logger.exception(
            f'Correction failed for transcript:\t {transcript.name}')
        raise


def save_corrected_treebank(transcript: Transcript, treebank: Treebank, error_dict: ErrorDict) -> str:
    corrected_file = treebank_to_file(treebank)
    transcript.corrected_content.save(
        get_corrected_filename(transcript), corrected_file)
    transcript.corrections = error_dict
    transcript.save()
    return transcript.corrected_content.path


def get_corrected_filename(transcript: Transcript, suffix: str = '_corrected') -> str:
    return os.path.basename(transcript.parsed_content.name).replace('.xml', f'{suffix}.xml')


def treebank_to_file(treebank: Treebank) -> File:
    content = etree.tostring(treebank, encoding='utf-8')
    file = File(io.BytesIO(content))
    return file


def create_utterance_objects(transcript):
    parse_file = transcript.best_available_treebank

    with open(parse_file.path, 'rb') as f:
        try:
            marked_utt_counter = 1
            doc = BeautifulSoup(f.read(), 'xml')
            utts = doc.find_all('alpino_ds')
            num_created = 0
            for utt in utts:
                uttno_el = utt.metadata.find(
                    'meta', {'name': 'uttno'}
                )
                uttno = int(uttno_el['value'])

                # replace existing utterances
                existing = Utterance.objects.filter(
                    transcript=transcript, uttno=uttno)
                if existing:
                    existing.delete()
                    logger.info(f'Deleting existing utterance {uttno}')

                sent = utt.sentence.text
                speaker = utt.metadata.find(
                    'meta', {'name': 'speaker'})['value']

                xsid_el = utt.metadata.find(
                    'meta', {'name': 'xsid'})

                # fields that should always be present
                instance = Utterance(
                    transcript=transcript,
                    uttno=uttno,
                    xsid=int(xsid_el['value']
                             ) if xsid_el is not None else None,
                    speaker=speaker,
                    sentence=sent,
                    parse_tree=str(utt)
                )

                if instance.for_analysis:
                    # setting utt_id according to targets
                    if transcript.target_ids:
                        # check if xsids are unique and consecutive
                        assert instance.xsid == marked_utt_counter
                    instance.utt_id = marked_utt_counter
                    marked_utt_counter += 1

                instance.save()
                num_created += 1
            logger.info(
                f'Created {num_created} (out of {len(utts)})'
                f'utterances for:\t{transcript.name}')

        except Exception as e:
            logger.exception(
                f'ERROR creating utterances for:\t{transcript.name}'
                f'with message:\t"{e}"')
            transcript.status = transcript.PARSING_FAILED
            transcript.save()


def correct_treebank(transcript: Transcript):
    try:
        treebank = etree.parse(transcript.parsed_content).getroot()
        method_name = transcript.corpus.method_category.name.lower()
        targets = get_targets(treebank, method_name)

        correction_options = SimpleNamespace(
            infilename=transcript.parsed_content.path,
            methodname=method_name,
            variant=None,
            annotationfilename=None,
            goldfilename=None,
            goldcountsfilename=None,
            platinuminfilename=None,
            includeimplies=True,
            logfilename=None,
            corr=corrn,
            methodfilename=None,
            doauchann=True,
            dospellingcorrection=False,
            dohistory=False,
            extendhistory=False
        )

        correction_parameters = CorrectionParameters(
            method=method_name,
            options=correction_options,
            allsamplecorrections={},
            thissamplecorrections={},
            treebank=treebank,
            contextdict={}
        )

        corr, error_dict, origandalts = correcttreebank(
            treebank=treebank, targets=targets, correctionparameters=correction_parameters, corr=corrn)

        return corr, error_dict, origandalts

    except Exception as e:
        logger.exception(e)
        raise


def correct_uncorrected_transcripts():
    uncorrected = list(Transcript.objects.filter(corrected_content=''))
    print(f'{len(uncorrected)} uncorrected transcripts')

    while len(uncorrected):
        t = uncorrected.pop()
        print(f'{len(uncorrected)} left')
        correct_transcript(t)
