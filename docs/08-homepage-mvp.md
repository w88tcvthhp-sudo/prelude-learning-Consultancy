# 08 · Homepage MVP: content reduction and visual hierarchy

**Date:** 9 October 2026. **Baseline:** commit `652f700` (live after Phase 1).
**Scope:** the homepage only, plus one relocation of unique content to Who I Help. No URLs, metadata or other pages changed.

## 1. Audit of the current homepage

Visible words are counted from the page's `<main>` content, excluding the navigation and footer.

| # | Current section | Words | Headings | Calls to action and links |
|---|---|---|---|---|
| 1 | Hero: headline, service line, 45-word introduction, principle statement | 87 | H1 | **Discuss a challenge**; Explore our services |
| 2 | "Three connected services": three pillars, each with a question and a five-item list | 181 | H2, 3 × H3 | 6 links to the pillar pages |
| 3 | Approach teaser: the Performance & Capability Cycle, with diagram | 78 | H2 | See how the approach works |
| 4 | Selected case studies: DS4D, Healthcare, anonymised owner-led business | 175 | H2, 3 × H3 | 5 links; View case studies |
| 5 | Who we work with: specialist sectors and a ten-item "who else" list | 147 | H2, 2 × H3 | none |
| 6 | Founder strip: biography and six credentials | 113 | H2 | More about Jason |
| 7 | DS4D testimonial | 51 | none | none |
| 8 | Capability Readiness Review and a five-item resources list | 91 | 2 × H2 | **Take the Capability Readiness Review**; 6 resource links |
| 9 | Book band | 78 | H2 | About the book |
| 10 | Four featured insights | 33 | H2 | 5 links |
| 11 | Final CTA band | 37 | H2 | **Discuss a challenge**; Explore our services |
| | **Total** | **1,071** | | **5 button CTAs competing**, about 40 links |

**Page height at baseline:** 13,515 px at 375 px wide; 10,854 px at 768; 8,572 px at 1024; 8,897 px at 1440.

**Primary CTA position:** the "Discuss a challenge" button finished 914 px down the page at 375 × 900 px, just below the first screen on a typical phone.

**Repeated messages:**
- "Understand the problem first" appears in sections 1, 2, 3 and 11.
- The service list appears in section 1 and again in section 2.
- "Explore our services" appears twice.
- The founder's career is told in section 6 and again in section 5's footnote.

**SEO baseline (kept unchanged):**
- **Title:** "Prelude Learning & Consultancy | Capability Consulting, Business Analysis & Workforce Development".
- **Description:** begins "Solving problems training alone can't fix. Independent UK consultancy for capability consulting, TNA and DSAT, business analysis and improvement, and learning and workforce development…".
- **H1:** "Solving problems training alone can't fix."
- **Canonical:** `/`.
- **Schema:** WebSite and ProfessionalService.
- **Key terms on the page:** capability consulting, business analysis and improvement, learning and workforce development, Training Needs Analysis, DSAT, learning strategy, Defence, public services.

## 2. Before and after

| Current section | Decision | Reason | Where the content lives now |
|---|---|---|---|
| 1 Hero | **Condense** | Keep the headline and the three-service line. Cut the 45-word introduction and the separate principle statement to about 30 words. Make the hero shorter, so the primary CTA sits on the first screen on mobile. Secondary CTA changes to "Explore our work". | Homepage |
| — | **New: The problems we solve** | The buyer needs to recognise their own situation before reading about services. Three problems, each linked to the relevant service. | Homepage |
| 2 Three services | **Condense** | Keep the three service lines. Replace each question and five-item list with one 25 to 30-word description and a link. The lists are already on the pillar pages. | Homepage, and the pillar pages |
| 3 Approach and Cycle | **Remove from homepage; merge one sentence** | The full method is on Our approach, which is in the Services menu. The services introduction keeps one sentence about the approach, with a link. | `approach/` |
| 4 Case studies | **Condense to two, and merge the testimonial** | DS4D is the flagship. Healthcare shows cross-sector, regulated-environment work at scale and has its own full page. The anonymised example becomes a one-line link, which also makes clear that Prelude's own contracts are separate from the founder-led studies. | Homepage; `case-studies.html` |
| 5 Who we work with | **Relocate** | Sector lists don't help a buyer decide on the homepage. The footer already carries sector links. The "who else we work with" list and the transferability note are unique, so they move to Who I Help. | `who-i-help.html` (new section) |
| 6 Founder strip | **Condense** | A 70-word introduction, four credentials and the link to About. The photo is kept but smaller, so this section supports the evidence rather than competing with it. | Homepage; `about.html` |
| 7 Testimonial | **Merge into the evidence section** | The quote belongs beside the DS4D work it describes. The wording is unchanged. | Homepage |
| 8 CRR and resources | **Remove the section; keep a contextual link** | The CRR stays in the footer and is linked from the pillar pages. On the homepage it becomes a secondary text link under the final CTA, so it no longer competes with "Discuss a challenge". The resources stay in the Insights menu. | `capability-readiness-review.html`, `resources/` |
| 9 Book band | **Remove from homepage** | The book is under Insights, in the footer and on the Insights page. | `training-isnt-always-the-answer/` |
| 10 Featured insights | **Relocate** | The Insights page did not link to these four articles, so removing them from the homepage would have weakened their internal linking. They move to a new "Start here" list on the Insights page. | `insights.html#start-here` |
| 11 Final CTA | **Retain and reword** | "What challenge are you trying to solve?" with one primary button. The duplicate "Explore our services" button is dropped. | Homepage |

**Result:** 11 sections become 6, which are:
1. Hero
2. Problems
3. Services
4. Evidence
5. Founder
6. Final CTA

