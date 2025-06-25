from typing import Tuple
from analysis.models import AssessmentMethod, Transcript
from sastadev.sastacore import SastaCoreParameters, sastacore
from sastadev.targets import get_targets
from lxml import etree
from sastadev.methods import Method
from sastadev.sastatypes import SampleSizeTuple

from analysis.results.results import AllResults
from annotations.reader import read_saf
from parse.parse_utils import correct_transcript


def prepare_parameters(infilename: str, method: Method, targets: int, annotationinput: bool) -> SastaCoreParameters:
    return SastaCoreParameters(
        annotationinput=annotationinput,
        themethod=method,
        infilename=infilename,
        targets=targets
    )


def prepare_treebanks(transcript: Transcript) -> Tuple[Tuple[str, etree.ElementTree]]:
    orig_fp = transcript.parsed_content.path

    # TODO: FIX THIS PROPERLY
    if not transcript.corrected_content:
        correct_transcript(transcript)
    corr_fp = transcript.corrected_content.path

    orig_treebank = etree.parse(orig_fp).getroot()
    corr_treebank = etree.parse(corr_fp).getroot()
    return (
        (orig_fp, orig_treebank),
        (corr_fp, corr_treebank)
    )


def run_sastacore(transcript: Transcript, method: AssessmentMethod, annotation_input: bool = False) -> Tuple[AllResults, SampleSizeTuple]:
    # get treebanks
    orig_tb, corr_tb = prepare_treebanks(transcript)
    # Convert method to sastadev version
    sdmethod = method.to_sastadev()
    # Retrieve targets from corrected treebank
    targets = get_targets(corr_tb[1], sdmethod.name)

    if annotation_input:
        existing_results = read_saf(
            transcript.latest_run.annotation_file.path, sdmethod)
        params = prepare_parameters(
            transcript.latest_run.annotation_file.path,
            sdmethod, targets, annotation_input)
        res = sastacore(
            origtreebank=None,
            correctedtreebank=corr_tb[1],
            annotatedfileresults=existing_results,
            scp=params
        )
    else:
        params = prepare_parameters(
            corr_tb[0], sdmethod, targets, annotation_input)
        res = sastacore(
            origtreebank=orig_tb[1],
            correctedtreebank=corr_tb[1],
            annotatedfileresults=None,
            scp=params
        )

    return res
