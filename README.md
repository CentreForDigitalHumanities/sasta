[sd-link]: https://github.com/CentreForDigitalHumanities/sastadev/
[sasta-prod]: https://sasta.hum.uu.nl/
[user-docs]: https://CentreForDigitalHumanities.github.io/sasta/
[sd-docs]: https://sastadev.readthedocs.io/en/latest/introduction.html
[sd-pypi]: https://pypi.org/project/sastadev/

# SASTA: Semi-Automatische Spontane Taal Analyse
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10600256.svg)](https://doi.org/10.5281/zenodo.10600256)

SASTA is a tool for the analysis of spontaneous language transcripts, to aid clinical linguists and research into language development and language disorders. SASTA analyzes a transcript grammatically using [Alpino](https://www.ineo.tools/resources/alpino), an automatic utterance parser for Dutch, and can recognize a significant number of forms of deviant language use and analyze them correctly, following multiple assessment methods available for Dutch ([TARSP](https://www.pearsonclinical.nl/tarsp), [STAP](https://www.hetwap.nl/wp-content/uploads/2018/04/2008-STAP-HANDLEIDING.pdf) and [ASTA](https://klinischelinguistiek.nl/uploads/201307asta4eversie.pdf)).

## Overview

* SASTA can analyze transcripts following multiple assessment methods available for Dutch:
  * [TARSP](https://www.pearsonclinical.nl/tarsp) (Schlichting 2005, 2017) for young children (1–4 years), inspired by LARSP for English (Crystal et al. 1989);
  * [STAP](https://www.hetwap.nl/wp-content/uploads/2018/04/2008-STAP-HANDLEIDING.pdf) (Verbeek et al. 2007, van Ierland et al. 2008) for older children (4–8 years);
  * [ASTA](https://klinischelinguistiek.nl/uploads/201307asta4eversie.pdf) (Boxum et al. 2013) for adults suffering from aphasia.
* SASTA generates as output a method-specific form and an annotated transcript. The generated transcript can be corrected by a linguist, if needed, and re-uploaded into SASTA, after which SASTA generates an adapted method-specific form. Overall, SASTA achieves an accuracy between 88 and 95% on training data for TARSP and STAP.
* SASTA accepts as input transcripts in MS Word or plain text (given some SASTA-specific requirements), as well as CHAT (MacWhinney 2000), and uses [AuCHAnn](https://www.ineo.tools/resources/auchann) to generate valid CHAT files for transcripts accompanied by an interpretation, which significantly improves results.
* SASTA analyzes a transcript grammatically using [Alpino](https://www.ineo.tools/resources/alpino). It then uses specially constructed (XPath) queries for all measures defined within the assessment method to count the frequencies of linguistic phenomena in the spontaneous language sample. As such, SASTA may be considered a spin-off of [GrETEL](https://www.ineo.tools/resources/gretel), that can be used to investigate syntactic phenomena using query-by-example.
* Further development of SASTA is ongoing, in close collaboration with researchers in language development and with linguists in clinics.

## Contents
This repository contains the source code for the SASTA web application, which consists of a Django backend and Angular frontend.

This repository does _not_ include input data, as these can be privacy sensistive. Refer to the documentation for instructions on constructing your own input data.

## Sastadev

SASTA relies on a [Python package][sd-pypi] called ``sastadev`` in the backend. This package is freely available on [Github][sd-link], with documentation available on [Read the Docs][sd-docs].

## Usage
If you are interested in using SASTA, the most straightforward way to get started is to make an account at [sasta.hum.uu.nl][sasta-prod]. This server is maintained by the Research Software Lab and runs the most current release.

Consult the [user documentation][user-docs] for all information on using the application, input formats, and output formats.

Self-hosting is an option, though support by the Research Software Lab is not provided.

## Development
The [documentation directory](./docs/) contains documentation for developers. This includes [running the application through Docker](./docs/local-installation%20(Docker).md).

## License
SASTA is shared under a BSD-3 Clause licence See [LICENSE](./LICENSE) for more information.

## Citation
If you wish to cite this repository, please use the metadata provided in our [CITATION.cff file](./CITATION.cff).

## Contact
For questions, small feature suggestions, and bug reports, feel free to [create an issue](https://github.com/CentreForDigitalHumanities/sasta/issues/new). You can also contact the [Centre for Digital Humanities](https://cdh.uu.nl/contact/).

## Publications on SASTA

* Odijk, J. (2021). Towards Semi-Automatic Analysis of Spontaneous Language for Dutch. In *Selected papers from the CLARIN Annual Conference 2020* (Vol. 180, pp. 165-175). (Linköping Electronic Conference Proceedings). Linköping University Press. https://doi.org/10.3384/ecp18018
* Renckens, E., & Odijk, J. (2021). Online tool SASTA analyseert taal. *eData & Research*, *15*(2), 7-7. https://edata.nl/2021/02/10/online-tool-sasta-analyseert-taal/

## Other relevant publications

* Boxum, E., van der Scheer, F. and Zwaga, M. (2013). *ASTA: Analyse voor Spontane Taal bij Afasie* (4th ed.). Vereniging voor Klinische Linguïstiek.
* Crystal, D., Fletcher, P. and Garman, M. (1989). *Grammatical Analysis of Language Disability* (2nd ed.). London: Cole and Whurr. https://hdl.handle.net/10092/17651
* van Ierland, M., Verbeek, J. and van den Dungen, L. (2008). *Spontane Taal Analyse Procedure: Handleiding van het STAP-instrument*. Universiteit van Amsterdam.
* MacWhinney, B. (2000). *The CHILDES project: Tools for analyzing talk: Transcription format and programs* (3rd ed.). Lawrence Erlbaum Associates Publishers.
* Odijk, J. (2023, 30 Jan.). *Taaltechnologie voor taalkundig onderzoek*. Valedictory speech, Utrecht University. https://surfdrive.surf.nl/files/index.php/s/pzNHSgd6t8L0Wnk
* Schlichting, L. (2005). *TARSP: Taal Analyse Remediëring en Screening Procedure: Taalontwikkelingsschaal van
Nederlandse kinderen van 1–4 jaar* (7th ed.). Amsterdam: Pearson. ISBN 978 90 265 1355 8.
* Schlichting, L. (2017). *TARSP: Taal analyse remediëring en screening procedure: Taalontwikkelingsschaal Van Nederlandse Kinderen van 1–4 Jaar met Aanvullende Structuren tot 6 jaar* (8th ed.). Amsterdam: Pearson. ISBN 978 90 430 3561 3.
* Verbeek, J., van Ierland, M. and van den Dungen, L. (2007). *Spontane Taal Analyse Procedure: Verantwoording van het STAP-instrument*. Universiteit van Amsterdam.
