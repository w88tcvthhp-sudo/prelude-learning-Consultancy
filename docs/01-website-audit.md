# 01 · Website audit (Phase 0)

**Date:** 9 October 2026
**Baseline:** commit `77f06ca` on `main`, which was the live code at the time of the audit. `python3 build.py` reproduced the committed HTML exactly.
**Method:** repository inspection plus automated checks with Python and Playwright/Chromium against a local server.
**Not checked:** the live site's HTTP behaviour (the audit environment's network could not reach prelude-learning.com), Google Search Console, field Core Web Vitals and real screen readers.

This file records the site as it was before remediation. What has changed since is in `07-change-log.md`; the decisions that drove those changes are in section 8.

## 1. Technical architecture

| Layer | What exists | Assessment |
|---|---|---|
| Generation | `build.py` (≈5,900 lines of Python) generates every page from shared `head()`, `nav()` and `footer()` functions. The content is inline Python strings. The generated HTML is committed. | One build route means the header and footer are guaranteed consistent. The risk is that two generations of templates, plus late string-replacement patches (`_rep`), make the file fragile. Vercel does not run `build.py`, so HTML must be rebuilt locally before every commit. |
| Styling | `styles.css` (1,128 lines), with brand tokens in `:root` and dated override blocks appended | Works, but layered. Three heading scales and two section systems (`section/.divider` and `.sec`) coexist. |
| Scripts | `script.js` (nav, reveal, accordion), `crr.js`, `resources.js`, `toolkit-form.js` | Small, with no framework. Content uses `.reveal` (opacity 0 until JavaScript runs). Reduced motion is respected. |
| Hosting | Vercel (Hobby plan): static files plus two Node functions (`/api/toolkit-access`, `/api/toolkit-download`) with private Blob storage. No `vercel.json`. | Simple. No redirect or header configuration exists yet. Hobby is limited to non-commercial use. |
| Forms | Formspree (`xeeyazed`) for contact, resources and toolkit records | Works for a static site. |
| Fonts | Satoshi and General Sans from the Fontshare CDN, loaded as render-blocking third-party CSS | A performance cost and a third-party request. |
| Analytics | None. `data-event` hooks are in the markup, and the privacy policy states there is no analytics. | Conversion cannot currently be measured. |
| Repository | Public on GitHub. No tests, linting or CI. | Secrets correctly sit in Vercel environment variables. |

## 2. Page and URL inventory

113 HTML files: 110 indexable, plus `404`, `thank-you` and the toolkit downloads page (noindex). The sitemap lists exactly those 110 pages.

| Group | Count | URLs |
|---|---|---|
| Home | 1 | `/` (file `index.html`) |
| Company | 4 | `about.html`, `how-i-work.html`, `who-i-help.html`, `contact.html` |
| Service pillars | 3 + 1 | `capability-consulting/`, `business-analysis/`, `workforce-development/`, plus `approach/` |
| Services hub and detail | 1 + 12 | `services.html`, `dsat-consultancy`, `training-needs-analysis`, `capability-framework-design`, `training-governance-assurance`, `leadership-development`, `talent-development`, `workforce-planning`, `apprenticeships`, `digital-learning`, `lms-optimisation`, `learning-operations`, `learning-strategy` (`.html`) |
| Sectors | 5 | `defence`, `healthcare`, `housing`, `public-sector`, `professional-services` (`.html`) |
| Case studies | 1 + 8 | `case-studies.html`, `mod-digital-skills-for-defence`, `sio-course-rapid-tna`, `defence-capability-framework-design`, `nato-royal-navy-training-modernisation`, `op-isotrope-role-architecture-redesign`, `healthcare-learning-transformation`, `housing-leadership-onboarding-transformation`, `defence-apprenticeship-success-programme` |
| Insights | 1 + 66 + 1 | `insights.html`, 66 articles (13 "complete guide" pillar articles plus supporting pieces), and the manifesto `why-training-isnt-the-problem.html` |
| Tools and resources | 3 | `capability-readiness-review.html`, `resources/`, `glossary.html` |
| Book | 3 | `training-isnt-always-the-answer/`, `book-toolkit/`, `book-toolkit/downloads/` (noindex) |
| Legal and utility | 3 | `privacy.html`, `thank-you.html` (noindex), `404.html` (noindex) |
| Functions | 2 | `/api/toolkit-access`, `/api/toolkit-download` |

## 3. Navigation, layout and components

