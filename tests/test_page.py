#!/usr/bin/env python3
"""Checks the civicactiontoolbox.org splash page against its spec (spec.md),
which implements the Claude Design handoff of 2026-08-14.

Run with:  python3 tests/test_page.py
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GFORM_URL = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSe5XGSfHNzg9tgDWIGP4QKfFAFhV_vvY-Gl3NdPk4IQWWqSvQ/viewform"
)

failures = []


def check(name, condition, detail=""):
    if condition:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}  {detail}")
        failures.append(name)


html_src = (ROOT / "index.html").read_text()
css_src = (ROOT / "styles.css").read_text()

# Two CTAs (hero + closing card) open the early-access Google Form in a new
# tab, and both carry waitlist-cta so GA logs them.
btns = re.findall(r'<a[^>]+href="' + re.escape(GFORM_URL) + r'"[^>]*>', html_src)
check(
    "Two CTAs link to the Google Form",
    len(btns) == 2
    and all(
        "waitlist-cta" in b and 'target="_blank"' in b and 'rel="noopener"' in b
        for b in btns
    ),
    f"found {len(btns)}",
)

# GitHub Pages serves the custom domain from this file — exact content matters.
check(
    "CNAME is exactly civicactiontoolbox.org",
    (ROOT / "CNAME").read_text().strip() == "civicactiontoolbox.org",
)

# Toolbox brand tokens (cobalt/yellow/cream), not Planet Detroit's blue —
# the product has its own brand per the design handoff.
check(
    "Toolbox brand colors used, PD blue absent",
    all(c in css_src for c in ("#1B2FC4", "#FFD028", "#FFF3DC", "#C42D18"))
    and "2982C4" not in css_src.upper(),
)

# Handoff pairing rule: eyebrows on cobalt are periwinkle, never red.
check(
    "Cobalt-section eyebrow is periwinkle",
    ".eyebrow-on-cobalt { color: #A0A1D2; }" in css_src
    and 'class="eyebrow eyebrow-on-cobalt"' in html_src,
)

# Launch messaging matches the Google Form's "early 2027" (Nina's call,
# 2026-08-14 — the design handoff's "Fall 2026" was inconsistent with the form).
check(
    'Says early 2027, no fall/2026 launch copy',
    "Coming Early 2027" in html_src
    and "Fall 2026" not in html_src
    and "this fall" not in html_src,
)

# Product is named "Civic Action Toolbox" — never "Builder".
check(
    'Named "Toolbox", no "Builder"',
    "Civic Action Toolbox" in html_src and "Builder" not in html_src,
)

# Every referenced local asset exists on disk (broken image = broken page).
assets = re.findall(r'(?:src|href)="(assets/[^"]+)"', html_src)
missing = [a for a in set(assets) if not (ROOT / a).is_file()]
check("All referenced assets exist", assets and not missing, f"missing: {missing}")

# The product mock scales via the fixed-width transform (704px design width);
# without this script the mock overflows on small screens.
check(
    "Mock scale script present",
    "clientWidth / 704" in html_src and "transform-origin: top left" in css_src,
)

# The decorative mock must be hidden from screen readers, with a label on the
# wrapper instead.
check(
    "Mock is aria-hidden with labelled wrapper",
    'aria-hidden="true"' in html_src and 'aria-label="A civic action box' in html_src,
)


class TagBalance(HTMLParser):
    def __init__(self):
        super().__init__()
        self.counts = {}

    def handle_starttag(self, tag, attrs):
        if tag in ("div", "section", "a", "p", "span"):
            self.counts[tag] = self.counts.get(tag, 0) + 1

    def handle_endtag(self, tag):
        if tag in ("div", "section", "a", "p", "span"):
            self.counts[tag] = self.counts.get(tag, 0) - 1


parser = TagBalance()
parser.feed(html_src)
unbalanced = {t: n for t, n in parser.counts.items() if n != 0}
check("div/section/a/p/span tags balanced", not unbalanced, str(unbalanced))

print()
if failures:
    print(f"{len(failures)} check(s) failed")
    sys.exit(1)
print("All checks passed")
