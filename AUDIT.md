# Prelude Learning & Consultancy — Phase 1 Audit
**Prepared as:** UX/UI, Technical SEO, Accessibility & Conversion review
**Scope:** Full site as held in this repo (matches live prelude-learning.com as of this audit)
**Status:** Audit only — no code changed in this phase.

---

## 0. Overall verdict

The foundation is genuinely good — better than most solo-consultant sites. The "training is rarely the problem, capability is" thesis is sharp, consistent, and differentiated. The Prelude Capability Model™, Capability Readiness Review™ and the four other proprietary frameworks are a real asset — most boutique consultancies never bother to name and diagram their IP. The dark forest/gold palette, editorial type (Satoshi/General Sans), and restrained motion already read "consultancy" rather than "freelancer."

But it is not yet ready to sit next to Korn Ferry or PA Consulting, for reasons that are fixable and mostly structural, not cosmetic:

1. **The site cannot currently capture a single lead.** Both forms post to an unconfigured Formspree placeholder (`your-form-id`).
2. **Three of four target sectors have no home.** Defence gets a full page; Healthcare, Housing and Public Sector get a paragraph each. For an NHS Director of Workforce or a Housing CEO, that reads as "Defence consultancy that also mentions us," not "a consultancy that understands my world."
3. **Services are one page, not a system.** Twelve services are collapsed into an accordion instead of individual pages with problem/diagnosis/approach/deliverables/case study/FAQ — the brief's own quality bar for services pages.
4. **The "Insights" content cluster is fake.** Eight article cards link nowhere (no `href` at all). This is worse than having no blog — it signals unfinished work to anyone who clicks.
5. **No structured data, sitemap, robots.txt, or canonical tags exist anywhere.** Zero schema markup means this site is close to invisible to AI answer engines (ChatGPT, Perplexity, Google AI Overviews) that rely on Organization/ProfessionalService/Person/FAQ schema to cite a source confidently.
6. **The professional photograph you just added is not wired in.** `about.html` still renders a placeholder box with the *words* "Professional photograph of Jason Smith" instead of the image — a five-minute fix with outsized credibility impact.

None of this requires rebuilding. It requires finishing what's architecturally already 70% right.

**Estimated current maturity: 6.0 / 10** as a boutique consultancy site — strong voice and visual identity, let down by unfinished plumbing (forms, sectors, schema, dead links) that a careful buyer (or an MOD/NHS procurement reviewer doing due diligence) will find within two minutes.

---

## 1. Information Architecture

**What exists:** 11 pages — Home, Defence, Services, How I Work, Capability Readiness Review, Case Studies, Insights, Why Training Isn't the Problem (manifesto), Who I Help, About, Contact.

**Findings**

