# Verakore Change Management Record — Mobile Menu Remediation (Website)

## Administrative
- Change ID: CM-2025-09-22-MM
- Request Date: 2025-09-22
- Category: Emergency Change
- Requester: Raul Rosa (Client)
- Change Owner: Verakore Web Ops
- Systems/Assets: Public marketing site (`index.html`, `services.html`, `partnerships.html`, `careers.html`)
- Repository/Path: `github/verakore-prod`

## 1. Purpose
Improve mobile navigation usability and accessibility on the public website. Fix visibility/contrast issues, inconsistent link targets, and unreliable mobile menu behavior (overlay, close-on-click, body scroll lock). Reduce bounce and prevent user confusion on small screens.

## 2. Scope
- Pages: `index.html`, `services.html`, `partnerships.html`, `careers.html`
- In-scope elements: Mobile navbar menu (Home, Services, About, Contact), hamburger toggler visibility, menu overlay behavior. No content or backend changes.

## 3. Change Description
Implemented consistent mobile menu patterns across all pages:
- Standardized link targets for `Home`, `Services`, `About`, `Contact` between pages.
- Added solid white overlay panel for the expanded mobile menu with increased z-index and touch targets.
- Improved `.nav-link` active/focus styles for contrast and selection clarity.
- Darkened hamburger icon on iOS Safari via `.navbar-light .navbar-toggler-icon { filter: invert(.5); opacity:.9; }`.
- Close-on-click: tapping a menu item collapses the menu.
- Scroll lock: body scrolling disabled while the menu is open.
- Homepage only: hid oversized hero illustration on phones to remove distracting empty box.

## 4. Files Modified
- `github/verakore-prod/index.html`
  - CSS: mobile overlay styles, active/focus states, darker toggler icon, hero illustration hide class.
  - HTML: added `hero-illustration` class to hero image column; standardized nav items; set `Home` as active.
  - JS: close-on-click + scroll lock listeners.
- `github/verakore-prod/services.html`
  - CSS: mobile overlay styles.
  - HTML: standardized nav targets.
  - JS: close-on-click + scroll lock listeners.
- `github/verakore-prod/partnerships.html`
  - CSS: mobile overlay styles.
  - HTML: standardized nav targets.
  - JS: close-on-click + scroll lock listeners.
- `github/verakore-prod/careers.html`
  - CSS: mobile overlay styles.
  - HTML: standardized nav targets.
  - JS: close-on-click + scroll lock listeners.

## 5. Risk/Impact Assessment
- User impact: Positive; clearer mobile navigation and predictable behavior.
- Technical risk: Low. Front-end only, no dependencies or backend services.
- Reversion complexity: Low (single-commit revert).
- Security: No change to authentication, data, or headers.

## 6. Rollback Plan
- Git: Revert the commit associated with Change ID `CM-2025-09-22-MM` to restore prior versions of the four files listed above.
- Cache: Invalidate CDN/browser cache if needed to restore prior behavior.

## 7. Implementation Plan (Steps Executed)
1) Add mobile overlay CSS to all pages (`.navbar-collapse{position:absolute;top:100%;left:0;right:0;background:#fff;box-shadow:...;padding:...;z-index:1100}`), enlarge link touch targets, and stronger active/focus styles.
2) Darken hamburger icon for iOS visibility: `.navbar-light .navbar-toggler-icon{filter:invert(.5);opacity:.9}` and remove border.
3) Standardize nav targets across pages:
   - `index.html`: `#home`, `services.html#home`, `#about`, `#contact`.
   - Other pages: `index.html#home`, `services.html#home`, `index.html#about`, `index.html#contact`.
4) Add close-on-click + scroll lock JS: collapse menu on link click; lock body scroll on show; restore on hide.
5) Homepage: add `hero-illustration` class and hide on small screens.
6) Lint check: no linter errors after edits.

## 8. Validation Plan & Results
- Devices/Browsers: iOS Safari, Chrome/Android, Chrome/Edge desktop responsive tools.
- Checks:
  - Menu opens on tap with white panel and readable links: PASS
  - Active/focus state visible: PASS
  - Tapping a link closes the menu and navigates correctly: PASS
  - Page doesn't scroll while menu is open: PASS
  - Hero content not obscured by navbar; homepage hero illustration hidden on phones: PASS

## 9. Schedule
- Implementation: 2025-09-22, outside peak traffic hours.
- Maintenance window: Not required (front-end only), but executed promptly due to mobile usability concerns.

## 10. Approvals
- CAB (Internal): Lead Engineer, Operations Manager — Pending/Approved per emergency protocol
- Client Representative: Raul Rosa — Pending/Approved

## 11. Post-Implementation Notes
- Recommend purging CDN or instructing users to hard-refresh if stale mobile CSS persists.
- Next steps (optional): align typography scale and hero paddings across pages for further polish; optimize images for mobile.




