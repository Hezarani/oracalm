"""Command-line interface for OraCalm.

Examples
--------
    oracalm list
    oracalm show mdas --lang tr
    oracalm score mdas 3 3 4 2 5
    oracalm score corah_das 1,2,3,2
"""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .core import score, render_form
from .instruments import list_instruments, get_instrument


def _parse_responses(tokens):
    """Accept space- or comma-separated integers."""
    joined = " ".join(tokens).replace(",", " ")
    parts = [p for p in joined.split() if p != ""]
    try:
        return [int(p) for p in parts]
    except ValueError:
        raise SystemExit("error: responses must be integers, e.g. 'score mdas 3 3 4 2 5'")


def _cmd_list(_args):
    print("Available instruments:\n")
    for meta in list_instruments():
        lo, hi = meta["score_range"]
        langs = ", ".join(meta["languages"])
        print(f"  {meta['id']:<10} {meta['full_name']}")
        print(f"             population: {meta['population']}, items: {meta['n_items']}, "
              f"range: {lo}-{hi}, languages: {langs}")
    print("\nDisclaimer: educational / research aid, not a diagnostic device.")


def _cmd_show(args):
    print(render_form(args.instrument, language=args.lang))


def _cmd_score(args):
    responses = _parse_responses(args.responses)
    result = score(args.instrument, responses, language=args.lang)
    inst = get_instrument(args.instrument)
    print(f"{result.full_name} ({result.instrument_name})")
    print(f"  Total: {result.total} / {result.max_total}  (range {result.min_total}-{result.max_total})")
    print(f"  Band:  {result.band_label}")
    print(f"  Note:  {result.band_description}")
    if result.flags:
        print("  Flags:")
        for f in result.flags:
            print(f"    - {f}")
    cite = inst["citation"]
    ref = f"{cite['authors']} ({cite['year']}). {cite['title']}. {cite['journal']}."
    print(f"  Source: {ref}")
    print("  Disclaimer: screening aid only; not a diagnosis.")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="oracalm",
        description="Score validated dental-anxiety instruments (MDAS, Corah DAS, MCDASf).",
    )
    parser.add_argument("--version", action="version", version=f"oracalm {__version__}")
    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list", help="list available instruments")
    p_list.set_defaults(func=_cmd_list)

    p_show = sub.add_parser("show", help="print an instrument's items and options")
    p_show.add_argument("instrument", help="instrument id (e.g. mdas)")
    p_show.add_argument("--lang", default="en", help="language code (default: en)")
    p_show.set_defaults(func=_cmd_show)

    p_score = sub.add_parser("score", help="score a set of responses")
    p_score.add_argument("instrument", help="instrument id (e.g. mdas)")
    p_score.add_argument("responses", nargs="+", help="one integer per item")
    p_score.add_argument("--lang", default="en", help="language code (default: en)")
    p_score.set_defaults(func=_cmd_score)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    try:
        args.func(args)
    except (KeyError, ValueError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
