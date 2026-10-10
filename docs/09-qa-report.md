# 09 · Visual and technical QA report

**Date:** 9 October 2026.
**Scope:** the live site at commit `cf22a2d` (final homepage), plus local regression tests of the fixes in this report.
**Status of fixes:** applied in the local repository only; not committed, not pushed, not deployed.

## How it was tested

| Area | Tool | Where |
|---|---|---|
| Lighthouse | Lighthouse 13.5.0 through PageSpeed Insights (Moto G Power on Slow 4G for mobile; desktop profile) | Live site |
| Automated accessibility | axe-core 4.10.2, tags wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa and best-practice, injected into each page | Live site, 11 pages |
| Visual and responsive checks | Playwright with Chromium at 375, 768, 1024 and 1440 px, with full-page screenshots and scripted checks for overflow, images, target sizes, text size and console errors | Local server (`python3 -m http.server`) on the same code |
| Manual accessibility | Playwright keyboard tests (Tab, Enter, Escape), reduced-motion emulation, JavaScript disabled, script.js blocked, scripted contrast calculation, plus review of the screenshots | Local |
| Technical SEO | Scripted checks of all 113 HTML files, plus live HTTP checks for redirects, headers, `robots.txt`, `sitemap.xml` and 404 | Local and live |
| Functional checks | Playwright (navigation, dropdowns, contact form against a **mocked** Formspree endpoint, resource dialog, Capability Readiness Review scoring) and live checks of PDF and toolkit endpoints | Local and live |

**Limitations:**
- No Chrome UX Report field data exists for the site ("No Data" in PageSpeed Insights), so there are no field LCP, CLS or INP values. Total Blocking Time is the only interaction metric available.
- No screen-reader, Safari, Firefox or real-device testing was done.
- The contact form was not submitted to the live endpoint.
- In the local browser tests Fontshare was blocked by the test environment, so fonts fell back to system fonts and some "failed to load resource" console messages came from that. They are not site defects.

## 1. Lighthouse (live, measured)

| Page | Device | Perf. | Access. | Best pr. | SEO | FCP | LCP | TBT | CLS | Speed Index |
|---|---|---|---|---|---|---|---|---|---|---|
| Home, run 1 | Mobile | 89 | 96 | 100 | 100 | 2.8 s | 2.8 s | 0 ms | 0 | 4.5 s |
| Home, run 2 | Mobile | 89 | 96 | 100 | 100 | 2.8 s | 2.8 s | 0 ms | 0 | 4.3 s |
| Home, run 1 | Desktop | 100 | 96 | 100 | 100 | 0.5 s | 0.5 s | 0 ms | 0.031 | 0.9 s |
| Home, run 2 | Desktop | 100 | 96 | 100 | 100 | 0.4 s | 0.5 s | 0 ms | 0.03 | 0.6 s |
| Contact | Mobile | 91 | 96 | 100 | 100 | 2.8 s | 2.8 s | 0 ms | 0 | 3.0 s |
| Contact | Desktop | 100 | 96 | 96 | 100 | 0.4 s | 0.4 s | 0 ms | 0 | 0.6 s |
| Capability Consulting | Mobile | 100 | 96 | 100 | 100 | 1.5 s | 1.5 s | 0 ms | 0 | 1.5 s |
| Capability Consulting | Desktop | 100 | 96 | 100 | 100 | 0.4 s | 0.4 s | 0 ms | 0.001 | 0.5 s |
| DS4D case study | Mobile | 91 | 96 | 100 | 100 | 2.8 s | 2.8 s | 0 ms | 0 | 3.0 s |
| DS4D case study | Desktop | 100 | 96 | 100 | 100 | 0.4 s | 0.7 s | 0 ms | 0.002 | 0.4 s |

