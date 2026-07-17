# Prelude Learning & Consultancy — Final Review

**Engagement:** Full-site redesign across four phases (Audit → Foundation → Content & Positioning → Optimisation)
**Scope:** 11 original pages → 45 pages, one generator (`build.py`) as the single source of truth throughout
**Status:** All four phases complete. Two items intentionally deferred pending your decision (see Remaining Recommendations).

For the detailed, page-by-page reasoning behind every decision below, see `AUDIT.md` — this document is the executive summary the original brief asked for.

---

## Overall score

| | Score | Verdict |
|---|---|---|
| **Before** | 6.0 / 10 | Strong positioning and visual identity, undercut by non-functional lead capture, three under-served sectors, a one-page services catalogue, dead content links, and zero structured data. |
| **After** | **8.5 / 10** | Sits credibly beside Korn Ferry, Kineo and PA Consulting on structure, content depth and technical foundation. The 1.5-point gap to a 10 is almost entirely the two deferred items below — a site that can't yet capture a lead, however good it looks, isn't finished. |

---

## Complete change log

### Phase 1 — Audit & quick fixes
- Full UX/UI/SEO/accessibility/content audit written to `AUDIT.md`.
- Wired the real professional photograph into `about.html` (was a placeholder box).
- Fixed the homepage/about/case-study stat counters so real numbers render in the HTML, not just after a JS animation — non-JS visitors and crawlers previously saw "0" for every headline metric.
- Replaced 9 fake "Read the article →" links on the Insights page with honest "In development" labels (later replaced with real articles in Phase 3).
- Added Company No. 16918049 to every page footer, plus a genuine, non-placeholder `privacy.html` (UK GDPR-appropriate).
- Found and fixed a pre-existing syntax error that meant `build.py` (the site generator) couldn't run at all.
- Found and fixed a build.py ↔ live-HTML drift where a prior session had hand-wired real case-study photos into the HTML without updating the generator — `python3 build.py` would have silently reverted them to placeholders.

### Phase 2 — Foundation
- **Fully reconciled `build.py`** with the live HTML (the Phase 1 drift was more extensive than first thought — `defence.html` and `how-i-work.html` had the same problem). Verified with a full diff: zero regressions.
- **Semantic HTML & accessibility**: `<main>` landmark and skip-to-content link on every page; `:focus-visible` states on nav, buttons and cards (previously only form fields had one); contrast-checked and fixed `--stone-dim` against its actual card backgrounds (was failing AA at 3.0:1, now 4.6:1+).
- **Navigation**: promoted "Who I Help" from footer-only into the primary nav.
- **Technical SEO**: canonical tags, `og:url`, `og:image`, Twitter Cards on every page; `robots.txt`; a self-regenerating `sitemap.xml`.
- **Designed a custom Open Graph share image** (1200×630, on-brand) from scratch — there wasn't one to reuse.
- **Structured data**: `ProfessionalService` + `Person` (founder) JSON-LD with topic/entity coverage, Companies House identifier, and breadcrumbs on every page.

### Phase 3 — Content & Positioning
- **4 new sector pages**: Healthcare, Housing, Public Sector, Professional Services — each with hero, services, proprietary frameworks, methodology, track record, trust signals, 5 FAQs, and CTA.
- **Nav restructured** into a "Sectors" dropdown (Defence/Healthcare/Housing/Public Sector/Professional Services) — hover-reveal on desktop, tap-to-expand on mobile.
- **12 individual service pages**, each with the full Problem / Diagnosis / Approach / Deliverables / Outcomes / Proof / FAQs / CTA structure the brief specified — replacing what had been a single 12-item accordion.
- **8 individual case-study pages**, each expanded to Challenge / Context / Approach / Deliverables / Outcome / Commercial Impact / Transferability / Lessons — the full consultancy format, with `Article` schema.
- **9 Insight articles** written from scratch (~500–700 words of genuine content each), replacing the "In development" placeholders — DSAT Explained, TNA Best Practice, Building Capability Frameworks, Leadership Under Pressure, Public Sector Workforce Development, Learning Technology Lessons, Apprenticeship Success, Defence Training Governance, From Training to Readiness.
- **FAQ component + FAQPage schema** built once, reused everywhere — 25 sector FAQs + 36 service FAQs + 5 Defence FAQs + 27 article FAQs, all schema-validated.
- Fixed the homepage sector cards (Healthcare and Housing both used to link to the generic Services page).

### Phase 4 — Optimisation
- **Sticky CTA** site-wide, dismissible, suppressed on Contact/Privacy.
- **Image performance pass**: 2.31MB → 1.62MB across 18 photos (30% reduction), zero visible quality loss, all `width`/`height` attributes kept accurate for CLS protection.
- **Touch target fixes**: burger menu, sticky-CTA close button, and filter pills all brought up to the 44×44px accessibility guideline.
- Full mobile QA across representative page types.

---

