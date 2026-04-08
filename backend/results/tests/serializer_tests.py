from xml.etree import ElementTree as etree
from collections import Counter

from sastadev.allresults import AllResults
from results.serializers import (
    allresults_from_dict,
    allresults_from_json,
    allresults_to_dict,
    allresults_to_json,
)


def test_serializer(example_allresults):
    allresults_in = example_allresults
    d = allresults_to_dict(allresults_in)
    output = allresults_from_dict(d)
    assert allresults_in.uttcount == output.uttcount
    assert allresults_in.filename == output.filename
    assert allresults_in.annotationinput == output.annotationinput
    assert allresults_in.allutts == output.allutts
    assert allresults_in.postresults == output.postresults
    assert allresults_in.coreresults == output.coreresults
    assert allresults_in.exactresults == output.exactresults
    assert allresults_in.allmatches == output.allmatches
    # TODO: reinstate this
    # assert allresults_in.analysedtrees.keys() == output.analysedtrees.keys()
    # for k in allresults_in.analysedtrees.keys():
    #     assert etree.tostring(allresults_in.analysedtrees[k]) == etree.tostring(output.analysedtrees[k])


def test_json_serializer_supports_tuple_keys_in_postresults():
    allresults_in = AllResults(
        uttcount=1,
        filename='single_utt',
        coreresults={},
        exactresults={},
        allmatches={},
        analysedtrees=[],
        annotationinput=True,
        allutts={'1': ['foo']},
        postresults={
            'A046': Counter({('beet', '1'): 1, ('ongeluk', '1'): 1}),
            'A165': 'output_file_name',
        },
    )

    json_str = allresults_to_json(allresults_in)
    output = allresults_from_json(json_str)

    assert allresults_in.postresults == output.postresults
