"""Scoring engine for OraCalm dental-anxiety instruments.

All logic is dependency-free and deterministic. The public entry points are
:func:`score` and :func:`interpret`.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional

from .instruments import get_instrument, allowed_values, get_item_options


@dataclass
class ScoreResult:
    """The outcome of scoring one completed questionnaire."""
    instrument_id: str
    instrument_name: str
    full_name: str
    population: str
    language: str
    responses: List[int]
    total: int
    min_total: int
    max_total: int
    band_label: str
    band_description: str
    flags: List[str] = field(default_factory=list)
    interpretation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __str__(self) -> str:  # human-friendly one-liner
        return (
            f"{self.instrument_name}: {self.total}/{self.max_total} "
            f"-> {self.band_label}"
        )


def interpret(instrument_id: str, total: int) -> Dict[str, Any]:
    """Return the interpretation band for a total score.

    Raises ``ValueError`` if the total falls outside the instrument's range.
    """
    inst = get_instrument(instrument_id)
    lo, hi = inst["score_range"]
    if not isinstance(total, int):
        raise TypeError("total must be an int")
    if total < lo or total > hi:
        raise ValueError(
            f"Total {total} is outside the valid range [{lo}, {hi}] for {inst['name']}."
        )
    for band in inst["bands"]:
        if band["min"] <= total <= band["max"]:
            return band
    # Should be unreachable if bands cover the full range.
    raise ValueError(f"No interpretation band matched total {total} for {inst['name']}.")


def _check_cutoffs(inst: Dict[str, Any], total: int) -> List[str]:
    flags: List[str] = []
    for cut in inst.get("cutoffs", []):
        thr, op = cut["threshold"], cut["operator"]
        hit = (op == ">=" and total >= thr) or (op == ">" and total > thr) or \
              (op == "<=" and total <= thr) or (op == "<" and total < thr) or \
              (op == "==" and total == thr)
        if hit:
            flags.append(f"{op}{thr}: {cut['label']}")
    return flags


def score(instrument_id: str, responses: List[int], language: str = "en") -> ScoreResult:
    """Score a completed questionnaire.

    Parameters
    ----------
    instrument_id:
        Instrument id or alias (e.g. ``"mdas"``, ``"corah_das"``, ``"mcdasf"``).
    responses:
        One integer per item, in item order, each within that item's allowed
        values (validated against the instrument definition).
    language:
        Language code for the returned prompt/interpretation strings.

    Returns
    -------
    ScoreResult
    """
    inst = get_instrument(instrument_id)
    items = inst["items"]

    if not isinstance(responses, (list, tuple)):
        raise TypeError("responses must be a list of integers")
    if len(responses) != len(items):
        raise ValueError(
            f"{inst['name']} expects {len(items)} responses, got {len(responses)}."
        )

    cleaned: List[int] = []
    for item, resp in zip(items, responses):
        if isinstance(resp, bool) or not isinstance(resp, int):
            raise TypeError(
                f"Item {item['id']} response must be an int, got {type(resp).__name__}."
            )
        allowed = allowed_values(inst, item)
        if resp not in allowed:
            raise ValueError(
                f"Item {item['id']} response {resp} is not one of {sorted(allowed)}."
            )
        cleaned.append(resp)

    total = sum(cleaned)
    lo, hi = inst["score_range"]
    band = interpret(instrument_id, total)
    flags = _check_cutoffs(inst, total)

    interpretation = (
        f"{inst['full_name']} total = {total} (range {lo}-{hi}): "
        f"{band['label']}. {band['description']}"
    )

    return ScoreResult(
        instrument_id=inst["id"],
        instrument_name=inst["name"],
        full_name=inst["full_name"],
        population=inst["population"],
        language=language,
        responses=cleaned,
        total=total,
        min_total=lo,
        max_total=hi,
        band_label=band["label"],
        band_description=band["description"],
        flags=flags,
        interpretation=interpretation,
    )


def render_form(instrument_id: str, language: str = "en") -> str:
    """Return a plain-text rendering of the questionnaire (items + options).

    Handy for CLIs, printouts, and quick review. Does not collect answers.
    """
    inst = get_instrument(instrument_id)
    lines: List[str] = []
    lines.append(f"{inst['name']} - {inst['full_name']}")
    prompt = inst.get("prompt", {}).get(language) or inst.get("prompt", {}).get("en", "")
    if prompt:
        lines.append(prompt)
    lines.append("")
    for item in inst["items"]:
        text = item["text"].get(language) or item["text"]["en"]
        lines.append(f"{item['id']}. {text}")
        for opt in get_item_options(inst, item, language):
            lines.append(f"     [{opt['value']}] {opt['label']}")
        lines.append("")
    lo, hi = inst["score_range"]
    lines.append(f"Total score range: {lo}-{hi}")
    return "\n".join(lines).rstrip() + "\n"