| Element | Finding |
|---|---|
| Header, navigation, logo, mobile menu | **Identical on all 113 pages.** All pages use one `nav()` function, and the only differences are the active-state highlight. The order is Home · About · Services ▾ · Case Studies · Insights ▾ · Contact, plus the "Discuss a challenge" button. |
| Footer | **Identical on all pages.** The 404 page differs only in using root-relative links, which is deliberate. |
| Page body template | **Inconsistent.** 18 pages use the newer system (`.sec`, `section_head`, breadcrumbs, case-study cards). 91 pages mix it with the legacy system (`.divider`, eyebrow and `p.lead` headings, framework SVG cards, the "proof" strip). Three pages are legacy-only: contact, glossary and privacy. |
| Breadcrumbs | Visible on only 13 pages. BreadcrumbList schema is on most pages but is always two levels, even on pages that are three levels deep. |
| Voice | Newer pages say "we" or "Prelude". Legacy pages (about, services, sectors, service detail, how-i-work, who-i-help) say "I" or "my". |
| "Proof" strip | Appears on 17 legacy pages: "Experience built in high-stakes environments: Ministry of Defence · Royal Navy · Korn Ferry · NHS & Healthcare · Housing Associations · Public Sector". It reads like a client list. |
| Framework graphics | Six ™ graphics spread across sector and legacy pages (see the terminology register below). |
| CTA | "Discuss a challenge" is used consistently. Secondary CTAs vary. |
| Heroes | Two hero styles. The pillar-page hero is offset from the section grid. |

## 4. Defects in the brief: confirmed or corrected

| Reported defect | Status | Evidence |
|---|---|---|
| Visible "None" under a case study | **Already fixed** (8 October). Not present anywhere. | Search of all 113 pages |
| Inconsistent navigation | **Corrected: header and footer are now consistent.** The real inconsistency is in page bodies, voice and components (section 3). | Hash comparison of the nav and footer on every page |
| Placeholders (TODO, TBC, Lorem) | None found | grep |
| Broken internal links or missing assets | None. 5,540 links checked; the only "misses" are function routes. | Link crawler |
| Inconsistent company name | None found | grep |
| Terminology overlap | **Confirmed** | Register below |
| Title and description lengths | 70 of 110 titles are over 60 characters; 55 descriptions are over 160 characters. No duplicates. | Metadata scan |
| Heading structure | Exactly one H1 on every page. Five pages skip a level: About, Contact, CRR, Services and Who I Help. | Script |
| `index.html` vs `/` | Canonical tag and sitemap use `/`, but every page's logo and Home link point to `index.html`. There is no redirect. The live response could not be tested from here. | Source |

**New defects found**

| # | Defect | Severity |
|---|---|---|
| N1 | The contact page shows an **unattributed quotation styled as a testimonial**: "Jason understands my environment, my problem, and has solved this before." | Critical |
| N2 | **About page conflicts with the homepage and book biography.** About says that through Korn Ferry Jason advised "Defence, Healthcare, Housing and the public sector" and professional services firms. The homepage and book say the healthcare and housing work were separate roles, and that the Korn Ferry work was DS4D. About's timeline also omits the healthcare and housing roles, and adds "25% operational performance improvement (up to)". | Critical |
| N3 | The proof strip lists Korn Ferry, an employer, alongside organisations that read as clients. "NHS" appears in the strip and in the healthcare case-study photo alt text, while the biography says "a healthcare provider". | High |
| N4 | The contact form has no spam honeypot, no privacy notice at the point of collection, and a "Sector" field rather than a "Nature of enquiry" field. | High |
| N5 | FAQPage schema is on 83 pages (66 articles and 17 service or sector pages). The FAQs are visible, so it isn't invalid, but it is broader than the brief allows. | Medium |
| N6 | No Person schema on About, and no Service schema on the service pages. | Medium |
| N7 | Photos are JPEG only, with no `srcset` (1.7 MB in total). The hero CSS uses the JPEG although a WebP exists. Fonts load as render-blocking third-party CSS. | Medium |
| N8 | Content overlap: TNA is covered by a service page, a complete guide, best practice, step-by-step, common mistakes, TNA vs skills gap and front-line commands. Capability frameworks are covered by a service page, building, what-is, multi-specialisation, Defence design and a case study. | Medium |
| N9 | The book uses the term "Prelude Method"; the site doesn't. The book interior still contains the placeholder text "[QR CODE – …]". (Book, not website.) | High (book) |

### Terminology register

