from typing import Optional

from celery import shared_task

from analysis.models import AnalysisRun, AssessmentMethod, Transcript
from analysis.query.run import annotate_transcript
from analysis.utils import update_analysis_run
from annotations.writers.saf_xlsx import SAFWriter
from results.serializers import allresults_to_json


@shared_task(bind=True)
def analyse_transcript_task(
    self,
    transcript_id: int,
    method_id: int,
    run_id: int,
    existing_annotations: Optional[str] = None,
) -> str:
    '''For a transcript and method, perform analysis and save results to an AnalysisRun'''
    # Retrieve objects
    transcript = Transcript.objects.get(pk=transcript_id)
    method = AssessmentMethod.objects.get(pk=method_id)
    run = AnalysisRun.objects.get(pk=run_id)

    run.task_id = self.request.id
    run.save(update_fields=['task_id'])

    # for testing purposes, wait to simulate a long-running task
    # import time
    # time.sleep(10)

    # Perform querying
    if existing_annotations:
        allresults = annotate_transcript(
            transcript, method, existing_annotations=existing_annotations
        )
    else:
        allresults = annotate_transcript(transcript, method)

    # Serialize results to JSON for storage in the AnalysisRun
    # Make analysedtrees and allmatches empty to save space
    allresults.analysedtrees = {}
    allresults.allmatches = {}

    # Store json allresults
    json_allresults = allresults_to_json(allresults)
    run.allresults = json_allresults

    # Store SAF file
    writer = SAFWriter(method.to_sastadev(), allresults)
    spreadsheet = writer.workbook
    _ = update_analysis_run(run=run, transcript=transcript, saf=spreadsheet)

    return 'Transcript analysed successfully'
