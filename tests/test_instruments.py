"""Data-integrity tests: every instrument definition must be internally consistent."""

import pytest

from oracalm.instruments import (
    INSTRUMENTS,
    list_instruments,
    get_instrument,
    allowed_values,
    get_item_options,
)

ALL_IDS = sorted(INSTRUMENTS)


def test_three_instruments_present():
    assert set(INSTRUMENTS) == {"mdas", "corah_das", "mcdasf"}
    assert len(list_instruments()) == 3


@pytest.mark.parametrize("iid", ALL_IDS)
def test_required_keys(iid):
    inst = INSTRUMENTS[iid]
    for key in ("id", "name", "full_name", "population", "languages",
                "items", "score_range", "bands", "citation", "provenance"):
        assert key in inst, f"{iid} missing {key}"
    assert inst["id"] == iid


@pytest.mark.parametrize("iid", ALL_IDS)
def test_score_range_matches_items(iid):
    """Min/max achievable totals must equal the declared score_range."""
    inst = INSTRUMENTS[iid]
    lo_sum, hi_sum = 0, 0
    for item in inst["items"]:
        vals = [o["value"] for o in get_item_options(inst, item, "en")]
        lo_sum += min(vals)
        hi_sum += max(vals)
    assert [lo_sum, hi_sum] == inst["score_range"], (
        f"{iid}: achievable range [{lo_sum},{hi_sum}] != declared {inst['score_range']}"
    )


@pytest.mark.parametrize("iid", ALL_IDS)
def test_bands_cover_range_contiguously(iid):
    """Bands must tile the whole score range with no gaps or overlaps."""
    inst = INSTRUMENTS[iid]
    lo, hi = inst["score_range"]
    bands = sorted(inst["bands"], key=lambda b: b["min"])
    assert bands[0]["min"] == lo
    assert bands[-1]["max"] == hi
    for a, b in zip(bands, bands[1:]):
        assert b["min"] == a["max"] + 1, f"{iid}: gap/overlap between {a} and {b}"
    # every integer in range resolves to exactly one band
    for total in range(lo, hi + 1):
        matches = [bd for bd in bands if bd["min"] <= total <= bd["max"]]
        assert len(matches) == 1, f"{iid}: total {total} matched {len(matches)} bands"


@pytest.mark.parametrize("iid", ALL_IDS)
def test_options_are_1_to_5_integers(iid):
    inst = INSTRUMENTS[iid]
    for item in inst["items"]:
        vals = sorted(allowed_values(inst, item))
        assert vals == [1, 2, 3, 4, 5], f"{iid} item {item['id']} values {vals}"


@pytest.mark.parametrize("iid", ALL_IDS)
def test_every_item_has_english_text(iid):
    inst = INSTRUMENTS[iid]
    for item in inst["items"]:
        assert item["text"].get("en"), f"{iid} item {item['id']} missing EN text"


@pytest.mark.parametrize("iid", ALL_IDS)
def test_declared_languages_have_all_item_text(iid):
    inst = INSTRUMENTS[iid]
    for lang in inst["languages"]:
        for item in inst["items"]:
            assert item["text"].get(lang), f"{iid} item {item['id']} missing {lang} text"


def test_mdas_is_multilingual():
    assert set(["en", "tr", "fa"]).issubset(set(INSTRUMENTS["mdas"]["languages"]))


def test_citations_have_doi_or_pmid():
    for iid, inst in INSTRUMENTS.items():
        cite = inst["citation"]
        assert cite.get("doi") or cite.get("pmid"), f"{iid} citation lacks DOI/PMID"


def test_get_instrument_aliases_and_case():
    assert get_instrument("MDAS")["id"] == "mdas"
    assert get_instrument("das")["id"] == "corah_das"
    assert get_instrument("corah")["id"] == "corah_das"
    assert get_instrument("mcdas")["id"] == "mcdasf"
    assert get_instrument(" Corah DAS ")["id"] == "corah_das"


def test_get_instrument_unknown_raises():
    with pytest.raises(KeyError):
        get_instrument("nope")
