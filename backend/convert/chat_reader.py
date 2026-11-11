import logging
from typing import Dict, List, Optional, Set, Tuple

from analysis.convert.chat_converter import REPLACEMENTS
from analysis.models import MethodCategory
from chamd.chat_reader import ChatFile, ChatHeader, ChatLine
from chamd.chat_reader import ChatReader as ChatParser
from chamd.chat_reader import ChatTier, MetaValue

logger = logging.getLogger('sasta')

TARGET_ROLES = ['Target_Child', 'Target_Adult', 'Participant']
XSID_POSTCODES = ['[+ G]', '[+ VU]']


def apply_replacements(line: ChatLine) -> ChatLine:
    # perform all replacements
    for rep in REPLACEMENTS:
        code = rep['code']
        func = rep['function']
        allow_skip = rep['allow_skip']

        all_comments = []
        done = False
        while not done:
            try:
                # apply replacement function
                new_text, comment = func(line.text)
            except Exception as e:
                if allow_skip:
                    # if replacement category is skippable: log and move on
                    logger.warn(e)
                    print('error in {} for utterance "{}": {}'.format(
                        func.__name__, line.text, e))
                    new_text, comment = line.text, None
                else:
                    # else, raise an error
                    logger.warn(e.args[0])
                    raise e

            if comment:
                # if there was a comment, apply replacement
                line.text = new_text
                all_comments.append(comment)
            else:
                # no comment means we are done
                # add all comments as a tier
                if len(all_comments) > 0:
                    tier_code = f'x{code}'
                    tier = ChatTier(tier_code, ','.join(all_comments))
                    line.tiers[tier_code] = tier
                done = True
    return line


class ChatDocument:
    def __init__(self, inputdoc: ChatFile, method_category: MethodCategory):
        self.method_category = method_category
        self.headers: List[ChatHeader] = inputdoc.headers or []
        self.header_metadata: Dict = inputdoc.header_metadata or {}
        self.file_metadata: Dict[str, MetaValue] = inputdoc.metadata or {}
        self.charmap: Dict[str, str] = inputdoc.charmap or {}
        read_lines = inputdoc.lines or []
        self.lines: List[ChatLine] = [*map(apply_replacements, read_lines)]
        # SASTA specific attributes
        self.target_speakers: Set[str] = self.find_target_speakers()
        self.process_postcodes()
        self.target_uttids: bool = self.has_xsids
        self.assign_target_xsids()

    @classmethod
    def from_chatfile(cls, filepath: str, method_category: MethodCategory):
        reader = ChatParser()
        doc = reader.read_file(filepath)
        # TODO: probably want to let this condition go if it
        # only concerns warning
        # assert not reader.errors
        for err in reader.errors:
            logger.debug(err)
        return cls(doc, method_category)

    def replacements(self, line: ChatLine) -> None:
        # perform all replacements
        for rep in REPLACEMENTS:
            code = rep['code']
            func = rep['function']
            allow_skip = rep['allow_skip']

            all_comments = []
            done = False
            while not done:
                try:
                    # apply replacement function
                    new_text, comment = func(line.text)
                except Exception as e:
                    if allow_skip:
                        # if replacement category is skippable: log and move on
                        logger.warn(e)
                        print('error in {} for utterance "{}": {}'.format(
                            func.__name__, line.text, e))
                        new_text, comment = line.text, None
                    else:
                        # else, raise an error
                        logger.warn(e.args[0])
                        raise e

                if comment:
                    # if there was a comment, apply replacement
                    self.text = new_text
                    all_comments.append(comment)
                else:
                    # no comment means we are done
                    # add all comments as a tier
                    if len(all_comments) > 0:
                        tier_code = f'x{code}'
                        tier = ChatTier(tier_code, ','.join(all_comments))
                        line.tiers[tier_code] = tier
                    done = True

    def apply_replacements(self):
        for line in self.lines:
            self.replacements(line)

    def find_target_speakers(self) -> Set[str]:
        results = set([])
        participants = self.header_metadata.get('participants')
        results |= self.find_target_roles(participants)
        ids = self.header_metadata.get('id')
        results |= self.find_target_roles(ids)
        return results

    def process_postcodes(self) -> None:
        current_xsid = 1
        for line in self.lines:
            if any(postcode in line.original for postcode in self.method_category.marking_postcodes):
                line.tiers['xsid'] = ChatTier('xsid', str(current_xsid))
                current_xsid += 1

    def assign_target_xsids(self) -> None:
        '''
        If there are target speakers, and no specifically targetted utterances,
        mark all utterances by target speakers with an xsid
        '''
        if (len(self.target_speakers) > 0) and not (self.has_xsids):
            current_xsid = 1
            for line in self.lines:
                if line.metadata['speaker'].text in self.target_speakers:
                    line.tiers['xsid'] = ChatTier('xsid', str(current_xsid))
                    current_xsid += 1

    @staticmethod
    def find_target_roles(header: Optional[Dict]) -> Set[str]:
        if not header:
            return set([])
        return {
            code for (code, info) in header.items()
            if info['role'] in TARGET_ROLES
        }

    @property
    def has_xsids(self) -> bool:
        tiers = [ln.tiers for ln in self.lines]
        return any(t.get('xsid') for t in tiers)

    def __eq__(self, other) -> bool:
        safe_headers = ('session',)

        if all((self.charmap == other.charmap,
                self._eq_headers(other),
                self._eq_header_metadata(other, safe_headers),
                self._eq_file_metadata(other, safe_headers),
                self._eq_lines(other)
                )):
            return True
        return False

    def _eq_headers(self, other) -> bool:
        # Compare headers, ignoring linestartno to allow rewriting multiline headers to a single line
        ignore_keys = ('linestartno',)
        filtered_self = [{k: v for (k, v) in d.items() if k not in ignore_keys} for d in [h.__dict__ for h in self.headers]]
        filtered_other = [{k: v for (k, v) in d.items() if k not in ignore_keys} for d in [h.__dict__ for h in other.headers]]
        return filtered_self == filtered_other

    def _eq_header_metadata(self, other, safe_headers: Tuple[str]) -> bool:
        if self.header_metadata.keys() != other.header_metadata.keys():
            return False
        for k, v in self.header_metadata.items():
            if other.header_metadata[k] != v:
                if k not in safe_headers:
                    return False
        return True

    def _eq_file_metadata(self, other, safe_headers: Tuple[str]) -> bool:
        if self.file_metadata.keys() != other.file_metadata.keys():
            return False
        for k, v in self.file_metadata.items():
            if str(v) != str(other.file_metadata[k]):
                if k not in safe_headers:
                    return False
        return True

    def _eq_lines(self, other):
        for i, ln in enumerate(self.lines):
            otherln = other.lines[i]
            if ln.original != otherln.original:
                return False
            if [str(t) for t in ln.tiers] != [str(t) for t in otherln.tiers]:
                return False
        return True
