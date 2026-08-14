# Spec: Civic Action Toolbox splash page

**Date:** 2026-08-14
**Status:** Built

## Purpose

A one-screen splash page at **civicactiontoolbox.org** (domain purchased 2026-08-14) that introduces the Civic Action Toolbox and sends visitors to the beta waitlist signup form. This is the product's own front door — distinct from civiclab.planetdetroit.org, which covers the whole Civic Action Lab.

## Users

Newsroom editors and publishers who hear about the Toolbox (conferences, LION/INN, word of mouth) and type in or click the product URL.

## User workflow

1. Visitor lands on civicactiontoolbox.org.
2. They see the product name, what it does in one sentence, and a sample of what a civic action box looks like.
3. They click **Join the beta waitlist**, which opens the Google Form ("Civic Action Toolbox — Beta Waitlist") in a new tab.
4. Secondary links lead to the Civic Action Lab site and planetdetroit.org.

## Requirements

- Single static HTML page + CSS, no build step (same pattern as civic-action-lab).
- Planet Detroit design system: accent blue #2982C4 for the signup button (orange is reserved for donation asks), dark background #333333, sans-serif headlines, Georgia body.
- Waitlist button opens the Google Form in a new tab and logs a GA `waitlist_click` event.
- CNAME file for civicactiontoolbox.org; hosted on GitHub Pages from `Planet-Detroit/civic-action-toolbox`.
- Consistent naming: "Civic Action Toolbox" everywhere, never "Builder".

## Acceptance criteria

- [x] Page links to the beta waitlist Google Form (new tab, noopener).
- [x] CNAME file contains exactly `civicactiontoolbox.org`.
- [x] Brand blue #2982C4 is used; the old off-brand blue rgb(45,128,195) is not.
- [x] "Builder" does not appear on the page.
- [x] Links to civiclab.planetdetroit.org and planetdetroit.org present.
- [x] HTML tags balanced (automated check).

## Out of scope

- Multi-page site, pricing page, product screenshots (nothing shippable exists yet to screenshot).
- Its own OG share image (follow-up; page ships without one).
- Separate GA property — reuses the Civic Action Lab GA tag for now; traffic is distinguishable by hostname in GA reports.

## Connects to

- Google Form: Civic Action Toolbox — Beta Waitlist (signups live in the form's Responses tab).
- civiclab.planetdetroit.org (the Lab's landing page, same waitlist form).
- Planet Detroit design system (`~/projects/design-system`).

## Known risks

- The domain won't show the page until DNS records are set at the registrar (instructions in README).
- Naming: if "Toolbox" changes again, the domain itself is the hard-to-change part.

## Success metric

Waitlist signups attributable to the product URL (GA `waitlist_click` events with hostname civicactiontoolbox.org).
