#!/usr/bin/env python3
"""Checks the civicactiontoolbox.org splash page against its spec (spec.md).

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

# The signup button opens the beta waitlist Google Form in a new tab.
btn = re.search(r'<a[^>]+href="' + re.escape(GFORM_URL) + r'"[^>]*>', html_src)
check(
    "Waitlist button links to the Google Form",
    btn is not None
    and "waitlist-cta" in btn.group(0)
    and 'target="_blank"' in btn.group(0)
    and 'rel="noopener"' in btn.group(0),
    f"found: {btn.group(0) if btn else 'none'}",
)

# GitHub Pages serves the custom domain from this file — exact content matters.
check(
    "CNAME is exactly civicactiontoolbox.org",
    (ROOT / "CNAME").read_text().strip() == "civicactiontoolbox.org",
)

# Design-system blue only (see ~/projects/design-system/colors/palette.html).
check(
    "Brand blue #2982C4 used, off-brand blue absent",
    ("2982C4" in css_src.upper() or "41, 130, 196" in css_src)
    and "45, 128, 195" not in css_src + html_src,
)

# Product is named "Civic Action Toolbox" — never "Builder".
check(
    'Named "Toolbox", no "Builder"',
    "Civic Action Toolbox" in html_src and "Builder" not in html_src,
)

# Cross-links to the Lab and Planet Detroit.
check(
    "Links to civiclab and planetdetroit.org",
    "civiclab.planetdetroit.org" in html_src
    and 'href="https://planetdetroit.org' in html_src,
)


class TagBalance(HTMLParser):
    def __init__(self):
        super().__init__()
        self.counts = {}

    def handle_starttag(self, tag, attrs):
        if tag in ("div", "section", "a", "p"):
            self.counts[tag] = self.counts.get(tag, 0) + 1

    def handle_endtag(self, tag):
        if tag in ("div", "section", "a", "p"):
            self.counts[tag] = self.counts.get(tag, 0) - 1


parser = TagBalance()
parser.feed(html_src)
unbalanced = {t: n for t, n in parser.counts.items() if n != 0}
check("div/section/a/p tags balanced", not unbalanced, str(unbalanced))

print()
if failures:
    print(f"{len(failures)} check(s) failed")
    sys.exit(1)
print("All checks passed")