| Term | Pages | What the repository shows it to be |
|---|---|---|
| Prelude Performance & Capability Cycle (Understand, Diagnose, Define, Intervene, Prove) | 4 (home, approach, book, case studies) | The working **method**, also used in the book |
| Prelude Capability Model™ (six layers: Mission → Evidence) | 12 | A **model** of what capability is made of, used for diagnosis |
| Capability Improvement Approach™ (Mission, Gap, Root Cause, Intervention, Impact, Improve) | 8 (sectors, services, how-i-work, glossary) | An **older method**. It overlaps almost entirely with the Cycle. |
| Capability Readiness Review™ | Every page (footer); content on the CRR page | The **entry diagnostic**: ten questions at three levels (self-assessment, facilitated, full) |
| Capability Diagnostic™ | 2 | The name of the third CRR level (an engagement). It is also the name of Tool 07 in the book. |
| Capability Diagnostic Framework™ (5 tiers) | 3 (defence, public sector, glossary) | A graphic that overlaps with the Capability Model |
| Training vs Capability Decision Model™ | 10 | A single decision test. Distinct, and consistent with the book. |
| Capability Readiness Maturity Model™ | 3 | A five-stage maturity scale. Distinct. |
| Prelude Method | 0 on the site; used in the book | Undefined on the site |

## 5. Unverified claims and missing evidence

The repository holds no evidence for any of these: no baseline, method, period or source.

| Claim | Pages | Attribution as published | Recommended action |
|---|---|---|---|
| +20% operational readiness | 10 | Defence Capability Framework Design (founder-led) | Evidence needed, or qualitative wording |
| −20% time-to-competence | 10 | Housing (founder-led) | As above |
| −20% failure rate | 7 | NATO & Royal Navy (founder-led) | As above |
| +17% pass rates | 7 | NATO & Royal Navy | As above |
| +15% response effectiveness | 11 | OP ISOTROPE | As above. Also confirm OP ISOTROPE may be named publicly. |
| −18% compliance gaps | 12 | Healthcare | As above. Confirm whether the provider was NHS. |
| 95% completion and 100% funding compliance | 11 / 6 | Defence apprenticeships | As above |
| "Up to 25% operational performance improvement" | 1 (About) | Unattributed | Remove unless evidenced |
| "15,000 staff/colleagues" | 15 | Healthcare employer (scale, not outcome) | Low risk if the figure is accurate. Confirm. |
| "Progress in ten weeks that had stalled for twelve months" | 5 | DS4D testimonial | Depends on testimonial permission |
| DS4D testimonial (homepage) | 1 | "Senior client, DS4D"; refers to "Jason and his team" (founder, in the Korn Ferry team context) | Confirm written permission and attribution wording |
| Contact-page quotation | 1 | None | **Remove**, or supply the source |
| Proof strip (MoD, RN, Korn Ferry, NHS…) | 17 | Implies clients | Relabel as founder experience, or remove |
| Korn Ferry scope on About | 1 | Founder | Correct to the facts |

The case studies already carry "Founder-led experience" labels and an evidence note (October work). Service, sector and article pages repeat the figures without those labels.

## 6. MoSCoW backlog

**Must (Phase 1, credibility and integrity)**
- M1: Remove or replace the unattributed contact-page quotation. *Small effort.*
- M2: Evidence register (file 03), then apply your decisions on every figure across about 22 pages. Most figures come from data in `build.py`. *Medium.*
- M3: Correct the About page biography and timeline so it matches the verified career (Royal Navy → healthcare provider → social housing → Korn Ferry/DS4D → Prelude). Remove unsupported statistics. *Small.*
- M4: Relabel the proof strip ("Founder's experience includes…") or remove it. Correct the NHS references if needed. *Small.*
- M5: Home URL consistency. Change internal Home and logo links to `/`, and (needs approval) add `vercel.json` with a 301 from `/index.html` to `/`. *Small.*
- M6: Terminology decision, then standardise copy and graphics. *Medium.*
- M7: Contact form: privacy notice, honeypot, "Nature of enquiry" field, optional engagement type and timescale, and "what happens next" text. *Small.*

