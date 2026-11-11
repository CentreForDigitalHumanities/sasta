from collections import Counter
from xml.etree import ElementTree as etree

from sastadev.allresults import AllResults
import pytest
from os import path as op

HERE = op.dirname(op.abspath(__file__))
EXAMPLE_TESTDATA_DIR = op.join(HERE, 'tests', 'data', 'tarsp_example')


@pytest.fixture
def example_allresults(
    example_coreresults,
    example_exactresults,
    example_postresults,
    example_allmatches,
    example_allutts,
    example_analysedtrees,
    example_annotationinput,
    example_filename,
):
    return AllResults(
        uttcount=7,
        coreresults=example_coreresults,
        exactresults=example_exactresults,
        postresults=example_postresults,
        allmatches=example_allmatches,
        allutts=example_allutts,
        analysedtrees=example_analysedtrees,
        annotationinput=example_annotationinput,
        filename=example_filename,
    )


@pytest.fixture
def example_allmatches():
    # lxml nodes
    return {}


@pytest.fixture
def example_allutts():
    return {
        '1': ['allemaal', 'varkens', 'zit', 'erin', '.'],
        '2': ['die', 'kan', 'je', 'de', 'varken', 'doen', '.'],
        '3': ['dit', 'is', 'een', 'touw', '.'],
        '4': ['naar', 'boven', 'gaat', '.'],
        '5': ['al', 'bijna', '.'],
        '6': ['hij', 'wil', 'naar', 'boven', '.'],
        '7': ['is', 'helemaal', 'veilig', 'in', 'die', 'varken', '.'],
    }


@pytest.fixture
def example_analysedtrees():
    # lxml nodes
    with open(op.join(EXAMPLE_TESTDATA_DIR, 'corrected_parse.xml')) as f:
        whole_tree = etree.parse(f)
    return {str(i + 1): t for i, t in enumerate(whole_tree.iter('alpino_ds'))}


@pytest.fixture
def example_annotationinput():
    return False


@pytest.fixture
def example_coreresults():
    return {
        ('T007', 'T007'): Counter({'1': 2, '5': 2, '4': 1, '6': 1, '7': 1}),
        ('T013', 'T013'): Counter(),
        ('T019', 'T019'): Counter(),
        ('T020', 'T020'): Counter(),
        ('T024', 'T024'): Counter(),
        ('T031', 'T031'): Counter(),
        ('T046', 'T046'): Counter({'1': 1, '6': 1}),
        ('T048', 'T048'): Counter(),
        ('T055', 'T055'): Counter(),
        ('T058', 'T058'): Counter({'1': 1}),
        ('T061', 'T061'): Counter(),
        ('T067', 'T067'): Counter(),
        ('T068', 'T068'): Counter(),
        ('T069', 'T069'): Counter(),
        ('T078', 'T078'): Counter(),
        ('T082', 'T082'): Counter(),
        ('T091', 'T091'): Counter(),
        ('T092', 'T092'): Counter(),
        ('T093', 'T093'): Counter(),
        ('T096', 'T096'): Counter(),
        ('T107', 'T107'): Counter({'1': 1}),
        ('T118', 'T118'): Counter(),
        ('T119', 'T119'): Counter({'1': 1, '2': 1, '3': 1, '4': 1, '6': 1, '7': 1}),
        ('T123', 'T123'): Counter(),
        ('T134', 'T134'): Counter(),
        ('T139', 'T139'): Counter(),
        ('T141', 'T141'): Counter(),
        ('T143', 'T143'): Counter(),
        ('T148', 'T148'): Counter(),
        ('T156', 'T156'): Counter(),
        ('T006', 'T006'): Counter({'2': 1, '3': 1}),
        ('T032', 'T032'): Counter({'2': 1}),
        ('T044', 'T044'): Counter({'2': 1}),
        ('T049', 'T049'): Counter({'2': 1}),
        ('T050', 'T050'): Counter({'2': 1}),
        ('T063', 'T063'): Counter({'2': 1, '3': 1, '6': 1}),
        ('T077', 'T077'): Counter({'2': 1}),
        ('T097', 'T097'): Counter({'2': 2, '3': 1, '7': 1}),
        ('T101', 'T101'): Counter({'2': 1, '3': 1, '6': 1, '7': 1}),
        ('T127', 'T127'): Counter({'2': 1}),
        ('T132', 'T132'): Counter({'7': 3, '2': 1, '3': 1, '4': 1, '6': 1}),
        ('T035', 'T035'): Counter({'3': 1}),
        ('T052', 'T052'): Counter({'3': 1, '7': 1}),
        ('T076', 'T076'): Counter({'3': 1}),
        ('T030', 'T030'): Counter({'4': 1, '5': 1}),
        ('T114', 'T114'): Counter({'4': 1, '6': 1}),
        ('T122', 'T122'): Counter({'5': 1}),
        ('T043', 'T043'): Counter({'6': 1}),
        ('T073', 'T073'): Counter({'6': 1}),
        ('T012', 'T012'): Counter({'7': 1}),
        ('T033', 'T033'): Counter({'7': 1}),
        ('T054', 'T054'): Counter({'7': 1}),
        ('T116', 'T116'): Counter({'7': 1}),
        ('T125', 'T125'): Counter({'7': 1}),
    }


