"""Behavioural tests for the scoring engine."""

import pytest

import oracalm
from oracalm.core import score, interpret, render_form, ScoreResult


# --- min / max totals -------------------------------------------------------

@pytest.mark.parametrize("iid, n_items, lo, hi", [
    ("mdas", 5, 5, 25),
    ("corah_das", 4, 4, 20),
    ("mcdasf", 8, 8, 40),
])
def test_min_and_max_totals(iid, n_items, lo, hi):
    assert score(iid, [1] * n_items).total == lo
    assert score(iid, [5] * n_items).total == hi


# --- MDAS scoring & cut-off -------------------------------------------------

def test_mdas_moderate_no_flag():
    r = score("mdas", [3, 3, 4, 2, 5])  # 17
    assert r.total == 17
    assert r.band_label == "Moderate dental anxiety"
    assert r.flags == []


def test_mdas_cutoff_19_flagged():
    r = score("mdas", [4, 4, 4, 4, 3])  # 19
    assert r.total == 19
    assert "High dental anxiety" in r.band_label
    assert any(">=19" in f for f in r.flags)


def test_mdas_boundary_18_is_moderate():
    assert interpret("mdas", 18)["label"] == "Moderate dental anxiety"
    assert "High" in interpret("mdas", 19)["label"]


def test_mdas_alias_and_language_passthrough():
    r = score("MDAS", [1, 1, 1, 1, 1], language="tr")
    assert r.instrument_id == "mdas"
    assert r.language == "tr"
    assert r.band_label == "Low dental anxiety"


# --- Corah scoring & cut-offs -----------------------------------------------

def test_corah_thresholds():
    assert interpret("corah_das", 8)["label"].startswith("Low")
    assert interpret("corah_das", 12)["label"] == "Moderate anxiety"
    assert interpret("corah_das", 13)["label"] == "High anxiety"
    assert interpret("corah_das", 15)["label"].startswith("Severe")


def test_corah_double_flag_at_15():
    r = score("das", [4, 4, 4, 3])  # 15
    assert r.total == 15
    assert any(">=13" in f for f in r.flags)
    assert any(">=15" in f for f in r.flags)


def test_corah_flag_at_13_not_15():
    r = score("corah_das", [3, 3, 3, 4])  # 13
    assert any(">=13" in f for f in r.flags)
    assert not any(">=15" in f for f in r.flags)


# --- MCDASf -----------------------------------------------------------------

def test_mcdasf_moderate_band():
    r = score("mcdasf", [2, 2, 3, 2, 3, 2, 2, 3])  # 19
    assert r.total == 19
    assert r.band_label == "Moderate anxiety"
    assert r.flags == []  # no cut-offs defined for MCDASf


# --- validation errors ------------------------------------------------------

def test_wrong_length_raises():
    with pytest.raises(ValueError):
        score("mdas", [1, 2, 3])


def test_out_of_range_value_raises():
    with pytest.raises(ValueError):
        score("mdas", [1, 2, 3, 4, 6])


def test_non_int_raises():
    with pytest.raises(TypeError):
        score("mdas", [1, 2, 3, 4, "5"])


def test_bool_rejected():
    with pytest.raises(TypeError):
        score("mdas", [True, 1, 1, 1, 1])


def test_interpret_out_of_range_raises():
    with pytest.raises(ValueError):
        interpret("mdas", 26)
    with pytest.raises(ValueError):
        interpret("mdas", 4)


# --- result object & rendering ---------------------------------------------

def test_score_result_roundtrip_dict():
    r = score("mdas", [2, 2, 2, 2, 2])
    d = r.to_dict()
    assert d["total"] == 10
    assert d["instrument_id"] == "mdas"
    assert isinstance(r, ScoreResult)
    assert "MDAS" in str(r)


def test_render_form_contains_items_and_options():
    text = render_form("mdas", language="en")
    assert "Modified Dental Anxiety Scale" in text
    assert "tooth drilled" in text
    assert "[5] Extremely anxious" in text


def test_render_form_turkish():
    text = render_form("mdas", language="tr")
    assert "Kaygılı değilim" in text


def test_package_exposes_public_api():
    assert hasattr(oracalm, "score")
    assert hasattr(oracalm, "interpret")
    assert oracalm.__version__ == "0.1.0"
    assert len(oracalm.list_instruments()) == 3
