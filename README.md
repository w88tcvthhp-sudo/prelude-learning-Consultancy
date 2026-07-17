# Prelude Learning & Consultancy — Website (Jason Smith)

Premium, static, multi-page authority site positioning Jason Smith as a Capability,
Learning & Workforce Development Consultant for Defence, Healthcare, Housing and the
Public Sector. No build dependencies to deploy — plain HTML/CSS/JS/SVG. Brand fonts
(Satoshi & General Sans) load from the Fontshare CDN.

## Pages
- index.html ........................ Home
- defence.html ...................... Defence Capability & DSAT landing page
- services.html ..................... Services (3 grouped categories)
- how-i-work.html ................... Five-stage engagement / what to expect
- capability-readiness-review.html .. The Capability Readiness Review(TM) + interactive diagnostic
- case-studies.html ................. 7 case studies (7-part narrative)
- insights.html ..................... Insights + gated lead-magnet resources
- about.html ........................ About Jason
- contact.html ...................... Discuss Your Capability Challenge

## Shared / assets
- styles.css ........ all styling (brand tokens in :root)
- script.js ......... nav, mobile menu, reveal, accordion, filters, counters
- crr.js ............ Capability Readiness Review self-assessment scoring (CRR page only)
- build.py .......... generator that produces every page from shared parts (optional; run `python3 build.py`)
- assets/logo, assets/icons, assets/favicon.svg
- PHOTOGRAPHY-BRIEF.md . art direction + ready-to-use image prompts for every photo slot

## Proprietary framework graphics (inline SVG, brand-styled)
Capability Readiness Review(TM), Capability Improvement Approach(TM),
Training vs Capability Decision Model(TM), Readiness Maturity Model(TM),
Capability Diagnostic Framework(TM) — used across home, defence, services, how-i-work and the CRR page.

## Deploy to GoDaddy (cPanel)
cPanel -> File Manager -> public_html -> upload prelude-website.zip -> Extract ->
move files out of the prelude-website/ subfolder so index.html sits in public_html
(keep assets/ alongside). Primary domain prelude-learning.com; forward .co.uk and .org to it.

## Before publishing — replace placeholders
- IMAGES: every photo is a styled placeholder. Photoreal images could not be generated
  in the build environment — use PHOTOGRAPHY-BRIEF.md to commission or generate them.
- CONTACT FORM: done. Both the contact form and the resource-request form post to a live Formspree endpoint (https://formspree.io/f/xeeyazed).
- RESOURCE / CRR DOWNLOADS: "Request this resource" links point to the contact page;
  wire to your email tool or a gated form to capture leads. The CRR "Download/print"
  uses the browser print dialog (print-to-PDF) with a dedicated print stylesheet.
- TESTIMONIAL: homepage quote is a marked placeholder — replace with an attributable one.
- ACCURACY/CLEARANCE: confirm all metrics and named programmes (DS4D, OP ISOTROPE) are
  accurate and cleared for public release before going live.
