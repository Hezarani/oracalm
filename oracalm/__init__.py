"""OraCalm — open, dependency-free scoring for validated dental-anxiety instruments.

Supported instruments:
    * ``mdas``      Modified Dental Anxiety Scale (adults; EN/TR/FA)
    * ``corah_das`` Corah's Dental Anxiety Scale (adults; EN)
    * ``mcdasf``    Modified Child Dental Anxiety Scale, faces version (children; EN)

Quick start::

    import oracalm
    result = oracalm.score("mdas", [3, 3, 4, 2, 5])
    print(result.total, result.band_label)

This is an educational / research aid, not a diagnostic device.
"""

from .core import score, interpret, render_form, ScoreResult
from .instruments import INSTRUMENTS, list_instruments, get_instrument

__version__ = "0.1.0"

__all__ = [
    "score",
    "interpret",
    "render_form",
    "ScoreResult",
    "INSTRUMENTS",
    "list_instruments",
    "get_instrument",
    "__version__",
]
