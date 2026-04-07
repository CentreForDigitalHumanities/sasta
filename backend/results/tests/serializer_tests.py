from xml.etree import ElementTree as etree

from results.serializers import allresults_from_dict, allresults_to_dict


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
