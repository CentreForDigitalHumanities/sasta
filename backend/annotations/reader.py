from sastadev.allresults import AllResults
from sastadev.methods import Method
from sastadev.SAFreader import get_golddata, richscores2scores


def read_saf(saf_filename: str, method: Method, includeimplies: bool = False) -> AllResults:
    '''Wrapper around SASTADEV SAF reader'''
    infilename = saf_filename
    allutts, richexactscores = get_golddata(infilename, method, includeimplies)
    exactresults = richscores2scores(richexactscores)
    annotatedfileresults = AllResults(uttcount=len(allutts),
                                      coreresults={},
                                      exactresults=exactresults,
                                      postresults={},
                                      allmatches={},
                                      filename=infilename,
                                      analysedtrees=[],
                                      allutts=allutts,
                                      annotationinput=True)
    return annotatedfileresults
