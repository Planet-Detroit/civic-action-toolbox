# Civic Action Toolbox — Splash Page

One-screen splash site for **civicactiontoolbox.org**: what the Civic Action Toolbox is, an example action box, and a button to the beta waitlist Google Form. See `spec.md` for the full spec.

## Tech

- Static HTML + CSS, no build step (same pattern as civic-action-lab)
- Hosted on **GitHub Pages** from `Planet-Detroit/civic-action-toolbox`
- Custom domain via `CNAME` file
- Colors/type follow the Planet Detroit design system (`~/projects/design-system`)
- GA4 tracking shares the Civic Action Lab property (`G-5QQJ9SVV07`) — filter by hostname `civicactiontoolbox.org` in GA reports; the waitlist button logs a `waitlist_click` event with `link_location: splash`

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
