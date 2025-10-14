import os

from analysis.query.query_transcript import run_sastacore
from django.conf import settings
from parse.parse_utils import (correct_treebank, initial_parse,
                               save_corrected_treebank)


def test_analysis(db, all_transcripts):
    '''Make sure all of the test files can be analysed'''

    for t in all_transcripts:
        results = run_sastacore(t, t.corpus.default_method)
        assert results


def test_single_transcript_fullrun(db, single_utt, single_utt_transcript):
    '''Make sure a single transcript can be run through the full pipeline'''
    # start with a fresh transcript
    transcript = single_utt_transcript

    # upload the content
    with open(single_utt['chat'], 'rb') as f:
        transcript.content.save(os.path.basename(single_utt['chat']), f)
    transcript.save()
    assert os.path.exists(transcript.content.path)

    # parse the transcript
    parsed_output_path = os.path.join(
        settings.MEDIA_ROOT, transcript.upload_path_parsed(single_utt['name'] + '.xml'))
    parsed_path = initial_parse(transcript.content.path,
                                parsed_output_path)
    assert parsed_path
    assert os.path.exists(parsed_path)

    # save the parsed content
    with open(parsed_path, 'rb') as f:
        transcript.parsed_content.save(os.path.basename(parsed_path), f)
    transcript.save()

    # check the parsed content, disabled for now because there are subtle differences
    # between the expected and actual parsed content due to different parsing versions
    # _compare_lines(transcript.parsed_content.path, single_utt['parsed'])

    # correct the treebank
    treebank, error_dict, _orig_alts = correct_treebank(transcript)
    assert treebank

    # save the corrected treebank
    corrected_fn = save_corrected_treebank(transcript, treebank, error_dict)
    assert os.path.isfile(corrected_fn)

    # analyse the transcript
    results, _samplesize = run_sastacore(
        transcript, transcript.corpus.default_method)
    benchmark_results = single_utt.get('allresults')
    assert benchmark_results

    # assert that results are correct
    non_empty_exactresults = {k: v for k,
                              v in results.exactresults.items() if v}
    assert non_empty_exactresults == benchmark_results.exactresults




    # TODO: upload corrected annotations

    # TODO: re-analyse the transcript


def _compare_lines(file1, file2):
    """Compare two files line by line."""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
    for (l1, l2) in zip(lines1, lines2):
        assert l1.strip() == l2.strip(
        ), f"Lines differ: '{l1.strip()}' != '{l2.strip()}'"
