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

# ---- See it work (see-it-work/index.html, Oct 17 2026) ----
# The home page offers "See it work" (its own GA event, not a waitlist
# CTA); the demo page shows a real published box through the Toolbox's own
# hosted page (an iframe by box key — never a copy), links the story, ends
# in the early-access form, and never mentions pilot partners or prices.
demo_src = (ROOT / "see-it-work" / "index.html").read_text()
check("Home page has a See it work button to the demo page",
      'href="see-it-work/"' in html_src and "see-it-cta" in html_src and "see_it_work_click" in html_src)
frame = re.search(r'<iframe[^>]+>', demo_src)
check("Demo page frames a published box by key", bool(frame)
      and re.search(r'src="https://app\.civicactiontoolbox\.org/box/box_[a-z0-9]+"', frame.group(0)) is not None
      and 'data-box="box_' in frame.group(0))
check("Demo page links the story on planetdetroit.org",
      'href="https://planetdetroit.org/' in demo_src and "demo-story-link" in demo_src)
check("Demo page ends in the early-access form with its own GA event",
      re.search(r'<a[^>]+href="' + re.escape(GFORM_URL) + r'"[^>]*waitlist-cta', demo_src) is not None
      and "demo_waitlist_click" in demo_src)
check("Demo page promises the March paste box and nothing more",
      "Paste your own story here in March" in demo_src)
# (The story's own dollar figure is fine; a price is "a month" or "per month".)
check("Demo page names no pilot partner or price",
      not re.search(r"Bridge Michigan|MinnPost|Sahan|per month|\$\d[\d,.]* (a|per) month", demo_src))
check("Demo frame grows to the box's height from the app's message only",
      "addEventListener('message'" in demo_src
      and "e.origin !== 'https://app.civicactiontoolbox.org'" in demo_src
      and "cat-box-height" in demo_src
      and 'loading="lazy"' not in demo_src)
demo_parser = TagBalance()
demo_parser.feed(demo_src)
demo_unbalanced = {t: n for t, n in demo_parser.counts.items() if n != 0}
check("Demo page tags balanced", not demo_unbalanced, str(demo_unbalanced))

print()
if failures:
    print(f"{len(failures)} check(s) failed")
    sys.exit(1)
print("All checks passed")
