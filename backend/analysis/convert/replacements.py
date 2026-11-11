import re
from string import ascii_lowercase
import os.path as op
import json
from sastadev.conf import settings as sdsettings


def instantiate_anonymizations():
    json_path = op.join(sdsettings.SD_DIR, 'data', 'anonymization.json')
    with open(json_path, 'r') as f:
        return json.load(f)


ANONYMIZATIONS = instantiate_anonymizations()


class NoAlphabetLetter(ValueError):
    pass


def letter_index(letter: str) -> int:
    '''Return alphabet position for letter (0 if not found)'''
    try:
        return list(ascii_lowercase).index(letter.lower()) + 1
    except Exception:
        return 0


def fill_name(string):
    for specs in ANONYMIZATIONS:
        codes = '|'.join(sorted(specs['codes'], key=len, reverse=True))
        # groups: 1) word boundary 2) code 3) counter 4) word boundary
        pat = fr'(\b)\w*({codes})[^\d\W]*(\d*)(\b)'
        match = re.search(pat, string)

        def repl(match):
            raw_index = match.group(3) or '0'
            index = int(raw_index) if raw_index.isnumeric(
            ) else letter_index(raw_index)
            repl = specs['common'][index]
            return match.group(1) + repl + match.group(4)

        if match:
            newstring = re.sub(pat, repl, string, count=1)
            index = match.start()
            old = match.group(0)
            new = repl(match)
            comment = "{}|{}|{}".format(index, old, new)
            return newstring, comment

    # if no replacements were made, return original with no comment
    return string, None


def correct_punctuation(string):
    '''
    replace ellipses
    pattern: matches all '...' and '…' except when preceded by '+'
    or surrounded by '(' and ')'
    '''
    pattern = r'(?<!\+)(…|\.{3})(?!\))|(?<!\()(?<!\+)(…|\.{3})'
    match = re.search(pattern, string)
    if match:
        index = match.start()
        old = match.group(0)
        new = '+...'
        newstring = re.sub(pattern, new, string, count=1)
        comment = '{}|{}|{}'.format(index, old, new)
        return newstring, comment

    # replace hashtag
    pattern = r'#'
    match = re.search(pattern, string)
    if match:
        index = match.start()
        old = match.group()
        new = '(.)'
        newstring = re.sub(pattern, new, string, count=1)
        comment = '{}|{}|{}'.format(index, old, new)
        return newstring, comment

    # flag parentheses
    # pauses (.), (..) and (...) are okay, anything else should raise an error
    # pauses_removed = re.sub(r'\(\.{1,3}\)', '', string)
    # if '(' in pauses_removed or ')' in pauses_removed:
    #     raise ValueError('Parentheses in utterances are not allowed.')

    # if no replacements were made, return original with no comment
    return string, None


def replace_quotation_marks(string):
    ''' Replace left and right quote marks (Unicode 2018 and 2019)
        with a single quote (ASCII 39)
    '''
    pattern = r"[\u2018-\u2019]"
    res = re.sub(pattern, chr(39), string)

    return res, None
