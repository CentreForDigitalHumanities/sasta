# Changelog

All notable changes (beginning at version 0.2.0) to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.4] - 2024-06-11
### Added
-   Added outgoing links to homepage

## [0.9.3] - 2024-06-04
### Changed
-   Upgraded SASTADEV to 0.2.2

## [0.9.2] - 2024-05-28
### Added
-   Added a home page

### Changed
-   Locks first row and first two columns in SAF xlsx output

## [0.9.1] - 2024-05-20
### Fixed
-   Resolved various bugs that surfaced in release 0.9.0

## [0.9.0] - 2024-04-26
### Changed
Drastic changes to the way analysis is performed, replacing functionality by SASTADEV counterparts:
- reading SAF files
- performing analysis
- changed the SAF writer

## [0.8.2] - 2024-04-24
### Changed
Upgraded SASTADEV dependency

## [0.8.1] - 2024-01-31
### Added
- Adhere to FAIR software principles

## [0.6.3] - 2023-05-12

### Added
- User documentation

### Changed
- Split Angular frontend into core-, shared-, and feature- modules
- Extended anonymization codes and moved to a centrally located JSON file

### Added
- First version of user documentation

## [0.6.2] - 2022-02-15

### Changed
- Various frontend refactors
- Corpus and transcript divided in list and detail views to reduce data transfer

### Fixed
- Resolved a bug were corpora were being constantly retrieved, leading to very high data transfer

### Security
-   Fixed multipe vulnerabilities in backend and frontend.

## [0.6.1] - 2022-09-16

### Fixed
-   Resolved a bug where transcript paths were uncorrectly saved, leaving them unable to be downloaded
-   Resolved a bug where a dictionary was changed during iteration, preventing analysis

## [0.6.0] - 2022-07-27

### Added

-   Visualize parse trees for utterances

### Fixed

-   Resolved a bug where words would be misaligned when analyzing with existing annotations

### Changed

-   Implemented latest SASTADEV methods
-   Clearer error messages for parses that cannot be analysed

## [0.5.3] - 2022-07-27

### Fixed

-   Bump corpus2alpino version to 0.3.10

## [0.5.2] - 2022-07-26

### Fixed

-   Authentication guard for protected routes awaits checking user, preventing redirects to login after page refresh.

## [0.5.0] - 2022-06-28

### Fixed

-   Resolved a bug where corpora keep refreshing after leaving their page
-   Resolved several vulnerabilities in both backend and frontend

### Added

-   Implemented preprocessing steps for CHAT input files (anonymization, interpunction cleanup)
-   Separated parsed and reparsed/corrected treebanks. Admins can view them separately , both files are included in corpus downloads
-   Added comment row to annotation files, allowing free text. These are not interpreted by the analysis
-   Allows annotation in unaligned column, signifying either utterance-level or unaligned annotations

### Changed

-   Disabled method selection for non-admins. The latest method is used by default. Admins can still select older versions
-   Moved unaligned column to the first position, before word1..wordN in annotation files

## [0.4.0] - 2022-04-05

### Fixed

-   Resolved an issue where default methods were prevented from being set.
-   Some forms were not correctly updated after supplying manual corrections, e.g. ASTA WW and N. This is fixed by implementing aligned results functionality.

### Added

-   New SASTADEV method definitions.

### Changed

-   Extra corpus information and control:
    -   Overview of number of targeted utterances and targeting flags.
    -   Overview of all utterances.
    -   Shortcut to upload additional transcripts to the corpus.
-   Upload multiple files without zipping them.
-   In SASTA Output Format, lock all cells except annotation cells. This is implemented to avoid errors in manual correction files.
-   ASTA corrects Nouns and Verbs
-   use exactresults

## [0.3.2] - 2022-03-22

### Fixed

-   Resolved an issue where corrected transcripts were incorrectly analyzed.

## [0.3.1] - 2022-03-21

### Fixed

-   Resolved an issue where CHAT annotations were added to the wrong utterances.

## [0.3.0] - 2022-02-07

### Added

-   Implement latest method defintions.
-   Upgrade to Python 3.7.x
-   Concurrent parsing: up to 8 transcripts can be parsed in parallel.

### Changed

-   All marked utterances are given utterance IDs, no longer use utterance numbers. Analysis now numbers utterance 1-N, where N is number of marked utterances.
-   Phase out `python-ucto`, and by proxy `ucto` (through changes in `corpus2alpino`). Severly reduces dependency complexity.

### Removed

-   Dropped Python 3.6.x support.

### Security

-   Fixed multipe vulnerabilities in backend and frontend.

## [0.2.6] - 2021-12-17

### Changed

-   Differentiate CHAT postcode markers by method. For STAP `[+ VU]` is marked, for all methods `[+ G]`

## [0.2.5] - 2021-11-12

### Added

-   Process CHAT postcodes `[+ VU]` and `[+ G]` as utterance analysis markers

### Changed

-   Updated VKL logo

## [0.2.4] - 2021-09-23

### Fixed

-   Trailing whitespace in SIF headers is ignored

## [0.2.3] - 2021-09-23

### Changed

-   Run pre-queries before core-queries

## [0.2.0] - 2021-09-10

### Added

-   CHAT format input.
-   Asynchronous parsing; the parse process continues in the background.
-   Updates to query definitions and related SASTADEV functions.
-   Automatic corrections on input files to improve parses of irregular language (implemented in SASTADEV).
-   Logos for participating organisations.

### Changed

-   Give corpora a method category, can only query and annotate using methods within this category.
-   Updated look.

### Removed

-   Remove 'Inform only' choice, the option is forcibly set to true.

### Fixed

-   Asynchronous parsing ensures the application does not lock all users for the duration.

### Security

-   Fix multiple vulnerabilities in both frontend and backend.
