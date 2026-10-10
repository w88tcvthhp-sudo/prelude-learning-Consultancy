# 07 · Change log

## Final remediation and optimisation · 10 October 2026 (not yet committed)

Full details are in `10-final-remediation-report.md`.

**Content and UX**
- **Homepage evidence:** three cards. DS4D comes first, then Healthcare Learning Transformation, then the owner-led service business (linked to its anchor). They sit in one row on desktop and stack one per row at 1,000px and below.
- **Founder section:** the approved sector statement and the approved accountability wording. How I Work has been updated to match.
- **Mobile menu:** all top-level items are now 20px and all sub-links 16px. The root cause was an unscoped desktop font-size rule. The first item is no longer clipped on short screens.

**Technical**
- **Fonts (QA-07):** one Fontshare request per family, which fixes General Sans never loading. Fonts now load without blocking the first paint. Satoshi 900 has been dropped, preconnects corrected, and metric-matched fallbacks added.
- **Hero image (QA-07):** WebP via `image-set()`, with a 640px mobile variant and a homepage-only preload.
- **Headings (QA-08):** fixed on CRR (eyebrow H2) and Services (accordion buttons inside H3s).
- **Founder photo (QA-09):** responsive WebP (320–803w) with a JPEG fallback, lazy loading and intrinsic dimensions. `srcset` paths are now prefixed correctly on nested pages.
- **Language (QA-10):** `lang="en-GB"` on every page.
- **Content Security Policy (QA-12):** a `Content-Security-Policy-Report-Only` header in `vercel.json`. `build.py` keeps the script hashes in step automatically. There is no reporting endpoint yet.
- **Reduced motion:** smooth scrolling is turned off when a visitor's device asks for reduced motion.

## QA fixes · 9 October 2026 (not yet committed)

Full details are in `09-qa-report.md`.

**P1 fixes:**
- **Links:** breadcrumb and footer sector links are now underlined (WCAG 1.4.1).
- **Mobile menu:** the closed overlay menu is removed from the Tab order. The open menu now holds focus: the page behind becomes `inert`, and Escape and resizing close it cleanly.
- **Hidden content:** content no longer stays hidden if `script.js` fails or JavaScript is off. An inline flag in `<head>` falls back after 3 s.
- **Internal files:** a new `.vercelignore` stops `/docs`, `/resources-src`, `build.py` and the root `.md` files being served on the live site.

**P2 fixes:**
- **Owner-led example:** it now has its own anchor, and the homepage links straight to it.
- **Contact form:** errors are linked to their fields with `aria-describedby`.

## Homepage final remediation · 9 October 2026 (not yet committed)

- **Hero, problems, services, founder and final CTA:** copy updated to the final brief.
- **Evidence:** DS4D (founder-led) and the owner-led service business (anonymised Prelude example). The healthcare card has been removed from the homepage only.
- **Final CTA:** the CRR link has been removed.
- **Further detail:** see `08-homepage-mvp.md`, section 4.

## Homepage MVP · 9 October 2026

Details, before-and-after map and test results are in `08-homepage-mvp.md`.

- **Homepage:** 11 sections become 6:
  - hero;
  - the problems we solve;
  - how we help;
  - evidence of experience;
  - who you work with;
  - final CTA.

  The visible text drops from 1,071 to 632 words, and the button CTAs from 8 to 3. Title, description, canonical URL and schema are unchanged.
- **Who I Help:** a new "Sectors" section, moved from the homepage.
- **Insights:** a new "Start here" list of four core articles, moved from the homepage.
- **`styles.css`:** a homepage block has been appended (compact hero, problem cards, two-column evidence, founder layout, CTA aside).

## Phase 1 · 9 October 2026 · credibility and integrity

Decisions behind these changes are recorded in `01-website-audit.md`, section 8.