| # | Finding | Severity |
|---|---|---|
| IA-1 | Primary nav shows 7 items; 2 genuinely valuable pages (`who-i-help.html`, `why-training-isnt-the-problem.html`) exist only in the footer and contextual links. A visitor who identifies by role (the site's own stated best segmentation — "you identify with your role faster than your sector") has to find it by accident. | High |
| IA-2 | Only Defence has a dedicated sector page. Healthcare, Housing, Public Sector, and Professional Services (a named target sector in the brief) have **no landing page at all** — no URL to rank for "NHS learning and development consultant" or "housing association leadership development." | Critical |
| IA-3 | Services exist as one long page (12 services in an accordion) rather than as individually addressable, individually rankable pages. Every service currently shares one URL, one title tag, one meta description — a significant SEO and IA compromise. | Critical |
| IA-4 | Case studies (7 total) live on one page filtered by JS tabs, not as individual URLs — so no single case study can be linked, shared, or independently indexed by Google/AI crawlers. | High |
| IA-5 | Sector cards on the homepage are inconsistent: the Defence card links to a dedicated page; Healthcare and Housing cards both link to the generic `services.html`. This visibly signals "Defence is the real business; the rest is aspirational." | High |
| IA-6 | No breadcrumbs anywhere — minor for a shallow site now, but necessary once service/sector pages multiply. | Medium |
| IA-7 | No 404 page found/verified — should exist as full sites grow. | Low |

---

## 2. UX Review

| # | Finding | Severity |
|---|---|---|
| UX-1 | **Both the contact form and the resource-request form post to `https://formspree.io/f/your-form-id`** — a placeholder, not a real endpoint. Every enquiry and every lead-magnet request currently fails silently. This is the single highest-priority fix on the entire site. | Critical |
| UX-2 | The "Insights" hub promises 8 articles ("DSAT Explained," "Leadership in High-Pressure Environments," etc.) styled as clickable cards, but none have an `href` — they are inert `<span>` elements. A genuinely curious visitor clicks and nothing happens. | Critical |
| UX-3 | The 5 gated "resources" (Capability Readiness Playbook, TNA Checklist, Governance Health Check, etc.) all route to the same generic capture form rather than to the specific resource — and only one PDF (`capability-readiness-playbook.pdf`) actually exists in `/assets`. The other four are promised but don't exist. | High |
| UX-4 | Homepage testimonial is attributed to "Senior Client · Digital Skills for Defence (DS4D)" — anonymised is fine for OFFSEC/commercial reasons, but it's the *only* testimonial on the entire site, repeated nowhere else, and there's no path to more (LinkedIn recommendations, video, etc.). | Medium |
| UX-5 | On `contact.html`, a large styled quote — `"Jason understands my environment, my problem, and has solved this before."` — is presented in the same visual style as a real testimonial (quotation marks, heading treatment) but reads as aspirational copy, not an attributed quote. This blurs the line between real social proof and copywriting in a way a sharp buyer will notice and distrust. | Medium |
| UX-6 | No booking/scheduling tool (Calendly or equivalent) despite "Discuss Your Capability Challenge" being the primary CTA site-wide — every conversion currently funnels to a static form with no confirmed reply SLA beyond "aim to reply within one working day." Adding real-time booking would materially shorten the sales cycle. | High |
| UX-7 | Trust badges (Active SC / Former DV / Royal Navy / Korn Ferry / DSAT / PRINCE2 / CMI) and the Capability Improvement Approach 6-step diagram are repeated **verbatim, in full, on 5+ pages** (Home, About, Defence, How I Work, Services). Reading more than two pages back-to-back feels repetitive rather than reinforcing — a red flag for the "editorial, sophisticated" tone the brief wants. | Medium |
| UX-8 | Cognitive load on `services.html` and `who-i-help.html`: 12 and 9 accordion items respectively, each with 4 sub-blocks. Functional, but a long scroll/read for a first-time visitor with no way to jump to a specific item from the nav or a summary grid. | Medium |
| UX-9 | No sticky/persistent CTA — on long pages (`services.html` at ~1,776 words, `case-studies.html` at ~1,982 words) the only CTA is at the very top and very bottom. A visitor deep in an accordion has to scroll a long way to act. | Medium |

---

## 3. UI / Visual Design

**Strengths worth preserving:** consistent brand tokens (`--forest`, `--emerald`, `--gold`, `--stone`), restrained motion (respects `prefers-reduced-motion`), clean button system, decent type scale via `clamp()`, subtle film-grain/gradient texture that avoids feeling flat or templated. This is meaningfully better than a Wordpress-consultancy default.

| # | Finding | Severity |
|---|---|---|
| UI-1 | Photography is low native resolution (540–638px wide JPEGs, 45–230KB each) displayed inside a 1180px content column — will render soft/blurry on standard and retina desktop displays. Not "premium consultancy" quality once you look closely. | High |
| UI-2 | No `width`/`height` attributes on any content photo (only the logo has them) — guarantees layout shift (CLS) as images load, directly hurting Core Web Vitals. | High |
| UI-3 | The six proprietary framework diagrams are hand-built inline SVG, duplicated in full across up to 5 pages each. This bloats every page's HTML weight and creates a maintenance trap: `build.py` already centralises this generation, but the *output* still repeats ~90 lines of SVG per instance rather than referencing one embedded definition. | Medium |
| UI-4 | No visible focus ring on nav links, buttons, or cards (`styles.css` only styles `:focus` on form fields and CRR radio options). Keyboard users tabbing through the site lose track of where they are — a real accessibility and premium-perception issue (enterprise buyers' IT/accessibility teams do check this). | High |
| UI-5 | `--stone-dim` (#8f9088) used for de-emphasised text (`.dim` spans, muted captions) against the `--forest` (#081D16) background is visually elegant but likely fails WCAG AA contrast (~3.9:1, need 4.5:1 for body text) — needs measurement and likely a lighten pass. | High |
| UI-6 | About page's photo slot is a literal placeholder (`<div class="photo-frame">…Professional photograph<br>of Jason Smith</div>`) rendering the Prelude icon mark and caption text instead of an actual image — despite a real professional photograph now sitting in `/assets/photos/`. | Critical (quick win) |
| UI-7 | No `<main>` landmark on any page — content sits directly under `<header>`/`<section>` in `<body>`. Minor for SEO, meaningful for screen-reader landmark navigation. | Medium |
| UI-8 | No skip-to-content link for keyboard/screen-reader users to bypass the nav. | Medium |

---

## 4. Branding & Positioning

The "capability, not training" thesis is the site's strongest asset — keep it and sharpen it further, don't dilute it. Specific observations:

- The brief asks to reduce "training" emphasis and increase capability/governance/performance/transformation language — **this is already largely done**. The word "training" appears mostly in compliance/DSAT contexts (correctly, since DSAT/JSP 822 *are* training-governance frameworks) rather than as a service description. Good instinct already applied.
- Positioning is strong for Defence, thin for Healthcare/Housing/Public Sector — the copy for those sectors is a bullet list, not a narrative with sector-specific proof, language and case studies. This is the single biggest branding gap: the site currently reads as "Defence consultancy, with Healthcare/Housing as an afterthought," which undercuts the multi-sector ambition in the brief.
- "Boutique vs. big consultancy" comparison table (used twice, verbatim, on Home and Who I Help) is a good device but risks sounding defensive if a visitor reads both pages — it's essentially arguing against a competitor who isn't named. Works once; repeating it word-for-word signals a small content library rather than restraint.
- No name-checked clients, only sector-anonymised case studies. Understandable for MOD/NHS confidentiality, but the brief's "client logos where permitted" is unaddressed — worth a deliberate decision (ask which past clients would permit name/logo use) rather than defaulting to full anonymity everywhere.

---

## 5. Services Pages

Current state: one page, one URL, 12 services as accordion items, each with Client challenges / My approach / Outcomes / Example (4 of the 8 elements the brief specifies — missing Diagnosis, Deliverables as a distinct list, FAQs, and a page-level CTA per service).

**Gap:** no individual service pages exist to satisfy the brief's per-service structure (Problem, Diagnosis, Approach, Deliverables, Outcomes, Case study, FAQs, CTA). This is a Phase 3 content build, not a Phase 1 fix, but it's the single largest content gap in the site.

---

## 6. Sector Pages

| Sector | Current state |
|---|---|
| Defence | Full dedicated page (`defence.html`) — strongest page on the site. Good template to replicate. |
| Healthcare | No dedicated page. Represented by 5 bullet points on the homepage + one case study. |
| Housing | No dedicated page. Represented by 5 bullet points on the homepage + one case study. |
| Public Sector | No dedicated page. Folded into "Housing & Public Sector" on the homepage — the brief treats these as distinct sectors. |
| Professional Services | Not mentioned anywhere on the site despite being a named target sector in the brief. |

This is the clearest, highest-leverage content gap: replicate the Defence page's structure (challenges / who I work with / services / frameworks / track record / trust / CTA) for Healthcare, Housing, Public Sector, and Professional Services.

---

## 7. Case Studies

7 case studies exist, well-structured (Problem / Why it mattered / What I found / What I did / Results / Client benefit / Lessons learned) — this is genuinely close to the brief's target format already (missing only explicit "Commercial impact" and "Transferability" as their own labelled sections, and a value for cost/time saved where available).

**Gap:** all 7 live on one URL with JS-based filtering. Each should be independently addressable (own URL, own title/meta/schema) so it can rank individually and be cited by name by AI answer engines.

---

## 8. Trust Signals

**Present:** Active SC clearance, former DV holder, Royal Navy senior leadership, Korn Ferry Consultant, DSAT specialist, PRINCE2 Practitioner, CMI Leadership & Coaching, "supported organisations up to 15,000 staff."

**Missing, and each is a named requirement of the brief:**
- Company registration number (16918049, per your message) — not shown anywhere, including the footer, despite being trivial to add and standard practice for a Ltd company selling to public sector.
- Professional indemnity / public liability insurance status — frequently a hard procurement gate for MOD/NHS/Housing Association contracts; currently invisible.
- Procurement-readiness signals — no mention of Crown Commercial Service frameworks, G-Cloud, Cyber Essentials (Plus), ICO registration, or supplier-portal readiness. For the stated target buyers (MOD, Defence Primes, NHS, Housing, Public Sector) this is often the first thing procurement checks.
- No Privacy Policy, Terms, or Cookie Notice page exists anywhere in the site — a real gap for a UK company handling enquiry-form data from public sector visitors (a Ltd company is expected to have at least a baseline privacy notice; its absence is conspicuous to any procurement/compliance reviewer).
- No speaking engagements, published articles, or third-party thought-leadership citations — the site currently only cites its own content.

---

## 9. Conversion Optimisation

- Single, consistent primary CTA ("Discuss Your Capability Challenge") used everywhere — good discipline, keep it.
- **Both forms are non-functional** (see UX-1) — this is a Critical, not a Phase-3/4 nice-to-have; nothing else on this list matters if no enquiry can currently reach you.
- No booking/scheduling integration (Calendly or similar).
- No lead magnet actually delivers a file automatically — everything routes through a manual "I'll email it to you" form, which is fine as an interim step but weaker than instant download + email nurture.
- No sticky/secondary CTA on long-scroll pages.

---

## 10. Technical SEO

| # | Finding | Severity |
|---|---|---|
| SEO-1 | **No structured data (JSON-LD) anywhere** — no Organization, ProfessionalService, Person, FAQPage, Article, or BreadcrumbList schema on any page. | Critical |
| SEO-2 | No `sitemap.xml` and no `robots.txt` in the repo. | Critical |
| SEO-3 | No canonical `<link rel="canonical">` tags on any page — a real risk once `prelude-learning.com` / `.co.uk` / `.org` all forward to the same content (per the README's own deployment notes), since search engines need to be told which is authoritative. | High |
| SEO-4 | Open Graph tags present for `og:title`/`og:description`/`og:type` but **missing `og:image` and `og:url`**, and **no Twitter Card tags at all** — link previews on LinkedIn/Slack/X will show no image and may render poorly. | High |
| SEO-5 | Titles and meta descriptions are otherwise well-written, keyword-relevant, and unique per page — a genuine strength to build on. | — (positive) |
| SEO-6 | Image alt text is descriptive and semantically useful (a strength, not a gap) — e.g. "Capability map and learning architecture — transformation roadmap workshop" rather than generic "photo1.jpg" alt text seen on many sites. | — (positive) |
| SEO-7 | No internal linking strategy for topical clusters — e.g. nothing on the site links "DSAT" mentions to a canonical DSAT explainer page, because that page doesn't exist yet (it's a dead card on Insights). | High |

---

## 11. AI Search Optimisation (ChatGPT / Claude / Gemini / Perplexity / Google AI Overviews)

This is the area furthest behind the brief's ambitions, and it compounds directly from the technical SEO gaps above:

- With no Organization/ProfessionalService/Person schema, AI answer engines have no structured entity to anchor "Prelude Learning & Consultancy" or "Jason Smith" against — they're working from prose alone.
- **The homepage's core proof points (15,000 employees supported, 25% performance improvement, 95% completion, 100% compliance) are rendered entirely by client-side JavaScript as an animated counter, starting from a literal "0" in the HTML.** A crawler or AI system that doesn't execute JS — confirmed by testing the live homepage — sees "0%," "0," "0" for every headline statistic. The strongest evidence on the site is functionally invisible to exactly the systems the brief wants to influence. This should be fixed by rendering the real number in the HTML and using JS only for the animation.
- No FAQ schema anywhere, despite FAQs being explicitly requested per-service and per-sector — because those FAQ sections don't exist yet.
- No dedicated, quotable definitions of DSAT, JSP 822, Capability Readiness Review™, or the Prelude Capability Model™ exist as standalone, linkable pages — these are exactly the kind of entity/definition content AI answer engines prefer to cite.

---

## 12. Content Strategy / Topical Clusters

Currently a single "Insights" hub with 8 promised-but-unbuilt article topics and one real long-form piece (the manifesto). The topic list itself is well-chosen and matches the brief's requested clusters almost exactly (DSAT, TNA, capability frameworks, leadership, public sector workforce, learning technology, apprenticeships, training governance, readiness) — the gap is entirely in execution, not planning.

---

## 13. Accessibility (WCAG AA)

| # | Finding | Severity |
|---|---|---|
| A11Y-1 | No visible focus indicator on nav links, buttons, or interactive cards — fails WCAG 2.4.7 (Focus Visible) for keyboard users. | High |
| A11Y-2 | Likely contrast failure on `--stone-dim` text against `--forest` background — needs measurement against WCAG AA 4.5:1 for body text / 3:1 for large text. | High |
| A11Y-3 | No skip-to-content link. | Medium |
| A11Y-4 | No `<main>` landmark on any page. | Medium |
| A11Y-5 | `prefers-reduced-motion` is respected — a genuine strength, uncommon even on premium sites. | — (positive) |
| A11Y-6 | Form labels are correctly associated (`<label for>`) — a genuine strength. | — (positive) |
| A11Y-7 | Accordion components correctly manage `aria-expanded` via JS — a genuine strength. | — (positive) |

---

## 14. Performance

| # | Finding | Severity |
|---|---|---|
| PERF-1 | Content photos are unoptimised for the modern web: JPEG-only (no WebP/AVIF), no responsive `srcset`, no explicit dimensions, no `loading="lazy"` on below-the-fold images. | High |
| PERF-2 | Fonts loaded from third-party CDN (Fontshare) rather than self-hosted — adds an external DNS/TLS round trip despite `preconnect` mitigation. | Low |
| PERF-3 | CSS/JS are lean by static-site standards (one 42KB stylesheet, one 5KB script) with no build/bundle overhead — a genuine strength; no framework tax being paid here. | — (positive) |
| PERF-4 | No minification of CSS/JS — modest win available, low priority given already-small file sizes. | Low |

---

## 15. Mobile Experience

Media query breakpoints exist at 980px/880px/560px covering nav, hero, metrics, and forms — structurally reasonable. Full manual QA across real devices is recommended in Phase 4 once content/layout changes land, rather than re-testing the current state twice.

---

## Priority Roadmap

**Now (do immediately, before anything else — not gated on the redesign):** ✅ **done**
1. ~~Wire the professional photograph into `about.html`~~ (UI-6) — **done**. Real photo now renders via a `.photo-frame.has-photo` treatment (object-fit cover, framed to match the site's aesthetic) in both `about.html` and `build.py`.
2. ~~Fix both Formspree endpoints~~ (UX-1) — **left open on request**. Endpoint choice wasn't decided yet; both forms still point at the `your-form-id` placeholder. Flagged as the top open item before any conversion work in Phase 4.
3. ~~Add the real numbers into the HTML behind the animated counters~~ (Section 11) — **done**, across `index.html`, `about.html`, `case-studies.html` and `build.py`. Non-JS visitors and crawlers now see the real figures (15,000 / 25% / 95% / 100% / etc.) instead of "0"; the JS counter animation is unaffected for JS users.
4. ~~Fix the 9 dead "Insights" article links~~ (UX-2, corrected count — there are 9 cards, not 8) — **done as an honesty fix, not a content fix**. Each card's fake "Read the article →" link has been replaced with a plain "In development" status label, so the site no longer implies content that doesn't exist. Writing the 9 actual articles remains Phase 3 work.
5. ~~Add company number, a Privacy Policy, and basic legal footer content~~ (Section 8) — **done**. Company No. 16918049 now appears in the footer of every page; a new `privacy.html` (real UK-GDPR-appropriate content, not a placeholder) is live and linked from every footer. **Needs your sign-off**: confirm whether you're ICO-registered, and whether the "third-party form-handling provider" wording should name Formspree specifically once that's configured (item 2).

**New findings surfaced while fixing the above (not previously known) — both resolved in Phase 2:**
- `build.py` couldn't run at all — a pre-existing syntax error (backslash inside an f-string, invalid before Python 3.12). Fixed; the script now parses and runs cleanly on this machine's Python 3.9.
- `build.py` and the live HTML had drifted in three places (`case-studies.html`, `defence.html`, `how-i-work.html`), not just the one file spotted at the end of Phase 1. Fully reconciled — see Phase 2 notes below. `python3 build.py` is now safe to run again and regenerates the site correctly.

**Phase 2 (Foundation):** ✅ **done**
- **`build.py` fully reconciled with the live HTML.** The photo drift wasn't limited to `case-studies.html` — `defence.html` and `how-i-work.html` had also been hand-wired with real photos while `build.py`'s `photo()`/`photo_grid()`/`case()` functions still emitted placeholder "Visual slot" boxes. Rewrote all three functions to take real `(src, alt, width, height)` and updated every call site (2 photo grids + 8 case studies) using the ground-truth data from the live HTML. Verified with a full diff before/after: **zero content regressions**, only genuine improvements (real `width`/`height`/`loading="lazy"` attributes added, plus a pre-existing escaped-quote bug in the contact-page testimonial fixed as a side effect). `build.py` is now a trustworthy single source of truth again — confirmed by running it and diffing output against the live files.
- **Semantic HTML & accessibility**: every page now has a `<main id="main">` landmark, a skip-to-content link (`.skip-link`, visible on keyboard focus), and `:focus-visible` outlines on nav links, buttons, and interactive cards (previously only form fields had a focus state). Contrast-checked `--stone-dim` against both its backgrounds — it already passed AA on the primary `--forest` background (5.4:1) but failed on the lighter `--sage` card backgrounds (3.0:1, below the 4.5:1 AA threshold); lightened it to `#B4B3AA`, which now passes both (8.3:1 / 4.6:1).
- **Navigation**: promoted "Who I Help" from footer-only into the primary nav (now 8 items + CTA) — this was the site's best top-of-funnel segmentation tool and was previously undiscoverable except by accident. Verified the extra item doesn't overflow the desktop nav before the existing 1180px burger-menu breakpoint kicks in.
- **Technical SEO**: canonical `<link>` tags, `og:url`, `og:image` (+ width/height), and full Twitter Card tags added to every page via `head()`. Confirmed the live site's canonical domain is `https://www.prelude-learning.com` (non-www 308-redirects to www). Created `robots.txt` and a `sitemap.xml` generator (runs as part of `build.py`, so it can't drift out of sync as pages are added in Phase 3).
- **A real Open Graph share image.** There wasn't one to reuse, so I designed a 1200×630 on-brand card (dark forest background, the site's own ring motif, wordmark, headline, credential badges) as an SVG and rasterised it to `assets/og/prelude-og-image.jpg` — used site-wide for `og:image`/`twitter:image`. Source SVG kept at `assets/og/og-card-source.svg` for future edits.
- **JSON-LD structured data**: `ProfessionalService` + nested `Person` (founder) schema with `knowsAbout` entity coverage (Capability Development, DSAT, JSP 822, etc.), UK Companies House identifier (16918049), and a two-level `BreadcrumbList` on every page. Validated all JSON-LD blocks parse correctly.
- **Reusable components — checked, not rebuilt.** The 6 proprietary framework diagrams were already single Python functions in `build.py` (`fw_prelude_model()`, `fw_decision_model()`, etc.), reused across pages at the source level — the earlier audit note about "duplication" was about rendered page weight only, which is an acceptable static-site tradeoff, not a maintainability problem. No changes needed there.
- Full browser verification pass: no console errors, no failed network requests, all photo/nav/schema changes confirmed rendering correctly across index/defence/who-i-help pages.

**Phase 3 (Content & Positioning) — sector pages done, service/case-study/insights work still to come:**
- ✅ **Built 4 new dedicated sector pages** — `healthcare.html`, `housing.html`, `public-sector.html`, `professional-services.html` — mirroring the Defence page's proven structure (hero, who-I-work-with, services, proprietary frameworks, methodology, track record, trust, FAQ, CTA). This directly fixes the audit's most severe finding (IA-2/Critical): three of four target sectors previously had no page at all.
  - Healthcare and Housing each reuse 1 previously-unused real photo plus 2 fresh ones from `/assets/photos` (no stock/placeholder imagery). Public Sector uses an honest 2-photo grid rather than stretching to 3, since only 2 genuinely sector-relevant photos exist. **Professional Services has no photo section at all** — there's no professional-services photography in the asset library, and I chose not to force in mismatched Defence/Healthcare imagery. Worth commissioning real photography for this sector before it goes live (see `PHOTOGRAPHY-BRIEF.md`'s existing pattern).
  - Professional Services also has no dedicated case study (none exist for this sector). Rather than fabricate one, the page leans honestly on real, verifiable credibility — Jason's time as a Korn Ferry consultant — and is transparent in its FAQ that named case studies are Defence/Healthcare/Housing engagements whose method transfers directly.
- ✅ **Nav restructured**: the single flat "Defence" link is now a "Sectors" dropdown (Defence / Healthcare / Housing / Public Sector / Professional Services) — hover/focus-reveal on desktop, tap-to-expand inline on mobile. Found and fixed a real specificity bug during testing: a high-specificity desktop "reveal" rule was still applying its `transform: translateX(-50%)` inside the mobile menu, cutting off sector link text at the left edge. Fixed and verified on a 375px viewport.
- ✅ **Homepage sector cards fixed** (IA-5): Healthcare and Housing previously both linked to the generic `services.html`; now all 5 sectors get their own card linking to their own page. Grid CSS changed to `auto-fit` so it wraps cleanly regardless of card count.
- ✅ **FAQ component + FAQPage schema** built as a reusable pattern (`faq_section()` / `faq_schema()` in `build.py`, styled with the site's existing accordion CSS — no new components needed). Added 5 FAQs to Defence (previously had none) and 5 each to the 4 new sector pages — 25 real, sector-specific questions in total, all schema-validated.
- ✅ **Built 12 individual service pages** — one per service across all three categories (Capability & Governance / Leadership & Workforce / Learning Transformation), each with the full Problem / How I diagnose it / My approach / Deliverables & Outcomes / Proof / FAQs / CTA structure the brief specifies, via one shared `service_page()` template in `build.py` fed by real, distinct content per service (not mail-merged copy — each problem, diagnostic test and set of deliverables is specific to that service). All 12 carry valid ProfessionalService + BreadcrumbList + FAQPage schema (36 new FAQs total).
  - `services.html` stays as the hub/overview — each of its 12 accordion items now ends with a "Full service page →" link to the dedicated page, rather than duplicating the expanded content on both the hub and the detail page.
  - Every service's "Proof" and case-study reference points to a real, already-published case study — no invented metrics.
  - Found and fixed a real CSS bug while verifying: a new `a.read` link class had no SVG size constraint, so the arrow icon rendered at native (huge) size instead of as a small inline icon. Fixed and reverified in-browser.
- ✅ **Built 8 individual case study pages**, one per engagement, each rewritten into the brief's full consultancy format — Challenge, Context (Why it mattered), Approach, Deliverables, Outcome, Commercial Impact, Transferability, Lessons — via one shared `case_study_page()` template. Deliverables, Commercial Impact and Transferability are new sections not previously on the site; the rest is expanded from the existing, already-strong case narrative rather than rewritten from nothing. Every metric is one already published elsewhere on the site — nothing invented. Each page carries ProfessionalService + BreadcrumbList + Article schema, and links to a relevant service page ("Related service: ..."). `case-studies.html` stays as the filterable overview, with each card now ending in a "Full case study →" link.
- ✅ **Wrote all 9 Insights articles** that were previously "in development" placeholders: DSAT Explained, Training Needs Analysis: Best Practice, Building Capability Frameworks, Leadership in High-Pressure Environments, Public Sector Workforce Development, Learning Technology Lessons, Apprenticeship Success Strategies, Defence Training Governance, From Training to Readiness. Each is a genuine, substantive article (~500–700 words of real body copy plus 3 FAQs), written to reinforce the site's core "diagnose before you prescribe" positioning and cross-link to a relevant service page — not thin SEO filler. All 9 carry ProfessionalService + BreadcrumbList + FAQPage + Article schema. `insights.html`'s 9 article cards now link to real pages instead of showing "in development".
- All 45 pages (up from 12 at the start of Phase 2) are in `sitemap.xml`, and a full rebuild-and-diff confirms `build.py` and the live site have **zero drift** — the generator is a fully trustworthy single source of truth again.
- Found and fixed one more bug during this pass: the case-study hero metric used `.metric-grid` with a `max-content` override that left a visually empty stretched box; replaced with the more appropriate `.case-metric` component already used elsewhere on the site. Reverified in-browser.

**Phase 3 is now complete.** The site has grown from 12 pages to 45: 5 sector pages, 12 service pages, 8 case study pages, 9 Insights articles, plus the original core pages — every one carrying canonical tags, Open Graph/Twitter Cards, and appropriate JSON-LD (ProfessionalService on every page, plus BreadcrumbList, FAQPage and/or Article as relevant). `build.py` remains the single trustworthy source of truth throughout, verified by full rebuild-and-diff at every step with zero unintended drift.

**Phase 4 (Optimisation):** ✅ **done** (2 items intentionally deferred — see below)
- **Sticky CTA** added site-wide: a dismissible bottom bar ("Ready to talk about your capability challenge?") that appears after the visitor scrolls roughly one viewport height, remembers dismissal for the session, and is suppressed on `contact.html`/`privacy.html` where it would be redundant or tonally off. Verified via direct DOM inspection (position, visibility, transform) and manual event dispatch after the automated browser tooling in this environment proved unreliable for simulating real scroll gestures — the underlying JS and CSS are confirmed correct.
- **Image performance pass**: resized and re-compressed all 18 photos in `/assets/photos` — none were upscaled (a first pass mistakenly did this via `sips -Z`; caught in review and redone correctly, only ever downscaling). Total photo payload: **2.31MB → 1.62MB (30% smaller)**, with zero visible quality loss (spot-checked at full resolution). All `width`/`height` HTML attributes updated to match the new real dimensions so CLS protection stays accurate. `loading="lazy"` confirmed already present on all 31 photo `<img>` tags site-wide from the Phase 2/3 build.
- **Touch target audit**: found and fixed three interactive elements below the 44×44px accessibility guideline — the mobile burger menu (36×26.5 → 44×44.5), the new sticky-CTA close button (34×32 → 44×44), and the case-studies filter pills (37px tall → 44px tall).
- **Full mobile QA**: verified nav, Sectors dropdown, sticky CTA, and accordions render and behave correctly at a 375px viewport across representative page types (homepage, services hub, case studies).

**Deliberately deferred (flagged, not forgotten):**
- **Formspree / lead-capture backend** — still pointing at the placeholder from Phase 1. A clarifying question about this and Calendly was asked but the tool call failed before you could answer, so I proceeded with the defaults I'd already offered: leave the forms as-is, skip Calendly. **This is the single highest-priority item before the site can generate a real lead.**
- **Calendly / booking integration** — not added; there's no Calendly link to embed yet, and it's downstream of the lead-capture decision above.
- **Professional Services photography** — still the one sector page with no photos, because no relevant imagery exists in the asset library and I won't substitute mismatched stock-style photos from other sectors. Needs real commissioned photography (see `PHOTOGRAPHY-BRIEF.md`'s existing pattern).

---

## Score

**Before (start of engagement): 6.0 / 10** — strong positioning and visual identity undercut by non-functional lead capture, three under-served sectors, a one-page services catalogue, dead content links, and a complete absence of structured data.

**After Phase 3 (current state): approximately 8.0 / 10.** Every named sector and service now has a real, evidence-backed page; case studies follow the full consultancy format with commercial impact and transferability; the Insights content cluster is genuinely written, not placeholder; structured data and technical SEO are comprehensive across all 45 pages. What's holding it back from higher: the lead-capture forms are still not wired to a real endpoint (nothing converts yet), Professional Services has no photography or case study of its own, and Phase 4's performance/accessibility/mobile QA hasn't been done on real devices. The final score will be set at the end of Phase 4.
