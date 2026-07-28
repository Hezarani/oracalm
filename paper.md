---
title: 'OraCalm: open, multilingual scoring for validated dental-anxiety instruments'
tags:
  - dentistry
  - dental anxiety
  - psychometrics
  - screening
  - Python
authors:
  - name: Hossein Boustani Hezarani
    orcid: 0009-0007-8481-0498
    affiliation: 1
affiliations:
  - name: Independent researcher; Decadentry.com, Ankara, Türkiye
    index: 1
date: 28 July 2026
bibliography: paper.bib
---

# Summary

`OraCalm` is a dependency-free Python library, command-line tool, and self-contained
web demo for scoring validated **dental-anxiety** questionnaires. It implements the
published scoring keys, cut-offs, and interpretation bands of three widely used
instruments — the Modified Dental Anxiety Scale (MDAS) [@Humphris1995], Corah's
Dental Anxiety Scale [@Corah1969], and the faces version of the Modified Child
Dental Anxiety Scale (MCDASf) [@Howard2007] — each with a full source citation and,
for the MDAS, aligned English/Turkish/Persian item sets. `OraCalm` is an
educational and research aid; it is explicitly **not** a diagnostic device and
stores no personal data.

# Statement of need

Dental anxiety is prevalent, frequently under-detected, and routinely measured with
brief self-report instruments, but those instruments live in journal appendices and
clinic PDFs. As a result, researchers and educators re-implement the same scoring
and cut-off logic ad hoc, producing avoidable inconsistency, and there is no small,
tested, reusable component that turns a completed questionnaire into a scored,
interpreted, and *cited* result. `OraCalm` fills that gap: it encodes each
instrument's scoring key exactly once, validates responses against the instrument
definition, and returns a structured result with the interpretation band and any
triggered cut-offs. Because dental anxiety and its measurement are studied across
languages [@Hoglund2024; @Enshaei2024], the library is built to carry aligned
multilingual item sets as data, demonstrated here with the MDAS in English, Turkish,
and Persian (including right-to-left rendering in the web demo).

# Functionality

The public API is deliberately small: `score(instrument, responses)` returns a
`ScoreResult` (total, range, interpretation band, cut-off flags, and a
human-readable interpretation); `interpret(instrument, total)` maps a raw total to
its band; `list_instruments()` and `get_instrument(id)` expose the catalogue; and
`render_form(instrument, language)` renders the questionnaire for printing or a CLI.
Instruments are declared as data — item stems, response options, score range,
interpretation bands, validated cut-offs, and citation — so new instruments or
languages are added without touching the engine. A command-line entry point
(`oracalm score|show|list`) and a single-file web demo are included.

# Quality control

`OraCalm` ships with an automated test suite (43 tests) that checks both behaviour
and data integrity: every instrument's minimum and maximum achievable totals equal
its declared range; the interpretation bands tile the entire range with no gaps or
overlaps; responses are validated for count and allowed values; cut-off flags fire
at the correct thresholds (e.g. MDAS ≥19; Corah ≥13 and ≥15); and the multilingual
item sets are complete for every declared language.

# Availability and disclaimer

`OraCalm` is released under the MIT license at
<https://github.com/Hezarani/oracalm>. The **instruments** remain the intellectual
property of their authors and are reproduced for educational/research use with
attribution; commercial redistribution should be cleared with the instrument
owners. The tool supports screening and education only and does not replace clinical
judgement or the original instruments' manuals.

# References
