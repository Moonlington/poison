#!/usr/bin/env python3
"""WCAG contrast check for the Poison theme colour parameters.

The theme takes free-form hex values, so nothing stops a palette from shipping
link or body text that fails contrast. Run this after changing any colour param.

    python3 scripts/contrast.py            # checks the pairs below
    python3 scripts/contrast.py --fg #d81a1a --bg #faf9f6

Exit code 1 if any pair fails the 4.5:1 threshold for normal text.
"""
from __future__ import annotations

import argparse
import sys

AA_NORMAL = 4.5
AA_LARGE = 3.0


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))

    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def ratio(fg: str, bg: str) -> float:
    l1, l2 = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


# (label, foreground param, background param)
PAIRS = [
    ("light  text_color        on content_bg_color", "#222222", "#FAF9F6"),
    ("light  link_color        on content_bg_color", "#d81a1a", "#FAF9F6"),
    ("light  list_color        on content_bg_color", "#5a5a5a", "#FAF9F6"),
    ("light  date_color        on content_bg_color", "#515151", "#FAF9F6"),
    ("dark   text_color_dark   on content_bg_color_dark", "#eeeeee", "#121212"),
    ("dark   link_color_dark   on content_bg_color_dark", "#f42020", "#121212"),
    ("dark   list_color_dark   on content_bg_color_dark", "#9d9d9d", "#121212"),
    ("dark   date_color_dark   on content_bg_color_dark", "#9a9a9a", "#121212"),
    ("sidebar_p_color          on sidebar_bg_color", "#909090", "#202020"),
    ("sidebar_a_color          on sidebar_bg_color", "#FFFFFF", "#202020"),
    ("code_color_dark          on code_background_color_dark", "#ff8b8b", "#393D47"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fg")
    ap.add_argument("--bg")
    args = ap.parse_args()

    if args.fg and args.bg:
        r = ratio(args.fg, args.bg)
        verdict = "pass" if r >= AA_NORMAL else "FAIL (needs 4.5:1 for body text)"
        print(f"{args.fg} on {args.bg}: {r:.2f}:1 — {verdict}")
        return 0 if r >= AA_NORMAL else 1

    failed = 0
    print(f"{'pair':58} {'ratio':>7}  verdict")
    for label, fg, bg in PAIRS:
        r = ratio(fg, bg)
        ok = r >= AA_NORMAL
        failed += 0 if ok else 1
        verdict = "AA" if ok else ("AA-large only" if r >= AA_LARGE else "FAIL")
        print(f"{label:58} {r:6.2f}:1  {verdict}")
    print()
    if failed:
        print(f"{failed} pair(s) below {AA_NORMAL}:1 — pick a darker foreground for light mode, "
              "a lighter one for dark mode, or raise the background contrast.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
