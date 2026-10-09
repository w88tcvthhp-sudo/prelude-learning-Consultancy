# 04 · SEO audit (baseline and Phase 1 changes)

**Date:** 9 October 2026. **Baseline:** commit `77f06ca`.
**Method:** automated scan of the generated HTML (titles, descriptions, canonicals, robots, structured data, headings, links) with Python and BeautifulSoup.
**Not available:** Google Search Console, ranking or traffic data, crawl data from the live site, field Core Web Vitals. This audit covers what can be checked from the repository; it cannot say how the site currently performs in search.

## 1. Baseline

| Area | Finding | Assessment |
|---|---|---|
| Indexable pages | 110 of 113 HTML pages. `404`, `thank-you` and the toolkit downloads page are `noindex`. | Correct. |
| Sitemap | `sitemap.xml` lists exactly the 110 indexable pages, with `/` for the homepage. | Correct. No `lastmod` dates. |
| robots.txt | Allows everything except `/api/`, the toolkit downloads page and four email-gated PDFs. Points to the sitemap. | Correct for the current gating. |
| Canonical tags | Present on all 113 pages; all use `https://www.prelude-learning.com`. | Consistent. The apex domain should redirect to www (check in Vercel > Domains). |
| Home URL | Canonical and sitemap use `/`, but every page linked to `index.html` from the logo and Home link, and there was no redirect. | Split signal. **Fixed in Phase 1.** |
| Titles | No duplicates. 70 of 110 are longer than 60 characters, so they are likely to be truncated in results. | Backlog S5. |
| Descriptions | No duplicates. 55 are longer than 160 characters; 3 are shorter than 70 (all noindex pages). | Backlog S5. |
| H1 | Exactly one on every page. | Correct. |
| Heading order | Five pages skipped a level (About, Contact, CRR, Services, Who I Help). | Two fixed in Phase 1; three remain (S6). |
| Structured data | `ProfessionalService` (113), `BreadcrumbList` (109, always two levels), `FAQPage` (83), `Article` (74), `WebSite`, `DefinedTermSet`, `Book` and `Person` (1 each). All JSON-LD parses. | FAQPage is broader than needed (N5). No `Person` on About and no `Service` on service pages (N6). Breadcrumbs should reflect real depth. Backlog S7. |
| Internal links | 5,540 internal links, none broken (the only unresolved targets are the two serverless function routes). | Good. |
| Content overlap | Training Needs Analysis and capability frameworks are each covered by six or seven pages with overlapping intent (N8). | Risk of pages competing with each other. Backlog C1. |
| Thin pages | 29 indexable pages under 400 words, mostly case studies and supporting articles. | Case studies are deliberately concise; review supporting articles in C1. |
| Images | JPEG only, about 1.7 MB in total, no `srcset`; hero CSS uses a JPEG although a WebP exists. | Backlog S8. |
| Fonts | Fontshare CSS is render-blocking and third-party. | Backlog S8 (decision 10 pending). |
| Social metadata | Open Graph and Twitter tags present. | Correct. |

## 2. Phase 1 changes with SEO effect

| Change | Effect |
|---|---|
| Logo, Home and breadcrumb links now point to `/` (all pages) | Internal links agree with the canonical URL. |
| `vercel.json`: permanent (301) redirect from `/index.html` to `/` | Consolidates any external links or bookmarks to `index.html`. |
| Article title and H1 "The Should We Train? Decision Tree, Explained" (URL unchanged: `/training-vs-capability-decision-model-explained.html`) | Term now matches the book. The URL was kept to preserve existing links and indexing. |
| Article title "What Drives Apprenticeship Completion and Funding Compliance" (URL unchanged) | Removes an unsupported figure from a title. |
| Glossary: four retired terms removed; five added (Capability Diagnostic, Golden Thread, Prelude Method, Prelude Performance & Capability Cycle, Should We Train? decision tree) | The `DefinedTermSet` schema follows automatically. Old glossary anchors (`#prelude-capability-model` and similar) no longer exist; no internal links used them. |
| About and Contact heading structure | No skipped levels on either page. |

No URLs were added, removed or renamed in Phase 1.

## 3. Measures after Phase 1

| Measure | Baseline | After Phase 1 |
|---|---|---|
| Pages | 113 (110 indexable) | 113 (110 indexable) |
| Titles over 60 characters | 70 | 70 |
| Descriptions over 160 characters | 55 | 55 |
| Pages with a skipped heading level | 5 | 3 |
| Internal links checked / broken | 5,540 / 0 | 5,555 / 0 |
| Internal links to `index.html` | 240 | 0 |

## 4. Recommended next steps (Phases 3 and 4)

1. Rewrite the 70 long titles and 55 long descriptions (S5). Keep the primary term at the start of each title.
2. Fix the three remaining heading skips (S6).
3. Add `Person` schema to About and `Service` schema to the pillar and service pages; keep `FAQPage` only where the FAQs are substantive; make `BreadcrumbList` reflect the real path (S7).
4. Serve WebP with `srcset`, and decide whether to self-host fonts (S8).
5. Consolidate the overlapping TNA and capability-framework pages into clear clusters, with 301 redirects for anything merged (C1).
6. Once the site has been live for a few weeks with these changes, connect Google Search Console and use real query data to prioritise C1.
