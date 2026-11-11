import pytest
import os.path as op


@pytest.fixture
def replace_names():
    # format: (string, expected_corrected_string, expected_comment)
    return [
        ('Ik heb honger.', 'Ik heb honger.', None),
        ('Ik heb een naam.', 'Ik heb een naam.', None),
        ('Ik heet NAAM.', 'Ik heet Maria.', '8|NAAM|Maria'),
        ('Ik heet NAAMKIND.', 'Ik heet Maria.', '8|NAAMKIND|Maria'),
        ('Ik heet NAAM1.', 'Ik heet Jan.', '8|NAAM1|Jan'),
        ('Ik heet VOORNAAM.', 'Ik heet Maria.', '8|VOORNAAM|Maria'),
        ('Ik heet NAAMOVERIG1.', 'Ik heet Jan.', '8|NAAMOVERIG1|Jan'),
        ('Ik heet VOORNAAM1.', 'Ik heet Jan.', '8|VOORNAAM1|Jan'),
        ('Ik heet ACHTERNAAM1.', 'Ik heet Hendriks.', '8|ACHTERNAAM1|Hendriks'),
        ('Ik heet TWEELINGZUS.', 'Ik heet Maria.', '8|TWEELINGZUS|Maria'),
        ('Ik heet NAAM1 en hij heet NAAM2.',
         'Ik heet Jan en hij heet NAAM2.',
         '8|NAAM1|Jan'),
        ('15 | PMA: in het uh hier in het PLAATSNAAM1 uh silahe ',
         '15 | PMA: in het uh hier in het Breda uh silahe ',
         '32|PLAATSNAAM1|Breda'),
        ('15 | PMA: in het uh hier in het PLAATSNAAM uh silahe ',
         '15 | PMA: in het uh hier in het Utrecht uh silahe ',
         '32|PLAATSNAAM|Utrecht'),
        ('Mijn achternaam is ACHTERNAAM2',
         'Mijn achternaam is Dekker',
         '19|ACHTERNAAM2|Dekker'
         )
    ]


@pytest.fixture
def replace_punc():
    # format: (string, expected_corrected_string, expected_comment)
    return [
        ('Dit is een voorbeeldzin.', 'Dit is een voorbeeldzin.', None),
        ('Dit (.) is (..) een (...) voorbeeldzin.',
         'Dit (.) is (..) een (...) voorbeeldzin.', None),
        ('Dit is een voorbeeldzin...', 'Dit is een voorbeeldzin+...', '23|...|+...'),
        ('Dit is een voorbeeldzin…', 'Dit is een voorbeeldzin+...', '23|…|+...'),
        ('Bla bla # bla', 'Bla bla (.) bla', '8|#|(.)'),
        ('ik noem som(s) Tony Too', 'ik noem som(s) Tony Too', None)
    ]


@pytest.fixture
def flag_punc():
    return [
        'Dit is een (mooie) voorbeeldzin.',
        'Dit is een (mooie voorbeeldzin.',
        'Dit is een mooie) voorbeeldzin.',
        '(... is geen goede pauze',
        '...) is geen goede pauze'
    ]


@pytest.fixture
def quotemarks():
    return [
        "’t kofschip",
        "‘t kofschip",
        "'t kofschip"
    ]


@pytest.fixture
def testfiles():
    here = op.dirname(op.abspath(__file__))
    fns = ['STAP_02', 'ASTA_01']
    return {fn: op.join(here, f'{fn}.docx') for fn in fns}


@pytest.fixture
def example_utterances():
    return [
        {
            'text': 'Dit is een voorbeeldzin.',
            'exp_text': 'Dit is een voorbeeldzin.',
            'exp_tiers': {},
        },
        {
            'text': 'Ik ben NAAM uit PLAATSNAAM2.',
            'exp_text': 'Ik ben Maria uit Leiden.',
            'exp_tiers': {'xano': '16|PLAATSNAAM2|Leiden, 7|NAAM|Maria'},
        },
        {
            'text': 'Ik ben BEROEP1 in het INSTELLING in LAND2.',
            'exp_text': 'Ik ben chirurg in het Diakonessenhuis in Japan.',
            'exp_tiers': {'xano': '7|BEROEP1|chirurg, 36|LAND2|Japan, 22|INSTELLING|Diakonessenhuis'},
        },
        {
            'text': 'Ik heb STUDIE en STUDIE1 gestudeerd.',
            'exp_text': 'Ik heb bedrijfskunde en informatica gestudeerd.',
            'exp_tiers': {'xano': '7|STUDIE|bedrijfskunde, 24|STUDIE1|informatica'},
        },
        {
            'text': 'Ik heet NAAM1 en hij heet NAAM2.',
            'exp_text': 'Ik heet Jan en hij heet Anna.',
            'exp_tiers': {'xano': '8|NAAM1|Jan, 24|NAAM2|Anna'},
        },
        {
            'text': 'Dit is een voorbeeldzin...',
            'exp_text': 'Dit is een voorbeeldzin+...',
            'exp_tiers': {'xpct': '23|...|+...'},
        },
        {
            'text': 'Dit... is een... voorbeeldzin.',
            'exp_text': 'Dit+... is een+... voorbeeldzin.',
            'exp_tiers': {'xpct': '3|...|+..., 14|...|+...'},
        },
        {
            'text': 'Ik heet # NAAM.',
            'exp_text': 'Ik heet (.) Maria.',
            'exp_tiers': {'xpct': '8|#|(.)', 'xano': '10|NAAM|Maria'},
        },
        {
            'text': 'XXX deed ik met VOORNAAM2 ACHTERNAAM2 deed ik samen VOORNAAM2 ACHTERNAAM2.',
            'exp_text': 'XXX deed ik met Anna Dekker deed ik samen Anna Dekker.',
            'exp_tiers': {'xano': '26|ACHTERNAAM2|Dekker, 57|ACHTERNAAM2|Dekker, 16|VOORNAAM2|Anna, 42|VOORNAAM2|Anna'}
        },
        {
            'text': 'Bla bla # bla...',
            'exp_text': 'Bla bla (.) bla+...',
            'exp_tiers': {'xpct': '13|...|+..., 8|#|(.)'}
        },
        {
            'text': 'Ik heet NAAM1 en hij heet NAAM2.',
            'exp_text': 'Ik heet Jan en hij heet Anna.',
            'exp_tiers': {'xano': '8|NAAM1|Jan, 24|NAAM2|Anna'},
        },
        {
            'text': 'Ik zit op de SCHOOL1 en hij op de SCHOOL2.',
            'exp_text': 'Ik zit op de Mariaschool en hij op de Calvijnschool.',
            'exp_tiers': {'xano': '13|SCHOOL1|Mariaschool, 38|SCHOOL2|Calvijnschool'},
        },
        {
            'text': '’s morgens sta ik op.',
            'exp_text': "'s morgens sta ik op.",
            'exp_tiers': {},
        },
    ]
