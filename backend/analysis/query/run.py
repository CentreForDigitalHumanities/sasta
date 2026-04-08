from typing import Optional

from sastadev.allresults import AllResults

from analysis.models import AssessmentMethod, Transcript
from analysis.query.query_transcript import run_sastacore


def annotate_transcript(
    transcript: Transcript,
    method: AssessmentMethod,
    ignore_existing: bool = False,
    existing_annotations: Optional[str] = None,
) -> AllResults:
    if not ignore_existing and existing_annotations:
        existing_annotations_file = existing_annotations
    else:
        existing_annotations_file = None

    allresults, _samplesize = run_sastacore(
        transcript=transcript,
        method=method,
        manual_annotations_file=existing_annotations_file,
    )
    return allresults