@pytest.fixture
def example_exactresults():
    return {
        ('T007', 'T007'): [
            ('1', 1),
            ('1', 4),
            ('4', 1),
            ('5', 1),
            ('5', 2),
            ('6', 3),
            ('7', 4),
        ],
        ('T013', 'T013'): [],
        ('T019', 'T019'): [],
        ('T020', 'T020'): [],
        ('T024', 'T024'): [],
        ('T031', 'T031'): [],
        ('T046', 'T046'): [('1', 3), ('6', 2)],
        ('T048', 'T048'): [],
        ('T055', 'T055'): [],
        ('T058', 'T058'): [('1', 2)],
        ('T061', 'T061'): [],
        ('T067', 'T067'): [],
        ('T068', 'T068'): [],
        ('T069', 'T069'): [],
        ('T078', 'T078'): [],
        ('T082', 'T082'): [],
        ('T091', 'T091'): [],
        ('T092', 'T092'): [],
        ('T093', 'T093'): [],
        ('T096', 'T096'): [],
        ('T107', 'T107'): [('1', 4)],
        ('T118', 'T118'): [],
        ('T119', 'T119'): [('1', 3), ('2', 2), ('3', 2), ('4', 3), ('6', 2), ('7', 1)],
        ('T123', 'T123'): [],
        ('T134', 'T134'): [],
        ('T139', 'T139'): [],
        ('T141', 'T141'): [],
        ('T143', 'T143'): [],
        ('T148', 'T148'): [],
        ('T156', 'T156'): [],
        ('T006', 'T006'): [('2', 1), ('3', 1)],
        ('T032', 'T032'): [('2', 4)],
        ('T044', 'T044'): [('2', 2)],
        ('T049', 'T049'): [('2', 1)],
        ('T050', 'T050'): [('2', 3)],
        ('T063', 'T063'): [('2', 3), ('3', 1), ('6', 1)],
        ('T077', 'T077'): [('2', 1)],
        ('T097', 'T097'): [('2', 1), ('2', 4), ('3', 3), ('7', 2)],
        ('T101', 'T101'): [('2', 4), ('3', 3), ('6', 3), ('7', 2)],
        ('T127', 'T127'): [('2', 2)],
        ('T132', 'T132'): [
            ('2', 4),
            ('3', 3),
            ('4', 1),
            ('6', 3),
            ('7', 2),
            ('7', 4),
            ('7', 5),
        ],
        ('T035', 'T035'): [('3', 3)],
        ('T052', 'T052'): [('3', 2), ('7', 1)],
        ('T076', 'T076'): [('3', 1)],
        ('T030', 'T030'): [('4', 1), ('5', 1)],
        ('T114', 'T114'): [('4', 1), ('6', 3)],
        ('T122', 'T122'): [('5', 0)],
        ('T043', 'T043'): [('6', 1)],
        ('T073', 'T073'): [('6', 1)],
        ('T012', 'T012'): [('7', 2)],
        ('T033', 'T033'): [('7', 5)],
        ('T054', 'T054'): [('7', 1)],
        ('T116', 'T116'): [('7', 4)],
        ('T125', 'T125'): [('7', 1)],
    }


@pytest.fixture
def example_filename():
    return ''


@pytest.fixture
def example_postresults():
    return {
        'T151': 0,
        'T152': 7,
        'T153': 1,
        'T154': 0,
        'T155': 1,
        'T157': None,
        'T158': 0,
        'T159': 0,
        'T160': 0,
        'T162': 1,
        'T165': '',  # output file name
    }
