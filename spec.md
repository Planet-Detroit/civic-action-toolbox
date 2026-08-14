# Spec: Civic Action Toolbox splash page

**Date:** 2026-08-14 (v2 — rebuilt from the Claude Design handoff, replacing the v1 one-screen page)
**Status:** Built

## Purpose

A single-page marketing splash at **civicactiontoolbox.org** whose one job is getting newsroom editors/publishers (and funders reading over their shoulder) to click through to the early-access Google Form. Launch messaging: **"Coming Fall 2026."**

## Design source

`~/Downloads/design_handoff_splash_page/` — a high-fidelity Claude Design handoff (README + `Splash Page.dc.html` + brand assets). The page recreates it pixel-accurately in this repo's static HTML + CSS setup. The Toolbox has its own brand, distinct from Planet Detroit's: cobalt `#1B2FC4`, brick red `#C42D18`, yellow `#FFD028`, cream `#FFF3DC`; display font Baloo 2 (800), body DM Sans (Google Fonts). No borders, shadows, or gradients.

## Page structure (five sections + footer)

1. **Hero (cobalt)** — logo lockup (icon + two-color HTML wordmark), "Coming Fall 2026", H1 "Readers don't lack outrage. They lack the phone number.", yellow pill CTA "Join the early access list".
2. **The product (cream)** — copy + a decorative hand-built mock of an action box beside a story, authored at 704px and scaled to fit via JS transform (never reflowed).
3. **How it works (cream)** — three white cards: Paste your story / Edit and embed / Count what happens.
4. **Stats (yellow)** — "$0 Free for newsrooms" and "10min from paste to published".
5. **Who's behind it (cobalt)** — Planet Detroit + Reynolds Journalism Institute fellowship, hello@civicactiontoolbox.org, white "Want in on the pilot?" card with second CTA.
6. **Footer (red)** — icon + civicactiontoolbox.org.

## Acceptance criteria

- [x] Both CTAs (hero + closing card) open the beta waitlist Google Form in a new tab and log GA `waitlist_click` with their location.
- [x] CNAME file contains exactly `civicactiontoolbox.org`.
- [x] Toolbox brand tokens used; Planet Detroit blue absent; eyebrows on cobalt are periwinkle (never red).
- [x] "Coming Fall 2026" messaging present.
- [x] "Civic Action Toolbox" naming, never "Builder".
- [x] All referenced assets exist; product mock scales via the 704px transform and is `aria-hidden` with a labelled wrapper.

## Out of scope

- OG share image (follow-up — could be exported from the design).
- Separate GA property — shares the Civic Action Lab tag; filter by hostname.
- Making the product mock a live interactive demo.

## Connects to

- Google Form: Civic Action Toolbox — Beta Waitlist (responses in Google Forms).
- Toolbox brand assets in `assets/` (from the Claude Design design system).
- GitHub Pages (`Planet-Detroit/civic-action-toolbox`) + GoDaddy/Kinsta DNS.

## Known risks / open items

- **Copy conflict:** page says "Coming Fall 2026" (per approved design) but the Google Form description still says "beta testing in early 2027", and civiclab.planetdetroit.org also says early 2027. One of them is wrong — Nina to decide which date is real; form/civiclab copy may need updating.
- **hello@civicactiontoolbox.org** appears on the page but the mailbox/forwarding must be set up at the domain/email provider or mail to it bounces.
- Domain shows the page only after DNS is pointed (GoDaddy or Kinsta DNS; records in README).

## Success metric

Waitlist signups attributable to the product URL (GA `waitlist_click` events with hostname civicactiontoolbox.org).
