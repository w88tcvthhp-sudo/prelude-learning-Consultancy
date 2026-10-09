# 06 · QA results

Only tests that were actually run are recorded here. Anything not tested is listed as such.

## Phase 1 (9 October 2026)

**Environment:** Linux build environment; Python 3; Playwright with Chromium; site served locally with `python3 -m http.server`. Fontshare and Formspree requests were blocked during browser tests, so fonts fell back to system fonts and no form was submitted.

| Check | Method | Result |
|---|---|---|
| Build | `python3 build.py` | Completes without errors. Running it twice produces identical output. |
| Internal links | Crawl of every `href`, `src`, `srcset` and form `action` in 113 pages, including in-page anchors | 5,555 checked. No broken links. The only unresolved targets are the serverless routes `/api/toolkit-access` and `/api/toolkit-download`, which exist only on Vercel (same as baseline). |
| One H1 per page | Script, 113 pages | Pass. |
| Heading order | Script | 3 pages still skip a level (CRR, Services, Who I Help), down from 5. Backlog S6. |
| Images without `alt`, duplicate IDs, empty links and buttons | Script | None found. The 40 "unlabelled inputs" reported are the CRR radio buttons, which are wrapped in `<label>` elements; this is a limitation of the script, not a defect. |
| Responsive layout and console errors | Playwright at 320, 375, 768, 1024 and 1440 px on 32 representative pages | No horizontal overflow and no JavaScript errors. One overflow on Contact at 320 and 375 px (long option text in the new select) was found and fixed. |
| Outcome figures outside case studies | Regex scan of all pages for the published figures | None outside the eight case-study pages and the case-study hub. |
| Retired terminology | Text search of all pages | No occurrences of Capability Improvement Approach, Capability Diagnostic Framework, Training vs Capability Decision Model, Prelude Capability Model or "Proprietary frameworks". |
| Links to `index.html` | Text search | None (240 at baseline). |
| `vercel.json` | JSON parse; patterns checked against Vercel's documented `source` syntax | Valid JSON. **Not validated by Vercel itself**: the schema and Vercel's tools could not be downloaded from this environment. If the file were invalid, Vercel would fail the deployment and keep the previous version live. |
| Playbook and CRR workbook PDFs (v1.1) | Rebuilt with Chromium; `pdfinfo`, `pdffonts`; pages rendered and inspected | Tagged, fonts embedded, page counts unchanged (23 and 12). A chapter heading that split across a page break was fixed. Not checked with a PDF/UA validator. |
| Visual review | Screenshots of Contact (desktop and mobile), About and the four new framework graphics | Reviewed. The Golden Thread graphic was too large at full width and was constrained. |

**Not tested in Phase 1:** the live site on Vercel (redirect, headers, functions); form submission to Formspree; screen readers; Lighthouse or Core Web Vitals; browsers other than Chromium.

**After pushing, please check on the live site:**

1. `https://www.prelude-learning.com/index.html` redirects to `/`.
2. The homepage, Contact, About and one service page load normally.
3. Send one test enquiry from the Contact page and confirm it arrives with the new fields.
4. The book toolkit access form still works.
