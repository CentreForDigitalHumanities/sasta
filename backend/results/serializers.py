import json
import xml.etree.ElementTree as _stdlib_etree
from collections import Counter

from lxml import etree
from sastadev.allresults import AllResults, reskeystr2reskey, showreskey

_ALLMATCHES_KEY_SEP = '|'


def _encode_results_key(key):
    return showreskey(key)


def _decode_results_key(s):
    return reskeystr2reskey(s)


def _encode_allmatches_key(key):
    results_key, utt_id = key
    return _encode_results_key(results_key) + _ALLMATCHES_KEY_SEP + utt_id


def _decode_allmatches_key(s):
    sep_idx = s.rfind(_ALLMATCHES_KEY_SEP)
    return (_decode_results_key(s[:sep_idx]), s[sep_idx + 1 :])


def _encode_syntree(node):
    if isinstance(node, _stdlib_etree.Element):
        return _stdlib_etree.tostring(node, encoding='unicode')
    return etree.tostring(node, encoding='unicode')


def _decode_syntree(xml_str):
    return etree.fromstring(xml_str)


def allresults_to_dict(allresults):
    coreresults = {
        _encode_results_key(k): dict(v) for k, v in allresults.coreresults.items()
    }
    exactresults = {
        _encode_results_key(k): list(v) for k, v in allresults.exactresults.items()
    }
    allmatches = {
        _encode_allmatches_key(k): [
            [_encode_syntree(node) for node in match] for match in matches
        ]
        for k, matches in allresults.allmatches.items()
    }
    analysedtrees = {
        utt_id: _encode_syntree(tree)
        for utt_id, tree in allresults.analysedtrees.items()
    }
    return {
        'uttcount': allresults.uttcount,
        'filename': allresults.filename,
        'annotationinput': allresults.annotationinput,
        'allutts': allresults.allutts,
        'postresults': allresults.postresults,
        'coreresults': coreresults,
        'exactresults': exactresults,
        'allmatches': allmatches,
        'analysedtrees': analysedtrees,
    }


def allresults_from_dict(d):
    coreresults = {
        _decode_results_key(k): Counter(v) for k, v in d['coreresults'].items()
    }
    exactresults = {
        _decode_results_key(k): [tuple(r) for r in v]
        for k, v in d['exactresults'].items()
    }
    allmatches = {
        _decode_allmatches_key(k): [
            tuple(_decode_syntree(node) for node in match) for match in matches
        ]
        for k, matches in d['allmatches'].items()
    }
    analysedtrees = {
        utt_id: _decode_syntree(xml_str)
        for utt_id, xml_str in d['analysedtrees'].items()
    }
    return AllResults(
        uttcount=d['uttcount'],
        filename=d['filename'],
        annotationinput=d['annotationinput'],
        allutts=d['allutts'],
        postresults=d['postresults'],
        coreresults=coreresults,
        exactresults=exactresults,
        allmatches=allmatches,
        analysedtrees=analysedtrees,
    )


def allresults_to_json(allresults):
    return json.dumps(allresults_to_dict(allresults))


def allresults_from_json(json_str):
    return allresults_from_dict(json.loads(json_str))
