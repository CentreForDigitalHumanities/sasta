import os.path as op

import pytest

from .chat_reader import ChatDocument
from .conftest import TEST_DIR


@pytest.mark.django_db
def test_chat_reader(chafiles, tarsp_category):
    for (input, _) in chafiles:
        doc = ChatDocument.from_chatfile(input, tarsp_category)
        assert len(doc.lines)


@pytest.mark.django_db
def test_marking_postcodes(chafiles, tarsp_category, stap_category):
    inf = op.join(TEST_DIR, 'TD16.cha')

    tarsp_doc = ChatDocument.from_chatfile(inf, tarsp_category)
    tarsp_num_xsid = len([x for x in tarsp_doc.lines if x.tiers.get('xsid')])
    assert tarsp_num_xsid == 42

    stap_doc = ChatDocument.from_chatfile(inf, stap_category)
    stap_num_xsid = len([x for x in stap_doc.lines if x.tiers.get('xsid')])
    assert stap_num_xsid == 42 + 16
