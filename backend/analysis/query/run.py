import logging

from analysis.models import (AnalysisRun, AssessmentMethod, Transcript)
from analysis.query.query_transcript import run_sastacore
from sastadev.allresults import AllResults

logger = logging.getLogger('sasta')


def annotate_transcript(transcript: Transcript, method: AssessmentMethod, ignore_existing: bool = False, provided_run: AnalysisRun = None) -> AllResults:
    if transcript.latest_run and \
            transcript.latest_run.annotation_file \
            and not ignore_existing:
        # run sastacore with pre-exising SAF file
        allresults, _samplesize = run_sastacore(transcript, method, True)
    else:
        # run sastacore normally
        allresults, _samplesize = run_sastacore(transcript, method, False)
    return allresults
