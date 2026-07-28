"""Validated dental-anxiety instrument definitions for OraCalm.

Each instrument encodes only *facts*: the item stems, the response scale, the
total-score range, interpretation bands, validated cut-offs, and a full source
citation. Scoring keys and cut-offs are not copyrightable; item wording is
reproduced from the published instruments with attribution (see ``provenance``).

Provenance / reuse notes per instrument:

* **MDAS** — Humphris, Morrison & Lindsay (1995). The authors make the MDAS
  *freely available for use* provided the source is cited (see the official
  MDAS site hosted at the University of St Andrews). English is the canonical
  wording; Turkish and Persian strings here are provided for convenience and
  should be checked against the officially validated Turkish (Tunç et al.) and
  Persian versions before clinical use.
* **Corah DAS** — Corah (1969). A classic, widely reproduced 4-item scale.
* **MCDASf** — Howard & Freeman (2007), faces version of the Modified Child
  Dental Anxiety Scale (Wong et al. 1998).

This library is an educational / research aid and is **not** a diagnostic
device. Interpretation bands support screening only; clinical judgement and the
original instruments' manuals take precedence.
"""

from __future__ import annotations

# --- Modified Dental Anxiety Scale (MDAS) -----------------------------------

_MDAS_SCALE = {
    "en": [
        {"value": 1, "label": "Not anxious"},
        {"value": 2, "label": "Slightly anxious"},
        {"value": 3, "label": "Fairly anxious"},
        {"value": 4, "label": "Very anxious"},
        {"value": 5, "label": "Extremely anxious"},
    ],
    "tr": [
        {"value": 1, "label": "Kaygılı değilim"},
        {"value": 2, "label": "Biraz kaygılıyım"},
        {"value": 3, "label": "Oldukça kaygılıyım"},
        {"value": 4, "label": "Çok kaygılıyım"},
        {"value": 5, "label": "Aşırı derecede kaygılıyım"},
    ],
    "fa": [
        {"value": 1, "label": "نگران نیستم"},
        {"value": 2, "label": "کمی نگرانم"},
        {"value": 3, "label": "نسبتاً نگرانم"},
        {"value": 4, "label": "خیلی نگرانم"},
        {"value": 5, "label": "بی‌نهایت نگرانم"},
    ],
}

_MDAS = {
    "id": "mdas",
    "name": "MDAS",
    "full_name": "Modified Dental Anxiety Scale",
    "population": "adult",
    "age_range": "adults",
    "languages": ["en", "tr", "fa"],
    "prompt": {
        "en": "Please indicate how anxious you would feel in each situation.",
        "tr": "Lütfen her durumda ne kadar kaygılı hissedeceğinizi belirtin.",
        "fa": "لطفاً مشخص کنید در هر موقعیت چقدر احساس نگرانی می‌کنید.",
    },
    "scale": _MDAS_SCALE,
    "items": [
        {"id": 1, "text": {
            "en": "If you went to your dentist for treatment tomorrow, how would you feel?",
            "tr": "Yarın diş tedavisi için diş hekiminize gitseniz, kendinizi nasıl hissederdiniz?",
            "fa": "اگر فردا برای درمان به دندان‌پزشک مراجعه کنید، چه احساسی خواهید داشت؟",
        }},
        {"id": 2, "text": {
            "en": "If you were sitting in the waiting room (waiting for treatment), how would you feel?",
            "tr": "Bekleme odasında (tedavi için beklerken) otururken kendinizi nasıl hissederdiniz?",
            "fa": "اگر در اتاق انتظار (در حال انتظار برای درمان) نشسته باشید، چه احساسی خواهید داشت؟",
        }},
        {"id": 3, "text": {
            "en": "If you were about to have a tooth drilled, how would you feel?",
            "tr": "Dişiniz oyulmak (frezelenmek) üzereyken kendinizi nasıl hissederdiniz?",
            "fa": "اگر قرار باشد دندانتان تراش داده شود، چه احساسی خواهید داشت؟",
        }},
        {"id": 4, "text": {
            "en": "If you were about to have your teeth scaled and polished, how would you feel?",
            "tr": "Diş taşlarınız temizlenip cilalanmak üzereyken kendinizi nasıl hissederdiniz?",
            "fa": "اگر قرار باشد دندان‌هایتان جرم‌گیری و پولیش شوند، چه احساسی خواهید داشت؟",
        }},
        {"id": 5, "text": {
            "en": "If you were about to have a local anaesthetic injection in your gum, above an upper back tooth, how would you feel?",
            "tr": "Üst arka dişinizin üzerindeki diş etine lokal anestezi iğnesi yapılmak üzereyken kendinizi nasıl hissederdiniz?",
            "fa": "اگر قرار باشد به لثه‌ی بالای دندان عقب فک بالا به شما آمپول بی‌حسی موضعی تزریق شود، چه احساسی خواهید داشت؟",
        }},
    ],
    "score_range": [5, 25],
    "bands": [
        {"min": 5, "max": 9, "label": "Low dental anxiety",
         "description": "Little or no dental anxiety indicated."},
        {"min": 10, "max": 18, "label": "Moderate dental anxiety",
         "description": "Some dental anxiety; below the validated high-anxiety cut-off."},
        {"min": 19, "max": 25, "label": "High dental anxiety (possible dental phobia)",
         "description": "At or above the validated MDAS cut-off (>=19): strong likelihood of dental phobia; consider anxiety-management support."},
    ],
    "bands_note": "Only the >=19 cut-off is formally validated (Humphris et al. 1995). The lower two bands are descriptive aids, not validated categories.",
    "cutoffs": [
        {"threshold": 19, "operator": ">=", "label": "High dental anxiety / possible dental phobia"},
    ],
    "citation": {
        "authors": "Humphris GM, Morrison T, Lindsay SJE",
        "title": "The Modified Dental Anxiety Scale: validation and United Kingdom norms",
        "journal": "Community Dental Health",
        "year": 1995,
        "volume": "12(3)",
        "pages": "143-150",
        "pmid": "7584581",
    },
    "provenance": "MDAS is made freely available for use by the authors provided the source is cited (official MDAS site, University of St Andrews). English wording is canonical; TR/FA strings are convenience translations pending verification against the validated versions.",
}

