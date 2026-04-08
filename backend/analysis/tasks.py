from io import StringIO
from typing import Optional

from celery import shared_task
from django.core.files import File

from analysis.models import AnalysisRun, AssessmentMethod, Transcript
from analysis.query.run import annotate_transcript
from analysis.utils import update_analysis_run
from annotations.writers.saf_xlsx import SAFWriter
from convert.chat_writer import ChatWriter


@shared_task(bind=True)
def analyse_transcript_task(
    self,
    transcript_id: int,
    method_id: int,
    run_id: int,
    existing_annotations: Optional[str] = None,
) -> str:
    """For a transcript and method, perform analysis and save results to an AnalysisRun"""
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

    # Store SAF file
    writer = SAFWriter(method.to_sastadev(), allresults)
    spreadsheet = writer.workbook
    _ = update_analysis_run(run=run, transcript=transcript, saf=spreadsheet)

    # Store form
    from analysis.views import _apply_stap_workaround

    form_func = method.category.get_form_function()
    form = form_func(allresults, None, in_memory=True)
    form.seek(0)
    content = _apply_stap_workaround(form, method)
    form_file = File(
        content, name=f'{transcript.name}_{method.category.name}_form.xlsx'
    )
    run.form_file.save(form_file.name, form_file, save=True)

    # Save annotated chat file
    from annotations.writers.saf_chat import enrich_chat

    enriched = enrich_chat(transcript, allresults, method)
    output = StringIO()
    writer = ChatWriter(enriched, target=output)
    writer.write()
    output.seek(0)
    run.annotated_chat_file.save(
        f'{transcript.name}_{method.category.name}_annotated.cha',
        File(output),
        save=True,
    )

    run.save()

    return 'Transcript analysed successfully'
