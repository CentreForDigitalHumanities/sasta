from celery import shared_task

from analysis.models import AnalysisRun, AssessmentMethod, Transcript
from analysis.query.run import annotate_transcript
from analysis.utils import update_analysis_run
from annotations.writers.saf_xlsx import SAFWriter


@shared_task
def annotate_transcript_task(transcript_id: int, method_id: int, run_id: int) -> str:
    '''For a transcript and method, perform analysis and save results to an AnalysisRun'''
    # Retrieve objects
    transcript = Transcript.objects.get(pk=transcript_id)
    method = AssessmentMethod.objects.get(pk=method_id)
    run = AnalysisRun.objects.get(pk=run_id)

    # for testing purposes, wait for 5 minutes to simulate a long-running task
    import time
    time.sleep(30)

    # Perform querying
    allresults = annotate_transcript(transcript, method)

    # Create XLSX annotations file
    writer = SAFWriter(method.to_sastadev(), allresults)
    spreadsheet = writer.workbook

    # Update the AnalysisRun with the new annotations file
    run = update_analysis_run(run, transcript, spreadsheet)

    return f'Transcript {transcript.name} annotated'
