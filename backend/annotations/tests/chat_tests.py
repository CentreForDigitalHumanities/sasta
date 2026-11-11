from annotations.writers.saf_chat import enrich_chat


def test_chat_enrich(single_utt_allresults, asta_transcripts):
    '''Tests the CHAT enrichment functionality'''
    transcript = asta_transcripts.get(name='single_utt')
    doc = enrich_chat(transcript=transcript, allresults=single_utt_allresults,
                      method=transcript.corpus.default_method)

    # Test the correct position of %xsyn annotations
    assert doc.lines[0].tiers.get('xsyn') is None
    assert doc.lines[1].tiers.get('xsyn') is not None


def test_chat_enrich_newids(single_utt_allresults, asta_transcripts, tmp_path):
    '''Tests the CHAT enrichment using new Corpus2Alpino style
    In this style, uttids are not overwritten by xsid.
    '''
    transcript = asta_transcripts.get(name='single_utt_newstyle')
    doc = enrich_chat(transcript=transcript, allresults=single_utt_allresults,
                      method=transcript.corpus.default_method)

    # Test the correct position of %xsyn annotations
    assert doc.lines[0].tiers.get('xsyn') is None
    assert doc.lines[1].tiers.get('xsyn') is not None
