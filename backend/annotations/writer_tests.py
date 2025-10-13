from annotations.constants import (SAF_COMMENT_COLUMN, SAF_FASES_COLUMN,
                                   SAF_LEVEL_HEADER, SAF_UNALIGNED_LEVEL,
                                   SAF_UTT_HEADER)
from annotations.writers.saf_xlsx import SAFWriter

from .utils import ljust


def test_safwriter(safwriter: SAFWriter):
    with open('/Users/a3248526/Documents/saf_writer_test.xlsx', 'wb') as f:
        safwriter.write(f)
    assert safwriter


def test_headers(safwriter: SAFWriter):
    found = safwriter._annotations_header_row()
    expected = [SAF_UTT_HEADER, SAF_LEVEL_HEADER, SAF_UNALIGNED_LEVEL,
                *[f'Word{n}' for n in range(1, 19)],
                SAF_FASES_COLUMN, SAF_COMMENT_COLUMN]
    assert found == expected


def test_uttlevel_row(safwriter: SAFWriter):
    id = '1'
    words = safwriter.results.allutts[id]
    found = safwriter._uttlevel_row(id, words)
    expected = ['1', SAF_UTT_HEADER, None, 'ja', 'uh', 'ik', 'vind', 'het',
                'beetje', 'moeilijk', 'om', 'het', 'goed', 'te', 'vertellen',
                'want', 'ik', 'heb', 'een', 'ongeluk', 'gehad', None, None]
    assert found == expected


def test_ljust_list():
    input = ['a', 'b', 'c']
    ljustified = ljust(input, 5)
    assert ljustified == input + [None, None]
    ljustified = ljust(input, 3)
    assert ljustified == input
    ljustified = ljust(input, 2)
    assert ljustified == input


def test_uttlevel_offset(safwriter: SAFWriter):
    assert safwriter._uttlevel_row_number(0, 'Samplegrootte') == 3
    assert safwriter._uttlevel_row_number(0, 'Taalmaat') == 5
    assert safwriter._uttlevel_row_number(0, 'Opmerkingen') == 8
    assert safwriter._uttlevel_row_number(2, 'Samplegrootte') == 17
    assert safwriter._uttlevel_row_number(2, 'Taalmaat') == 19
    assert safwriter._uttlevel_row_number(2, 'Opmerkingen') == 22