# --- Corah's Dental Anxiety Scale (DAS) -------------------------------------

_CORAH_RELAXED_SCALE = [
    {"value": 1, "label": "Relaxed"},
    {"value": 2, "label": "A little uneasy"},
    {"value": 3, "label": "Tense"},
    {"value": 4, "label": "Anxious"},
    {"value": 5, "label": "So anxious that I sometimes break out in a sweat or almost feel physically sick"},
]

_CORAH = {
    "id": "corah_das",
    "name": "Corah DAS",
    "full_name": "Corah's Dental Anxiety Scale",
    "population": "adult",
    "age_range": "adults",
    "languages": ["en"],
    "prompt": {"en": "Choose the answer that best describes how you would feel in each situation."},
    "scale": None,  # per-item options
    "items": [
        {"id": 1, "text": {"en": "If you had to go to the dentist tomorrow, how would you feel about it?"},
         "options": {"en": [
             {"value": 1, "label": "I would look forward to it as a reasonably enjoyable experience"},
             {"value": 2, "label": "I wouldn't care one way or the other"},
             {"value": 3, "label": "I would be a little uneasy about it"},
             {"value": 4, "label": "I would be afraid that it would be unpleasant and painful"},
             {"value": 5, "label": "I would be very frightened of what the dentist might do"},
         ]}},
        {"id": 2, "text": {"en": "When you are waiting in the dentist's office for your turn in the chair, how do you feel?"},
         "options": {"en": _CORAH_RELAXED_SCALE}},
        {"id": 3, "text": {"en": "When you are in the dentist's chair waiting while the dentist gets the drill ready to begin working on your teeth, how do you feel?"},
         "options": {"en": _CORAH_RELAXED_SCALE}},
        {"id": 4, "text": {"en": "You are in the dentist's chair to have your teeth cleaned. While you are waiting and the dentist is getting out the instruments which will be used to scrape your teeth around the gums, how do you feel?"},
         "options": {"en": _CORAH_RELAXED_SCALE}},
    ],
    "score_range": [4, 20],
    "bands": [
        {"min": 4, "max": 8, "label": "Low / minimal anxiety",
         "description": "Little dental anxiety indicated."},
        {"min": 9, "max": 12, "label": "Moderate anxiety",
         "description": "Moderate dental anxiety."},
        {"min": 13, "max": 14, "label": "High anxiety",
         "description": "High dental anxiety; some references flag scores >=13 as clinically significant."},
        {"min": 15, "max": 20, "label": "Severe anxiety (possible dental phobia)",
         "description": "Severe dental anxiety; a score >=15 is a commonly cited threshold for dental phobia."},
    ],
    "bands_note": "Cut-offs vary across the literature; >=13 (clinically anxious) and >=15 (severe/phobic) are the most commonly cited thresholds.",
    "cutoffs": [
        {"threshold": 13, "operator": ">=", "label": "Clinically significant anxiety (per some references)"},
        {"threshold": 15, "operator": ">=", "label": "Severe anxiety / possible dental phobia"},
    ],
    "citation": {
        "authors": "Corah NL",
        "title": "Development of a dental anxiety scale",
        "journal": "Journal of Dental Research",
        "year": 1969,
        "volume": "48(4)",
        "pages": "596",
        "doi": "10.1177/00220345690480041801",
    },
    "provenance": "Corah's DAS (1969) is a classic, widely reproduced 4-item scale. English wording only in this release.",
}

