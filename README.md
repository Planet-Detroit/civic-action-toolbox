# Civic Action Toolbox — Splash Page

Splash site for **civicactiontoolbox.org**: five full-bleed sections (hero, product mock, how it works, stats, who's behind it) driving to the early-access Google Form. Implements the Claude Design handoff of 2026-08-14 — see `spec.md` for details.

## Tech

- Static HTML + CSS + a small script that scales the product mock, no build step
- Hosted on **GitHub Pages** from `Planet-Detroit/civic-action-toolbox`
- Custom domain via `CNAME` file
- **Toolbox brand** (cobalt/red/yellow/cream, Baloo 2 + DM Sans via Google Fonts) — deliberately distinct from the Planet Detroit design system; brand marks live in `assets/`
- GA4 tracking shares the Civic Action Lab property (`G-5QQJ9SVV07`) — filter by hostname `civicactiontoolbox.org` in GA reports; both CTAs log a `waitlist_click` event with their location (hero or closing card)

## See it work (`see-it-work/`)

Added Oct 17, 2026 (the "try it right away" decision): a real Planet Detroit story and the real box the Toolbox built for it, shown live through the app's hosted box page in an iframe — nothing copied, no sign-in, no AI call. The frame points at `app.civicactiontoolbox.org/box/showcase/planet-detroit`, which picks the freshest Planet Detroit box with the most still ahead of it on every load, so nobody keeps this page fresh. The home page's "See it work" button logs `see_it_work_click`; the demo page's form button logs `demo_waitlist_click`; the story link logs `demo_story_click`. In March the page gains "Paste your own article" (built in the app, not here).

## Signup form

The button opens the **"Civic Action Toolbox — Beta Waitlist"** Google Form in a new tab — the same form used on civiclab.planetdetroit.org. Responses live in the form's **Responses** tab in Google Forms.

## DNS setup (one-time, at the domain registrar)

For civicactiontoolbox.org to show this page, these records must exist wherever the domain's DNS is managed:

| Type | Host | Value |
|------|------|-------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | planet-detroit.github.io |

After the records propagate (minutes to a few hours), GitHub Pages will detect the domain and issue an HTTPS certificate automatically. Until then the page is reachable at https://planet-detroit.github.io/civic-action-toolbox/.

## Tests

`python3 tests/test_page.py` — checks the waitlist link, CNAME contents, brand colors, naming, and cross-links.

## Making changes

Edit `index.html` / `styles.css`, run the tests, commit, push to `main`. GitHub Pages redeploys automatically.
