<div align="center">

# OraCalm

**Open, dependency-free scoring for validated dental-anxiety instruments — with multilingual item sets.**

[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-43%20passing-brightgreen.svg)](tests/)
[![Status](https://img.shields.io/badge/status-beta-orange.svg)](#roadmap)

</div>

> [!IMPORTANT]
> **OraCalm is an educational and research aid, not a diagnostic device.** It computes published scoring keys for **screening** only. It does not diagnose dental anxiety or phobia, stores no personal data, and never replaces clinical judgement or the original instruments' manuals.

---

## Why OraCalm

Dental anxiety is common, frequently under-detected, and measured with well-validated questionnaires — yet those instruments live in PDFs and journal appendices, and every project re-implements the scoring by hand. OraCalm encodes the **scoring keys, cut-offs, and interpretation bands** of widely used dental-anxiety instruments **once, correctly, and with citations**, as a small dependency-free Python library plus a clean web demo.

The scoring keys and cut-offs are facts; item wording is reproduced from the published instruments with attribution (see [Provenance & licensing](#provenance--licensing)).

## Instruments

| id | Instrument | Population | Items | Range | Validated cut-off | Languages | Source |
|----|------------|-----------|:-----:|:-----:|-------------------|-----------|--------|
| `mdas` | Modified Dental Anxiety Scale | Adults | 5 | 5–25 | **≥19** high anxiety / possible phobia | EN · TR · FA | Humphris et al. 1995 |
| `corah_das` | Corah's Dental Anxiety Scale | Adults | 4 | 4–20 | ≥13 clinically anxious; ≥15 severe | EN | Corah 1969 |
| `mcdasf` | Modified Child Dental Anxiety Scale (faces) | Children ~8–15y | 8 | 8–40 | no single agreed cut-off | EN | Howard & Freeman 2007 |

## Install

```bash
pip install oracalm          # once published to PyPI
# or, from a clone:
pip install -e .
```

## Quick start (Python)

```python
import oracalm

# Score a completed MDAS (one integer per item, in order)
result = oracalm.score("mdas", [3, 3, 4, 2, 5])
print(result.total)        # 17
print(result.band_label)   # 'Moderate dental anxiety'
print(result.flags)        # [] (below the ≥19 cut-off)

# A high-anxiety MDAS
oracalm.score("mdas", [4, 4, 4, 4, 3]).flags
# ['>=19: High dental anxiety / possible dental phobia']

# Interpret a raw total without re-scoring
oracalm.interpret("corah_das", 15)["label"]   # 'Severe anxiety (possible dental phobia)'

# Discover what's available
oracalm.list_instruments()
```

Every `ScoreResult` carries the total, the min/max range, the interpretation band, cut-off flags, and a human-readable interpretation, and serialises with `.to_dict()`.

## Command line

```bash
oracalm list                    # list instruments
oracalm show mdas --lang tr      # print the questionnaire (Turkish)
oracalm score mdas 3 3 4 2 5     # score (space- or comma-separated)
oracalm score das 4,4,4,3
```

```text
$ oracalm score das 4,4,4,3
Corah's Dental Anxiety Scale (Corah DAS)
  Total: 15 / 20  (range 4-20)
  Band:  Severe anxiety (possible dental phobia)
  Flags:
    - >=13: Clinically significant anxiety (per some references)
    - >=15: Severe anxiety / possible dental phobia
  Source: Corah NL (1969). Development of a dental anxiety scale. Journal of Dental Research.
```

## Web demo

A self-contained, mobile-friendly demo lives in [`demo/index.html`](demo/index.html) — pick an instrument, choose a language (MDAS: EN/TR/FA, with right-to-left support for Persian), tap through the items, and watch the score, severity band, and cut-off flags update live. No data leaves the page. Open the file directly, or host it on GitHub Pages.

The interface follows Apple's fluid-design principles — instant press feedback, calm critically-damped motion, translucent materials, optical typography, and full `prefers-reduced-motion` / `-transparency` / `-contrast` support — kept deliberately gentle for an anxiety-sensitive context.

## How scoring works

Each instrument is defined declaratively (see [`oracalm/instruments.py`](oracalm/instruments.py)) as: item stems, response options, total-score range, interpretation bands that tile the whole range, validated cut-offs, and a full citation. The engine ([`oracalm/core.py`](oracalm/core.py)) validates that every response is one of the item's allowed values and that the count matches, sums the responses, resolves the interpretation band, and evaluates cut-offs. The test suite proves that each instrument's achievable min/max equals its declared range and that the bands cover the range with no gaps or overlaps.

## Provenance & licensing

The **software** is MIT-licensed. The **instruments** are the intellectual property of their authors and are reproduced here for educational/research use with attribution:

- **MDAS** — made *freely available for use* by the authors provided the source is cited (official MDAS site, University of St Andrews). English wording is canonical; the **Turkish and Persian** strings are convenience translations and should be checked against the officially validated versions before clinical use.
- **Corah's DAS** (1969) — a classic, widely reproduced 4-item scale.
- **MCDASf** (Howard & Freeman 2007) — faces version of the Modified Child Dental Anxiety Scale (Wong et al. 1998).

If you plan **commercial** redistribution, verify the reuse terms of each instrument with its authors/publisher.

## Roadmap

- IDAF-4C+ (Index of Dental Anxiety and Fear) once reuse terms are confirmed.
- Additional validated language sets (contributions welcome, with a citation per translation).
- A `CITATION.cff`-linked Zenodo DOI on first tagged release.

## Citing OraCalm

If OraCalm supports your work, please cite the software (see [`CITATION.cff`](CITATION.cff)) **and** the original instrument(s) you used (see below).

## References

Instrument sources (retrieved via **PubMed**; DOIs/PMIDs linked):

- Humphris GM, Morrison T, Lindsay SJE. The Modified Dental Anxiety Scale: validation and United Kingdom norms. *Community Dent Health.* 1995;12(3):143–150. [PMID 7584581](https://pubmed.ncbi.nlm.nih.gov/7584581/)
- Corah NL. Development of a dental anxiety scale. *J Dent Res.* 1969;48(4):596. [doi:10.1177/00220345690480041801](https://doi.org/10.1177/00220345690480041801)
- Howard KE, Freeman R. Reliability and validity of a faces version of the Modified Child Dental Anxiety Scale. *Int J Paediatr Dent.* 2007;17(4):281–288. [doi:10.1111/j.1365-263X.2007.00830.x](https://doi.org/10.1111/j.1365-263X.2007.00830.x)

Recent validations motivating multilingual support: Höglund et al., *Acta Odontol Scand.* 2024 (Swedish MDAS) [doi:10.2340/aos.v83.42436](https://doi.org/10.2340/aos.v83.42436); Enshaei et al., *Clin Exp Dent Res.* 2024 (Persian child measure) [doi:10.1002/cre2.830](https://doi.org/10.1002/cre2.830).

## Contributing

Issues and pull requests welcome — especially validated translations (please include a citation) and additional validated instruments. Please keep the library dependency-free and add tests for any new instrument.

## License

[MIT](LICENSE) © 2026 Hossein Boustani Hezarani
