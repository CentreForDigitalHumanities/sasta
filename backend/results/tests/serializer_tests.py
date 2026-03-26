from xml.etree import ElementTree as etree

from results.serializers import allresults_from_dict, allresults_to_dict


def test_serializer(example_allresults):
    input = example_allresults
    d = allresults_to_dict(input)
    output = allresults_from_dict(d)
    assert input.uttcount == output.uttcount
    assert input.filename == output.filename
    assert input.annotationinput == output.annotationinput
    assert input.allutts == output.allutts
    assert input.postresults == output.postresults
    assert input.coreresults == output.coreresults
    assert input.exactresults == output.exactresults
    assert input.allmatches == output.allmatches
    assert input.analysedtrees.keys() == output.analysedtrees.keys()
    for k in input.analysedtrees.keys():
        assert etree.tostring(input.analysedtrees[k]) == etree.tostring(output.analysedtrees[k])