**Should (Phases 2–3)**
- S1: Homepage sequence as in the brief. Add "Recognise the problem" and typical outputs for each service; put evidence before methodology; close with "What challenge are you trying to solve?" and next steps. This mostly reorders existing material. *Medium.*
- S2: Engagement routes A–D: Initial Diagnostic, Fixed-Scope, Programme & Strategic Support, Specialist Associate. They replace the current four options on the pillar pages, services hub and contact page. No prices. *Medium.*
- S3: Move the legacy page bodies (12 service pages, 5 sectors, about, how-i-work, who-i-help, services, CRR, contact, glossary, privacy, manifesto) onto the newer component system. This means one hero, breadcrumbs everywhere and three-level BreadcrumbList schema. *Large.*
- S4: Standardise voice: "we" for Prelude, "Jason" in the third person for founder credentials. *Medium.*
- S5: Rewrite 70 titles and 55 descriptions to sensible lengths. *Medium.*
- S6: Fix the five heading skips. *Small.*
- S7: Schema. Add Person (About) and Service (pillar and service pages). Keep FAQPage only where the FAQs are substantive, and add none new. *Small.*
- S8: Performance. WebP and `srcset` for photos, WebP hero with fallback. Self-host fonts if the licence allows (approval). *Small to medium.*

**Could (Phase 4)**
- C1: Content architecture across eight clusters (landing page, supporting articles, case study, resource, conversion). Consolidate overlapping TNA and capability-framework pages, with 301s. *Large.*
- C2: Cookieless analytics (approval; privacy policy update). *Small.*
- C3: Make content visible without JavaScript (progressive reveal). *Small.*
- C4: Split `build.py` into template and data modules. Same output, no new framework. *Medium.*
- C5: Add `checks.py` (links, H1s, metadata, placeholders) so QA can be repeated. *Small.*

**Won't (this round):** framework migration, bulk new articles, published prices or availability, new tracking without approval.

## 7. Proposed sequence

| Phase | Work | Deliverables |
|---|---|---|
| 0 | Write the audit, evidence register and SEO baseline | Files 01, 03, 04 |
| 1 | M1–M7. Figures are changed only as you decide. | — |
| 2 | S1, S2, S4 and the contact journey | File 05 |
| 3 | S3, S5–S8 | — |
| 4 | C1, C3, C5 (C2 if approved) | — |
| 5 | QA at 375, 768, 1024 and 1440px | Files 06, 07, 02 |

As decided on 9 October 2026 (decision 14), changes are committed to `main` and Jason pushes them. There is no preview step, so every change is tested locally before it is handed over (see `06-qa-results.md`).

## 8. Decisions (9 October 2026)

| # | Question | Decision (Jason) | How it has been applied |
|---|---|---|---|
| 1 | Evidence for the outcome figures | The data was measured by the organisations at the time and is not held by Jason. | Figures appear only on the eight case-study pages and the case-study hub, labelled as reported by the organisation. Everywhere else the work is described without figures. "Up to 25%" removed. See `03-content-evidence-register.md`. |
| 2 | Contact-page quotation | Remove. | Removed. |
| 3 | DS4D testimonial | Keep. | Kept on the homepage. Recommendation: hold the client's written agreement to the wording on file. |
| 4 | Biography facts | Korn Ferry: engaged as Lead TNA, and the role grew well beyond it. Healthcare and housing: employed roles. Healthcare provider: NHS services delivered through an independent provider; no company names. OP ISOTROPE, SIO and NATO/RN may be named. | About page rewritten. Healthcare wording is "a provider of NHS-commissioned healthcare services". No employer names for healthcare or housing. |
| 5 | Prelude Ltd engagements | Only the Nunroyd Cleaning Services and Contractor Caddy work. | All eight published case studies remain labelled founder-led experience. The two anonymised examples are the Prelude engagements. Copy no longer implies Prelude delivered the eight studies. |
| 6 | Terminology | Follow the book, where it works for the website. | Cycle = method; Golden Thread replaces the Prelude Capability Model; Capability Diagnostic (eight domains) replaces the Capability Diagnostic Framework; Should We Train? decision tree replaces the Training vs Capability Decision Model; Capability Improvement Approach retired; CRR level 3 renamed "Full diagnostic"; Maturity Model kept. "Prelude Method" is used as in the book: a label for Prelude's own syntheses. |
| 7 | Voice | "We" for Prelude; Jason in the third person. | Applied to pages changed in Phase 1. Site-wide change is backlog item S4. |
| 8 | `vercel.json` | Yes: redirect and headers. | Added. |
| 9 | Analytics | Not yet decided. | None added. |
| 10 | Self-hosted fonts | Not yet decided. | No change. |
| 11 | Engagement routes A–D | Not yet decided. | Phase 2. |
| 12 | Contact form fields | Approve all. | Applied. |
| 13 | Primary domain | Not answered. Every canonical tag already uses `www.prelude-learning.com`. | Treated as primary. Confirm in Vercel that the apex domain redirects to www. |
| 14 | Workflow | Commit to `main`. | Commits are made on `main`; Jason pushes. |
