import os.path as op
from filecmp import cmp, clear_cache
from os import remove as rm

from analysis.convert.chat_converter import SifReader, Utterance
from analysis.convert.replacements import (correct_punctuation, fill_name,
                                           replace_quotation_marks)
from analysis.utils import docx_to_txt

HERE = op.dirname(op.abspath(__file__))


def test_docx_to_txt(testfiles):
    clear_cache()
    for fn, docx in testfiles.items():
        txt = docx_to_txt(docx, delete_docx=False)
        txt_exp = txt.replace(fn, f'{fn}_exp')
        assert cmp(txt, txt_exp, shallow=False)

        doc = SifReader(txt).document
        cha = op.join(HERE, f'{fn}.cha')
        doc.write_chat(cha)
        cha_exp = cha.replace(fn, f'{fn}_exp')

        assert doc.title.replace(
            '_', '-') == fn.replace('.docx', '').replace('_', '-')

        with open(cha, 'r') as of:
            with open(cha_exp) as ef:
                orig = of.readlines()
                exp = ef.readlines()
                for i, orig_line in enumerate(orig):
                    assert orig_line == exp[i]

        if op.exists(txt):
            rm(txt)
        if op.exists(cha):
            rm(cha)


def test_fill_name(replace_names):
    # fill in anonymised names
    for string, exp_string, exp_comment in replace_names:
        corrected, comment = fill_name(string)
        assert corrected == exp_string
        assert comment == exp_comment


def test_correct_punctuation(replace_punc):
    # cases where punctuation should be corrected
    for string, exp_string, exp_comment in replace_punc:
        corrected, comment = correct_punctuation(string)
        assert corrected == exp_string
        assert comment == exp_comment


# def test_flag_punctuation(flag_punc):
#     # cases where punctuation should raise an error
#     for string in flag_punc:
#         try:
#             done = False
#             while not done:
#                 string, _ = correct_punctuation(string)
#             assert False
#         except ValueError as e:
#             assert e.args[0] == 'Parentheses in utterances are not allowed.'


def test_fill_utterance(example_utterances):
    # combined corrections on utterances
    for data in example_utterances:
        utt = Utterance('XXX', data['text'])

        assert utt.text == data['exp_text']

        for tier_code in data['exp_tiers']:
            tier_value = data['exp_tiers'][tier_code]

            def matching(tier):
                return tier.code == tier_code and tier.value == tier_value

            assert any(map(matching, utt.tiers))


def test_quotemarks(quotemarks):
    expected = (quotemarks[-1], None)
    for line in quotemarks:
        assert replace_quotation_marks(line) == expected