# --- Modified Child Dental Anxiety Scale, faces version (MCDASf) -------------

_MCDASF_SCALE = {
    "en": [
        {"value": 1, "label": "Relaxed / not worried"},
        {"value": 2, "label": "Very slightly worried"},
        {"value": 3, "label": "Fairly worried"},
        {"value": 4, "label": "Worried a lot"},
        {"value": 5, "label": "Very worried"},
    ],
}

_MCDASF = {
    "id": "mcdasf",
    "name": "MCDASf",
    "full_name": "Modified Child Dental Anxiety Scale (faces version)",
    "population": "child",
    "age_range": "children ~8-15 years",
    "languages": ["en"],
    "prompt": {"en": "Show how you feel about each of these things using the faces (1 = relaxed/not worried, 5 = very worried)."},
    "scale": _MCDASF_SCALE,
    "items": [
        {"id": 1, "text": {"en": "Going to the dentist"}},
        {"id": 2, "text": {"en": "Having your teeth looked at"}},
        {"id": 3, "text": {"en": "Having your teeth scraped and polished"}},
        {"id": 4, "text": {"en": "Having an injection in the gum"}},
        {"id": 5, "text": {"en": "Having a filling"}},
        {"id": 6, "text": {"en": "Having a tooth taken out"}},
        {"id": 7, "text": {"en": "Being put to sleep to have treatment"}},
        {"id": 8, "text": {"en": "Having a mixture of 'gas and air' which will help you feel comfortable for treatment but cannot put you to sleep"}},
    ],
    "score_range": [8, 40],
    "bands": [
        {"min": 8, "max": 18, "label": "Low anxiety",
         "description": "Little dental anxiety indicated."},
        {"min": 19, "max": 30, "label": "Moderate anxiety",
         "description": "Moderate dental anxiety (around/above the reported normative mean ~19.8)."},
        {"min": 31, "max": 40, "label": "High anxiety",
         "description": "High dental anxiety; consider child-focused anxiety-management support."},
    ],
    "bands_note": "There is no single universally agreed MCDASf cut-off. Higher totals indicate greater anxiety (normative mean ~19.8; Howard & Freeman 2007). Bands here are descriptive; interpret with clinical judgement and consider item-level responses (e.g. injection, extraction).",
    "cutoffs": [],
    "citation": {
        "authors": "Howard KE, Freeman R",
        "title": "Reliability and validity of a faces version of the Modified Child Dental Anxiety Scale",
        "journal": "International Journal of Paediatric Dentistry",
        "year": 2007,
        "volume": "17(4)",
        "pages": "281-288",
        "doi": "10.1111/j.1365-263X.2007.00830.x",
    },
    "provenance": "Faces version (Howard & Freeman 2007) of the Modified Child Dental Anxiety Scale (Wong, Humphris & Lee 1998). English wording only in this release.",
}


INSTRUMENTS = {
    "mdas": _MDAS,
    "corah_das": _CORAH,
    "mcdasf": _MCDASF,
}

# Convenience aliases users may type.
ALIASES = {
    "das": "corah_das",
    "corah": "corah_das",
    "mcdas": "mcdasf",
    "mcdas-f": "mcdasf",
    "mcdasf": "mcdasf",
}


def list_instruments():
    """Return lightweight metadata for every instrument."""
    out = []
    for inst in INSTRUMENTS.values():
        out.append({
            "id": inst["id"],
            "name": inst["name"],
            "full_name": inst["full_name"],
            "population": inst["population"],
            "n_items": len(inst["items"]),
            "score_range": inst["score_range"],
            "languages": inst["languages"],
        })
    return out


def get_instrument(instrument_id):
    """Return the full instrument dict, accepting ids and common aliases."""
    if not isinstance(instrument_id, str):
        raise TypeError("instrument_id must be a string")
    key = instrument_id.strip().lower().replace(" ", "_")
    key = ALIASES.get(key, key)
    if key not in INSTRUMENTS:
        valid = ", ".join(sorted(INSTRUMENTS))
        raise KeyError(f"Unknown instrument '{instrument_id}'. Valid ids: {valid}.")
    return INSTRUMENTS[key]


def get_item_options(instrument, item, language="en"):
    """Return the list of {value, label} options that apply to an item."""
    if "options" in item:
        opts = item["options"]
    elif instrument.get("scale"):
        opts = instrument["scale"]
    else:
        raise ValueError(f"Instrument '{instrument['id']}' item {item['id']} has no options.")
    if language in opts:
        return opts[language]
    return opts["en"]  # fall back to canonical English options


def allowed_values(instrument, item):
    """The set of valid integer responses for an item (language-independent)."""
    return {opt["value"] for opt in get_item_options(instrument, item, "en")}
