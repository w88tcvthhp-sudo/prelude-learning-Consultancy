# Free resource PDFs: sources and build

The five free resources are written as HTML and printed to PDF by headless Chromium. Chromium produces tagged PDFs with selectable text, document language (en-GB) and bookmarks generated from the headings.

| Source (edit this) | Output (served by the website) |
|---|---|
| `capability-readiness-playbook.html` | `assets/resources/prelude-capability-readiness-playbook.pdf` |
| `capability-readiness-review-workbook.html` | `assets/resources/prelude-capability-readiness-review-workbook.pdf` |
| `defence-tna-checklist.html` | `assets/resources/prelude-defence-tna-checklist.pdf` |
| `learning-governance-health-check.html` | `assets/resources/prelude-learning-governance-health-check.pdf` |
| `workforce-capability-assessment.html` | `assets/resources/prelude-workforce-capability-assessment.pdf` |

The shared print styles (page size, running header and footer, cover, tables and worksheets) are in `prelude-doc.css`.

## Rebuild

```bash
npm i -D playwright && npx playwright install chromium   # one-off
node resources-src/build-resources.mjs                    # all five
node resources-src/build-resources.mjs playbook           # just one (any part of the file name)
```

After a rebuild, open each PDF and check the page breaks. Then update the page counts in `RESOURCES` in `build.py` and run `python3 build.py`.

## Keeping things consistent

- **Capability Readiness Review workbook.** The workbook must match the online self-assessment. Keep it in step with `CRR_QUESTIONS` and `CRR_OPTS` in `build.py` and with the bands and causes in `crr.js`. Currently that means 10 questions, scored 3/2/1/0, a score of total ÷ 30 × 100, bands at 80, 60 and 40, and any question scored 0 or 1 flagged.
- **Defence TNA Checklist.** It was checked against JSP 822 V7.0 (Volume 2 v3.0, February 2024; GOV.UK page last updated 25 November 2025). Re-check the references whenever JSP 822 is revised.
- **Version and date.** Each document shows its version and date in three places: the cover, the `@page` header string in its `<style>`, and the closing page. Update all three when you issue a new version.

## Fonts

The document template specifies Montserrat (headings) and Source Sans 3 (body). Neither font was available in the build environment, so v1.0 was set in Inter, which is embedded in the PDFs.

To use the brand fonts, put these files in `resources-src/fonts/` and rebuild:

- `Montserrat-SemiBold.ttf`
- `Montserrat-Bold.ttf`
- `SourceSans3-Regular.ttf`
- `SourceSans3-Semibold.ttf`
- `SourceSans3-It.ttf`

Both families are available under the SIL Open Font Licence. Check every page after switching fonts, because the line lengths change.

## Accessibility

The PDFs are tagged and bookmarked, and their text is selectable. They have **not** been validated against PDF/UA or WCAG with a dedicated checker such as PAC 2024. Run that check, and fix whatever it finds, before claiming conformance.

The worksheets are designed for printing or for annotating with a PDF editor. They are not fillable form fields.
