from django.core.management import call_command

from analysis.models import Corpus


def test_cleanup_dry_run_keeps_empty_corpora(tarsp_corpus):
    call_command('cleanup_old_transcripts', '1')
    assert Corpus.objects.filter(pk=tarsp_corpus.pk).exists()


def test_cleanup_remove_deletes_empty_corpora(tarsp_corpus):
    call_command('cleanup_old_transcripts', '1', '--remove')
    assert not Corpus.objects.filter(pk=tarsp_corpus.pk).exists()