### Content and claims
- **Contact page:** the unattributed testimonial-style quotation has been removed.
- **About page:** rewritten in the third person from the verified career:
  - Royal Navy (23 years);
  - national L&D operations for a provider of NHS-commissioned healthcare services;
  - leadership and onboarding programmes in social housing;
  - Lead Learning & Development Consultant with Korn Ferry on MOD DS4D;
  - founding Prelude.

  The "up to 25%" and other outcome statistics have been removed, and headings now follow the correct order.
- **Proof strip** (17 pages): now headed "The founder's experience includes". Korn Ferry has been removed (it was an employer, not a client), and the NHS wording has been corrected.
- **Trust strip:** "Supported organisations up to 15,000 staff" has been corrected to "L&D operations for around 15,000 colleagues".
- **Outcome figures:**
  - Removed from service, sector, pillar, article and About pages, and from the homepage.
  - They remain only on case-study pages and the hub, with a revised note saying they were reported by the organisation and that Prelude does not hold the data.
  - Case cards outside the hub now show the qualitative headline instead of a figure.
- **Sector pages:**
  - Headings that read as "track record" are now labelled founder-led experience.
  - Case cards now link to the case studies.
  - FAQs that overstated direct NHS and MOD work have been reworded.
- **Professional services page:** the Korn Ferry role is now described accurately.
- **"See how we've applied this approach"** now reads "Where this approach has been applied" (homepage, pillar and service pages). On case-study pages, "What we found" now reads "What was found".

### Terminology (aligned with *Training Isn't Always the Answer*)
- **Capability Improvement Approach:** retired. The sector-page method section now shows the Prelude Performance & Capability Cycle, and the services hub and How I Work show a Cycle graphic.
- **Prelude Capability Model:** replaced by the Golden Thread, which has a new ten-link graphic.
- **Capability Diagnostic Framework:** replaced by the Capability Diagnostic, which has a new eight-domain graphic.
- **Training vs Capability Decision Model:** replaced by the Should We Train? decision tree, with a redrawn graphic. The explanatory article has been rewritten to match the book; its URL is unchanged.
- **Capability Readiness Review level 3:** renamed "Full diagnostic".
- **`crr.js`:** the self-assessment's suggested next step for question 7 now refers to the Should We Train? decision tree.
- **Framework labels:** each graphic now states its source. "Proprietary frameworks" now reads "Frameworks we use".
- **Glossary:** four terms removed and five added.
- **PDFs:**
  - The **Capability Readiness Playbook v1.1** has a new chapter 4 on the Golden Thread. Chapter 6 and Worksheet 3 now use the eight Capability Diagnostic domains, chapter 7 uses the Should We Train? decision tree, and the CRR levels and trade mark notice have been updated.
  - The **CRR workbook v1.1** now uses the Should We Train? decision tree for question 7, and its trade mark notice has been updated.
  - A heading-break rule has been added to `resources-src/prelude-doc.css`.

### Contact form
- **New fields:** "Nature of enquiry" (required) replaces "Sector", and "Timescale" has been added (optional).
- **Spam and privacy:** a Formspree honeypot (`_gotcha`) has been added, along with a privacy notice at the point of collection.
- **"What happens next":** a three-step panel has been added.
- **Privacy policy:** the list of contact-form fields has been updated.

### Technical
- **Home links:** logo, Home and breadcrumb links now point to `/` instead of `index.html`.
- **New `vercel.json`:**
  - a permanent redirect from `/index.html` to `/`;
  - `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options` and `Permissions-Policy` headers;
  - cache rules for images (7 days) and PDFs (1 day).
- **`build.py`:**
  - two unused homepage bodies have been removed;
  - the Cycle definitions have moved ahead of the page bodies so every page can use them;
  - the old contact-page patches have been folded into the page source.
- **`styles.css`:** the contact page styles, select-width fix and Golden Thread width have been appended.

### Documentation
- **Added in `docs/`:**
  - `01-website-audit.md`
  - `02-remediation-backlog.md`
  - `03-content-evidence-register.md`
  - `04-seo-audit.md`
  - `06-qa-results.md`
  - this log