## SEO improvements
- Canonical URLs, Open Graph (incl. custom image), Twitter Cards on all 45 pages.
- `robots.txt` + self-maintaining `sitemap.xml`.
- 12 new service URLs, 8 new case-study URLs, 4 new sector URLs, 9 new article URLs — each independently indexable and rankable, versus the pre-existing single accordion/filtered-list pages.
- Confirmed and standardised on the live canonical domain (`https://www.prelude-learning.com`).

## UX improvements
- "Who I Help" and the sector structure both surfaced properly in navigation instead of being effectively hidden.
- Services and case studies broken out of accordions/filters into real, linkable, shareable pages.
- Sticky CTA reduces the distance to conversion on long pages.
- Dead "In development" content replaced with real, useful articles.
- Homepage sector cards now route to the correct dedicated page for every sector.

## Accessibility improvements
- Skip-to-content link and `<main>` landmark on every page.
- Keyboard focus states restored across nav, buttons, and interactive cards.
- Text contrast fixed where it was actually failing (card backgrounds, not the page background as first assumed).
- Three touch targets brought up to the 44×44px guideline.
- `prefers-reduced-motion` respected (pre-existing, verified still intact).

## Performance improvements
- Photo payload cut by 30% (2.31MB → 1.62MB) with no visible quality loss.
- `loading="lazy"` confirmed on all 31 photo images site-wide.
- Accurate `width`/`height` attributes prevent layout shift as images load.
- HTML pages remain lean (16–32KB each) — no framework tax, no bundler overhead.

## Conversion improvements
- Sticky CTA on every page except Contact/Privacy.
- Single, consistent primary CTA ("Discuss Your Capability Challenge") preserved and reinforced throughout new content.
- Every new page (sector, service, case study, article) ends with a CTA tied to what the visitor just read, not a generic sitewide banner.

## New pages created (34)
- **4 sectors**: `healthcare.html`, `housing.html`, `public-sector.html`, `professional-services.html`
- **12 services**: `dsat-consultancy.html`, `training-needs-analysis.html`, `capability-framework-design.html`, `training-governance-assurance.html`, `leadership-development.html`, `talent-development.html`, `workforce-planning.html`, `apprenticeships.html`, `digital-learning.html`, `lms-optimisation.html`, `learning-operations.html`, `learning-strategy.html`
- **8 case studies**: `mod-digital-skills-for-defence.html`, `sio-course-rapid-tna.html`, `defence-capability-framework-design.html`, `op-isotrope-role-architecture-redesign.html`, `healthcare-learning-transformation.html`, `housing-leadership-onboarding-transformation.html`, `defence-apprenticeship-success-programme.html`, `nato-royal-navy-training-modernisation.html`
- **9 articles**: `dsat-explained.html`, `training-needs-analysis-best-practice.html`, `building-capability-frameworks.html`, `leadership-in-high-pressure-environments.html`, `public-sector-workforce-development.html`, `learning-technology-lessons.html`, `apprenticeship-success-strategies.html`, `defence-training-governance.html`, `from-training-to-readiness.html`
- **1 legal**: `privacy.html`

## Structured data implemented
- `ProfessionalService` (with nested `Person`/founder) — every page
- `BreadcrumbList` — every page
- `FAQPage` — Defence + 4 sectors + 12 services + 9 articles (93 FAQ pairs total)
- `Article` — 8 case studies + 9 insight articles

---

## Remaining recommendations

**✅ Lead capture is now live.** Both the Contact form and the Insights resource-request form post to a real Formspree endpoint (`https://formspree.io/f/xeeyazed`), each tagged with a distinguishing `_subject` line so submissions arrive labelled "New capability enquiry" vs "Resource request." `privacy.html` now names Formspree explicitly, including the US data-transfer disclosure. **Recommend sending one real test submission through each form** to confirm delivery end-to-end and complete Formspree's one-time account-activation step — I didn't do this myself, since it sends a live email on your behalf.

1. **Calendly or booking tool**, once you've decided whether you want one and have a link to embed.

**Lower priority, whenever convenient:**
2. Commission real Professional Services photography — it's the one sector page without any, and the asset library has nothing suitable to reuse honestly.
3. Confirm your ICO registration status and add the registration number to the Privacy Policy if you're registered.
4. Consider named client logos/testimonials where confidentiality allows — every case study is currently anonymised, which is appropriate for MOD/NHS work but a named reference or two would strengthen credibility further.
5. A full Core Web Vitals audit (Lighthouse/PageSpeed Insights) against the live, deployed site — everything in this engagement was verified locally; real-world numbers depend on the final host's configuration (the site is live on Vercel per DNS checked in Phase 2, not the GoDaddy/cPanel setup described in the README — worth updating that document).

---

*Every code change in this engagement went through `build.py`, the site's generator — nothing was hand-edited into the live HTML files directly. Running `python3 build.py` at any point regenerates the entire site consistently from that single source.*