**Reports:** [Home](https://pagespeed.web.dev/analysis/https-www-prelude-learning-com/dk4rluyji1), [Home, second run](https://pagespeed.web.dev/analysis/https-www-prelude-learning-com/1kgyu0jyh1), [Contact](https://pagespeed.web.dev/analysis/https-www-prelude-learning-com-contact-html/8snpr640i2), [Capability Consulting](https://pagespeed.web.dev/analysis/https-www-prelude-learning-com-capability-consulting/gijtb3g2r4), [DS4D](https://pagespeed.web.dev/analysis/https-www-prelude-learning-com-mod-digital-skills-for-defence-html/k0hsnbde4w).

**Why the scores are what they are:**
- **Accessibility 96 on every page.** One failure: "Links rely on colour to be distinguishable" (the footer sector links and the breadcrumbs). This is QA-01, fixed locally.
- **Homepage mobile performance 89:**
  - **Render-blocking requests (estimated saving 1,840 ms):**
    - Fontshare CSS, 780 ms;
    - `styles.css`, 330 ms.
  - **LCP element:** the hero text, not an image. LCP breakdown: time to first byte 0 ms, load delay 400 ms, load 300 ms, **element render delay 1,660 ms** (waiting for the stylesheet and fonts).
  - **Speed Index 4.3–4.5 s on the homepage only.** The hero background image (`prelude-landscape.jpg`, 98 KB) is loaded from CSS, so the browser finds it late.
  - **Critical chain:** HTML → Fontshare CSS → three Fontshare font files (26 KB each), with a maximum critical path of 937 ms. See QA-07.
- **Desktop CLS 0.03:** caused by the web fonts swapping in. This is well inside the 0.1 "good" threshold.
- **Contact, desktop Best Practices 96:** one console error, a request for `prelude-icon.svg` that timed out during that run. It did not occur in any other run and the file returns 200, so it is treated as a network blip, not a defect.
- **Variation between runs:** Capability Consulting scored 100 on mobile with an FCP of 1.5 s, while the homepage, contact and DS4D pages measured 2.8 s. The difference is mainly the homepage hero image and the speed of the Fontshare requests on each run. Single Lighthouse runs vary, so treat ±5 points as noise.

## 2. Accessibility

### 2a. Automated (axe-core 4.10.2, live)

| Page | Violations | Needs review |
|---|---|---|
| Home | none | colour contrast (6), link in text block (5): text over the hero image and the footer, which axe can't compute |
| Contact | link-in-text-block (5, serious) | none |
| Capability Consulting, Business Analysis, Workforce Development | link-in-text-block (7, serious): breadcrumbs and footer | none |
| Case studies, DS4D, Healthcare case study | link-in-text-block (6–7) | none |
| About, Training Needs Analysis | link-in-text-block (5) | none |
| Capability Readiness Review | link-in-text-block (5); heading-order (1, moderate) | none |

### 2b. Manual and scripted (local)

| Check | Result |
|---|---|
| Skip link | First Tab stop; moves focus to `#main`. **Pass.** |
| Visible focus | 2 px gold outline on links, buttons and fields via `:focus-visible`. **Pass.** |
| Desktop dropdowns by keyboard | Enter opens and sets `aria-expanded="true"`; Tab moves into the items; Escape closes and returns focus to the button. **Pass.** |
| Mobile and tablet menu, closed (375, 768, 1024 px) | **Fail before fix:** 7 of the first 12 Tab stops landed on invisible, off-screen menu links. **After fix:** 0. |
| Mobile menu, open | Before the fix, focus stayed on the burger and Tab could reach the page behind the overlay. **After fix:** focus moves to the first link, the page behind is `inert`, and focus cycles through the menu, the close button and the logo. Escape closes the menu and returns focus to the burger. |
| Reduced motion (`prefers-reduced-motion: reduce`) | 0 of 28 content blocks hidden, transitions 0 s. **Pass.** |
| JavaScript disabled | **Fail before fix:** 23 of 28 homepage blocks invisible. **After fix:** 0. |
| `script.js` blocked or failed | **Fail before fix:** 23 blocks stayed invisible. **After fix:** all visible within 3 s. |
| Text contrast on solid backgrounds (home, contact, Capability Consulting, case studies, DS4D) | No failures against 4.5:1 or 3:1. |
| Text over the hero image | Not computable automatically. Visual check: white and stone text on the dark masked image reads clearly. Pass by inspection. |
| Form labels | Every contact field has a visible `<label>`; optional fields are marked "(optional)". **Pass.** |
| Form errors | Empty submit is blocked, focus goes to the first invalid field, and native messages plus visible inline messages appear. Before the fix the inline messages were not linked to their fields; now each uses `aria-describedby`. |
| Target size (WCAG 2.5.8) | No failures. Breadcrumb links are 17 px tall but meet the spacing exception, and the email link is 20 px tall inside text. |

**WCAG 2.2 AA view:**
- **Failures found and fixed locally:**
  - 1.4.1 Use of Color (QA-01);
  - 2.4.3 Focus Order, 2.4.7 Focus Visible and 2.4.11 Focus Not Obscured, for the off-screen menu (QA-02).
- **Remaining:** 1.3.1 heading order on two pages (QA-08).
- **Not claimed:** formal conformance. That would need screen-reader testing, other browsers and testing of the full page set.

## 3. Visual QA

| Page | 375 px | 768 px | 1024 px | 1440 px |
|---|---|---|---|---|
| Home | 7,900 | 5,871 | 5,033 | 5,243 |
| Contact | 4,161 | 2,979 | 2,304 | 2,095 |
| Capability Consulting | 9,588 | 7,034 | 6,345 | 6,597 |
| Business Analysis & Improvement | 12,500 | 9,321 | 7,673 | 7,790 |
| Learning & Workforce Development | 8,651 | 6,392 | 5,528 | 5,713 |
| Case studies | 9,041 | 6,445 | 5,679 | 5,585 |
| DS4D case study | 5,618 | 4,223 | 3,952 | 3,739 |
| Healthcare case study | 5,148 | 4,060 | 3,620 | 3,576 |

The table gives page height in pixels.

**Results across all 32 page and width combinations:**
- no horizontal overflow;
- no broken images (one lazy-loaded image reported as not loaded during the automated scroll was confirmed to load);
- no upscaled images;
- one H1 per page;
- cards stack to one column at 375 px;
- the footer renders at all widths.

**Screenshots** (each image shows a page at 375, 768, 1024 and 1440 px, after the fixes):
- [homepage](qa-2026-10-09/homepage.jpg)
- [contact](qa-2026-10-09/contact.jpg)
- [Capability Consulting](qa-2026-10-09/capability-consulting.jpg)
- [Business Analysis](qa-2026-10-09/business-analysis.jpg)
- [Workforce Development](qa-2026-10-09/workforce-development.jpg)
- [case studies](qa-2026-10-09/case-studies.jpg)
- [DS4D](qa-2026-10-09/case-study-ds4d.jpg)
- [Healthcare](qa-2026-10-09/case-study-healthcare.jpg)

## 4. Technical SEO

| Check | Result |
|---|---|
| Title tags | 113 of 113 present, no duplicates. 70 are longer than 60 characters (backlog S5). |
| Meta descriptions | 113 of 113 present. 55 are longer than 160 characters (S5). |
| Canonical URLs | 113 of 113 present; all match the page URL on `www`. |
| Indexability | 110 indexable pages, all in the sitemap. The 3 `noindex` pages (404, thank-you, toolkit downloads) are not in it. |
| robots.txt (live) | 200; allows the site; disallows `/api/`, the toolkit downloads page and four email-gated PDFs; references the sitemap. |
| sitemap.xml (live) | 200, 110 URLs. |
| Redirects (live) | `/index.html` → `/` (301 from `vercel.json`) confirmed. |
| 404 (live) | Unknown URLs return 404 with the branded page. |
| Headings | One H1 on every page. Heading-level skips on CRR and Services. |
| Structured data | Every JSON-LD block parses. Lighthouse SEO 100. Not run through Google's Rich Results Test. |
| Open Graph and Twitter | Present on every page; the `og:image` file exists. |
| Internal links | 5,545 checked, none broken. The only unresolved targets are the two Vercel function routes, which work live. |
| Security headers (live) | `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, `Permissions-Policy` and HSTS (`max-age=63072000`) present. No Content-Security-Policy. |

## 5. Functional QA

| Function | Result |
|---|---|
| Main navigation and footer links | All resolve (internal link check). |
| Dropdowns | Mouse (hover), click and keyboard all work; Escape closes. |
| Service links (homepage problem cards, service cards, menus) | All resolve to the three pillar pages and the TNA and Learning Strategy pages. |
| Case-study links | DS4D and the owner-led example resolve. The owner-led link now targets the card directly (QA-05). |
| Resource downloads, live | All five PDFs return 200 `application/pdf` (615–905 KB). |
| Resource dialog, local with mocked Formspree | Opens and focuses the email field; shows an empty-field error; shows a server error on a mocked 500; after success, offers the download; the PDF downloads; Escape closes and returns focus. The ungated workbook downloads directly. Without JavaScript, the fallback email form shows. |
| Contact form, local with mocked Formspree | Empty submit is blocked. A valid submission posts `name`, `email`, `organisation`, `enquiry_type`, `timescale`, `message`, `_gotcha` and `_next`, and lands on `thank-you.html?from=contact`. **Nothing was sent to the live endpoint.** |
| Capability Readiness Review | A test set of answers scores 63%, "Developing readiness", with three flagged risks. No script errors. |
| Book toolkit, live | Without the access cookie, `/api/toolkit-download` and `GET /api/toolkit-access` redirect (protected). The downloads page is `noindex`. Not tested with a real access code. |

## 6. Defects

| ID | Priority | Defect | Evidence | Affected files | Status |
|---|---|---|---|---|---|
| QA-01 | **P1** | Links in breadcrumbs and in the footer sector line are distinguished only by colour (contrast with surrounding text 1.23:1). Fails WCAG 1.4.1 and causes the Lighthouse accessibility score of 96 on every page. | axe link-in-text-block (serious) on 10 of 11 pages; Lighthouse | `styles.css` | **Fixed:** links are underlined |
| QA-02 | **P1** | On screens up to 1180 px, the closed overlay menu's 7 links stay in the Tab order while off-screen. When the menu is open, keyboard focus can reach the page behind it. | Playwright Tab sequence at 375, 768 and 1024 px | `styles.css`, `script.js` | **Fixed:** closed menu is `visibility:hidden`; open menu moves focus in and makes `main` and `footer` `inert`; Escape returns focus; resizing to desktop closes it |
| QA-03 | **P1** | All content below the hero (23 of 28 blocks on the homepage) is invisible if `script.js` fails to load or JavaScript is off. | JavaScript disabled and script.js-blocked tests | `build.py` (head), `styles.css`, `script.js` | **Fixed:** an inline flag enables the reveal effect only when scripts are running, and shows everything after 3 s if `script.js` hasn't started. The animation is unchanged in normal use. |
| QA-04 | **P1** | Internal working files are publicly served on the live domain:<br>• `/docs/*.md` (including the evidence register's open actions);<br>• `/AUDIT.md`, `/CONTENT-ROADMAP.md`, `/CHANGES-*.md`, `/README-TOOLKIT.md`;<br>• `/build.py`;<br>• `/resources-src/*.html`, which is duplicate, indexable copies of the PDF content. | Live requests returned 200 | new `.vercelignore` | **Fixed locally:** these paths are excluded from deployment. **Verify after deploy** that `/docs/01-website-audit.md` returns 404. The same files remain public on GitHub while the repository is public (see section 7). |
| QA-05 | P2 | The homepage owner-led card linked to the Business Analysis section of the case studies page. At 375 px the target card started 702 px down, so a visitor first saw a different case study. | Playwright measurement | `build.py` | **Fixed:** the card now has its own anchor (`#example-owner-led-service-business`) and lands at the top of the screen (100 px, clear of the header) at 375 and 1440 px |
| QA-06 | P2 | Inline error messages on the contact form were not linked to their fields. | DOM inspection | `build.py` (contact form) | **Fixed:** `aria-describedby` added |
| QA-07 | P2 | Homepage mobile performance is 89, held back by render-blocking third-party font CSS and late discovery of the hero image (see section 1). | Lighthouse, two runs | `build.py` (head), `styles.css` | **Open.** Self-hosting the fonts (decision 10) is the main fix: preload two WOFF2 files with `font-display: swap`. Also preload the hero image or serve a smaller WebP. Confirm the Fontshare licence first. |
| QA-08 | P2 | Heading-level skips on the CRR page (H1 → H3 in a framework card) and Services. | axe heading-order; scripted check | `build.py` | Open (backlog S6) |
| QA-09 | P2 | The founder photo is a 157 KB, 803 × 1200 JPEG shown at 160–220 px on the homepage. No photo has WebP or `srcset`. | Image check | `assets/photos`, `build.py` | Open (backlog S8) |
| QA-10 | P3 | The site's language is set to `en` rather than `en-GB`. | Source | `build.py` (head) | Open |
| QA-11 | P3 | Badge text (11 px, upper case) and the logo strapline (9.5 px) are small, though legible. | Scripted text-size check | `styles.css` | Open (optional) |
| QA-12 | P3 | No Content-Security-Policy. Lighthouse lists CSP, COOP and Trusted Types as unscored trust items. | Live headers; Lighthouse | `vercel.json` | Open (backlog C6: start report-only) |
| QA-13 | P3 | The pillar pages are long on mobile, for example 12,500 px for Business Analysis at 375 px. | Page heights | `build.py` | Open (content decision) |

No P0 (release-blocking) defects were found.

## 7. For Jason to decide

1. **GitHub repository visibility.** The repository is public, so the evidence register, audit and build files can be read on GitHub even after QA-04 is fixed. Making the repository private would not affect Vercel deployments.
2. **Fonts (decision 10).** Self-hosting is the single biggest improvement available to mobile performance (QA-07).

## 8. Regression results after the fixes (local)

| Check | Result |
|---|---|
| Build | Completes, deterministic |
| Internal links | 5,545 checked, none broken |
| Layout at 320, 375, 768, 1024 and 1440 px, 32 pages | No overflow, no console errors |
| Keyboard tests | Closed menu: 0 off-screen Tab stops at 375, 768 and 1024 px. Open menu: focus contained, Escape works. Desktop unchanged. |
| JavaScript disabled, and script.js blocked | All content visible (immediately, and after 3 s, respectively) |
| Normal load | Reveal animation unchanged |
| Contact form | All four required fields linked to their messages |
| Owner-led anchor | Card top at 100 px (375 px) and 103 px (1440 px) after navigating from the homepage |
| Underlines | Present on breadcrumb and footer sector links |
| Resource dialog, CRR scoring, contact submission (mocked) | Pass, as in section 5 |

**Not re-run after the fixes:** Lighthouse and axe. Both run against the live site, and the fixes aren't deployed. Re-run them after deployment: Lighthouse accessibility is expected to reach 100 once QA-01 is live, but that has not been measured.
