import pytest

from .chat_reader import ChatDocument
from .chat_writer import ChatWriter


@pytest.mark.django_db
def test_chat_writer(chafiles, tarsp_category):
    for inpath, outpath in chafiles:
        doc = ChatDocument.from_chatfile(inpath, tarsp_category)
        with open(outpath, 'w+', encoding='utf-8') as target:
            writer = ChatWriter(doc, target=target)
            writer.write()
        out_doc = ChatDocument.from_chatfile(outpath, tarsp_category)
        assert out_doc == doc