There are 2 button CTAs, the same "Discuss a challenge" in the hero and final band. "Explore our work" is a secondary ghost button in the hero.

**Visual emphasis:**
- The hero and the evidence section carry the most weight. Evidence is the only tinted section and the only one with a quotation.
- The problems and services sections are plain.
- The founder section uses the smaller heading size and a smaller photo.

## 3. Change report

### Section count and length

| Measure | Before | After |
|---|---|---|
| Content sections | 11 | 6 |
| Visible body words (main content) | 1,071 | 632 |
| Button CTAs | 8 (five different destinations) | 3: "Discuss a challenge" ×2, and "Explore our work" |
| Links in main content | 30 | 20 |
| Page height at 375 px | 13,515 px | 7,782 px (−42%) |
| Page height at 768 px | 10,854 px | 5,882 px (−46%) |
| Page height at 1024 px | 8,572 px | 5,072 px (−41%) |
| Page height at 1440 px | 8,897 px | 5,194 px (−42%) |
| Bottom of the primary CTA, 375 × 900 viewport | 914 px (below the first screen) | 650 px (on the first screen) |

**Words per section after the change:**

| Section | Words |
|---|---|
| Hero | 53 |
| Problems | 107 |
| Services | 127 |
| Evidence (including the testimonial and basis note) | 202 |
| Founder | 98 |
| Final CTA | 45 |

The evidence section is the longest by design.

### What was retained, merged, relocated and removed

**Retained and condensed:**
- The hero, with its headline unchanged.
- The three services.
- The founder introduction.
- The final CTA.

**New:**
- The problems section.

**Merged:**
- The DS4D testimonial now sits in the evidence section, with its wording unchanged.
- One sentence about the approach, linking to `approach/`, is folded into the services introduction.

**Relocated:**
- The sector lists and the transferability note moved to Who I Help, in a new "Sectors" section.
- The four featured insights moved to Insights, in a new "Start here" list.

**Removed from the homepage only (every page and URL is unchanged):**
- The Cycle diagram (still on `approach/`).
- The Capability Readiness Review and resources block. The CRR stays in the footer and on the pillar, services and About pages, and is now a secondary text link under the final CTA.
- The book band (still in the Insights menu, the footer and the Insights page).
- The anonymised owner-led business card (still on `case-studies.html`; it is referred to in the evidence note).

### Visual hierarchy

**Hero:**
- Top padding drops from 172 px to 148 px on desktop and from 124 px to 104 px on mobile.
- The H1 is smaller on narrow screens, and the principle statement is folded into a single introduction.

**Evidence** is the only tinted section and has the testimonial, so it is the visual centre of the page.

**Problems and services:**
- Both use the existing pillar cards.
- The problem cards have a quieter rule and smaller headings, so the two sections read differently.

**Founder:**
- Uses the smaller section-title size.
- The photo is about 220 px wide on desktop (it was up to 320 px).

**Final CTA:**
- One primary button, plus a quiet text link to the CRR.

**General:**
- No new colours, fonts, components, images or dependencies.

### SEO

**Unchanged:**
- The title, meta description, canonical URL, Open Graph and Twitter tags, and JSON-LD (WebSite and ProfessionalService).
- The H1 and the URL.

**Heading structure:**
- H1, then one H2 per section, with H3s for cards.
- No skipped levels.

**Key terms still in the visible copy:**
- Capability Consulting
- Business Analysis & Improvement
- Learning & Workforce Development
- Training Needs Analysis
- DSAT
- learning strategy
- organisational performance
- Defence and public services

**Removed links, and where they are now:**
- The resource anchor links are still on `resources/`.
- The book link is in the Insights menu and the footer.
- The four insight articles are now linked from the Insights page, which also strengthens their internal linking.
- `approach/` is still linked from the homepage (services introduction) and from the Services menu.

No redirects were needed, because no URLs changed.

**Side effect:** the new H2 on Who I Help removes one of the three remaining heading-level skips on the site.

### Tests performed

| Test | Result |
|---|---|
| Build (`python3 build.py`) | Completes; output is deterministic |
| Internal links, whole site | 5,547 checked, none broken (only the serverless routes are unresolved, as before) |
| Heading structure and image `alt` | Homepage passes; site-wide skips down from 3 to 2 |
| Layout at 320, 375, 768, 1024 and 1440 px | No horizontal overflow and no console errors on 32 pages, including the homepage, Who I Help and Insights. One mobile overflow in the founder section was found and fixed during testing. |
| Metadata comparison against the previous homepage | Title, description, canonical, Open Graph and schema identical |
| Visual review | Homepage at 1440 and 375 px; the founder, Insights and Who I Help sections |

**Not tested:** the live Vercel deployment, screen readers, Lighthouse and Core Web Vitals, and browsers other than Chromium. No conversion or performance improvement is claimed.

### For review before deployment

1. **Problems section wording.** The three problems are written from the brief's themes, not from client research. Check that they match the conversations you actually have.
2. **CTA capitalisation.** Buttons keep the site's sentence case ("Discuss a challenge", "Explore our work") rather than the brief's title case, to stay consistent with every other page.
3. **"Explore our work" destination.** It goes to `case-studies.html`, the existing case studies hub.
4. **Second case study.** Healthcare was chosen over Housing and the anonymised SME example for three reasons:
   - it has a full case-study page;
   - it shows scale (around 15,000 colleagues) in a regulated environment;
   - it is clearly not Defence.

   The anonymised SME work is Prelude's own contract but has no full page yet (backlog C7).
5. **DS4D testimonial.** The wording is unchanged. Written permission to use it is still an open action in `03-content-evidence-register.md`.
