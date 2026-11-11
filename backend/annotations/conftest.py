
import pytest

from annotations.writers.saf_xlsx import SAFWriter


@pytest.fixture
def safwriter(asta_method, single_utt_allresults):
    sd_method = asta_method.to_sastadev()
    writer = SAFWriter(sd_method, single_utt_allresults)
    return writer
