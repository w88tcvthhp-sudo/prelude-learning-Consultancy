# 02 · Remediation backlog

Prioritised with MoSCoW. Status as at 10 October 2026 (final remediation round, uncommitted). Item references (M1, S1, C1) match `01-website-audit.md`.

## Must (Phase 1: credibility and integrity)

| Ref | Item | Status |
|---|---|---|
| M1 | Remove the unattributed contact-page quotation | **Done** |
| M2 | Evidence register; figures shown only on case-study pages, labelled as reported by the organisation | **Done**. Jason to complete the "what was measured" column in `03` |
| M3 | Correct the About biography and timeline; remove unsupported statistics | **Done** |
| M4 | Relabel the proof strip as founder experience; correct NHS wording | **Done** |
| M5 | Home links to `/`; `vercel.json` 301 from `/index.html` and security headers | **Done** (not yet verified on Vercel) |
| M6 | Terminology aligned with the book, including the Playbook and CRR workbook PDFs (v1.1) | **Done** |
| M7 | Contact form: privacy notice, honeypot, nature of enquiry, timescale, next steps | **Done** |

## Should (Phases 2 and 3)

| Ref | Item | Depends on | Status |
|---|---|---|---|
| S1 | Homepage sequence: problems recognised, typical outputs, evidence before method, closing question | — | **Done** (homepage MVP, `08-homepage-mvp.md`) |
| S2 | Engagement routes A–D (no prices) on pillar pages, services hub and contact | Decision 11 | To do |
| S3 | Move legacy page bodies (12 service pages, 5 sectors, services, how-i-work, who-i-help, CRR, glossary, privacy, manifesto; About and Contact partly done) onto the newer components, with breadcrumbs everywhere | — | To do |
| S4 | Voice: "we" for Prelude, Jason in the third person, site-wide | — | Partly done (About, Contact, sector framework headings, FAQs changed in Phase 1) |
| S5 | Titles (70) and descriptions (55) to sensible lengths | — | To do |
| S6 | Fix the remaining heading skips (CRR, Services) | — | **Done** (QA-08; 0 skips site-wide) |
| S7 | Person and Service schema; FAQPage only where substantive; real-depth breadcrumbs | — | To do |
| S8 | WebP and `srcset`; WebP hero; fonts | — | **Done** except self-hosting fonts (QA-07, QA-09); see `10`, D3 |

## Could (Phase 4)

| Ref | Item | Depends on | Status |
|---|---|---|---|
| C1 | Eight-cluster content architecture; consolidate overlapping TNA and capability-framework pages with 301s | Search Console data, ideally | To do |
| C2 | Cookieless analytics, with a privacy policy update | Decision 9 | To do |
| C3 | Content visible without JavaScript | — | **Done** (QA-03) |
| C4 | Split `build.py` into templates and data (same output) | — | Started: two unused homepage bodies removed |
| C5 | `checks.py` for repeatable QA (links, H1s, metadata, placeholders, figures outside case studies) | — | To do |
| C6 | Content Security Policy (report-only first) | — | Report-only **done** (QA-12); enforce after validation on production |
| C7 | Turn the two Prelude engagements (Nunroyd, Contractor Caddy) into full case studies, with client permission | Client permission | New; to do |

| C8 | Self-host the official Fontshare WOFF2 files, unmodified (permitted by the ITF FFL; repo must stay private) | Files downloaded on the Mac | New; to do |
| C9 | Replace inline `style` attributes so `style-src` can drop `'unsafe-inline'` | C4 | New; to do |
| C10 | CSP reporting endpoint | A service Prelude controls | New; to do |

## Won't (this round)

Framework migration; bulk new articles; published prices or availability; tracking without approval.
