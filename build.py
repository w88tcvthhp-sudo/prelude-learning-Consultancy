#!/usr/bin/env python3
"""Generates the static HTML pages for the Prelude site from shared parts.
Run:  python3 build.py   (outputs *.html into this folder)."""
import os
import json

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2.4" aria-hidden="true"><path d="M4 12l5 5L20 6"/></svg>'
CROSS = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2.4" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

SECTOR_LINKS = [
    ("defence.html", "Defence", "defence"),
    ("healthcare.html", "Healthcare", "healthcare"),
    ("housing.html", "Housing", "housing"),
    ("public-sector.html", "Public Sector", "public-sector"),
    ("professional-services.html", "Professional Services", "professional-services"),
]

NAVLINKS = [
    ("services.html", "Services", "services"),
    ("who-i-help.html", "Who I Help", "who-i-help"),
    ("how-i-work.html", "How I Work", "how-i-work"),
    ("case-studies.html", "Case Studies", "case-studies"),
    ("insights.html", "Insights", "insights"),
    ("about.html", "About", "about"),
    ("contact.html", "Contact", "contact"),
]

# ------------------------------------------------------------------ SEO / schema
SITE_URL = "https://www.prelude-learning.com"
OG_IMAGE = f"{SITE_URL}/assets/og/prelude-og-image.jpg"

ORG_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "@id": f"{SITE_URL}/#organization",
    "name": "Prelude Learning & Consultancy",
    "alternateName": "Prelude Learning & Consultancy Ltd",
    "url": SITE_URL,
    "logo": f"{SITE_URL}/assets/logo/prelude-logo-primary.svg",
    "image": OG_IMAGE,
    "description": "Capability, readiness and workforce development consultancy for Defence, Healthcare, Housing, the Public Sector and Professional Services. DSAT and JSP 822 specialists.",
    "email": "jason.smith@prelude-learning.com",
    "areaServed": "GB",
    "address": {"@type": "PostalAddress", "addressCountry": "GB"},
    "identifier": {"@type": "PropertyValue", "propertyID": "UK Companies House", "value": "16918049"},
    "knowsAbout": ["Capability Development", "Learning Strategy", "Performance Consulting",
                   "Leadership Development", "Defence DSAT", "JSP 822", "Training Governance",
                   "Workforce Development", "Organisational Development", "Learning Technology"],
    "founder": {
        "@type": "Person",
        "@id": f"{SITE_URL}/about.html#person",
        "name": "Jason Smith",
        "jobTitle": "Founder & Capability Advisor",
        "image": f"{SITE_URL}/assets/photos/professional-photograph-of-jason-smith.jpeg",
        "worksFor": {"@type": "Organization", "name": "Prelude Learning & Consultancy Ltd"},
        "knowsAbout": ["Capability Development", "Learning Strategy", "Performance Consulting",
                       "Leadership Development", "Defence DSAT", "JSP 822", "Training Governance",
                       "Workforce Development", "Organisational Development"]
    }
}
ORG_SCHEMA_JSON = json.dumps(ORG_SCHEMA, indent=2)

def breadcrumb_schema(canonical_url, name):
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": canonical_url},
        ]
    }
    return json.dumps(data, indent=2)

def faq_schema(items):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ]
    }
    return json.dumps(data, indent=2)

def faq_section(items, heading="Frequently asked questions"):
    body = ""
    for i, (q, a) in enumerate(items):
        op = " open" if i == 0 else ""
        body += f'''      <div class="acc-item faq{op}">
        <button class="acc-head"><span class="acc-title">{q}</span><span class="plus" aria-hidden="true"></span></button>
        <div class="acc-body"><div class="acc-body-inner">
          <div class="acc-block"><p>{a}</p></div>
        </div></div>
      </div>
'''
    return f'''<section>
  <div class="wrap">
    <div class="eyebrow reveal">FAQs</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">{heading}</p>
    <div class="accordion">
{body}    </div>
  </div>
</section>
'''

def article_schema(headline, description, canonical_url):
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": description,
        "author": {"@type": "Person", "name": "Jason Smith"},
        "publisher": {
            "@type": "Organization",
            "name": "Prelude Learning & Consultancy Ltd",
            "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/assets/logo/prelude-logo-primary.svg"}
        },
        "mainEntityOfPage": canonical_url,
        "image": OG_IMAGE,
    }
    return json.dumps(data, indent=2)

def defined_term_set_schema(name, description, canonical_url, terms):
    data = {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "name": name,
        "description": description,
        "url": canonical_url,
        "hasDefinedTerm": [
            {
                "@type": "DefinedTerm",
                "name": term,
                "description": definition,
                "url": f"{canonical_url}#{slug}",
                "inDefinedTermSet": canonical_url
            }
            for slug, term, definition, _href, _label in terms
        ]
    }
    return json.dumps(data, indent=2)

def head(filename, title, desc, keywords="", og="website", breadcrumb=None, faq=None, article=None, noindex=False, terms=None):
    kw = f'\n<meta name="keywords" content="{keywords}">' if keywords else ""
    canonical_url = SITE_URL + "/" if filename == "index.html" else f"{SITE_URL}/{filename}"
    canonical = f'\n<link rel="canonical" href="{canonical_url}">'
    robots = '\n<meta name="robots" content="noindex,follow">' if noindex else ""
    schema_scripts = f'<script type="application/ld+json">\n{ORG_SCHEMA_JSON}\n</script>'
    if breadcrumb:
        schema_scripts += f'\n<script type="application/ld+json">\n{breadcrumb_schema(canonical_url, breadcrumb)}\n</script>'
    if terms:
        schema_scripts += f'\n<script type="application/ld+json">\n{defined_term_set_schema(title, desc, canonical_url, terms)}\n</script>'
    if faq:
        schema_scripts += f'\n<script type="application/ld+json">\n{faq_schema(faq)}\n</script>'
    if article:
        schema_scripts += f'\n<script type="application/ld+json">\n{article_schema(article[0], article[1], canonical_url)}\n</script>'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#081D16">
<title>{title}</title>
<meta name="description" content="{desc}">{kw}{canonical}{robots}
<meta property="og:type" content="{og}">
<meta property="og:site_name" content="Prelude Learning &amp; Consultancy">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical_url}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&f[]=general-sans@400,500,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
{schema_scripts}
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
'''

def nav(active):
    sector_keys = [k for _, _, k in SECTOR_LINKS]
    sector_active = active in sector_keys
    drop_links = ""
    for href, label, key in SECTOR_LINKS:
        cls = ' class="active"' if key == active else ""
        drop_links += f'        <a href="{href}"{cls}>{label}</a>\n'
    links = ""
    for href, label, key in NAVLINKS:
        cls = ' class="active"' if key == active else ""
        links += f'      <a href="{href}"{cls}>{label}</a>\n'
    drop_btn_cls = ' active' if sector_active else ''
    return f'''<nav id="nav">
  <div class="wrap nav-inner">
    <a href="index.html" class="logo" aria-label="Prelude home">
      <img src="assets/logo/prelude-icon.svg" alt="Prelude" width="34" height="34">
      <span class="mark">PRELUDE<span>Learning &amp; Consultancy</span></span>
    </a>
    <div class="nav-links" id="navLinks">
      <div class="nav-item has-dropdown">
        <button class="nav-drop-btn{drop_btn_cls}" aria-expanded="false" aria-haspopup="true">Sectors <svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
        <div class="nav-dropdown">
{drop_links}        </div>
      </div>
{links}      <a href="capability-readiness-review.html" class="nav-cta">Capability Review</a>
    </div>
    <div class="burger" id="burger" role="button" tabindex="0" aria-label="Menu"><span></span><span></span><span></span></div>
  </div>
</nav>
'''

def cta(title, text, secondary=None):
    sec = ""
    if secondary:
        sec = f'      <a href="{secondary[1]}" class="btn btn-ghost">{secondary[0]}</a>\n'
    return f'''<section class="cta-band">
  <div class="wrap">
    <h2 class="reveal">{title}</h2>
    <p class="reveal" data-d="1">{text}</p>
    <div class="cta-actions reveal" data-d="2">
      <a href="contact.html#book" class="btn btn-primary">Discuss Your Capability Challenge {ARROW}</a>
{sec}    </div>
  </div>
</section>
'''

METHOD_STEPS = [
    ("01", "Understand the Mission", "Get clear on what the organisation actually needs to achieve, and the standard performance has to meet."),
    ("02", "Analyse the Capability Gap", "Measure the real distance between current capability and what the mission demands — with evidence, not assumption."),
    ("03", "Identify Root Causes", "Separate genuine training needs from problems of structure, governance, leadership or process."),
    ("04", "Design the Right Intervention", "Build the solution that fits the cause — learning where it helps, but also structure, assurance or workforce design."),
    ("05", "Measure Impact", "Track the outcomes that matter: readiness, performance, compliance, completion and time-to-competence."),
    ("06", "Improve Continuously", "Feed results back in, so capability keeps improving rather than decaying once the project ends."),
]

def methodology(intro=True):
    steps = ""
    for n, t, p in METHOD_STEPS:
        steps += f'      <div class="mstep reveal"><div class="mnum">{n}</div><h3>{t}</h3><p>{p}</p></div>\n'
    lead = ('    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">'
            'A proprietary, repeatable method for turning capability problems into measurable performance.</p>\n') if intro else ""
    return f'''<section>
  <div class="wrap">
    <div class="eyebrow reveal">The Capability Improvement Approach</div>
{lead}    <div class="method-steps">
{steps}    </div>
  </div>
</section>
'''

TRUST_ITEMS = [
    "Active SC Clearance", "Former DV Holder", "Royal Navy Senior Leadership", "Korn Ferry Consultant",
    "Defence DSAT Specialist", "PRINCE2 Practitioner", "CMI Leadership &amp; Coaching",
    "Supported organisations up to 15,000 staff",
]

def trust(heading="Trust &amp; credibility", sub="The clearances, experience and qualifications behind the advice."):
    items = ""
    for t in TRUST_ITEMS:
        items += f'      <div class="trust-item">{CHECK}<span>{t}</span></div>\n'
    return f'''<section>
  <div class="wrap">
    <div class="eyebrow reveal">{heading}</div>
    <p class="lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">{sub}</p>
    <div class="trust-grid reveal" data-d="2">
{items}    </div>
  </div>
</section>
'''

def footer():
    return f'''<footer>
  <div class="wrap">
    <div class="foot-top">
      <div>
        <div class="logo">
          <img src="assets/logo/prelude-icon.svg" alt="Prelude" width="32" height="32" style="width:32px;height:32px">
          <span class="mark">PRELUDE<span>Learning &amp; Consultancy</span></span>
        </div>
        <p class="foot-tag">Jason Smith — Capability, Readiness &amp; Workforce Development Advisor. Training is rarely the problem. Capability is — and that's what I help Defence and public sector organisations build.</p>
        <p class="foot-tag" style="margin-top:14px;color:var(--gold);font-family:var(--display);font-size:13px;letter-spacing:.06em">Active SC · DSAT Specialist · PRINCE2 · CMI</p>
      </div>
      <div class="foot-domains">
        <span>Sectors</span>
        <a href="defence.html">Defence</a>
        <a href="healthcare.html">Healthcare</a>
        <a href="housing.html">Housing</a>
        <a href="public-sector.html">Public Sector</a>
        <a href="professional-services.html">Professional Services</a>
      </div>
      <div class="foot-domains">
        <span>Explore</span>
        <a href="who-i-help.html">Who I Help</a>
        <a href="services.html">Services</a>
        <a href="how-i-work.html">How I Work</a>
        <a href="capability-readiness-review.html">Capability Review</a>
        <a href="case-studies.html">Case Studies</a>
        <a href="why-training-isnt-the-problem.html">Manifesto</a>
        <a href="insights.html">Insights</a>
        <a href="glossary.html">Glossary</a>
        <a href="about.html">About</a>
      </div>
      <div class="foot-domains">
        <span>Contact</span>
        <a href="mailto:jason.smith@prelude-learning.com">jason.smith@prelude-learning.com</a>
        <a href="https://prelude-learning.com">prelude-learning.com</a>
        <a href="contact.html">Enquire</a>
        <a href="privacy.html">Privacy Policy</a>
      </div>
    </div>
    <div class="foot-bottom">
      <p>© <span id="yr"></span> Prelude Learning &amp; Consultancy Ltd. Company No. 16918049. All rights reserved. · <a href="privacy.html" style="color:var(--stone-dim);text-decoration:underline">Privacy Policy</a></p>
      <p>Learning Designed for Impact</p>
    </div>
  </div>
</footer>

<div class="sticky-cta" id="stickyCta">
  <div class="wrap sticky-cta-inner">
    <span class="sticky-cta-text">Ready to talk about your capability challenge?</span>
    <div class="sticky-cta-actions">
      <a href="contact.html#book" class="btn btn-primary">Discuss Your Capability Challenge {ARROW}</a>
      <button class="sticky-cta-close" id="stickyCtaClose" aria-label="Dismiss">&times;</button>
    </div>
  </div>
</div>

<script src="script.js"></script>
</body>
</html>
'''

def proof():
    items = ["Ministry of Defence", "Royal Navy", "Korn Ferry", "NHS &amp; Healthcare", "Housing Associations", "Public Sector"]
    row = "".join(f'<div class="proof-item">{i}</div>' for i in items)
    return f'''<section class="proof">
  <div class="wrap">
    <div class="proof-label">Experience built in high-stakes environments</div>
    <div class="proof-row reveal">{row}</div>
  </div>
</section>
'''

# ------------------------------------------------------------------ frameworks
def framework(tm, title, sub, svg):
    return f'''<div class="framework reveal">
  <div class="fw-trademark">{tm}</div>
  <h3>{title}</h3>
  <p class="fw-sub">{sub}</p>
  {svg}
</div>'''

def fw_readiness_review():
    # hexagonal wheel of the six diagnostic dimensions
    svg = '''<svg class="fw-svg" viewBox="0 0 820 470" role="img" aria-label="Capability Readiness Review: six dimensions assessed around a central readiness score">
  <polygon points="410,90 531,160 531,300 410,370 289,300 289,160" fill="none" stroke="rgba(200,169,106,.25)" stroke-width="1.4"/>
  <g stroke="rgba(200,198,189,.14)" stroke-width="1">
    <line x1="410" y1="230" x2="410" y2="90"/><line x1="410" y1="230" x2="531" y2="160"/><line x1="410" y1="230" x2="531" y2="300"/>
    <line x1="410" y1="230" x2="410" y2="370"/><line x1="410" y1="230" x2="289" y2="300"/><line x1="410" y1="230" x2="289" y2="160"/>
  </g>
  <circle cx="410" cy="230" r="50" fill="rgba(200,169,106,.06)" stroke="rgba(200,169,106,.5)" stroke-width="1.4"/>
  <text class="fw-dg-num" x="410" y="224" text-anchor="middle" font-size="12" letter-spacing="2">READINESS</text>
  <text class="fw-dg-sub" x="410" y="244" text-anchor="middle" font-size="10">score</text>
  <circle cx="410" cy="90" r="8" fill="#C8A96A"/><circle cx="531" cy="160" r="8" fill="#0E7A5A"/><circle cx="531" cy="300" r="8" fill="#C8A96A"/>
  <circle cx="410" cy="370" r="8" fill="#0E7A5A"/><circle cx="289" cy="300" r="8" fill="#C8A96A"/><circle cx="289" cy="160" r="8" fill="#0E7A5A"/>
  <text class="fw-dg-label" x="410" y="66" text-anchor="middle" font-size="16">Capability</text>
  <text class="fw-dg-label" x="553" y="158" text-anchor="start" font-size="16">Leadership</text>
  <text class="fw-dg-label" x="553" y="306" text-anchor="start" font-size="16">Process</text>
  <text class="fw-dg-label" x="410" y="398" text-anchor="middle" font-size="16">Governance</text>
  <text class="fw-dg-label" x="267" y="306" text-anchor="end" font-size="16">Workforce</text>
  <text class="fw-dg-label" x="267" y="158" text-anchor="end" font-size="16">Training</text>
</svg>'''
    return framework("Capability Readiness Review&trade;", "Six dimensions. One real problem.",
                     "Before investing in a solution, the Review tests performance across the six places the problem actually lives.", svg)

def fw_improvement_approach():
    steps = [("01","Mission"),("02","Gap"),("03","Root Cause"),("04","Intervention"),("05","Impact"),("06","Improve")]
    boxes = ""
    x = 8; w = 142; gap = 24
    for i,(n,t) in enumerate(steps):
        boxes += f'<rect x="{x}" y="34" width="{w}" height="84" rx="6" fill="rgba(255,255,255,.02)" stroke="rgba(200,198,189,.16)" stroke-width="1"/>'
        boxes += f'<text class="fw-dg-num" x="{x+18}" y="68" font-size="15">{n}</text>'
        boxes += f'<text class="fw-dg-label" x="{x+18}" y="96" font-size="15">{t}</text>'
        if i < len(steps)-1:
            ax = x+w+gap/2
            boxes += f'<path d="M{x+w+5} 76 h{gap-10}" stroke="#C8A96A" stroke-width="1.4" marker-end="url(#fwar)"/>'
        x += w+gap
    svg = f'''<svg class="fw-svg" viewBox="0 0 1004 150" role="img" aria-label="Capability Improvement Approach: Mission, Gap, Root Cause, Intervention, Impact, Improve">
  <defs><marker id="fwar" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="#C8A96A"/></marker></defs>
  {boxes}
</svg>'''
    return framework("Capability Improvement Approach&trade;", "A repeatable route from problem to performance.",
                     "Every engagement follows the same disciplined path — so improvement is structured, evidenced and sustained.", svg)

def fw_decision_model():
    svg = '''<svg class="fw-svg" viewBox="0 0 820 430" role="img" aria-label="Training vs Capability Decision Model">
  <rect x="285" y="20" width="250" height="58" rx="8" fill="rgba(255,255,255,.02)" stroke="rgba(200,198,189,.2)" stroke-width="1"/>
  <text class="fw-dg-label" x="410" y="54" text-anchor="middle" font-size="15">Performance gap identified</text>
  <line x1="410" y1="78" x2="410" y2="118" stroke="#C8A96A" stroke-width="1.4" marker-end="url(#dm)"/>
  <defs><marker id="dm" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="#C8A96A"/></marker></defs>
  <polygon points="410,124 540,200 410,276 280,200" fill="rgba(200,169,106,.06)" stroke="rgba(200,169,106,.5)" stroke-width="1.4"/>
  <text class="fw-dg-label" x="410" y="194" text-anchor="middle" font-size="14">Is the knowledge</text>
  <text class="fw-dg-label" x="410" y="214" text-anchor="middle" font-size="14">or skill missing?</text>
  <line x1="540" y1="200" x2="640" y2="200" stroke="#0E7A5A" stroke-width="1.4" marker-end="url(#dm)"/>
  <text class="fw-dg-num" x="590" y="190" text-anchor="middle" font-size="12">YES</text>
  <line x1="410" y1="276" x2="410" y2="330" stroke="#0E7A5A" stroke-width="1.4" marker-end="url(#dm)"/>
  <text class="fw-dg-num" x="424" y="306" text-anchor="start" font-size="12">NO</text>
  <rect x="648" y="172" width="160" height="56" rx="8" fill="rgba(14,122,90,.12)" stroke="rgba(14,122,90,.6)" stroke-width="1"/>
  <text class="fw-dg-label" x="728" y="198" text-anchor="middle" font-size="14">Training or</text>
  <text class="fw-dg-label" x="728" y="216" text-anchor="middle" font-size="14">knowledge solution</text>
  <rect x="200" y="330" width="420" height="76" rx="8" fill="rgba(255,255,255,.02)" stroke="rgba(200,169,106,.4)" stroke-width="1"/>
  <text class="fw-dg-num" x="410" y="360" text-anchor="middle" font-size="12" letter-spacing="2">CAPABILITY PROBLEM</text>
  <text class="fw-dg-label" x="410" y="384" text-anchor="middle" font-size="14">Structure &middot; Governance &middot; Leadership &middot; Process</text>
</svg>'''
    return framework("Training vs Capability Decision Model&trade;", "When training isn't the answer.",
                     "A simple test that stops organisations spending on courses when the real issue is structure, governance or leadership.", svg)

def fw_maturity_model():
    levels = [("1","Reactive"),("2","Compliant"),("3","Structured"),("4","Measured"),("5","Optimised")]
    bars = ""
    x = 30; bw = 150; gap = 22; base = 360
    for i,(n,t) in enumerate(levels):
        h = 70 + i*56
        y = base - h
        col = "#C8A96A" if i == len(levels)-1 else "rgba(14,122,90,.55)"
        fill = "rgba(200,169,106,.12)" if i == len(levels)-1 else "rgba(44,74,63,.4)"
        bars += f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" rx="5" fill="{fill}" stroke="{col}" stroke-width="1.4"/>'
        bars += f'<text class="fw-dg-num" x="{x+bw/2}" y="{y-14}" text-anchor="middle" font-size="15">{n}</text>'
        bars += f'<text class="fw-dg-label" x="{x+bw/2}" y="{base+26}" text-anchor="middle" font-size="14">{t}</text>'
        x += bw+gap
    svg = f'''<svg class="fw-svg" viewBox="0 0 890 410" role="img" aria-label="Capability Readiness Maturity Model: Reactive, Compliant, Structured, Measured, Optimised">
  <line x1="20" y1="360" x2="880" y2="360" stroke="rgba(200,198,189,.18)" stroke-width="1"/>
  {bars}
</svg>'''
    return framework("Capability Readiness Maturity Model&trade;", "Know where you are. See where to go.",
                     "Five stages of capability maturity — from reactive and ad-hoc to measured, optimised and continuously improving.", svg)

def fw_prelude_model():
    tiers = ["Mission &amp; Outcomes","Required Capability","Behaviours","Skills &amp; Knowledge","Governance &amp; Assurance","Performance Evidence"]
    x = 60; w = 500; h = 54; gap = 30; y = 16; parts = ""
    for i,t in enumerate(tiers):
        top = (i == 0)
        stroke = "#C8A96A" if top else "rgba(14,122,90,.6)"
        fill = "rgba(200,169,106,.12)" if top else "rgba(44,74,63,.4)"
        cls = "fw-dg-num" if top else "fw-dg-label"
        parts += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        parts += f'<text class="{cls}" x="{x+w/2}" y="{y+h/2+5}" text-anchor="middle" font-size="14.5" letter-spacing="1.5">{t.upper()}</text>'
        if i < len(tiers)-1:
            parts += f'<path d="M{x+w/2} {y+h+4} v{gap-9}" stroke="#C8A96A" stroke-width="1.4" marker-end="url(#pcm)"/>'
        y += h+gap
    vh = y - gap + 16
    svg = f'''<svg class="fw-svg" viewBox="0 0 620 {vh}" role="img" aria-label="Prelude Capability Model: Mission and Outcomes, Required Capability, Behaviours, Skills and Knowledge, Governance and Assurance, Performance Evidence">
  <defs><marker id="pcm" markerWidth="9" markerHeight="9" refX="4.5" refY="4.5" orient="auto"><path d="M0 0 L9 4.5 L0 9 z" fill="#C8A96A"/></marker></defs>
  {parts}
</svg>'''
    return framework("Prelude Capability Model&trade;", "How capability actually delivers performance.",
                     "Our primary framework. Performance is traced from mission down to evidence — when any layer is missing, capability fails, and no amount of training fixes it.", svg)

def snapshot(title, kind="map"):
    # lightweight branded "diagnostic output" visuals used as supporting artefacts
    if kind == "governance":
        body = '''<rect x="240" y="20" width="120" height="40" rx="5" fill="rgba(200,169,106,.12)" stroke="#C8A96A"/><text class="fw-dg-label" x="300" y="44" text-anchor="middle" font-size="12">Board / SRO</text>
  <line x1="300" y1="60" x2="300" y2="84" stroke="rgba(200,198,189,.3)"/><line x1="140" y1="84" x2="460" y2="84" stroke="rgba(200,198,189,.3)"/>
  <line x1="140" y1="84" x2="140" y2="100" stroke="rgba(200,198,189,.3)"/><line x1="300" y1="84" x2="300" y2="100" stroke="rgba(200,198,189,.3)"/><line x1="460" y1="84" x2="460" y2="100" stroke="rgba(200,198,189,.3)"/>
  <rect x="80" y="100" width="120" height="36" rx="5" fill="rgba(44,74,63,.4)" stroke="rgba(14,122,90,.6)"/><text class="fw-dg-sub" x="140" y="122" text-anchor="middle" font-size="11">Assurance</text>
  <rect x="240" y="100" width="120" height="36" rx="5" fill="rgba(44,74,63,.4)" stroke="rgba(14,122,90,.6)"/><text class="fw-dg-sub" x="300" y="122" text-anchor="middle" font-size="11">Delivery</text>
  <rect x="400" y="100" width="120" height="36" rx="5" fill="rgba(44,74,63,.4)" stroke="rgba(14,122,90,.6)"/><text class="fw-dg-sub" x="460" y="122" text-anchor="middle" font-size="11">Policy</text>'''
    elif kind == "architecture":
        body = '''<rect x="40" y="30" width="520" height="30" rx="4" fill="rgba(200,169,106,.1)" stroke="#C8A96A"/><text class="fw-dg-sub" x="300" y="50" text-anchor="middle" font-size="11">Strategic outcomes</text>
  <rect x="40" y="70" width="250" height="60" rx="4" fill="rgba(44,74,63,.4)" stroke="rgba(14,122,90,.6)"/><text class="fw-dg-sub" x="165" y="104" text-anchor="middle" font-size="11">Core pathway</text>
  <rect x="310" y="70" width="250" height="60" rx="4" fill="rgba(44,74,63,.4)" stroke="rgba(14,122,90,.6)"/><text class="fw-dg-sub" x="435" y="104" text-anchor="middle" font-size="11">Role-specific modules</text>'''
    else:  # capability map heat grid
        cells = ""
        import random
        random.seed(7)
        cols = ["Capability","Leadership","Process","Governance","Workforce"]
        for c in range(5):
            cells += f'<text class="fw-dg-sub" x="{70+c*98}" y="24" text-anchor="middle" font-size="10">{cols[c]}</text>'
        op = [0.55,0.25,0.7,0.4,0.85, 0.3,0.6,0.45,0.75,0.5, 0.65,0.35,0.55,0.6,0.4]
        k = 0
        for r in range(3):
            for c in range(5):
                cells += f'<rect x="{30+c*98}" y="{34+r*40}" width="84" height="32" rx="3" fill="rgba(14,122,90,{op[k]})" stroke="rgba(200,198,189,.1)"/>'
                k += 1
        body = cells
    return f'''<div class="framework reveal" style="padding:30px">
  <div class="fw-trademark">Diagnostic output &middot; illustrative</div>
  <h3 style="font-size:1.05rem;margin-bottom:18px">{title}</h3>
  <svg class="fw-svg" viewBox="0 0 600 160" role="img" aria-label="{title}">{body}</svg>
</div>'''

def fw_diagnostic_framework():
    tiers = [("Mission &amp; Outcomes",40,112,60,120),
             ("Required Capability",112,184,120,180),
             ("Behaviours",184,256,180,240),
             ("Evidence",256,328,240,300),
             ("Measurement &amp; Assurance",328,400,300,360)]
    cx = 400; polys = ""
    for i,(t,y0,y1,hw0,hw1) in enumerate(tiers):
        col = "#C8A96A" if i == 0 else "rgba(14,122,90,.55)"
        fill = "rgba(200,169,106,.10)" if i == 0 else "rgba(44,74,63,.34)"
        polys += f'<polygon points="{cx-hw0},{y0} {cx+hw0},{y0} {cx+hw1},{y1} {cx-hw1},{y1}" fill="{fill}" stroke="{col}" stroke-width="1.3"/>'
        polys += f'<text class="fw-dg-label" x="{cx}" y="{(y0+y1)/2+5}" text-anchor="middle" font-size="15">{t}</text>'
    svg = f'''<svg class="fw-svg" viewBox="0 0 800 440" role="img" aria-label="Capability Diagnostic Framework tiers from Mission to Measurement">
  {polys}
</svg>'''
    return framework("Capability Diagnostic Framework&trade;", "Trace performance from mission to measurement.",
                     "Capability only delivers when every layer aligns — outcomes, capability, behaviours, evidence and assurance.", svg)

# ------------------------------------------------------------------ sections
ROLES = ["Defence Programme Leaders","Capability Managers","Heads of Learning &amp; Development","HR Directors",
         "Workforce Development Leads","Transformation Leaders","Training Governance Leads",
         "Defence Digital Programme Managers","NHS Learning Leads","Housing Leadership Teams"]
def roles_section():
    chips = "".join(f'<div class="chip">{r}</div>' for r in ROLES)
    return f'''<section>
  <div class="wrap">
    <div class="eyebrow reveal">Who I work with</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">If this is your role, this is your problem too.</p>
    <div class="aud-grid reveal" data-d="2">{chips}</div>
    <div style="margin-top:30px" class="reveal"><a href="who-i-help.html" class="btn btn-ghost">See how I help your role {ARROW}</a></div>
  </div>
</section>'''

def comparison_section():
    you = ["Direct access to senior expertise","No junior consultants","No generic frameworks",
           "Real operational experience","Defence, Healthcare &amp; Housing expertise","Practical recommendations",
           "Evidence-based approaches","Solutions built around outcomes, not products"]
    them = ["Layers between you and senior people","Delivery handed to junior consultants","Templated, generic frameworks",
            "Limited frontline operational experience","Generalist, sector-agnostic coverage","Theoretical recommendations",
            "Assumption-led approaches","Solutions shaped around the firm's products"]
    yrows = "".join(f'<div class="cmp yes">{CHECK}<span>{x}</span></div>' for x in you)
    trows = "".join(f'<div class="cmp no">{CROSS}<span>{x}</span></div>' for x in them)
    return f'''<section>
  <div class="wrap">
    <div class="eyebrow reveal">Why choose Prelude</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">The senior expertise of a boutique. None of the overheads of a big firm.</p>
    <div class="compare">
      <div class="compare-col you reveal"><h3>Working with Prelude</h3><div class="sub">Senior, specialist, accountable</div>{yrows}</div>
      <div class="compare-col reveal" data-d="1"><h3>A typical large consultancy</h3><div class="sub">Scaled, generalist, layered</div>{trows}</div>
    </div>
  </div>
</section>'''

def crr_teaser():
    return f'''<section>
  <div class="wrap">
    <div class="eyebrow reveal">The first step</div>
    <p class="lead reveal" data-d="1">Most organisations know they have a problem. Few know whether it's <span class="dim">a capability, leadership, process, governance, workforce or training issue. The Capability Readiness Review&trade; identifies the real problem before you invest in the solution.</span></p>
    {fw_readiness_review()}
    <div style="margin-top:34px" class="reveal"><a href="capability-readiness-review.html" class="btn btn-primary">Take the Capability Readiness Review {ARROW}</a></div>
  </div>
</section>'''

def photo(src, alt, w, h):
    return f'<img src="assets/photos/{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" style="width:100%;border-radius:6px">'

def photo_grid(items, cols="3"):
    cells = "".join(photo(src, alt, w, h) for src, alt, w, h in items)
    cls = "photo-grid" + (" cols-2" if cols == "2" else "")
    return f'<div class="{cls} reveal">{cells}</div>'

def page(filename, title, desc, body, active, keywords="", og="website", extra_body="", breadcrumb=None, faq=None, article=None, noindex=False, terms=None):
    html = (head(filename, title, desc, keywords, og, breadcrumb, faq, article, noindex, terms) + nav(active)
            + f'<main id="main">{body}</main>' + extra_body + footer())
    with open(filename, "w") as f:
        f.write(html)
    print("wrote", filename)

# ------------------------------------------------------------------ helpers
def acc_item(num, title, ch, appr, out, ex, is_open=False, slug=None):
    chli = "".join(f"<li>{x}</li>" for x in ch)
    outli = "".join(f"<li>{x}</li>" for x in out)
    op = " open" if is_open else ""
    read_more = f'<div class="acc-block full"><a class="read" href="{slug}.html">Full service page: problem, approach, deliverables &amp; FAQs {ARROW}</a></div>' if slug else ""
    return f'''      <div class="acc-item{op}">
        <button class="acc-head"><span class="acc-num">{num}</span><span class="acc-title">{title}</span><span class="plus" aria-hidden="true"></span></button>
        <div class="acc-body"><div class="acc-body-inner">
          <div class="acc-block"><h4>Client challenges</h4><ul>{chli}</ul></div>
          <div class="acc-block"><h4>My approach</h4><p>{appr}</p></div>
          <div class="acc-block"><h4>Outcomes</h4><ul>{outli}</ul></div>
          <div class="acc-block"><h4>Example</h4><p>{ex}</p></div>
          {read_more}
        </div></div>
      </div>
'''

def buyer_acc(num, role, challenges, mistakes, outcomes, help_, is_open=False):
    chli = "".join(f"<li>{x}</li>" for x in challenges)
    outli = "".join(f"<li>{x}</li>" for x in outcomes)
    op = " open" if is_open else ""
    return f'''      <div class="acc-item{op}">
        <button class="acc-head"><span class="acc-num">{num}</span><span class="acc-title">{role}</span><span class="plus" aria-hidden="true"></span></button>
        <div class="acc-body"><div class="acc-body-inner">
          <div class="acc-block"><h4>Typical challenges</h4><ul>{chli}</ul></div>
          <div class="acc-block"><h4>Common mistakes</h4><p>{mistakes}</p></div>
          <div class="acc-block"><h4>Desired outcomes</h4><ul>{outli}</ul></div>
          <div class="acc-block"><h4>How Prelude helps</h4><p>{help_}</p></div>
        </div></div>
      </div>
'''

def case(sector_attr, sector_label, title, metric_fig, metric_label, problem, why, found, did, results, benefit, lessons, photo_src, photo_alt, photo_w, photo_h, count=None, suffix="", slug=None):
    didli = "".join(f"<li>{x}</li>" for x in did)
    resli = "".join(f"<li>{x}</li>" for x in results)
    if count:
        static_val = f'{int(count):,}<span class="unit">{suffix}</span>'
        fig = f'<div class="figure" data-count="{count}" data-suffix="{suffix}">{static_val}</div>'
    else:
        fig = f'<div class="figure">{metric_fig}</div>'
    read_more = f'<div class="cb"><a class="read" href="{slug}.html">Full case study: deliverables, commercial impact &amp; transferability {ARROW}</a></div>' if slug else ""
    return f'''    <article class="case reveal" data-sector="{sector_attr}">
      <div class="case-aside">
        <div class="case-sector">{sector_label}</div>
        <h3>{title}</h3>
        <div class="case-metric">{fig}<div class="label">{metric_label}</div></div>
        <img src="assets/photos/{photo_src}" alt="{photo_alt}" width="{photo_w}" height="{photo_h}" loading="lazy" style="width:100%;border-radius:6px;margin-top:18px">
      </div>
      <div class="case-body">
        <div class="cb"><h4>The problem</h4><p>{problem}</p></div>
        <div class="cb"><h4>Why it mattered</h4><p>{why}</p></div>
        <div class="cb"><h4>What I found</h4><p>{found}</p></div>
        <div class="cb"><h4>What I did</h4><ul>{didli}</ul></div>
        <div class="cb"><h4>Results</h4><ul>{resli}</ul></div>
        <div class="cb"><h4>Client benefit</h4><p>{benefit}</p></div>
        <div class="cb"><h4>Lessons learned</h4><p>{lessons}</p></div>
        {read_more}
      </div>
    </article>
'''

# ================================================================== HOME
home_body = f'''<header id="top">
  <svg class="ref-motif" viewBox="0 0 880 880" aria-hidden="true">
    <g class="rotate-slow">
      <line class="spoke" x1="440" y1="40" x2="440" y2="840"/><line class="spoke" x1="40" y1="440" x2="840" y2="440"/>
      <line class="spoke" x1="156" y1="156" x2="724" y2="724"/><line class="spoke" x1="724" y1="156" x2="156" y2="724"/>
    </g>
    <circle class="ring" cx="440" cy="440" r="380"/><circle class="ring em" cx="440" cy="440" r="280"/>
    <circle class="ring" cx="440" cy="440" r="180"/><circle class="ring" cx="440" cy="440" r="90"/>
    <circle class="ring em pulse" cx="440" cy="440" r="120"/>
    <circle class="node" cx="440" cy="440" r="7"/><circle class="node-em" cx="440" cy="160" r="5"/>
    <circle class="node" cx="720" cy="440" r="4"/><circle class="node-em" cx="252" cy="628" r="4"/><circle class="node" cx="628" cy="252" r="3.5"/>
  </svg>
  <div class="wrap hero-content">
    <div class="eyebrow reveal in">Capability · Learning · Workforce Development</div>
    <h1 class="reveal in" data-d="1">Solving Capability Problems <span class="gold">Training Alone Can't Fix.</span></h1>
    <p class="hero-sub reveal in" data-d="2">Training is rarely the problem. Capability is. When readiness slips, compliance fails or managers aren't performing, the cause is almost never a missing course. As a capability, readiness and workforce development advisor, I diagnose the real problem first — then use learning as one of several tools to fix it. 23+ years, DSAT specialist, Active SC clearance.</p>
    <div class="hero-actions reveal in" data-d="3">
      <a href="contact.html#book" class="btn btn-primary">Discuss Your Capability Challenge {ARROW}</a>
      <a href="case-studies.html" class="btn btn-ghost">View Case Studies</a>
    </div>
  </div>
  <div class="scroll-hint"><span class="line"></span>Scroll</div>
</header>

{proof()}
<section style="padding-top:84px">
  <div class="wrap">
    <div class="eyebrow reveal">Track record</div>
    <p class="lead reveal" data-d="1">Evidence, not promises.</p>
    <div class="metric-grid reveal" data-d="2">
      <div class="metric"><div class="figure" data-count="15000">15,000</div><div class="label">Employees supported across a single organisation</div></div>
      <div class="metric"><div class="figure" data-count="25" data-suffix="%">25<span class="unit">%</span></div><div class="label">Improvement in operational performance (up to)</div></div>
      <div class="metric"><div class="figure" data-count="95" data-suffix="%">95<span class="unit">%</span></div><div class="label">Apprenticeship completion rate</div></div>
      <div class="metric"><div class="figure" data-count="100" data-suffix="%">100<span class="unit">%</span></div><div class="label">Funding compliance</div></div>
      <div class="metric"><div class="figure">5 <span class="unit">sectors</span></div><div class="label">Defence, Healthcare, Housing, Public Sector &amp; Professional Services</div></div>
      <div class="metric"><div class="figure">Active <span class="unit">SC</span></div><div class="label">Security clearance held (former DV)</div></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <p class="lead reveal">Training is rarely the problem. Capability is. <span class="dim">When performance slips, most organisations commission a course before they understand the problem. Capability comes from people, behaviours, governance, leadership, structure, assurance and learning working together — so I diagnose before I prescribe.</span></p>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Our intellectual property</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">The model behind every engagement.</p>
    {fw_prelude_model()}
  </div>
</section>

<section style="padding-top:24px">
  <div class="wrap">
    <div class="eyebrow reveal">Common challenges I help solve</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">If you recognise your organisation here, we should talk.</p>
    <div class="challenge-grid">
      <div class="challenge-col reveal">
        <div class="ch-head"><img src="assets/icons/sector-defence.svg" alt=""><h3>Defence</h3></div>
        <ul><li>Training governance concerns</li><li>DSAT compliance requirements</li><li>Digital skills capability gaps</li><li>Operational readiness challenges</li><li>Workforce capability issues</li></ul>
        <a class="ch-foot" href="defence.html">Defence capability &amp; DSAT consultancy →</a>
      </div>
      <div class="challenge-col reveal" data-d="1">
        <div class="ch-head"><img src="assets/icons/sector-healthcare.svg" alt=""><h3>Healthcare</h3></div>
        <ul><li>Compliance performance</li><li>Mandatory training effectiveness</li><li>Leadership capability</li><li>Learning technology challenges</li><li>Workforce development</li></ul>
        <a class="ch-foot" href="healthcare.html">Healthcare &amp; NHS consultancy →</a>
      </div>
      <div class="challenge-col reveal" data-d="2">
        <div class="ch-head"><img src="assets/icons/sector-housing.svg" alt=""><h3>Housing</h3></div>
        <ul><li>Manager onboarding</li><li>Succession planning</li><li>Cultural transformation</li><li>Service standards</li><li>Workforce capability</li></ul>
        <a class="ch-foot" href="housing.html">Housing association consultancy →</a>
      </div>
      <div class="challenge-col reveal">
        <div class="ch-head"><img src="assets/icons/sector-public.svg" alt=""><h3>Public Sector</h3></div>
        <ul><li>Role &amp; workforce redesign</li><li>Transformation capability</li><li>Leadership under pressure</li><li>Training governance for public money</li><li>Restructuring at pace</li></ul>
        <a class="ch-foot" href="public-sector.html">Public sector consultancy →</a>
      </div>
      <div class="challenge-col reveal" data-d="1">
        <div class="ch-head"><img src="assets/icons/leadership.svg" alt=""><h3>Professional Services</h3></div>
        <ul><li>Partner-track leadership</li><li>Associate retention</li><li>Onboarding speed</li><li>Progression frameworks</li><li>Capability through growth</li></ul>
        <a class="ch-foot" href="professional-services.html">Professional services consultancy →</a>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

{crr_teaser()}
<div class="divider"></div>

{methodology()}
<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Selected work</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Problems I've solved in environments like yours.</p>
    <div class="feature-grid">
      <div class="feature-card reveal"><span class="tag-pill">Defence</span><h3>MOD Digital Skills for Defence (DS4D)</h3><p>Enterprise-wide digital capability analysis and DSAT-aligned TNA used for Defence-wide planning.</p></div>
      <div class="feature-card reveal" data-d="1"><span class="tag-pill">Defence</span><h3>Capability Framework Design</h3><p>A multi-specialisation framework and skills mapping that lifted operational readiness by 20%.</p></div>
      <div class="feature-card reveal" data-d="2"><span class="tag-pill">Healthcare</span><h3>Healthcare Learning Transformation</h3><p>Totara dashboards across 15,000 colleagues, cutting compliance gaps by 18%.</p></div>
    </div>
    <div style="margin-top:40px" class="reveal"><a href="case-studies.html" class="btn btn-ghost">View all case studies {ARROW}</a></div>
  </div>
</section>

<div class="divider"></div>

{roles_section()}
<div class="divider"></div>

{comparison_section()}
<div class="divider"></div>

{trust(heading="Why you can trust me", sub="Senior defence leadership experience, the right clearances, and recognised qualifications.")}
<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">In their words</div>
    <div class="quote-block reveal" data-d="1">
      <p>"In ten weeks, Jason and his team achieved more progress on the DS4D programme than had been delivered in the previous twelve months. Their ability to cut through complexity, identify the real capability issues, and turn analysis into practical action accelerated the programme significantly."</p>
      <cite>Senior Client · Digital Skills for Defence (DS4D)</cite>
    </div>
    <p class="muted reveal" data-d="2" style="margin-top:18px">Further references available on request across Defence, Healthcare and Housing.</p>
  </div>
</section>

{cta("Let's discuss your capability challenge.", "A practical, problem-first conversation — no sales pitch. We'll work out what's really going on and whether I can help.", secondary=("Explore services", "services.html"))}'''

# ================================================================== DEFENCE
DEFENCE_FAQ = [
    ("Is your DSAT knowledge current, or from years ago?", "Current. DSAT and JSP 822 application is ongoing specialist work, not a historic qualification — I keep pace with how the policy is actually being applied and audited today."),
    ("Can you move at pace without cutting governance corners?", "Yes — this is exactly what the Senior Information Officer (SIO) Rapid TNA case study demonstrates. Used as a decision-support framework rather than a box-ticking process, DSAT can move fast without losing defensibility."),
    ("What clearance do you hold, and is it enough for our programme?", "I hold Active SC clearance and am a former DV holder, and I'm comfortable operating in secure, regulated environments. If your programme needs a different level of vetting, tell me early and we'll work out whether that's achievable."),
    ("Do you work with prime contractors, or only direct with MOD?", "Both. I've supported enterprise-wide MOD programmes directly and worked alongside prime contractors and Front Line Commands on specific capability, TNA and governance workstrands."),
    ("How long does a typical Defence engagement take?", "It depends on the problem: a rapid TNA can be delivered in weeks; an enterprise capability framework or DSAT governance rebuild is typically a multi-month engagement. The Capability Readiness Review at the start gives both of us a realistic view before committing to scope."),
]

defence_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">Defence Capability &amp; DSAT Consultancy</div>
    <h1 class="reveal in" data-d="1">DSAT, governance and capability — from someone who's served.</h1>
    <p class="hero-sub reveal in" data-d="2">Specialist support for the Ministry of Defence, Defence Digital, DE&amp;S, Front Line Commands and prime contractors — covering JSP 822, training governance, Training Needs Analysis, capability frameworks, readiness and learning assurance.</p>
    <div class="hero-actions reveal in" data-d="3">
      <a href="contact.html#book" class="btn btn-primary">Discuss Your Capability Challenge {ARROW}</a>
      <a href="case-studies.html" class="btn btn-ghost">Defence case studies</a>
    </div>
  </div>
</header>

{proof()}
<section style="padding-top:84px">
  <div class="wrap">
    <div class="eyebrow reveal">Who I work with</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Built for Defence — at the enterprise and the front line.</p>
    <div class="proof-row reveal" data-d="2" style="justify-content:flex-start;margin-top:30px">
      <div class="proof-item">Ministry of Defence</div><div class="proof-item">Defence Digital</div><div class="proof-item">DE&amp;S</div><div class="proof-item">Front Line Commands</div><div class="proof-item">Prime Contractors</div>
    </div>
    {photo_grid([
      ("defence-operational-planning-briefing.jpeg", "Senior leaders reviewing operational plans", 638, 360),
      ("defence-operations-centre-interior.jpeg", "Defence headquarters — operations centre interior", 638, 360),
      ("defence-training-governance-workshop.jpeg", "Training governance workshop in session", 1000, 562),
    ], cols="3")}
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Defence consultancy services</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">DSAT and capability expertise, applied to your operating environment.</p>
    <div class="feature-grid">
      <div class="feature-card reveal"><img src="assets/icons/governance.svg" alt=""><h3>JSP 822 Expertise</h3><p>Practical, current application of JSP 822 and the Defence Systems Approach to Training — without drowning teams in process.</p></div>
      <div class="feature-card reveal" data-d="1"><img src="assets/icons/assurance.svg" alt=""><h3>DSAT Consultancy</h3><p>End-to-end DSAT support, from analysis and design through to governance and assurance.</p></div>
      <div class="feature-card reveal" data-d="2"><img src="assets/icons/strategy.svg" alt=""><h3>Training Needs Analysis</h3><p>DSAT-compliant TNA that separates real training need from capability, structure and process issues.</p></div>
      <div class="feature-card reveal"><img src="assets/icons/capability.svg" alt=""><h3>Capability Frameworks</h3><p>Multi-specialisation competency frameworks and skills mapping for assessment and workforce planning.</p></div>
      <div class="feature-card reveal" data-d="1"><img src="assets/icons/sector-defence.svg" alt=""><h3>Training Governance</h3><p>Audit-ready governance and clear decision rights across providers, sites and the training pipeline.</p></div>
      <div class="feature-card reveal" data-d="2"><img src="assets/icons/readiness.svg" alt=""><h3>Readiness Assessment</h3><p>Evidence-based assessment of whether people, roles and competencies are aligned to operational demand.</p></div>
      <div class="feature-card reveal"><img src="assets/icons/insight.svg" alt=""><h3>Learning Assurance</h3><p>Assurance that learning is effective, compliant and defensible — supporting the mission, not just the inspection.</p></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Proprietary frameworks</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">The thinking I bring to every Defence engagement.</p>
    {fw_prelude_model()}
    {fw_decision_model()}
    {fw_diagnostic_framework()}
  </div>
</section>

<div class="divider"></div>

{methodology()}
<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Defence track record</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Delivered across MOD, Royal Navy and NATO programmes.</p>
    <div class="feature-grid">
      <div class="feature-card reveal"><span class="tag-pill">DS4D</span><h3>Digital Skills for Defence</h3><p>DSAT-aligned capability analysis, TNA and learning architecture adopted for Defence-wide planning.</p></div>
      <div class="feature-card reveal" data-d="1"><span class="tag-pill">+20% readiness</span><h3>Capability Framework Design</h3><p>Consistent competency standards that increased operational readiness by 20%.</p></div>
      <div class="feature-card reveal" data-d="2"><span class="tag-pill">+17% pass rates</span><h3>NATO &amp; Royal Navy Modernisation</h3><p>DSAT-compliant TNA, blended learning and coaching — 17% higher pass rates, 20% fewer failures.</p></div>
    </div>
    <div style="margin-top:40px" class="reveal"><a href="case-studies.html" class="btn btn-ghost">All Defence case studies {ARROW}</a></div>
  </div>
</section>

<div class="divider"></div>

{trust(heading="Cleared and credible", sub="Active SC clearance, senior Royal Navy leadership, and DSAT specialism.")}
<div class="divider"></div>

{faq_section(DEFENCE_FAQ, "Common questions from Defence programme teams.")}
{cta("Need DSAT or capability support?", "Tell me what you're facing — JSP 822, governance, TNA or readiness. A practical conversation, no sales pitch.", secondary=("View services", "services.html"))}'''

# ================================================================== HEALTHCARE
HEALTHCARE_FAQ = [
    ("We already run mandatory training — why aren't our compliance gaps closing?", "Because compliance gaps are usually a data, governance or system problem, not a course-completion problem. Adding more mandatory training rarely fixes unreliable reporting or unclear ownership — diagnosing where the real gap sits usually does."),
    ("Do you work directly with NHS trusts, or only through suppliers?", "Both. I work directly with trusts, Integrated Care Boards and independent providers, and alongside existing suppliers where that's the better fit for your organisation."),
    ("Can you improve our Totara or LMS reporting without a full platform replacement?", "In most cases, yes. The healthcare work behind this site's case studies was configuration, dashboards and information management — not a re-platform. A new system is rarely the fix; trustworthy data and clear pathways usually are."),
    ("What clearance or information governance standards do you work to?", "I hold Active SC clearance and I'm comfortable in regulated, audited environments. Tell me your information governance requirements early and we'll agree how to work within them."),
    ("How is this different from a generic healthcare training provider?", "I don't sell courses. The first step is always diagnosis — working out whether the real issue is training, data, leadership, governance or process — before recommending anything. Training is one tool among several, not the default answer."),
]

healthcare_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">Healthcare &amp; NHS Capability Consultancy</div>
    <h1 class="reveal in" data-d="1">Compliance you can trust. Learning that changes practice.</h1>
    <p class="hero-sub reveal in" data-d="2">Specialist support for NHS trusts, Integrated Care Boards and independent healthcare providers — covering compliance assurance, learning technology, workforce capability and leadership development for clinical and operational managers.</p>
    <div class="hero-actions reveal in" data-d="3">
      <a href="contact.html#book" class="btn btn-primary">Discuss Your Capability Challenge {ARROW}</a>
      <a href="case-studies.html" class="btn btn-ghost">Healthcare case study</a>
    </div>
  </div>
</header>

{proof()}
<section style="padding-top:84px">
  <div class="wrap">
    <div class="eyebrow reveal">Who I work with</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Built for healthcare providers under real regulatory pressure.</p>
    <div class="proof-row reveal" data-d="2" style="justify-content:flex-start;margin-top:30px">
      <div class="proof-item">NHS Trusts</div><div class="proof-item">Integrated Care Boards</div><div class="proof-item">Community &amp; Mental Health Providers</div><div class="proof-item">Independent Healthcare Providers</div>
    </div>
    {photo_grid([
      ("healthcare-nhs-strategy-meeting.jpeg", "NHS leadership team in a strategy planning meeting", 638, 360),
      ("healthcare-clinician-lms-tablet.jpeg", "Clinician reviewing learning pathways on a tablet device", 540, 360),
      ("healthcare-workforce-planning-meeting.jpeg", "Compliance dashboard review in a workforce planning meeting", 1000, 562),
    ], cols="3")}
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Healthcare consultancy services</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Capability expertise, applied to regulated clinical and operational environments.</p>
    <div class="feature-grid">
      <div class="feature-card reveal"><img src="assets/icons/assurance.svg" alt=""><h3>Compliance &amp; Mandatory Training Assurance</h3><p>Diagnosing whether compliance gaps sit in training, data or governance — before recommending more mandatory courses.</p></div>
      <div class="feature-card reveal" data-d="1"><img src="assets/icons/systems.svg" alt=""><h3>Learning Technology &amp; LMS Optimisation</h3><p>Totara and LMS dashboards, pathways and information management that turn your platform into trustworthy capability intelligence.</p></div>
      <div class="feature-card reveal" data-d="2"><img src="assets/icons/capability.svg" alt=""><h3>Workforce Capability &amp; Planning</h3><p>Mapping workforce capability against clinical and operational demand, so planning is evidence-based, not assumption-led.</p></div>
      <div class="feature-card reveal"><img src="assets/icons/leadership.svg" alt=""><h3>Leadership Development</h3><p>Leadership and management development for clinical and operational managers, grounded in high-pressure operational experience.</p></div>
      <div class="feature-card reveal" data-d="1"><img src="assets/icons/governance.svg" alt=""><h3>Training Governance &amp; Audit Readiness</h3><p>Governance and assurance that stands up to CQC and internal audit scrutiny — useful to leaders, not just inspectors.</p></div>
      <div class="feature-card reveal" data-d="2"><img src="assets/icons/development.svg" alt=""><h3>Digital Learning Adoption</h3><p>Blended and digital learning designed for adoption and behaviour change, not just completion rates.</p></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Proprietary frameworks</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">The thinking I bring to every healthcare engagement.</p>
    {fw_prelude_model()}
    {fw_decision_model()}
  </div>
</section>

<div class="divider"></div>

{methodology()}
<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Healthcare track record</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Reliable data changes behaviour faster than more mandatory training.</p>
    <div class="feature-grid">
      <div class="feature-card reveal"><span class="tag-pill">-18% compliance gaps</span><h3>Healthcare Learning Transformation</h3><p>Totara dashboards and structured pathways across 15,000 colleagues, cutting compliance gaps by 18% and giving leaders visibility they could trust.</p></div>
    </div>
    <div style="margin-top:40px" class="reveal"><a href="case-studies.html" class="btn btn-ghost">All case studies {ARROW}</a></div>
  </div>
</section>

<div class="divider"></div>

{trust(heading="Cleared and credible", sub="Active SC clearance and experience operating in regulated, audited environments.")}
<div class="divider"></div>

{faq_section(HEALTHCARE_FAQ, "Common questions from healthcare and NHS leaders.")}
{cta("Need healthcare capability or compliance support?", "Tell me what you're facing — compliance, LMS, leadership or workforce planning. A practical conversation, no sales pitch.", secondary=("View services", "services.html"))}'''

# ================================================================== HOUSING
HOUSING_FAQ = [
    ("Our managers are experienced but inconsistent — is that a training problem?", "Usually not. Inconsistent management is more often a sign that expectations and standards were never written down, not that managers lack skills. The fix is usually structure and clarity, with development layered on top — not a course on its own."),
    ("How quickly can new starters become productive?", "The Housing Leadership &amp; Onboarding Transformation case study cut time-to-competence by 20% — by designing values and expectations into onboarding deliberately, rather than leaving new managers to learn by chance."),
    ("Do you work with ALMOs and combined authority housing teams, as well as traditional housing associations?", "Yes. The same capability thinking applies whether you're a large G15 housing association, a smaller regional provider, or an ALMO managing stock on behalf of a local authority."),
    ("Can this work alongside our existing L&D team rather than replacing it?", "That's the usual arrangement. I work as a diagnostic and design partner alongside your existing team's capacity, not as a replacement for it."),
    ("What size of organisation do you typically work with?", "From housing associations with a few hundred staff to organisations managing tens of thousands of homes. The Capability Readiness Review scales to the size of the problem, not a fixed engagement size."),
]

housing_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">Housing Association Capability Consultancy</div>
    <h1 class="reveal in" data-d="1">Managers who are ready on day one. Onboarding that doesn't rely on luck.</h1>
    <p class="hero-sub reveal in" data-d="2">Specialist support for housing associations, ALMOs and local authority housing teams — covering manager onboarding, leadership development, succession planning and culture that's designed in, not left to chance.</p>
    <div class="hero-actions reveal in" data-d="3">
      <a href="contact.html#book" class="btn btn-primary">Discuss Your Capability Challenge {ARROW}</a>
      <a href="case-studies.html" class="btn btn-ghost">Housing case study</a>
    </div>
  </div>
</header>

{proof()}
<section style="padding-top:84px">
  <div class="wrap">
    <div class="eyebrow reveal">Who I work with</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Built for housing providers balancing service, growth and scrutiny.</p>
    <div class="proof-row reveal" data-d="2" style="justify-content:flex-start;margin-top:30px">
      <div class="proof-item">Housing Associations</div><div class="proof-item">ALMOs</div><div class="proof-item">Registered Providers</div><div class="proof-item">Local Authority Housing Teams</div>
    </div>
    {photo_grid([
      ("housing-community-impact-meeting.jpeg", "Housing team discussing community impact and service outcomes", 1000, 562),
      ("housing-services-site-walkthrough.jpeg", "Housing services site walkthrough with a resident-facing team", 540, 360),
      ("housing-management-development-workshop.jpeg", "Onboarding journey — housing management development workshop", 1000, 666),
    ], cols="3")}
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Housing consultancy services</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Capability expertise, applied to how housing actually operates.</p>
    <div class="feature-grid">
      <div class="feature-card reveal"><img src="assets/icons/leadership.svg" alt=""><h3>Manager &amp; Leadership Onboarding</h3><p>Structured onboarding for new and promoted managers, so capability doesn't depend on who happened to train them.</p></div>
      <div class="feature-card reveal" data-d="1"><img src="assets/icons/development.svg" alt=""><h3>Values-Based Induction</h3><p>Induction that makes culture and service expectations explicit from day one, not assumed through osmosis.</p></div>
      <div class="feature-card reveal" data-d="2"><img src="assets/icons/systems.svg" alt=""><h3>Succession Planning</h3><p>Identifying and developing the next generation of managers before a vacancy forces a rushed decision.</p></div>
      <div class="feature-card reveal"><img src="assets/icons/insight.svg" alt=""><h3>Culture &amp; Service Standards</h3><p>Turning unwritten expectations into standards that can be trained to, measured against and held to account.</p></div>
      <div class="feature-card reveal" data-d="1"><img src="assets/icons/capability.svg" alt=""><h3>Workforce Capability Planning</h3><p>Aligning roles, skills and structure to service demand — particularly through growth, merger or restructuring.</p></div>
      <div class="feature-card reveal" data-d="2"><img src="assets/icons/strategy.svg" alt=""><h3>Digital Learning for Distributed Teams</h3><p>Learning designed for teams spread across sites and neighbourhoods, not assuming everyone sits in one office.</p></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Proprietary frameworks</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">The thinking I bring to every housing engagement.</p>
    {fw_prelude_model()}
    {fw_maturity_model()}
  </div>
</section>

<div class="divider"></div>

{methodology()}
<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Housing track record</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Values and expectations have to be designed in — not left to osmosis.</p>
    <div class="feature-grid">
      <div class="feature-card reveal"><span class="tag-pill">-20% time-to-competence</span><h3>Housing Leadership &amp; Onboarding Transformation</h3><p>Leadership pathways and values-based onboarding that cut time-to-competence by 20% and lifted consistency of leadership standards.</p></div>
    </div>
    <div style="margin-top:40px" class="reveal"><a href="case-studies.html" class="btn btn-ghost">All case studies {ARROW}</a></div>
  </div>
</section>

<div class="divider"></div>

{trust(heading="Cleared and credible", sub="Structured, evidence-based capability work — grounded in how housing actually operates.")}
<div class="divider"></div>

{faq_section(HOUSING_FAQ, "Common questions from housing leadership teams.")}
{cta("Need housing leadership or onboarding support?", "Tell me what you're facing — onboarding, manager capability or succession. A practical conversation, no sales pitch.", secondary=("View services", "services.html"))}'''

# ================================================================== PUBLIC SECTOR
PUBLIC_SECTOR_FAQ = [
    ("Can you work within public sector procurement routes?", "Yes — I can work through direct engagement or via the procurement route your organisation already uses. Tell me what's required and we'll work out the right way in."),
    ("Do you have experience with rapid or crisis-response capability needs?", "Yes. The Operational Role Architecture Redesign delivered during a national crisis response (Op Isotrope) is a direct example — role ambiguity, not individual skill, was the biggest drag on effectiveness under crisis pace, and clarity of role beat volume of training."),
    ("How do you handle value-for-money scrutiny on your recommendations?", "Recommendations are evidence-based by design, so they're defensible to auditors, scrutiny committees and elected members — not assertions that collapse under questioning."),
    ("Can you support restructuring without adding headcount to our L&D function?", "Yes — engagements are scoped around your existing team's capacity. I bring the diagnostic method and the analysis; your team isn't left carrying a parallel programme on top of business as usual."),
    ("Do you work with central government as well as local authorities?", "Yes, across central government departments, arm's-length bodies, combined and local authorities, and public sector transformation programmes more broadly."),
]

public_sector_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">Public Sector Capability &amp; Workforce Consultancy</div>
    <h1 class="reveal in" data-d="1">Capability that survives budget pressure, restructuring and scrutiny.</h1>
    <p class="hero-sub reveal in" data-d="2">Specialist support for local and central government, arm's-length bodies and public sector transformation programmes — covering workforce planning, role architecture, leadership development and training governance for public money.</p>
    <div class="hero-actions reveal in" data-d="3">
      <a href="contact.html#book" class="btn btn-primary">Discuss Your Capability Challenge {ARROW}</a>
      <a href="case-studies.html" class="btn btn-ghost">Public sector case study</a>
    </div>
  </div>
</header>

{proof()}
<section style="padding-top:84px">
  <div class="wrap">
    <div class="eyebrow reveal">Who I work with</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Built for public sector teams under real constraint.</p>
    <div class="proof-row reveal" data-d="2" style="justify-content:flex-start;margin-top:30px">
      <div class="proof-item">Local &amp; Combined Authorities</div><div class="proof-item">Central Government Departments</div><div class="proof-item">Arm's-Length Bodies</div><div class="proof-item">Transformation Programmes</div>
    </div>
    {photo_grid([
      ("public-sector-stakeholder-roundtable.jpeg", "Public sector leaders in a stakeholder roundtable discussion", 540, 360),
      ("public-sector-transformation-workshop.jpeg", "Public sector transformation workshop mapping capability and learning architecture", 1000, 562),
    ], cols="2")}
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Public sector consultancy services</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Capability expertise, applied under real budget and scrutiny pressure.</p>
    <div class="feature-grid">
      <div class="feature-card reveal"><img src="assets/icons/systems.svg" alt=""><h3>Workforce &amp; Role Architecture Redesign</h3><p>Redesigning roles and structure to scale cleanly under pressure — proven in national crisis response, transferable to any restructuring.</p></div>
      <div class="feature-card reveal" data-d="1"><img src="assets/icons/strategy.svg" alt=""><h3>Transformation &amp; Change Capability</h3><p>Diagnosing the capability a transformation programme actually needs, before the solution is designed — so change survives launch.</p></div>
      <div class="feature-card reveal" data-d="2"><img src="assets/icons/leadership.svg" alt=""><h3>Leadership Development Under Pressure</h3><p>Leadership development grounded in real high-pressure operational experience, not theoretical models.</p></div>
      <div class="feature-card reveal"><img src="assets/icons/governance.svg" alt=""><h3>Training Governance &amp; Assurance</h3><p>Governance and assurance that stands up to scrutiny committees and audit — built for public money, not just process compliance.</p></div>
      <div class="feature-card reveal" data-d="1"><img src="assets/icons/development.svg" alt=""><h3>Digital &amp; Learning Technology</h3><p>Learning technology that improves delivery and reporting without assuming budget for a full re-platform.</p></div>
      <div class="feature-card reveal" data-d="2"><img src="assets/icons/capability.svg" alt=""><h3>Capability Frameworks for Restructuring</h3><p>Consistent, defensible competency standards that hold up when roles and structures are changing fast.</p></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Proprietary frameworks</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">The thinking I bring to every public sector engagement.</p>
    {fw_prelude_model()}
    {fw_diagnostic_framework()}
  </div>
</section>

<div class="divider"></div>

{methodology()}
<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Public sector track record</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">In a crisis, clarity of role beats volume of training every time.</p>
    <div class="feature-grid">
      <div class="feature-card reveal"><span class="tag-pill">+15% response effectiveness</span><h3>Operational Role Architecture Redesign (Op Isotrope)</h3><p>Role architecture redesign during national crisis response, improving response effectiveness by 15% and enabling faster, clearer scaling.</p></div>
    </div>
    <div style="margin-top:40px" class="reveal"><a href="case-studies.html" class="btn btn-ghost">All case studies {ARROW}</a></div>
  </div>
</section>

<div class="divider"></div>

{trust(heading="Cleared and credible", sub="Evidence-based recommendations that stand up to audit, scrutiny and elected members.")}
<div class="divider"></div>

{faq_section(PUBLIC_SECTOR_FAQ, "Common questions from public sector leaders.")}
{cta("Need public sector capability or workforce support?", "Tell me what you're facing — restructuring, transformation or governance. A practical conversation, no sales pitch.", secondary=("View services", "services.html"))}'''

# ================================================================== PROFESSIONAL SERVICES
PROFESSIONAL_SERVICES_FAQ = [
    ("You mostly work with Defence and public sector — do you understand professional services firms?", "Yes. Before founding Prelude, I worked as a Korn Ferry consultant advising organisations on leadership, talent and workforce development — Korn Ferry is itself a professional services firm, and that experience sits alongside the operational and Defence background this site describes."),
    ("We're a partnership, not a corporate hierarchy — does your approach still apply?", "Yes. The Prelude Capability Model traces performance from mission to evidence regardless of structure — it adapts to partnership and track-based progression models as readily as to line-management hierarchies."),
    ("Can this help with associate or graduate retention?", "Talent leaving before it matures is a capability and pathway problem more often than a pay problem. Structured development pathways and clearer progression are directly in scope."),
    ("Do you have case studies specifically from professional services firms?", "Not yet published on this site — the case studies here are drawn from Defence, Healthcare and Housing engagements. The method and the Korn Ferry background transfer directly; I'm happy to discuss relevant experience and references in a first conversation."),
    ("What does a first engagement usually look like?", "The same as any sector: a Capability Readiness Review to find where the real problem sits, before recommending anything — never a course or programme sold before the diagnosis is done."),
]

professional_services_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">Professional Services Capability Consultancy</div>
    <h1 class="reveal in" data-d="1">Capability thinking built in Defence and consulting — applied to your firm.</h1>
    <p class="hero-sub reveal in" data-d="2">Specialist support for law firms, accountancy and financial advisory practices, and management and specialist consultancies — covering leadership and partner-track development, talent retention, onboarding and capability frameworks for progression.</p>
    <div class="hero-actions reveal in" data-d="3">
      <a href="contact.html#book" class="btn btn-primary">Discuss Your Capability Challenge {ARROW}</a>
      <a href="about.html" class="btn btn-ghost">About Jason's background</a>
    </div>
  </div>
</header>

{proof()}
<section style="padding-top:84px">
  <div class="wrap">
    <div class="eyebrow reveal">Who I work with</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Built for partnership-model and professional services firms.</p>
    <div class="proof-row reveal" data-d="2" style="justify-content:flex-start;margin-top:30px">
      <div class="proof-item">Law Firms &amp; Partnerships</div><div class="proof-item">Accountancy &amp; Financial Advisory Firms</div><div class="proof-item">Management &amp; Specialist Consultancies</div><div class="proof-item">Insurance &amp; Financial Services</div>
    </div>
    <p class="lead reveal" data-d="3" style="margin-top:36px;font-size:clamp(1.1rem,1.8vw,1.4rem)">Before founding Prelude, I worked as a <span class="gold">Korn Ferry consultant</span> — advising organisations on leadership, talent and workforce development. <span class="dim">That's professional services experience in its own right, not a sector I'm reaching into cold.</span></p>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Professional services consultancy services</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Capability expertise, applied to partnership and career-track structures.</p>
    <div class="feature-grid">
      <div class="feature-card reveal"><img src="assets/icons/leadership.svg" alt=""><h3>Leadership &amp; Partner-Track Development</h3><p>Building judgement and leadership capability for people moving from technical expert to people leader — grounded, not theoretical.</p></div>
      <div class="feature-card reveal" data-d="1"><img src="assets/icons/systems.svg" alt=""><h3>Talent Development &amp; Retention</h3><p>Structured pathways that give associates and specialists a reason to stay and a clear route to progress.</p></div>
      <div class="feature-card reveal" data-d="2"><img src="assets/icons/development.svg" alt=""><h3>Onboarding &amp; Time-to-Billable Acceleration</h3><p>Onboarding designed to get new joiners contributing and billable faster, without cutting corners on quality.</p></div>
      <div class="feature-card reveal"><img src="assets/icons/capability.svg" alt=""><h3>Capability Frameworks for Progression</h3><p>Consistent, defensible standards for career-track and partnership progression — usable for assessment, not just aspiration.</p></div>
      <div class="feature-card reveal" data-d="1"><img src="assets/icons/strategy.svg" alt=""><h3>Learning Technology for Distributed Teams</h3><p>Digital and blended learning that works for teams split across offices, clients and time zones.</p></div>
      <div class="feature-card reveal" data-d="2"><img src="assets/icons/insight.svg" alt=""><h3>Culture &amp; Capability During Growth or Merger</h3><p>Keeping capability and culture intact when the firm is growing, merging or restructuring at pace.</p></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Proprietary frameworks</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">The thinking I bring to every professional services engagement.</p>
    {fw_prelude_model()}
    {fw_decision_model()}
  </div>
</section>

<div class="divider"></div>

{methodology()}
<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">The same method, proven elsewhere</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Different sector. Same discipline: diagnose before you prescribe.</p>
    <div class="feature-grid">
      <div class="feature-card reveal"><span class="tag-pill">95% completion</span><h3>Talent &amp; Progression Pathways</h3><p>Structured pathways and coaching driving 95% completion where drop-off had previously been driven by weak progress management, not ability.</p></div>
      <div class="feature-card reveal" data-d="1"><span class="tag-pill">-20% time-to-competence</span><h3>Leadership &amp; Onboarding Design</h3><p>Values-based onboarding and leadership pathways cutting time-to-competence by 20% for new and promoted managers.</p></div>
    </div>
    <div style="margin-top:40px" class="reveal"><a href="case-studies.html" class="btn btn-ghost">See how the method was applied {ARROW}</a></div>
  </div>
</section>

<div class="divider"></div>

{trust(heading="Cleared and credible", sub="Korn Ferry consulting background, plus operational leadership experience most training providers don't have.")}
<div class="divider"></div>

{faq_section(PROFESSIONAL_SERVICES_FAQ, "Common questions from professional services leaders.")}
{cta("Need leadership, talent or capability support for your firm?", "Tell me what you're facing — progression, retention or onboarding. A practical conversation, no sales pitch.", secondary=("About Jason's background", "about.html"))}'''

# ================================================================== ABOUT
about_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">About</div>
    <h1 class="reveal in" data-d="1">23+ years building capability where the stakes are real.</h1>
    <p class="hero-sub reveal in" data-d="2">I'm Jason Smith. From Royal Navy operational leadership to advising large organisations on capability, readiness and assurance — I solve the problems training alone never fixes.</p>
  </div>
</header>

<div class="divider"></div>

<section>
  <div class="wrap split">
    <div class="reveal stack-gap">
      <div class="eyebrow">My background</div>
      <p>My career began in the Royal Navy, where I spent years in operational leadership — responsible for people, performance and readiness in demanding, high-pressure environments. There, capability isn't a slide in a deck; it's whether your team can deliver when it matters.</p>
      <p>Over 23+ years I've moved from operational leadership into capability development and workforce performance — building training and assurance to exacting Defence standards, and learning to connect what happens on the ground with what the board needs to see.</p>
      <p>Today I bring that perspective to Defence, Healthcare, Housing, the wider public sector and — through my time as a Korn Ferry consultant — professional services firms, as an independent capability advisor who has actually operated inside the environments my clients work in.</p>
    </div>
    <div class="reveal" data-d="2">
      <div class="photo-frame has-photo"><img src="assets/photos/professional-photograph-of-jason-smith.jpeg" alt="Jason Smith, Founder of Prelude Learning &amp; Consultancy" width="803" height="1200" loading="lazy"></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Why organisations bring me in</div>
    <p class="lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Not for courses — for clarity, evidence and results.</p>
    <div class="reasons reveal" data-d="2">
      <div class="reason">{CHECK}<div class="rt">I don't sell courses — I identify capability gaps.<span>The work starts with your problem, not my product list.</span></div></div>
      <div class="reason">{CHECK}<div class="rt">I build evidence-based solutions.<span>Recommendations stand on analysis, not assertion.</span></div></div>
      <div class="reason">{CHECK}<div class="rt">I understand regulated environments.<span>DSAT, assurance and audit are familiar ground.</span></div></div>
      <div class="reason">{CHECK}<div class="rt">I speak operational and executive language.<span>From the front line to the board, without translation loss.</span></div></div>
      <div class="reason">{CHECK}<div class="rt">I align learning with organisational performance.<span>Capability is judged by outcomes, not activity.</span></div></div>
      <div class="reason">{CHECK}<div class="rt">I've operated in high-stakes environments.<span>Royal Navy leadership, Defence programmes, national crisis response.</span></div></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">The path here</div>
    <p class="lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">A career spent building capability under pressure.</p>
    <div class="timeline reveal" data-d="2">
      <div class="tl-item"><div class="when">ROYAL NAVY</div><h3>Operational leadership</h3><p>Senior leadership and training delivery to Defence standards in high-pressure operational environments — where capability is measured by readiness.</p></div>
      <div class="tl-item"><div class="when">DEFENCE</div><h3>Defence capability specialist</h3><p>Built and assured training and capability aligned to DSAT (JSP 822) — from TNA through governance and audit-ready evidence.</p></div>
      <div class="tl-item"><div class="when">KORN FERRY</div><h3>Consultant</h3><p>Advised large organisations on capability, leadership and workforce development across Defence, Healthcare, Housing and the public sector.</p></div>
      <div class="tl-item"><div class="when">PRELUDE</div><h3>Independent capability advisor</h3><p>Now partnering directly with leaders to turn capability and readiness challenges into measurable performance.</p></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">By the numbers</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Experience measured in outcomes.</p>
    <div class="metric-grid reveal" data-d="2">
      <div class="metric"><div class="figure" data-count="23" data-suffix="+">23<span class="unit">+</span></div><div class="label">Years in capability, leadership &amp; readiness</div></div>
      <div class="metric"><div class="figure" data-count="15000">15,000</div><div class="label">Staff supported across a single organisation</div></div>
      <div class="metric"><div class="figure" data-count="95" data-suffix="%">95<span class="unit">%</span></div><div class="label">Apprenticeship completion rate</div></div>
      <div class="metric"><div class="figure" data-count="25" data-suffix="%">25<span class="unit">%</span></div><div class="label">Operational performance improvement (up to)</div></div>
    </div>
  </div>
</section>

<div class="divider"></div>

{trust()}
{cta("Think we might be a fit?", "Tell me about your capability challenge. If I can help, I'll tell you how. If I can't, I'll tell you that too.", secondary=("See the evidence", "case-studies.html"))}'''

# ================================================================== SERVICES
cap_gov = (
    acc_item("01", "DSAT Consultancy",
        ["Training that can't demonstrate DSAT (JSP 822) compliance", "Weak audit trails and assurance evidence", "Inconsistent governance across providers"],
        "I review your training system against DSAT, find the gaps, and put in place the structures and evidence needed to stand up to scrutiny — pragmatically.",
        ["Audit-ready, DSAT-aligned governance", "Clear roles and decision rights", "Defensible assurance evidence"],
        "DSAT-aligned analysis and governance for MOD Digital Skills for Defence.", is_open=True, slug="dsat-consultancy")
    + acc_item("02", "Training Needs Analysis",
        ["Investing in training without knowing the true gap", "Symptoms treated instead of causes", "No baseline to measure improvement"],
        "A structured TNA that separates capability problems from training problems using evidence, so investment goes where it moves performance.",
        ["Evidence-based recommendations", "A clear baseline and priorities", "Confidence that spend is targeted"],
        "DSAT-compliant TNA underpinning a 17% increase in pass rates on Royal Navy / NATO programmes.", slug="training-needs-analysis")
    + acc_item("03", "Capability Framework Design",
        ["No consistent competency standards", "Roles and skills defined differently across teams", "Hard to plan workforce or measure readiness"],
        "I design multi-specialisation capability frameworks, map skills to roles, and make them usable for assessment, development and planning.",
        ["Consistent, defensible standards", "Skills mapping and workforce planning", "Improved operational readiness"],
        "Multi-specialisation Defence framework contributing to a 20% increase in operational readiness.", slug="capability-framework-design")
    + acc_item("04", "Training Governance &amp; Assurance",
        ["Governance that can't keep pace with delivery", "Assurance that doesn't reassure", "Risk hidden until audit"],
        "I build governance and assurance that is both audit-ready and useful — giving leaders confidence and inspectors evidence.",
        ["Trustworthy assurance evidence", "Clear governance and ownership", "Reduced compliance risk"],
        "Training governance embedded across DS4D and operational training programmes.", slug="training-governance-assurance")
)
lead_wf = (
    acc_item("05", "Leadership Development",
        ["Technically strong people promoted without support", "Inconsistent leadership under pressure", "Development that doesn't transfer to the job"],
        "Leadership and management development grounded in real operational experience and CMI-aligned coaching — building judgement and confidence.",
        ["Leaders who carry capability through change", "Consistent leadership standards", "Stronger succession and retention"],
        "Leadership pathways and values-based onboarding for a housing association, cutting time-to-competence by 20%.", slug="leadership-development")
    + acc_item("06", "Talent Development",
        ["Talent leaving before it matures", "No clear development pathways", "Over-reliance on recruitment"],
        "Structured talent and development pathways that grow capability from within and give people a reason to stay.",
        ["A sustainable internal pipeline", "Clear progression", "Reduced recruitment cost and risk"],
        "Coaching and structured pathways driving 95% apprenticeship completion.", slug="talent-development")
    + acc_item("07", "Workforce Planning",
        ["Capability and demand out of step", "Roles unclear during change or scaling", "No line of sight from skills to mission"],
        "I align roles, skills and structure to operational demand — so the workforce is ready for what's coming, not just what's here.",
        ["Roles and skills aligned to demand", "Clearer structure under change", "Improved readiness"],
        "Role architecture redesign during national crisis response (OP ISOTROPE), improving response effectiveness by 15%.", slug="workforce-planning")
    + acc_item("08", "Apprenticeships",
        ["Low completion rates", "Funding compliance risk", "Programmes that don't build real capability"],
        "Structured pathways, coaching and active progress management that keep learners on track and funding compliant throughout.",
        ["95% completion rates", "100% funding compliance", "Genuine capability, not just certificates"],
        "Defence Apprenticeship Success Programme — 95% completion, 100% funding compliance.", slug="apprenticeships")
)
learn_tx = (
    acc_item("09", "Digital Learning",
        ["Digital learning bought but underused", "Content that doesn't change behaviour", "Transformation that stalls after launch"],
        "Digital and blended learning designed for outcomes and adoption — so modernisation improves performance, not just format.",
        ["Higher engagement and completion", "Measurable performance gains", "Sustainable, adopted change"],
        "Blended and e-learning interventions reducing failure rates by 20% on operational training.", slug="digital-learning")
    + acc_item("10", "LMS Optimisation",
        ["An LMS that frustrates more than it helps", "Compliance reporting that can't be trusted", "Poor visibility of learning data"],
        "LMS optimisation — dashboards, pathways and information management (including Totara) that turn your platform into reliable capability intelligence.",
        ["Trustworthy compliance reporting", "Clear dashboards and pathways", "Reduced compliance gaps"],
        "Totara dashboards across 15,000 healthcare colleagues, cutting compliance gaps by 18%.", slug="lms-optimisation")
    + acc_item("11", "Learning Operations",
        ["Learning delivery that's inconsistent or manual", "Effort spent on admin, not impact", "No reliable view of what's working"],
        "I streamline how learning is planned, delivered and measured — so the operation runs predictably and frees time for what matters.",
        ["More efficient delivery", "Consistent, repeatable processes", "Better management information"],
        "Information management improvements across a 15,000-strong workforce.", slug="learning-operations")
    + acc_item("12", "Learning Strategy",
        ["Learning disconnected from organisational goals", "Activity measured instead of impact", "No coherent direction for investment"],
        "A clear learning strategy that aligns capability investment to organisational performance — with a practical, fundable roadmap.",
        ["Learning aligned to goals", "Stronger value for money", "A roadmap leaders can back"],
        "Strategic learning architecture and roadmaps for enterprise Defence capability planning.", slug="learning-strategy")
)
def service_page(slug, cat_label, num, title, h1, hero_sub, problem, diagnosis, approach, deliverables, outcomes, case_title, case_metric, case_text, faqs):
    del_li = "".join(f"<li>{d}</li>" for d in deliverables)
    out_li = "".join(f"<li>{o}</li>" for o in outcomes)
    body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">{cat_label} · Service {num}</div>
    <h1 class="reveal in" data-d="1">{h1}</h1>
    <p class="hero-sub reveal in" data-d="2">{hero_sub}</p>
    <div class="hero-actions reveal in" data-d="3">
      <a href="contact.html#book" class="btn btn-primary">Discuss Your Capability Challenge {ARROW}</a>
      <a href="services.html" class="btn btn-ghost">All services</a>
    </div>
  </div>
</header>

{proof()}
<section style="padding-top:84px">
  <div class="wrap article">
    <div class="eyebrow reveal">The problem</div>
    <p class="reveal" style="font-size:1.1rem;line-height:1.75">{problem}</p>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap article">
    <div class="eyebrow reveal">How I diagnose it</div>
    <p class="reveal" style="font-size:1.1rem;line-height:1.75">{diagnosis}</p>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap article">
    <div class="eyebrow reveal">My approach</div>
    <p class="reveal" style="font-size:1.1rem;line-height:1.75">{approach}</p>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">What you get</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Deliverables, and the outcomes they drive.</p>
    <div class="feature-grid cols-2">
      <div class="feature-card reveal"><h3>Deliverables</h3><ul class="dot-list">{del_li}</ul></div>
      <div class="feature-card reveal" data-d="1"><h3>Outcomes</h3><ul class="dot-list">{out_li}</ul></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Proof, not promises</div>
    <div class="feature-grid" style="grid-template-columns:1fr">
      <div class="feature-card reveal"><span class="tag-pill">{case_metric}</span><h3>{case_title}</h3><p>{case_text}</p></div>
    </div>
    <div style="margin-top:32px" class="reveal"><a href="case-studies.html" class="btn btn-ghost">All case studies {ARROW}</a></div>
  </div>
</section>

<div class="divider"></div>

{faq_section(faqs, f"Common questions about {title.lower()}.")}
{cta(f"Need help with {title.lower()}?", "A practical, problem-first conversation — no sales pitch. We'll work out what's really going on and whether I can help.", secondary=("View all services", "services.html"))}'''
    page(f"{slug}.html", f"{title} | Prelude",
         hero_sub, body, "services", breadcrumb=title, faq=faqs)

SERVICES = [
    dict(slug="dsat-consultancy", cat="Capability &amp; Governance", num="01", title="DSAT Consultancy",
         h1="DSAT compliance that stands up to scrutiny — without drowning your team in process.",
         hero_sub="Defence capability and DSAT consultancy for training that can demonstrate JSP 822 compliance, with audit trails and governance that actually hold up.",
         problem="Training that can't demonstrate DSAT (JSP 822) compliance is a recurring risk across Defence programmes — not because the training is wrong, but because the evidence trail behind it is weak, inconsistent across providers, or assembled in a panic before an audit rather than built in from the start.",
         diagnosis="I start by testing whether your governance can survive an unannounced audit request today, not in a fortnight. Can two different sites or providers show the same evidence in the same format? Are governance decisions actually documented, or just \"known\" by the people who made them? Where the answer is no, that's where the real risk sits — usually well before the training itself.",
         approach="I review your training system against DSAT, identify the specific gaps between what's happening and what's defensible, and put in place the structures and evidence needed to stand up to scrutiny — pragmatically, without adding process for its own sake.",
         deliverables=["A DSAT gap analysis report, mapped against JSP 822", "An audit-ready evidence framework your team can maintain", "A governance and decision-rights matrix", "Recommendations for standardising practice across providers or sites"],
         outcomes=["Audit-ready, DSAT-aligned governance", "Clear roles and decision rights", "Defensible assurance evidence, produced on demand rather than assembled under pressure"],
         case_title="MOD Digital Skills for Defence (DS4D)", case_metric="Defence-wide",
         case_text="DSAT-aligned capability analysis and governance embedded across an enterprise-wide Defence programme — progress in ten weeks that had stalled for twelve months.",
         faqs=[
             ("Is this only relevant to MOD, or also to primes and suppliers?", "Both. DSAT governance matters wherever training is being delivered against a Defence requirement — whether you're MOD, a prime contractor, or a training provider working to Defence standards."),
             ("How long does a DSAT gap analysis take?", "A focused gap analysis is typically weeks, not months. The Capability Readiness Review at the start gives a realistic view of scope before anything is committed."),
             ("Will this slow down delivery while we fix governance?", "No — the Senior Information Officer (SIO) Rapid TNA case study is a direct example of DSAT used to accelerate decisions, not delay them, when it's treated as a decision-support framework rather than a box-ticking exercise."),
         ]),
    dict(slug="training-needs-analysis", cat="Capability &amp; Governance", num="02", title="Training Needs Analysis",
         h1="A Training Needs Analysis that finds the real gap, not just the loudest complaint.",
         hero_sub="DSAT-compliant Training Needs Analysis that separates genuine training needs from capability, structure and process issues — so investment goes where it actually moves performance.",
         problem="Most organisations invest in training without knowing the true gap. Symptoms get treated instead of causes, and without a baseline, nobody can say afterwards whether the investment actually worked — only that a course was delivered.",
         diagnosis="Before recommending anything, I test whether the presenting issue is actually a training need at all: is the knowledge or skill genuinely missing, or is performance being held back by unclear roles, weak governance, or a structure that works against the outcome? Evidence answers this question — assumption doesn't.",
         approach="A structured TNA that separates capability problems from training problems using evidence, so investment goes where it moves performance, not just where it's easiest to commission a course.",
         deliverables=["A DSAT-compliant TNA report with a clear evidence base", "A prioritised set of recommendations, ranked by impact", "A performance baseline to measure improvement against", "A defensible rationale for what's training and what isn't"],
         outcomes=["Evidence-based recommendations leaders can defend", "A clear baseline and set of priorities", "Confidence that spend is targeted at what actually moves performance"],
         case_title="NATO &amp; Royal Navy Training Modernisation", case_metric="+17% pass rates",
         case_text="A DSAT-compliant TNA pinpointed the specific points in the training pipeline where learners were being set up to fail — lifting pass rates by 17% and cutting failures by 20%.",
         faqs=[
             ("How is this different from a standard training needs survey?", "A survey asks people what training they want. A TNA tests whether training is the right answer at all — using evidence, not opinion, and stopping at the point where the real issue turns out to be structural."),
             ("Do you run TNAs outside Defence?", "Yes — the method is sector-agnostic. DSAT compliance is specific to Defence and regulated environments, but the underlying discipline of testing cause before prescribing a solution applies everywhere."),
             ("What if the TNA concludes that training isn't the answer?", "Then that's the finding, and it's the useful one — the alternative is spending on training that was never going to fix the problem. Root causes beat symptoms every time."),
         ]),
    dict(slug="capability-framework-design", cat="Capability &amp; Governance", num="03", title="Capability Framework Design",
         h1="Competency standards that mean the same thing in every team.",
         hero_sub="Multi-specialisation capability frameworks and skills mapping that make 'ready' mean the same thing everywhere in your organisation — usable for assessment, development and workforce planning.",
         problem="Without consistent competency standards, roles and skills get defined differently by every team, which makes it near-impossible to assess people fairly, plan the workforce with any confidence, or measure whether the organisation is actually ready.",
         diagnosis="I test this directly: can two different managers assess the same person's competence against the same standard and reach the same answer? If \"ready\" means something different in every team, that inconsistency — not a lack of individual skill — is usually the real operational risk.",
         approach="I design multi-specialisation capability frameworks, map skills to roles, and make the framework genuinely usable for assessment, development and workforce planning — not a document that gets published once and never opened again.",
         deliverables=["A multi-specialisation capability framework document", "A skills-to-role mapping matrix", "Assessment criteria that different assessors can apply consistently", "A workforce planning tool built on the same standards"],
         outcomes=["Consistent, defensible standards across every team", "Skills mapping that supports real workforce planning", "Measurably improved operational readiness"],
         case_title="Defence Capability Framework Design", case_metric="+20% readiness",
         case_text="A multi-specialisation framework and skills mapping exercise that gave the organisation a single, trusted view of capability — lifting operational readiness by 20%.",
         faqs=[
             ("Does this replace our existing job descriptions?", "Not necessarily — it usually sits above them, giving a consistent standard that job descriptions and assessment processes can be checked against, rather than replacing everything from scratch."),
             ("How long does a framework take to design?", "It depends on the number of specialisations and how fragmented current practice is. A focused single-specialisation framework can be weeks; an enterprise multi-specialisation framework is a longer, phased piece of work."),
             ("Will people actually use it, or will it sit on a shelf?", "That's the design test I apply throughout — a framework only changes behaviour when it's built for assessment and planning from day one, not published and hoped for."),
         ]),
    dict(slug="training-governance-assurance", cat="Capability &amp; Governance", num="04", title="Training Governance &amp; Assurance",
         h1="Governance that's audit-ready and actually useful to the people running it.",
         hero_sub="Training governance and assurance that gives leaders real confidence and inspectors defensible evidence — built to keep pace with delivery, not slow it down.",
         problem="Governance that can't keep pace with delivery is a common failure mode: assurance processes exist, but they don't reassure anyone, and risk stays hidden until it surfaces at audit — by which point it's expensive and reputationally painful to fix.",
         diagnosis="The test I apply is simple: does your governance actually inform decisions in real time, or does it just record what already happened? Would your assurance evidence survive an unannounced audit tomorrow, or does it need weeks of preparation first?",
         approach="I build governance and assurance that is both audit-ready and genuinely useful day to day — giving leaders real-time confidence and inspectors defensible evidence, rather than two separate systems pulling in different directions.",
         deliverables=["A governance framework and structure chart with clear ownership", "Assurance evidence templates your team can maintain without extra admin burden", "An audit-readiness checklist", "A decision-rights matrix across providers, sites and delivery partners"],
         outcomes=["Trustworthy assurance evidence, available on demand", "Clear governance and ownership at every level", "Materially reduced compliance risk"],
         case_title="Digital Skills for Defence (DS4D) Governance", case_metric="Enterprise-wide",
         case_text="Training governance embedded across DS4D and operational training programmes, giving decision-makers evidence they could defend rather than assumptions they hoped would hold.",
         faqs=[
             ("Is this just a paperwork exercise?", "No — the test throughout is whether governance is useful to the people running it day to day, not just defensible on paper. If it doesn't help leaders make better decisions, it isn't doing its job."),
             ("Can you work with our existing governance structures rather than replacing them?", "Usually yes. Most engagements strengthen and clarify what's already there — adding the missing evidence trail and decision rights — rather than tearing it down and starting again."),
             ("How do you handle governance across multiple delivery partners or sites?", "By defining a single set of decision rights and evidence standards that every partner or site is held to consistently — which is usually where the current risk sits, in the gaps between different local practices."),
         ]),
    dict(slug="leadership-development", cat="Leadership &amp; Workforce", num="05", title="Leadership Development",
         h1="Leaders who carry capability through change, not just a certificate.",
         hero_sub="Leadership and management development grounded in real operational experience and CMI-aligned coaching — building the judgement and confidence that technical expertise alone doesn't give you.",
         problem="Technically strong people get promoted into leadership roles without real support, and the result is inconsistent leadership under pressure — because development that doesn't transfer to the job is really just a certificate, not a capability.",
         diagnosis="I test whether the gap is a skills gap or an expectations gap: do new leaders know precisely what's expected of them from day one, or are they working it out by trial and error while carrying a team? Most \"leadership problems\" turn out to be the second, not the first.",
         approach="Leadership and management development grounded in real operational experience and CMI-aligned coaching — building judgement and confidence under pressure, not just theoretical models that don't survive contact with a real team.",
         deliverables=["A leadership development pathway, mapped to your management levels", "A structured coaching programme", "A manager onboarding toolkit that sets expectations explicitly from day one", "Assessment criteria to track leadership capability, not just attendance"],
         outcomes=["Leaders who carry capability through organisational change", "Consistent leadership standards across teams", "Stronger succession planning and retention"],
         case_title="Housing Leadership &amp; Onboarding Transformation", case_metric="-20% time-to-competence",
         case_text="Leadership pathways and values-based onboarding for a housing association, cutting time-to-competence by 20% and lifting consistency of leadership standards.",
         faqs=[
             ("Is this generic leadership training, or tailored to our organisation?", "Tailored. Generic leadership content is exactly what this approach is built to avoid — the pathway and coaching are built around your actual management levels, pressures and expectations."),
             ("Do you coach individuals, or design programmes for cohorts?", "Both, depending on the problem — sometimes it's one-to-one coaching for people stepping into a role now, sometimes it's a structured pathway for a whole management cohort."),
             ("How do you measure whether leadership development has actually worked?", "Against the outcomes that matter operationally — consistency of standards, retention, and how quickly new leaders become genuinely effective — not just attendance or satisfaction scores."),
         ]),
    dict(slug="talent-development", cat="Leadership &amp; Workforce", num="06", title="Talent Development",
         h1="A pipeline people want to stay in, not a reason to leave.",
         hero_sub="Structured talent and development pathways that grow capability from within and give people a genuine reason to stay, rather than relying on recruitment to fill every gap.",
         problem="Talent leaves before it matures when there's no clear development pathway — and the default response, over-reliance on recruitment, is expensive, slow, and doesn't fix the underlying reason people left in the first place.",
         diagnosis="I ask a simple question first: do your people know their next step, or are they guessing? Retention problems that look like a pay problem are very often a pathway problem — people leave organisations where they can't see where they're going.",
         approach="Structured talent and development pathways that grow capability from within — giving people a genuine, visible reason to stay and progress, rather than leaving development to chance or informal mentoring relationships.",
         deliverables=["A talent pathway framework with clear progression criteria", "A structured coaching and mentoring model", "Development milestones tied to real capability, not just tenure", "A retention risk assessment for your current talent pool"],
         outcomes=["A sustainable internal pipeline, not a permanent recruitment problem", "Clear, visible progression for people who might otherwise leave", "Reduced recruitment cost and risk"],
         case_title="Defence Apprenticeship Success Programme", case_metric="95% completion",
         case_text="Coaching and structured development pathways drove 95% apprenticeship completion, where drop-off had previously been caused by weak progress management, not learner ability.",
         faqs=[
             ("Is this only relevant to formal talent programmes, or also day-to-day retention?", "Both — the same pathway thinking applies whether you're running a formal talent scheme or just trying to stop good people leaving because they can't see a future."),
             ("How is this different from a standard succession plan?", "A succession plan identifies who might fill a role next. This builds the actual development pathway that gets people ready for it — the two are meant to work together, not substitute for each other."),
             ("Can this work for a small team, or does it need scale?", "It scales down as well as up — the discipline of clear pathways and visible progression matters as much for a team of ten as for an organisation of thousands."),
         ]),
    dict(slug="workforce-planning", cat="Leadership &amp; Workforce", num="07", title="Workforce Planning",
         h1="A workforce ready for what's coming, not just what's here.",
         hero_sub="Aligning roles, skills and structure to operational demand — so restructuring, scaling or crisis response doesn't get slowed down by ambiguity about who does what.",
         problem="When capability and demand fall out of step, roles become unclear exactly when clarity matters most — during change or scaling — and without a clear line of sight from skills to mission, workforce decisions default to guesswork.",
         diagnosis="I test this with a direct question: if demand doubled tomorrow, could you say precisely which roles and skills you'd need, and where the gaps are? If roles were designed for yesterday's problem and haven't been revisited, that's usually where the real constraint sits.",
         approach="I align roles, skills and structure to actual operational demand — so the workforce is ready for what's coming, not just resourced for what's here today.",
         deliverables=["A role architecture review and redesign", "A workforce plan mapping skills to current and future demand", "Structural recommendations for scaling or restructuring cleanly", "A skills-to-mission traceability map"],
         outcomes=["Roles and skills genuinely aligned to demand", "Clearer structure and accountability under change", "Measurably improved readiness"],
         case_title="Operational Role Architecture Redesign (Op Isotrope)", case_metric="+15% response effectiveness",
         case_text="Role architecture redesign during a national crisis response, improving response effectiveness by 15% by removing role ambiguity — the biggest drag on effectiveness under crisis pace.",
         faqs=[
             ("Do you only do this for crisis or emergency scenarios?", "No — Op Isotrope is the clearest proof point because the pressure was extreme, but the same discipline applies to routine restructuring, growth, or service redesign."),
             ("How is workforce planning different from a headcount review?", "A headcount review asks how many people. This asks what roles, skills and structure are actually needed to deliver the mission — headcount follows from that, not the other way round."),
             ("Can this be done without disrupting current delivery?", "Yes — the analysis phase runs alongside business as usual, and implementation is typically phased so delivery isn't put at risk while the workforce plan is being rolled out."),
         ]),
    dict(slug="apprenticeships", cat="Leadership &amp; Workforce", num="08", title="Apprenticeships",
         h1="95% completion, not just enrolment.",
         hero_sub="Structured pathways, coaching and active progress management that keep apprentices on track and funding compliant throughout — building genuine capability, not just certificates.",
         problem="Low completion rates and funding compliance risk are the two problems that consistently undermine apprenticeship programmes — and both usually trace back to the same root cause: programmes that aren't actively managed once someone is enrolled.",
         diagnosis="I look at where drop-off actually happens in your pipeline, and test whether it's driven by learner ability — which is rare — or by weak progress management and support, which is common. I also check whether your funding evidence would survive an ESFA audit today.",
         approach="Structured pathways, coaching and active progress management that keep learners on track and funding compliant throughout — treating completion as an operations problem as much as a teaching one.",
         deliverables=["A progress management system with early-warning triggers", "A coaching and support framework for apprentices at risk of dropping off", "A funding compliance audit trail", "Programme design recommendations to build genuine capability, not just pass an exam"],
         outcomes=["95% completion rates, proven at scale", "100% funding compliance", "Genuine capability built, not just qualifications gained"],
         case_title="Defence Apprenticeship Success Programme", case_metric="95% / 100%",
         case_text="Coaching, progress management and structured pathways delivered 95% completion and 100% funding compliance — proof that completion is an operations problem as much as a teaching one.",
         faqs=[
             ("Is this specific to Defence apprenticeships, or does it apply more broadly?", "The method applies to any apprenticeship programme — Defence, healthcare, housing or elsewhere. Funding rules differ by sector; the underlying discipline of active progress management doesn't."),
             ("What causes most apprenticeship drop-off, in your experience?", "Weak progress management and support, far more often than learner ability. People disengage when they lose sight of where they are in the programme and nobody notices early enough to intervene."),
             ("Can you audit an existing programme rather than redesign from scratch?", "Yes — a funding compliance and progress management review of an existing programme is often the right first step, rather than assuming a full redesign is needed."),
         ]),
    dict(slug="digital-learning", cat="Learning Transformation", num="09", title="Digital Learning",
         h1="Digital learning that changes behaviour, not just format.",
         hero_sub="Digital and blended learning designed for outcomes and adoption — so modernisation actually improves performance, instead of just moving the same content onto a screen.",
         problem="Digital learning gets bought and then sits underused, because content that doesn't change behaviour was never going to work regardless of the delivery format — and transformation programmes routinely stall after launch once the initial push fades.",
         diagnosis="I look past the content itself and ask what happens in week two after launch, not just week one. Is the problem the material, or the fact that nobody designed for genuine adoption — manager reinforcement, workflow integration, ongoing measurement?",
         approach="Digital and blended learning designed for outcomes and adoption from the outset — so modernisation improves performance, not just the format the content happens to be delivered in.",
         deliverables=["A digital learning design aligned to real behaviour-change goals", "An adoption and rollout plan, including manager reinforcement", "A measurement framework tracking behaviour change, not just completion", "Recommendations on blended vs. fully digital delivery, by content type"],
         outcomes=["Higher engagement and completion rates", "Measurable performance gains, not just activity metrics", "Sustainable, adopted change rather than a launch-week spike"],
         case_title="NATO &amp; Royal Navy Training Modernisation", case_metric="-20% failure rate",
         case_text="Blended and e-learning interventions, designed around where learners were actually failing, reduced failure rates by 20% on operational training.",
         faqs=[
             ("Do you build the digital content yourselves, or design the strategy?", "The focus is diagnosis and design — working out what should be digital, why, and how it will actually be adopted — then working with your existing content or development resource, or recommending where to source it."),
             ("How do you measure whether digital learning has actually changed behaviour?", "Against the operational metric the learning was meant to influence — error rates, compliance, performance data — not just completion percentages, which measure activity, not impact."),
             ("What usually causes digital learning to fail after launch?", "Absence of manager reinforcement and workflow integration, far more often than the content itself. Digital learning designed in isolation from how work actually happens rarely sticks."),
         ]),
    dict(slug="lms-optimisation", cat="Learning Transformation", num="10", title="LMS Optimisation",
         h1="An LMS you'd trust enough to put in a board report.",
         hero_sub="LMS optimisation — dashboards, pathways and information management, including Totara — that turns your platform into reliable capability intelligence instead of a frustrating administrative burden.",
         problem="An LMS that frustrates more than it helps is a common complaint, but the deeper issue is usually that compliance reporting can't be trusted and learning data has poor visibility — which means leaders are managing risk blind, even though the data technically exists.",
         diagnosis="I ask a direct question: do you trust the numbers your LMS produces enough to put them in a board report unchecked? Very often the honest answer is no — and the cause is usually configuration and information management, not the platform itself.",
         approach="LMS optimisation — dashboards, pathways and information management, including Totara — that turns your existing platform into reliable capability intelligence rather than recommending a costly re-platform as the default fix.",
         deliverables=["An LMS configuration and information architecture review", "Dashboard design for leadership-level reporting", "An information management framework for ongoing data reliability", "Pathway redesign aligned to real learner and compliance needs"],
         outcomes=["Trustworthy compliance reporting leaders can act on", "Clear dashboards and learning pathways", "Materially reduced compliance gaps"],
         case_title="Healthcare Learning Transformation", case_metric="-18% compliance gaps",
         case_text="Totara dashboards and structured pathways across 15,000 colleagues cut compliance gaps by 18%, giving leaders visibility they could finally trust.",
         faqs=[
             ("Do we need to replace our LMS to fix this?", "Usually not. Most of the engagements behind this page's results were configuration, dashboards and information management on an existing platform — not a re-platform."),
             ("Do you work with platforms other than Totara?", "Yes — Totara features prominently in the case studies here, but the diagnostic approach to dashboards, pathways and information management applies to most modern LMS platforms."),
             ("How long does an LMS optimisation project typically take?", "A focused configuration and dashboard project can be delivered in a small number of months; broader information management change across a large organisation takes longer and is usually phased."),
         ]),
    dict(slug="learning-operations", cat="Learning Transformation", num="11", title="Learning Operations",
         h1="A learning operation that runs predictably, not by heroics.",
         hero_sub="Streamlining how learning is planned, delivered and measured — so the operation runs predictably and your team's time goes to impact, not admin.",
         problem="Learning delivery that's inconsistent or manual quietly consumes enormous effort on administration rather than impact, and without a reliable view of what's actually working, teams end up repeating the same fixes without knowing if they helped.",
         diagnosis="I look at how much of your L&D team's time genuinely goes to admin versus impact, and ask a blunt test question: could someone new run this operation from documentation alone, or does it depend on specific people's memory and improvisation?",
         approach="I streamline how learning is planned, delivered and measured — so the operation runs predictably and repeatably, freeing time for the work that actually moves capability rather than administrative overhead.",
         deliverables=["An operating model redesign for learning delivery", "Documented, repeatable processes", "A management information framework showing what's actually working", "Recommendations to reduce administrative load on delivery teams"],
         outcomes=["More efficient, predictable delivery", "Consistent, repeatable processes that don't depend on one person", "Better management information for leadership decisions"],
         case_title="Healthcare Learning Transformation", case_metric="15,000-strong workforce",
         case_text="Information management improvements across a 15,000-strong workforce turned a manual, inconsistent operation into one leadership could see and trust.",
         faqs=[
             ("Is this about cutting our L&D team, or making it more effective?", "The latter. The goal is to redirect existing capacity from admin to impact — not to reduce headcount, but to stop good people spending their time on avoidable manual work."),
             ("What's the first thing you look at in a learning operations review?", "Where time actually goes versus where it's supposed to go — most operations have a gap between the two that nobody has measured directly before."),
             ("Can this run alongside business as usual?", "Yes — the review phase doesn't require pausing delivery, and changes are typically phased in so the operation keeps running while it improves."),
         ]),
    dict(slug="learning-strategy", cat="Learning Transformation", num="12", title="Learning Strategy",
         h1="A learning strategy leaders can explain in two sentences.",
         hero_sub="A clear learning strategy that aligns capability investment to organisational performance — with a practical, fundable roadmap, not a document that sits in a drawer.",
         problem="Learning that's disconnected from organisational goals ends up measured by activity — courses run, hours completed — instead of impact, and without a coherent direction, investment gets spread thin across whatever seems urgent that quarter.",
         diagnosis="I test whether you can explain your learning strategy's link to organisational strategy in two sentences. If it takes longer than that, or the answer is really a list of programmes rather than a rationale, that's the gap the strategy needs to close.",
         approach="A clear learning strategy that aligns capability investment to organisational performance, backed by a practical, fundable roadmap that leadership can actually commit to — not an aspirational document with no path to delivery.",
         deliverables=["A learning strategy document tied explicitly to organisational goals", "A prioritised, fundable investment roadmap", "An impact measurement framework distinct from activity metrics", "A governance structure to keep the strategy live, not shelved"],
         outcomes=["Learning genuinely aligned to organisational goals", "Stronger demonstrable value for money", "A roadmap leadership will actually back and fund"],
         case_title="Digital Skills for Defence (DS4D)", case_metric="Enterprise-wide",
         case_text="Strategic learning architecture and roadmaps for enterprise Defence capability planning, moving leaders from buying courses to building capability against a defined requirement.",
         faqs=[
             ("How is a learning strategy different from a training plan?", "A training plan lists what's being delivered. A learning strategy explains why — the link to organisational goals, the priorities, and how impact will be measured — with the training plan as one output of that thinking, not the starting point."),
             ("Who should be involved in building the strategy?", "Typically L&D leadership plus the business leaders whose goals the strategy needs to serve — a strategy built by L&D alone, without that input, rarely survives contact with real budget decisions."),
             ("How often should a learning strategy be revisited?", "Annually at minimum, and whenever organisational strategy itself shifts significantly — a learning strategy tied to goals that have moved on stops being useful very quickly."),
         ]),
]

for _svc in SERVICES:
    service_page(_svc["slug"], _svc["cat"], _svc["num"], _svc["title"], _svc["h1"], _svc["hero_sub"],
                  _svc["problem"], _svc["diagnosis"], _svc["approach"], _svc["deliverables"], _svc["outcomes"],
                  _svc["case_title"], _svc["case_metric"], _svc["case_text"], _svc["faqs"])

services_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">Services</div>
    <h1 class="reveal in" data-d="1">Grouped around your problem, not my product list.</h1>
    <p class="hero-sub reveal in" data-d="2">Three areas of work. Open any service to see the client challenges, my approach, the outcomes and an example of the work.</p>
  </div>
</header>

<div class="divider"></div>

<section style="padding-top:60px">
  <div class="wrap">
    <div class="svc-cat">
      <div class="svc-cat-head reveal"><span class="cat-no">A</span><h2>Capability &amp; Governance</h2></div>
      <div class="accordion">
{cap_gov}      </div>
    </div>
    <div class="svc-cat">
      <div class="svc-cat-head reveal"><span class="cat-no">B</span><h2>Leadership &amp; Workforce</h2></div>
      <div class="accordion">
{lead_wf}      </div>
    </div>
    <div class="svc-cat">
      <div class="svc-cat-head reveal"><span class="cat-no">C</span><h2>Learning Transformation</h2></div>
      <div class="accordion">
{learn_tx}      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

{roles_section()}
<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">How the work fits together</div>
    {fw_improvement_approach()}
  </div>
</section>

<div class="divider"></div>

{methodology()}
{cta("Not sure which of these you need?", "That's normal — and it's exactly what a first conversation is for. We'll work out the real problem together.", secondary=("View case studies", "case-studies.html"))}'''

# ================================================================== CASE STUDY PAGES
def case_study_page(slug, sector_label, title, metric_fig, metric_label,
                     challenge, context, approach, deliverables, outcome,
                     commercial_impact, transferability, lessons,
                     photo_src, photo_alt, photo_w, photo_h,
                     related_slug, related_title, count=None, suffix=""):
    approach_li = "".join(f"<li>{x}</li>" for x in approach)
    deliverables_li = "".join(f"<li>{x}</li>" for x in deliverables)
    outcome_li = "".join(f"<li>{x}</li>" for x in outcome)
    if count:
        static_val = f'{int(count):,}<span class="unit">{suffix}</span>'
        fig = f'<div class="figure" data-count="{count}" data-suffix="{suffix}">{static_val}</div>'
    else:
        fig = f'<div class="figure">{metric_fig}</div>'
    body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">{sector_label} Case Study</div>
    <h1 class="reveal in" data-d="1">{title}</h1>
    <div class="case-metric reveal in" data-d="2" style="display:inline-block;margin-top:20px">{fig}<div class="label">{metric_label}</div></div>
    <div class="hero-actions reveal in" data-d="3">
      <a href="contact.html#book" class="btn btn-primary">Discuss Your Capability Challenge {ARROW}</a>
      <a href="case-studies.html" class="btn btn-ghost">All case studies</a>
    </div>
  </div>
</header>

{proof()}
<section style="padding-top:84px">
  <div class="wrap">
    <img src="assets/photos/{photo_src}" alt="{photo_alt}" width="{photo_w}" height="{photo_h}" loading="lazy" style="width:100%;border-radius:6px" class="case-hero-img reveal">
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap article">
    <div class="eyebrow reveal">The challenge</div>
    <p class="reveal" style="font-size:1.1rem;line-height:1.75">{challenge}</p>
    <h2 class="reveal" style="margin-top:36px;font-size:1.3rem">Why it mattered</h2>
    <p class="reveal" style="font-size:1.1rem;line-height:1.75">{context}</p>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">The approach</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">What I did, and what it delivered.</p>
    <div class="feature-grid cols-2">
      <div class="feature-card reveal"><h3>Approach</h3><ul class="dot-list">{approach_li}</ul></div>
      <div class="feature-card reveal" data-d="1"><h3>Deliverables</h3><ul class="dot-list">{deliverables_li}</ul></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">The outcome</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Results, measured.</p>
    <ul class="dot-list reveal" data-d="2" style="max-width:640px;font-size:17px">{outcome_li}</ul>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap split">
    <div class="reveal stack-gap">
      <div class="eyebrow">Commercial impact</div>
      <p>{commercial_impact}</p>
    </div>
    <div class="reveal stack-gap" data-d="1">
      <div class="eyebrow">Transferability</div>
      <p>{transferability}</p>
    </div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap article">
    <div class="eyebrow reveal">Lessons learned</div>
    <p class="reveal" style="font-size:1.1rem;line-height:1.75">{lessons}</p>
  </div>
</section>

<div class="divider"></div>

<section class="cta-band">
  <div class="wrap">
    <h2 class="reveal">Recognise this in your organisation?</h2>
    <p class="reveal" data-d="1">Let's talk about what it would take to get a similar result for you.</p>
    <div class="cta-actions reveal" data-d="2">
      <a href="contact.html#book" class="btn btn-primary">Discuss Your Capability Challenge {ARROW}</a>
      <a href="{related_slug}.html" class="btn btn-ghost">Related service: {related_title}</a>
    </div>
  </div>
</section>'''
    page(f"{slug}.html", f"{title} | Prelude Case Study",
         f"{context}"[:300], body, "case-studies", breadcrumb=title,
         article=(title, context[:300]))

CASE_STUDIES_FULL = [
    dict(slug="mod-digital-skills-for-defence", sector="Defence", title="MOD Digital Skills for Defence (DS4D)",
         metric_fig="Defence-wide", metric_label="Building capability, not course catalogues",
         challenge="Defence was framing a digital problem as a training problem — but the real question was what digital capability Defence actually required, and how to align the workforce to it.",
         context="Commissioning courses against an undefined capability requirement risks spending heavily and still missing the mission. The stakes were enterprise-wide digital readiness.",
         approach=["Defined the digital capability requirements against mission and outcomes", "Mapped the skills, behaviours and workforce needs required to deliver them", "Aligned learning architecture to strategic outcomes — not the other way round", "Embedded governance and assurance so decisions stayed defensible"],
         deliverables=["An evidence-based digital capability requirement, mapped to mission", "A skills and behaviours framework for the digital workforce", "A learning architecture aligned to strategic outcomes", "A governance structure decision-makers could defend"],
         outcome=["A clear, evidence-based view of future capability requirements", "Learning architecture aligned to strategic outcomes", "Decision-makers equipped to plan and defend digital capability investment", "Progress in ten weeks that had stalled for twelve months"],
         commercial_impact="Enterprise-wide digital investment decisions moved from assumption to evidence — reducing the risk of committing significant training budget against a capability requirement nobody had actually defined.",
         transferability="The method — define the capability requirement before designing the learning — applies directly to any large organisation modernising a workforce against new technology, in or outside Defence.",
         lessons="At enterprise scale, the first job is to define the capability the mission requires. Training plans built before that are course catalogues, not capability.",
         photo_src="public-sector-transformation-workshop.jpeg", photo_alt="Capability map and learning architecture — transformation roadmap workshop", photo_w=1000, photo_h=562,
         related_slug="learning-strategy", related_title="Learning Strategy"),
    dict(slug="sio-course-rapid-tna", sector="Defence · DSAT", title="Senior Information Officer (SIO) Course — Rapid TNA",
         metric_fig="None", metric_label="Speed and governance, together",
         challenge="A Senior Information Officer course needed analysis at pace — but the team feared that moving quickly would mean cutting DSAT corners and losing defensibility.",
         context="Many believe Defence change is slow because of DSAT. In reality, DSAT is often treated as a process to complete rather than a framework to support decision-making — and that, not governance itself, is what slows things down.",
         approach=["Conducted a rapid, focused Training Needs Analysis", "Identified immediate improvements that could be actioned at once", "Assessed future role requirements and undertook new role analysis", "Developed policy recommendations from the evidence", "Maintained DSAT defensibility and JSP 822 compliance throughout"],
         deliverables=["A rapid TNA report with immediate and future-state findings", "New role analysis for future requirements", "Policy recommendations backed by evidence", "A defensible DSAT/JSP 822 compliance trail, produced at pace"],
         outcome=["Immediate, actionable improvements identified quickly", "Future role requirements defined with evidence", "Policy recommendations leaders could stand behind", "Full DSAT defensibility and JSP 822 compliance preserved"],
         commercial_impact="Avoided the false choice between speed and governance — the organisation got a faster answer without incurring the cost or risk of a later governance failure or audit finding.",
         transferability="Any regulated environment that assumes governance and pace are in conflict can apply the same test: is the framework being used to support decisions, or just to complete a process?",
         lessons="DSAT is a framework to support decisions, not a process to endure. Treated that way, it accelerates good decisions rather than delaying them.",
         photo_src="defence-training-governance-workshop.jpeg", photo_alt="Rapid TNA diagnostic — training governance workshop", photo_w=1000, photo_h=562,
         related_slug="training-needs-analysis", related_title="Training Needs Analysis"),
    dict(slug="defence-capability-framework-design", sector="Defence", title="Defence Capability Framework Design",
         metric_fig=None, metric_label="Increase in operational readiness", count="20", suffix="%",
         challenge="Competency standards were inconsistent, so people couldn't be assessed, developed or planned for in a consistent way.",
         context="Inconsistent standards meant readiness couldn't be measured or trusted — a real operational risk.",
         approach=["Multi-specialisation capability framework design", "Skills mapping across roles and specialisations", "Workforce planning support built on the same standards"],
         deliverables=["A multi-specialisation capability framework", "A skills-to-role mapping matrix", "Assessment criteria usable across every team", "A workforce planning tool built on consistent standards"],
         outcome=["Consistent, defensible standards across every team", "20% increase in operational readiness", "A single, trusted view of capability"],
         commercial_impact="Readiness that can be measured and trusted directly reduces operational risk — and a single set of standards removes the duplicated effort of every team building its own definition of 'ready'.",
         transferability="Any organisation running multiple teams or specialisations against inconsistent standards — not just Defence — faces the same readiness-measurement risk this framework solved.",
         lessons="A framework only changes behaviour when it's usable for assessment and planning — not simply published.",
         photo_src="capability-framework-review-2.jpeg", photo_alt="Capability framework snapshot — two professionals reviewing framework documentation", photo_w=540, photo_h=360,
         related_slug="capability-framework-design", related_title="Capability Framework Design"),
    dict(slug="op-isotrope-role-architecture-redesign", sector="Defence · Crisis response", title="Operational Role Architecture Redesign (Op Isotrope)",
         metric_fig=None, metric_label="Improvement in response effectiveness", count="15", suffix="%",
         challenge="A national crisis required the organisation to scale rapidly — but roles and skills weren't clear enough to do it cleanly.",
         context="In a crisis, ambiguity costs time and effectiveness the organisation didn't have.",
         approach=["Role architecture redesign under crisis timescales", "Skills alignment to immediate operational need", "Organisational structure improvements to support rapid scaling"],
         deliverables=["A redesigned role architecture for crisis-scale operation", "Clarified accountabilities across newly scaled teams", "Structural recommendations that supported rapid onboarding"],
         outcome=["15% improvement in response effectiveness", "Faster, clearer scaling under pressure", "Reduced role ambiguity across newly formed teams"],
         commercial_impact="In a national crisis response, effectiveness gains translate directly into lives and outcomes affected, and into avoided cost of confusion and rework during the highest-pressure phase of the operation.",
         transferability="Any organisation that needs to scale a workforce rapidly and cleanly — merger, crisis response, sudden demand growth — faces the same role-clarity problem this engagement solved.",
         lessons="In a crisis, clarity of role beats volume of training every time.",
         photo_src="defence-operational-planning-briefing.jpeg", photo_alt="Operational role architecture — defence planning briefing", photo_w=638, photo_h=360,
         related_slug="workforce-planning", related_title="Workforce Planning"),
    dict(slug="healthcare-learning-transformation", sector="Healthcare", title="Healthcare Learning Transformation",
         metric_fig=None, metric_label="Reduction in compliance gaps", count="18", suffix="%",
         challenge="Across 15,000 colleagues, learning compliance and reporting were unreliable, leaving leaders blind to risk.",
         context="In healthcare, compliance gaps aren't admin — they're patient safety and regulatory exposure.",
         approach=["Totara dashboard design and configuration", "Structured learning pathway redesign", "Information management improvements across the platform"],
         deliverables=["Totara dashboards giving leaders real-time visibility", "Structured, role-based learning pathways", "An information management framework for ongoing data reliability"],
         outcome=["18% reduction in compliance gaps", "Clear visibility of learning risk for the first time", "Leaders able to trust their own compliance reporting"],
         commercial_impact="Reliable compliance reporting reduces regulatory exposure directly, and the same dashboards removed a significant amount of manual reporting effort across the organisation.",
         transferability="Any regulated organisation managing compliance training at scale — not only healthcare — faces the same trust-in-the-data problem this engagement solved.",
         lessons="Reliable data changes behaviour faster than more mandatory training.",
         photo_src="healthcare-workforce-planning-meeting.jpeg", photo_alt="Compliance dashboard — NHS workforce planning meeting", photo_w=1000, photo_h=562,
         related_slug="lms-optimisation", related_title="LMS Optimisation"),
    dict(slug="housing-leadership-onboarding-transformation", sector="Housing", title="Housing Leadership &amp; Onboarding Transformation",
         metric_fig=None, metric_label="Reduction in time-to-competence", count="20", suffix="%",
         challenge="Onboarding was slow and leadership development inconsistent, holding back performance and retention.",
         context="Slow onboarding meant new colleagues took too long to contribute — and inconsistent leadership cost engagement.",
         approach=["Leadership development pathway design", "Values-based onboarding redesign", "Digital learning solutions for distributed teams"],
         deliverables=["A leadership development pathway for new and promoted managers", "A values-based onboarding programme", "Digital learning content for teams spread across sites"],
         outcome=["20% reduction in time-to-competence", "More consistent leadership standards", "Faster productive contribution from new starters"],
         commercial_impact="Cutting time-to-competence by 20% means new colleagues reach full productivity faster — a direct reduction in the cost of onboarding and the risk period before someone is fully effective.",
         transferability="Any organisation with distributed teams and a pattern of inconsistent onboarding — housing, retail, healthcare, professional services — faces the same underlying problem this solved.",
         lessons="Values and expectations have to be designed into onboarding — not left to osmosis.",
         photo_src="housing-management-development-workshop.jpeg", photo_alt="Onboarding journey — housing management development workshop", photo_w=1000, photo_h=666,
         related_slug="leadership-development", related_title="Leadership Development"),
    dict(slug="defence-apprenticeship-success-programme", sector="Defence", title="Defence Apprenticeship Success Programme",
         metric_fig=None, metric_label="Completion rate · 100% funding compliance", count="95", suffix="%",
         challenge="Apprenticeship completion and qualification rates needed to improve, with funding compliance under scrutiny.",
         context="Low completion wastes investment and risks funding — and fails the people on the programme.",
         approach=["Coaching and learner support for at-risk apprentices", "Active progress management with early-warning triggers", "Structured development pathways aligned to funding rules"],
         deliverables=["A progress management system with early-warning triggers", "A coaching and support framework", "A funding compliance audit trail"],
         outcome=["95% completion rate", "100% funding compliance", "Genuine capability built, not just qualifications gained"],
         commercial_impact="Protecting apprenticeship funding compliance avoids clawback risk directly, while 95% completion means training spend actually converts into deployable capability rather than wasted investment.",
         transferability="Any apprenticeship or funded training programme, in any sector, that has completion or funding-compliance risk can apply the same progress-management discipline.",
         lessons="Completion is an operations problem as much as a teaching one.",
         photo_src="defence-secure-operations-centre.jpeg", photo_alt="Progress governance — defence operations centre", photo_w=1000, photo_h=562,
         related_slug="apprenticeships", related_title="Apprenticeships"),
    dict(slug="nato-royal-navy-training-modernisation", sector="Defence · NATO &amp; Royal Navy", title="NATO &amp; Royal Navy Training Modernisation",
         metric_fig=None, metric_label="Increase in pass rates · 20% fewer failures", count="17", suffix="%",
         challenge="Established training needed to lift operational readiness and learner performance.",
         context="Pass and failure rates directly affect how quickly capable people reach the front line.",
         approach=["DSAT-compliant Training Needs Analysis", "Blended learning design targeted at the specific failure points", "Coaching interventions", "E-learning solutions"],
         deliverables=["A DSAT-compliant TNA identifying specific pipeline failure points", "Redesigned blended learning content", "A coaching intervention model", "Supporting e-learning modules"],
         outcome=["17% increase in pass rates", "20% reduction in failure rates", "Higher readiness and better learner performance"],
         commercial_impact="Fewer failures means less wasted training capacity and faster time for capable people to reach the front line — a direct improvement in the return on the training pipeline's cost.",
         transferability="Any training pipeline with an identifiable pass/fail bottleneck — not only military — can apply the same targeted-diagnosis approach rather than redesigning the whole programme.",
         lessons="Target the few points that move pass rates, rather than redesigning everything.",
         photo_src="defence-military-operations-room.jpeg", photo_alt="Learning pathway — NATO and Royal Navy training modernisation", photo_w=596, photo_h=335,
         related_slug="training-needs-analysis", related_title="Training Needs Analysis"),
]

for _cs in CASE_STUDIES_FULL:
    case_study_page(_cs["slug"], _cs["sector"], _cs["title"], _cs["metric_fig"], _cs["metric_label"],
                     _cs["challenge"], _cs["context"], _cs["approach"], _cs["deliverables"], _cs["outcome"],
                     _cs["commercial_impact"], _cs["transferability"], _cs["lessons"],
                     _cs["photo_src"], _cs["photo_alt"], _cs["photo_w"], _cs["photo_h"],
                     _cs["related_slug"], _cs["related_title"],
                     count=_cs.get("count"), suffix=_cs.get("suffix", ""))

cs_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">Case Studies</div>
    <h1 class="reveal in" data-d="1">Problems solved. Risk reduced. Results measured.</h1>
    <p class="hero-sub reveal in" data-d="2">Real capability, governance and learning projects across Defence, Healthcare and Housing — told as stories, with the commercial outcome that mattered.</p>
    <div class="filter-bar reveal in" data-d="3">
      <button class="filter-btn active" data-filter="all">All</button>
      <button class="filter-btn" data-filter="defence">Defence</button>
      <button class="filter-btn" data-filter="healthcare">Healthcare</button>
      <button class="filter-btn" data-filter="housing">Housing</button>
    </div>
  </div>
</header>

<div class="divider"></div>

<section style="padding-top:20px">
  <div class="wrap">
    <p class="lead reveal" style="margin-bottom:10px">Every study below was diagnosed against the Prelude Capability Model&trade; — mission and outcomes first, training last.</p>
    {fw_prelude_model()}
  </div>
</section>

<section>
  <div class="wrap">
{case("defence","Defence","MOD Digital Skills for Defence (DS4D)","Defence-wide","Building capability, not course catalogues",
  "Defence was framing a digital problem as a training problem — but the real question was what digital capability Defence actually required, and how to align the workforce to it.",
  "Commissioning courses against an undefined capability requirement risks spending heavily and still missing the mission. The stakes were enterprise-wide digital readiness.",
  "The challenge was never simply training. Once we mapped mission to capability, it was clear the gaps sat in undefined capability requirements, unmapped behaviours and workforce needs, and a learning estate that wasn't aligned to strategic outcomes.",
  ["Defined the digital capability requirements against mission and outcomes","Mapped the skills, behaviours and workforce needs required to deliver them","Aligned learning architecture to strategic outcomes — not the other way round","Embedded governance and assurance so decisions stayed defensible"],
  ["A clear, evidence-based view of future capability requirements","Learning architecture aligned to strategic outcomes","Decision-makers equipped to plan and defend digital capability investment","Progress in ten weeks that had stalled for twelve months"],
  "Leaders moved from buying courses to building capability — investing with confidence against a defined requirement rather than assumption.",
  "At enterprise scale, the first job is to define the capability the mission requires. Training plans built before that are course catalogues, not capability.",
  "public-sector-transformation-workshop.jpeg", "Capability map and learning architecture — transformation roadmap workshop", 1000, 562, slug="mod-digital-skills-for-defence")}
{case("defence","Defence · DSAT","Senior Information Officer (SIO) Course — Rapid TNA",None,"Speed and governance, together",
  "A Senior Information Officer course needed analysis at pace — but the team feared that moving quickly would mean cutting DSAT corners and losing defensibility.",
  "Many believe Defence change is slow because of DSAT. In reality, DSAT is often treated as a process to complete rather than a framework to support decision-making — and that, not governance itself, is what slows things down.",
  "Used as a decision-support framework rather than a box-ticking process, DSAT could move fast. The real constraints were unclear current requirements and undefined future role needs — not the methodology.",
  ["Conducted a rapid, focused Training Needs Analysis","Identified immediate improvements that could be actioned at once","Assessed future role requirements and undertook new role analysis","Developed policy recommendations from the evidence","Maintained DSAT defensibility and JSP 822 compliance throughout"],
  ["Immediate, actionable improvements identified quickly","Future role requirements defined with evidence","Policy recommendations leaders could stand behind","Full DSAT defensibility and JSP 822 compliance preserved"],
  "The organisation proved it didn't have to choose between speed and governance — with the right approach, it achieved both.",
  "DSAT is a framework to support decisions, not a process to endure. Treated that way, it accelerates good decisions rather than delaying them.",
  "defence-training-governance-workshop.jpeg", "Rapid TNA diagnostic — training governance workshop", 1000, 562, slug="sio-course-rapid-tna")}
{case("defence","Defence","Defence Capability Framework Design",None,"Increase in operational readiness",
  "Competency standards were inconsistent, so people couldn't be assessed, developed or planned for in a consistent way.",
  "Inconsistent standards meant readiness couldn't be measured or trusted — a real operational risk.",
  "Each team was defining roles and competence differently, so 'ready' meant different things in different places.",
  ["Multi-specialisation capability framework","Skills mapping across roles","Workforce planning support"],
  ["Consistent, defensible standards","20% increase in operational readiness"],
  "A single, trusted view of capability that underpinned assessment, development and workforce planning.",
  "A framework only changes behaviour when it's usable for assessment and planning — not simply published.",
  "capability-framework-review-2.jpeg", "Capability framework snapshot — two professionals reviewing framework documentation", 540, 360, count="20", suffix="%", slug="defence-capability-framework-design")}
{case("defence","Defence · Crisis response","Operational Role Architecture Redesign (OP ISOTROPE)",None,"Improvement in response effectiveness",
  "A national crisis required the organisation to scale rapidly — but roles and skills weren't clear enough to do it cleanly.",
  "In a crisis, ambiguity costs time and effectiveness the organisation didn't have.",
  "Under crisis pace, role ambiguity — not individual skill — was the biggest drag on effectiveness.",
  ["Role architecture redesign","Skills alignment to operational need","Organisational structure improvements"],
  ["15% improvement in response effectiveness","Faster, clearer scaling"],
  "The organisation scaled at pace without losing clarity of role, accountability or capability.",
  "In a crisis, clarity of role beats volume of training every time.",
  "defence-operational-planning-briefing.jpeg", "Operational role architecture — defence planning briefing", 638, 360, count="15", suffix="%", slug="op-isotrope-role-architecture-redesign")}
{case("healthcare","Healthcare","Healthcare Learning Transformation",None,"Reduction in compliance gaps",
  "Across 15,000 colleagues, learning compliance and reporting were unreliable, leaving leaders blind to risk.",
  "In healthcare, compliance gaps aren't admin — they're patient safety and regulatory exposure.",
  "Compliance data existed, but it couldn't be trusted — so leaders were managing risk blind.",
  ["Totara dashboards","Structured learning pathways","Information management improvements"],
  ["18% reduction in compliance gaps","Clear visibility of learning risk"],
  "Leaders gained confidence in compliance reporting across a 15,000-strong workforce.",
  "Reliable data changes behaviour faster than more mandatory training.",
  "healthcare-workforce-planning-meeting.jpeg", "Compliance dashboard — NHS workforce planning meeting", 1000, 562, count="18", suffix="%", slug="healthcare-learning-transformation")}
{case("housing","Housing","Housing Leadership &amp; Onboarding Transformation",None,"Reduction in time-to-competence",
  "Onboarding was slow and leadership development inconsistent, holding back performance and retention.",
  "Slow onboarding meant new colleagues took too long to contribute — and inconsistent leadership cost engagement.",
  "Onboarding was inconsistent and leadership expectations were unwritten, so new managers learned by chance.",
  ["Leadership development pathways","Values-based onboarding","Digital learning solutions"],
  ["20% reduction in time-to-competence","More consistent leadership"],
  "New colleagues became productive faster, under a consistent leadership standard.",
  "Values and expectations have to be designed into onboarding — not left to osmosis.",
  "housing-management-development-workshop.jpeg", "Onboarding journey — housing management development workshop", 1000, 666, count="20", suffix="%", slug="housing-leadership-onboarding-transformation")}
{case("defence","Defence","Defence Apprenticeship Success Programme",None,"Completion rate · 100% funding compliance",
  "Apprenticeship completion and qualification rates needed to improve, with funding compliance under scrutiny.",
  "Low completion wastes investment and risks funding — and fails the people on the programme.",
  "Drop-off was driven by weak progress management and support — not by learner ability.",
  ["Coaching and learner support","Progress management","Structured development pathways"],
  ["95% completion rate","100% funding compliance"],
  "A stronger internal pipeline and protected funding, with genuine capability built — not just qualifications gained.",
  "Completion is an operations problem as much as a teaching one.",
  "defence-secure-operations-centre.jpeg", "Progress governance — defence operations centre", 1000, 562, count="95", suffix="%", slug="defence-apprenticeship-success-programme")}
{case("defence","Defence · NATO &amp; Royal Navy","NATO &amp; Royal Navy Training Modernisation",None,"Increase in pass rates · 20% fewer failures",
  "Established training needed to lift operational readiness and learner performance.",
  "Pass and failure rates directly affect how quickly capable people reach the front line.",
  "A DSAT-compliant TNA pinpointed the specific points in the pipeline where learners were being set up to fail.",
  ["DSAT-compliant TNA","Blended learning design","Coaching interventions","E-learning solutions"],
  ["17% increase in pass rates","20% reduction in failure rates"],
  "Higher readiness and better learner performance, with less wasted training effort.",
  "Target the few points that move pass rates, rather than redesigning everything.",
  "defence-military-operations-room.jpeg", "Learning pathway — NATO and Royal Navy training modernisation", 596, 335, count="17", suffix="%", slug="nato-royal-navy-training-modernisation")}
  </div>
</section>

{cta("Recognise your organisation in any of these?", "If so, let's talk about what it would take to get the same result for you.", secondary=("Explore services", "services.html"))}'''

# ================================================================== GLOSSARY
# Each entry: (slug, term, definition, link_href, link_label)
GLOSSARY_TERMS = [
    ("active-sc-dv-clearance", "Active SC / DV Clearance", "UK Government security clearance levels — Security Check (SC) and the higher Developed Vetting (DV) — required to work on sensitive Defence and government programmes. Jason holds Active SC clearance and is a former DV holder.", "about.html", "About Jason's clearances"),
    ("apprenticeship-funding-compliance", "Apprenticeship Funding Compliance", "The evidence and audit trail required to protect government-funded apprenticeship investment — proving that funded time, off-the-job training and progress tracking meet the rules, not just that someone eventually qualified.", "apprenticeships.html", "Apprenticeships service"),
    ("capability-diagnostic-framework", "Capability Diagnostic Framework&trade;", "Prelude's framework for tracing performance from mission and outcomes down through required capability, behaviours and evidence — used to identify exactly which layer is missing when capability fails.", "defence.html", "See it applied on the Defence page"),
    ("capability-framework", "Capability Framework", "A defined, consistent standard of competence for a role or specialisation, used for assessment, development and workforce planning. Unlike a job description, a capability framework is meant to be applied the same way by every assessor, not interpreted locally by every team.", "what-is-a-capability-framework.html", "Read the full definition"),
    ("capability-improvement-approach", "Capability Improvement Approach&trade;", "Prelude's six-stage method for turning a capability problem into measurable performance: understand the mission, analyse the gap, identify root causes, design the right intervention, measure impact, and improve continuously.", "how-i-work.html", "How I Work"),
    ("capability-readiness-maturity-model", "Capability Readiness Maturity Model&trade;", "Five stages of organisational capability maturity, from Reactive (ad-hoc, no evidence) through Compliant and Structured to Measured and Optimised. Most organisations can place themselves on this scale within one conversation.", "how-i-work.html", "How I Work"),
    ("capability-readiness-review", "Capability Readiness Review&trade;", "Prelude's ten-question diagnostic for identifying which of six areas — capability, leadership, process, governance, workforce or training — a performance problem actually sits in, before any solution is designed.", "capability-readiness-review.html", "Take the free self-assessment"),
    ("capability-vs-competency", "Capability vs Competency", "Related but distinct: competency usually describes an individual's skill or behaviour, while capability describes whether the organisation as a whole — people, governance, structure and process together — can reliably deliver the outcome. An organisation can have competent individuals and still lack capability.", "capability-vs-competency-explained.html", "Read the full explanation"),
    ("change-management", "Change Management", "The discipline of managing the human and structural side of organisational transformation — communication, adoption, resistance and sequencing — distinct from capability building, though the two need to work together for change to stick.", "change-management-vs-capability-building.html", "Read the full explanation"),
    ("cmi", "CMI", "The Chartered Management Institute — the UK's professional body for management and leadership, awarding recognised qualifications in leadership and coaching.", "about.html", "About Jason's qualifications"),
    ("dsat", "DSAT", "The Defence Systems Approach to Training — the methodology set out in JSP 822 for designing, delivering and assuring training across UK Defence. In practice, it's a structured way of answering five questions: what capability is required, how will training be designed, developed and delivered to build it, and how will you know it worked.", "dsat-explained.html", "Read: DSAT Explained"),
    ("evaluation-kirkpatrick", "Evaluation (Kirkpatrick Model)", "The standard four-level model for measuring training effectiveness: reaction, learning, behaviour and results. Most organisations measure only the first level (did people enjoy it) and call it evaluation — genuine evaluation asks whether behaviour and results actually changed.", "kirkpatricks-model-in-practice.html", "Read the full article"),
    ("jsp-822", "JSP 822", "The Ministry of Defence Joint Service Publication that sets out DSAT requirements — the policy document behind Defence training governance, assurance and audit.", "dsat-explained.html", "Read: DSAT Explained"),
    ("learning-governance", "Learning Governance", "The decision rights and evidence trail behind how training and learning are assured, audited and held accountable — who owns which decision, and what evidence proves it was made well.", "training-governance-complete-guide.html", "Read the complete guide"),
    ("learning-strategy", "Learning Strategy", "The document connecting capability investment to organisational goals — what's being invested in, why, and how impact will be measured — as distinct from a training plan, which just lists what's being delivered.", "learning-strategy-complete-guide.html", "Read the complete guide"),
    ("lms", "LMS (Learning Management System)", "The platform used to deliver, track and report on training. An LMS produces data by default, but data isn't the same as trustworthy reporting — most LMS problems are configuration and information management issues, not platform failures.", "what-is-an-lms.html", "Read the full definition"),
    ("organisational-development", "Organisational Development", "The discipline of improving how an organisation functions structurally — roles, governance, culture and process — rather than only developing individual skills. Capability work often surfaces organisational development needs that training alone can't address.", "services.html", "Explore services"),
    ("performance-consulting", "Performance Consulting", "Diagnosing why organisational performance is falling short before prescribing a solution — testing whether the cause is genuinely a skills gap, or something structural, before recommending training, restructuring or anything else.", "performance-consulting-complete-guide.html", "Read the complete guide"),
    ("prelude-capability-model", "Prelude Capability Model&trade;", "Prelude's primary framework, tracing performance from mission and outcomes down through required capability, behaviours, skills and knowledge, governance and assurance, to performance evidence. When any layer is missing, capability fails — and no amount of training fixes it.", "how-i-work.html", "How I Work"),
    ("prince2", "PRINCE2", "A structured project management methodology widely used across UK government and Defence programmes. Jason is a PRINCE2 Practitioner.", "about.html", "About Jason's qualifications"),
    ("skills-framework", "Skills Framework", "A map of the specific skills required for particular roles — narrower and more operational than a capability framework, which sets the broader standard a role needs to meet. Skills frameworks are what make workforce planning and succession possible in practice.", "what-is-a-skills-framework.html", "Read the full definition"),
    ("succession-planning", "Succession Planning", "Preparing the pipeline for critical roles before a vacancy forces a rushed decision — identifying and developing likely successors ahead of need, rather than reacting when someone leaves.", "succession-planning-critical-roles.html", "Read the article"),
    ("tna", "TNA (Training Needs Analysis)", "The structured process of testing whether a performance gap is genuinely a training gap, or whether it's being held back by something else — unclear roles, weak governance, or a structure working against the outcome. A properly run TNA can conclude that training isn't the answer.", "training-needs-analysis-complete-guide.html", "Read the complete guide"),
    ("totara", "Totara", "An open-source Learning Management System, built on Moodle, widely used across UK healthcare and public sector organisations for its flexibility around compliance reporting and structured learning pathways.", "totara-vs-off-the-shelf-lms.html", "Read the comparison"),
    ("training-governance", "Training Governance", "Governance applied specifically to training delivery and compliance — audit-ready evidence, clear decision rights, and defensible assurance that training is meeting the standard it's supposed to.", "training-governance-complete-guide.html", "Read the complete guide"),
    ("training-vs-capability-decision-model", "Training vs Capability Decision Model&trade;", "Prelude's test for whether a performance gap needs training or something structural: if the knowledge or skill is genuinely missing, it's a training problem. If it isn't, the real issue is usually structure, governance, leadership or process.", "training-vs-capability-decision-model-explained.html", "Read the full explanation"),
    ("workforce-planning", "Workforce Planning", "Aligning roles, skills and structure to actual operational demand, so an organisation is ready for what's coming, not just resourced for what's here today.", "workforce-planning.html", "Workforce Planning service"),
]

def glossary_body():
    nav_chips = "".join(f'<a href="#{slug}" class="chip">{term}</a>' for slug, term, _d, _h, _l in GLOSSARY_TERMS)
    items = ""
    for slug, term, definition, href, label in GLOSSARY_TERMS:
        items += f'''      <div class="glossary-item" id="{slug}">
        <dt>{term}</dt>
        <dd>{definition} <a class="read" href="{href}">{label} &rarr;</a></dd>
      </div>
'''
    return f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">Insights</div>
    <h1 class="reveal in" data-d="1">Capability &amp; Learning Glossary</h1>
    <p class="hero-sub reveal in" data-d="2">Plain-English definitions of the terms used across this site — DSAT, TNA, capability frameworks and the rest — each linking through to where we cover it properly.</p>
    <div class="glossary-nav reveal in" data-d="3">{nav_chips}</div>
  </div>
</header>

<div class="divider"></div>

<section>
  <div class="wrap">
    <dl class="glossary-list">
{items}    </dl>
  </div>
</section>

{cta("Want this thinking applied to your organisation?", "Insight is useful. Applied insight changes outcomes. Let's talk about yours.", secondary=("See the evidence", "case-studies.html"))}'''

page("glossary.html", "Capability &amp; Learning Glossary — DSAT, TNA &amp; Key Terms Explained | Prelude",
     "Plain-English definitions of DSAT, TNA, capability frameworks and the other terms used across Prelude's site — each linking through to a deeper article or service page.",
     glossary_body(), "insights", breadcrumb="Glossary", terms=GLOSSARY_TERMS)

# ================================================================== INSIGHT ARTICLES
def insight_article_page(slug, category, title, h1, hero_sub, sections, faqs, related_slug, related_title, kind="Insight", related_reading=None):
    body_html = ""
    for heading, paragraphs in sections:
        body_html += f'<h2 class="reveal">{heading}</h2>\n'
        for p in paragraphs:
            body_html += f'<p class="reveal">{p}</p>\n'
    reading_html = ""
    if related_reading:
        items = "".join(f'<li><a class="read" href="{s}.html">{t} &rarr;</a></li>' for t, s in related_reading)
        reading_html = f'''<div class="divider"></div>

<section>
  <div class="wrap article">
    <div class="eyebrow reveal">Related reading</div>
    <ul class="dot-list reveal" style="margin-top:20px">{items}</ul>
  </div>
</section>

'''
    body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">{category} &middot; {kind}</div>
    <h1 class="reveal in" data-d="1">{h1}</h1>
    <p class="hero-sub reveal in" data-d="2">{hero_sub}</p>
  </div>
</header>

<div class="divider"></div>

<section>
  <div class="wrap article">
{body_html}  </div>
</section>

{reading_html}<div class="divider"></div>

{faq_section(faqs, "Common questions on this topic.")}
<section class="cta-band">
  <div class="wrap">
    <h2 class="reveal">Want this thinking applied to your organisation?</h2>
    <p class="reveal" data-d="1">Insight is useful. Applied insight changes outcomes. Let's talk about yours.</p>
    <div class="cta-actions reveal" data-d="2">
      <a href="contact.html#book" class="btn btn-primary">Discuss Your Capability Challenge {ARROW}</a>
      <a href="{related_slug}.html" class="btn btn-ghost">{related_title}</a>
    </div>
  </div>
</section>'''
    page(f"{slug}.html", f"{title} | Prelude Insights", hero_sub, body, "insights",
         breadcrumb=title, faq=faqs, article=(title, hero_sub))

INSIGHTS_FULL = [
    dict(slug="dsat-explained", category="Defence", title="DSAT Explained",
         h1="DSAT Explained: What JSP 822 Actually Asks of You",
         hero_sub="The Defence Systems Approach to Training, without the acronym overload — what it actually requires, and why it gets blamed for problems it didn't cause.",
         sections=[
             ("What DSAT actually is",
              ["DSAT — the Defence Systems Approach to Training — is the methodology set out in JSP 822 for designing, delivering and assuring training across Defence. Strip away the acronym and it's a structured way of answering five questions: what capability is required, how will training be designed to build it, how will it be developed, how will it be delivered, and how will you know it worked.",
               "It exists for a reasonable purpose: training that isn't systematically designed against a real requirement tends to drift — delivering what's easy to teach rather than what the mission actually needs."]),
             ("Why DSAT gets a bad reputation",
              ["Almost every complaint about DSAT is really a complaint about how it's been implemented locally, not about the framework itself. Treated as a checklist to complete before training can be signed off, it becomes exactly the slow, bureaucratic process people assume it is.",
               "Treated as a decision-support framework — a structured way of testing whether a proposed intervention actually addresses the capability requirement — it does the opposite: it stops organisations wasting time and money on training that was never going to work."]),
             ("The phases, in plain English",
              ["DSAT runs through Analysis (what's the capability requirement, and what's the gap), Design (what should the training look like to close it), Development (building the actual content and materials), Delivery (running it), and Evaluation (did it work, and what does that tell you for next time).",
               "The phases aren't meant to be a one-way waterfall. The most effective DSAT implementations treat Analysis and Evaluation as a loop — using what you learn from delivery to sharpen the next round of analysis, rather than starting from zero each time."]),
             ("Where organisations go wrong",
              ["The most common failure is skipping straight to Design and Development because someone has already decided training is the answer — which defeats the purpose of the Analysis phase, whose actual job is to test that assumption.",
               "The second most common failure is treating Evaluation as a satisfaction survey rather than a test of whether the capability gap actually closed. A course that everyone enjoyed but that didn't move the underlying metric hasn't been evaluated properly — it's been rated."]),
             ("Using DSAT to move faster, not slower",
              ["The Senior Information Officer Rapid TNA case study is a direct example: a team that assumed speed and DSAT compliance were in conflict discovered that used properly, as a decision framework rather than a process to endure, DSAT accelerated good decisions rather than delaying them.",
               "The real constraint in that engagement wasn't the methodology — it was unclear current requirements and undefined future role needs. Once those were resolved, DSAT-defensible answers came quickly."]),
         ],
         faqs=[
             ("Is DSAT only relevant to the Ministry of Defence?", "DSAT and JSP 822 are Defence-specific, but the underlying discipline — define the capability requirement, test whether training is the right intervention, evaluate against the outcome, not just satisfaction — applies to any regulated or high-stakes training environment."),
             ("Does DSAT compliance slow down urgent training requirements?", "Not when it's applied as intended. Speed problems usually come from unclear requirements or treating DSAT as sequential paperwork, not from the framework itself — see the Rapid TNA case study for a direct example."),
             ("What's the difference between DSAT and a standard instructional design model like ADDIE?", "They share the same broad shape — analysis through evaluation — but DSAT is specifically aligned to Defence governance, assurance and audit requirements under JSP 822, with defensibility built into every phase."),
         ],
         related_slug="dsat-consultancy", related_title="DSAT Consultancy",
         related_reading=[
             ("Training Governance: The Complete Guide", "training-governance-complete-guide"),
             ("What Is JSP 822? A Plain-English Explanation", "what-is-jsp-822"),
             ("Governance vs Compliance: Why the Distinction Matters", "governance-vs-compliance"),
         ]),
    dict(slug="training-needs-analysis-best-practice", category="Method", title="Training Needs Analysis: Best Practice",
         h1="Training Needs Analysis: Best Practice for Finding the Real Gap",
         hero_sub="How to run a TNA that finds the real gap and gives leaders evidence — not a survey that just confirms what people already assumed.",
         sections=[
             ("Why most TNAs fail before they start",
              ["Most Training Needs Analyses fail for a simple reason: they start from an assumption that training is needed, and work backwards to justify it, rather than starting from the performance gap and testing what's actually causing it.",
               "A TNA that begins with \"what course do you think you need\" has already skipped the one question that matters: is this a training need at all?"]),
             ("The questions a good TNA actually asks",
              ["A defensible TNA tests whether the knowledge or skill is genuinely missing, or whether performance is being held back by something else — unclear roles, weak governance, a structure working against the outcome, or simply unclear expectations.",
              "It also asks what evidence exists for the current position, rather than relying on the loudest stakeholder's opinion of where the gap sits."]),
             ("Evidence vs assumption",
              ["The difference between a TNA that leaders can act on and one that gets quietly shelved is almost always the evidence base. A TNA built on a handful of interviews with people who requested the training in the first place will tend to recommend more training — that's a sampling bias, not a finding.",
               "Performance data, error rates, incident reports, and structured observation are all more defensible starting points than a survey of what people say they want."]),
             ("Common mistakes",
              ["The most common mistake is letting a TNA become a wishlist exercise — asking stakeholders what training they'd like, then packaging the answers as a needs analysis. The second is failing to establish a baseline, so nobody can say afterwards whether the intervention actually worked.",
               "A close third is treating every request as equally urgent, rather than prioritising by evidenced impact on performance."]),
             ("What a defensible TNA looks like",
              ["The NATO and Royal Navy Training Modernisation case study is a clear example: a DSAT-compliant TNA pinpointed the specific points in the training pipeline where learners were being set up to fail, rather than recommending a wholesale redesign.",
               "That precision — targeting the few points that actually move performance, rather than redesigning everything — lifted pass rates by 17% and cut failures by 20%, with far less wasted effort than a blanket response would have taken."]),
         ],
         faqs=[
             ("How long should a proper TNA take?", "It depends on scope, but a focused TNA against a specific performance problem is typically weeks, not months. Scope creep — trying to analyse everything at once — is usually what turns a TNA into a multi-month project."),
             ("Who should be interviewed or consulted during a TNA?", "A mix of people closest to the performance problem and people accountable for the outcome — not only the people who originally requested training, whose view is useful but not sufficient on its own."),
             ("What happens if the TNA concludes training isn't needed?", "That's a legitimate and valuable finding — it means investment can be redirected to whatever is actually causing the gap, rather than being spent on training that wouldn't have worked."),
         ],
         related_slug="training-needs-analysis", related_title="Training Needs Analysis",
         related_reading=[
             ("Training Needs Analysis: The Complete Guide", "training-needs-analysis-complete-guide"),
             ("How to Run a DSAT-Compliant TNA, Step by Step", "dsat-compliant-tna-step-by-step"),
             ("Common TNA Mistakes That Waste Budget", "common-tna-mistakes"),
         ]),
    dict(slug="building-capability-frameworks", category="Capability", title="Building Capability Frameworks",
         h1="Building Capability Frameworks People Actually Use",
         hero_sub="Designing competency frameworks people actually use — not a document that gets published once and never opened again.",
         sections=[
             ("Why most frameworks gather dust",
              ["Most capability frameworks are built as compliance documents — something to point to when asked whether standards exist — rather than as working tools that inform assessment, development and workforce planning day to day.",
               "The tell is simple: if nobody has opened the framework document since it was published, it isn't a capability framework. It's an artefact."]),
             ("What makes a framework usable",
              ["A usable framework is built with its end use in mind from the start: can a manager use it to assess someone fairly, can HR use it to plan the workforce, can an individual use it to understand what progression actually requires.",
               "That means involving the people who'll use it in its design, and testing early drafts against real assessment scenarios rather than finalising the document in isolation."]),
             ("Multi-specialisation design",
              ["Organisations with multiple specialisations or role types often end up with inconsistent, locally-invented standards — because nobody owns a framework that spans all of them. Multi-specialisation design deliberately maps common ground across roles while preserving what's genuinely distinct about each.",
               "Done well, this makes cross-specialisation workforce planning possible for the first time, because 'ready' means something comparable across the organisation."]),
             ("The consistency test",
              ["The clearest test of whether a framework is working: can two different managers assess the same person against the same standard and reach the same conclusion? If the answer varies by manager, the framework isn't providing the consistency it was built for, however well-written the document is.",
               "This is exactly the risk the Defence Capability Framework Design case study addressed — before the framework, 'ready' meant different things in different teams, which is an operational risk, not just an administrative inconvenience."]),
             ("Proof it can work",
              ["That multi-specialisation framework and skills mapping exercise lifted operational readiness by 20% — not because the document itself changed anything, but because it was designed from the outset to be usable for assessment, development and workforce planning, and was actually adopted as a result."]),
         ],
         faqs=[
             ("How is a capability framework different from a set of job descriptions?", "Job descriptions describe a role. A capability framework defines the standard of competence expected — usable for assessing anyone against that standard, regardless of exact job title, and for planning the workforce against future needs."),
             ("Do frameworks need to be reviewed regularly?", "Yes — a framework tied to a mission or operating model that has since changed will drift out of relevance quickly. Annual review, or review whenever the operating model shifts significantly, keeps it usable."),
             ("Can a small organisation justify building a formal framework?", "Scale down the ambition, not the discipline — a lightweight framework covering a handful of core roles can deliver the same consistency benefit for a small team as a multi-specialisation framework does for an enterprise."),
         ],
         related_slug="capability-framework-design", related_title="Capability Framework Design",
         related_reading=[
             ("Capability Development: The Complete Guide", "capability-development-complete-guide"),
             ("What Is a Capability Framework? A Practical Definition", "what-is-a-capability-framework"),
             ("Multi-Specialisation Capability Frameworks Explained", "multi-specialisation-capability-frameworks"),
         ]),
    dict(slug="leadership-in-high-pressure-environments", category="Leadership", title="Leadership in High-Pressure Environments",
         h1="What the Military Teaches About Leaders Who Hold Up When It Counts",
         hero_sub="Leadership that holds up under real pressure looks different from leadership that only has to work in comfortable conditions — and it can be built deliberately.",
         sections=[
             ("Leadership under pressure is different",
              ["Leadership in calm conditions and leadership under real pressure are not the same skill, even though they're often developed with the same generic training. Under pressure, the cost of hesitation or unclear communication rises sharply, and there's rarely time to think a decision through from first principles.",
               "Operational leadership — in the Royal Navy, in Defence programmes, in genuine crisis response — trains for exactly this: judgement that holds up when the comfortable assumptions of a classroom don't apply."]),
             ("Judgement over instruction",
              ["The instinct in many organisations is to develop leaders through instruction — teaching a model, a framework, a set of steps to follow. Under real pressure, models are useful scaffolding, but what actually determines outcomes is judgement: the ability to read a situation, prioritise correctly, and act despite incomplete information.",
               "Building judgement takes deliberate practice under realistic pressure, coaching, and feedback — not a single workshop, however well designed."]),
             ("The promotion trap",
              ["A recurring failure pattern: technically excellent people are promoted into leadership roles on the strength of their technical ability, then given little real support for the very different demands of leading a team, especially under pressure.",
               "The result is inconsistent leadership — not because the person lacks capability, but because nobody built the specific judgement and confidence the new role actually requires."]),
             ("Building leaders before the pressure arrives",
              ["The most effective interventions set expectations explicitly from day one, rather than leaving new leaders to work out what's expected of them through trial and error while already carrying a team. The Housing Leadership & Onboarding Transformation case study is a direct example — values-based onboarding and leadership pathways cut time-to-competence by 20%, precisely because expectations were designed in rather than left to chance."]),
         ],
         faqs=[
             ("Is this only relevant to organisations with genuinely high-stakes operations?", "The discipline transfers even where the stakes are lower — any organisation promoting technical experts into leadership roles without deliberate support faces the same underlying gap, just with a smaller blast radius when it goes wrong."),
             ("Can leadership judgement really be taught, or is it innate?", "It can be built deliberately, through realistic practice, coaching and honest feedback — but it rarely develops from classroom instruction alone, which is why the approach here is grounded in real operational experience rather than theoretical models."),
             ("How long does it take to see a difference in leadership consistency?", "It depends on the starting point, but the housing sector case study saw a measurable 20% reduction in time-to-competence, which reflects how quickly deliberate onboarding and pathway design can change outcomes versus leaving development to chance."),
         ],
         related_slug="leadership-development", related_title="Leadership Development",
         related_reading=[
             ("Leadership Development: The Complete Guide", "leadership-development-complete-guide"),
             ("Why Promoting Your Best Technical Expert Often Fails", "why-promoting-technical-experts-fails"),
             ("Succession Planning for Critical Roles", "succession-planning-critical-roles"),
         ]),
    dict(slug="public-sector-workforce-development", category="Public Sector", title="Public Sector Workforce Development",
         h1="Building Capability and Pipelines Under Real Budget Pressure",
         hero_sub="Workforce development in the public sector has to survive scrutiny, restructuring and budget pressure that most private-sector models never have to account for.",
         sections=[
             ("The public sector's specific constraint",
              ["Public sector workforce development operates under constraints that private-sector models rarely have to account for: budget scrutiny, political and reputational visibility, and the expectation that every recommendation can be defended to auditors and elected members, not just to a board.",
               "That doesn't make workforce development harder in principle — it makes evidence non-negotiable. Recommendations that can't be defended under scrutiny don't survive contact with the budget process."]),
             ("Why headcount thinking fails",
              ["A common default under budget pressure is to think in headcount — how many people can we afford — rather than in roles, skills and structure. Headcount thinking treats every post as interchangeable, which breaks down exactly when restructuring or scaling requires specific capability, not just bodies.",
               "Workforce planning that starts from mission and capability requirement, then works out the roles and skills needed to deliver it, survives restructuring far better than headcount-first thinking."]),
             ("Workforce planning as risk management",
              ["In public sector contexts, workforce capability gaps surface as service failures, scrutiny committee findings, or reputational risk — not just as internal inefficiency. Treating workforce planning as a risk management discipline, not just an HR process, tends to get it the attention and resource it needs."]),
             ("The Op Isotrope example",
              ["The Operational Role Architecture Redesign delivered during a national crisis response demonstrates the point under the most extreme version of budget and time pressure imaginable: role ambiguity, not individual skill or lack of resource, was the biggest drag on effectiveness.",
               "Clarity of role — who does what, with what authority — improved response effectiveness by 15%, without requiring additional headcount. That's the workforce planning discipline public sector organisations need even outside a crisis."]),
         ],
         faqs=[
             ("Can workforce development recommendations survive procurement and scrutiny processes?", "Yes, provided they're evidence-based from the outset — recommendations built on defensible analysis, rather than assertion, are designed to withstand scrutiny committee and audit questioning."),
             ("Does this approach require additional budget, or can it work within existing constraints?", "Much of the value comes from using existing headcount and structure more effectively — as the Op Isotrope case study shows, the gain came from role clarity, not from additional resource."),
             ("How does this differ from a standard headcount or establishment review?", "An establishment review typically asks how many posts an organisation can afford. This starts from the capability the mission requires and works out the roles and structure needed to deliver it — headcount follows from that analysis rather than driving it."),
         ],
         related_slug="workforce-planning", related_title="Workforce Planning",
         related_reading=[
             ("Building Capability Into Organisational Change: The Complete Guide", "organisational-change-capability-complete-guide"),
             ("Role Architecture Redesign During Rapid Scaling or Crisis Response", "role-architecture-redesign-rapid-scaling-crisis"),
             ("Why Transformation Programmes Stall After Go-Live", "why-transformation-programmes-stall-after-go-live"),
         ]),
    dict(slug="learning-technology-lessons", category="Technology", title="Learning Technology Lessons",
         h1="Why So Many LMS Investments Underdeliver — And How to Get Value",
         hero_sub="Most underperforming learning platforms don't need replacing — they need the configuration, dashboards and information management that were missing from the original rollout.",
         sections=[
             ("The re-platform trap",
              ["The default response to a frustrating LMS is often to replace it — but a new platform inherits the same configuration and information management problems unless those are fixed first. Re-platforming is expensive, disruptive, and frequently doesn't solve the actual problem.",
               "Before recommending a new system, it's worth testing whether the current one has ever been properly configured for your actual reporting and pathway needs — in many cases, it hasn't."]),
             ("Configuration over replacement",
              ["Most of the value in the Healthcare Learning Transformation and Learning Operations case studies referenced across this site came from configuration, dashboards and information management on an existing Totara platform — not from buying something new.",
               "The question worth asking first is always: is this a platform problem, or an information management problem sitting on top of a perfectly adequate platform?"]),
             ("Dashboards leaders actually trust",
              ["An LMS produces data by default, but data isn't the same as trustworthy reporting. Leaders need to be confident enough in the numbers to put them in a board report unchecked — and that confidence comes from deliberate dashboard design and information governance, not from the platform's out-of-the-box reports.",
               "The Healthcare Learning Transformation case study cut compliance gaps by 18% largely because dashboards were redesigned around what leaders actually needed to see and trust, not around what the platform generated by default."]),
             ("Adoption is the real project",
              ["Whether you configure an existing platform or genuinely need a new one, the harder and more important project is adoption: making sure managers, learners and administrators actually use the system as intended, week after week, not just in the launch period.",
               "Digital learning that stalls after launch almost always stalls for this reason — the technology worked, but nobody designed for what happens in week two."]),
         ],
         faqs=[
             ("How do we know if our problem is the platform or the configuration?", "Start by testing whether your current reporting is trustworthy and whether pathways match how people actually work — if not, that's usually a configuration and information management gap, fixable without replacing the platform."),
             ("Is this specific to Totara, or does it apply to other LMS platforms?", "The diagnostic approach applies broadly — Totara features in the case studies referenced here, but the underlying discipline of configuration, dashboard design and information management transfers to most modern LMS platforms."),
             ("How long does an LMS optimisation project typically take compared to a re-platform?", "A focused configuration and dashboard project is typically a matter of months; a full re-platform is a much longer, higher-risk undertaking — which is exactly why it's worth ruling out the cheaper fix first."),
         ],
         related_slug="lms-optimisation", related_title="LMS Optimisation",
         related_reading=[
             ("Learning Technology: The Complete Guide", "learning-technology-complete-guide"),
             ("What Is an LMS? And What It Can't Do for You", "what-is-an-lms"),
             ("Totara vs Off-the-Shelf LMS Platforms: What to Consider", "totara-vs-off-the-shelf-lms"),
         ]),
    dict(slug="apprenticeship-success-strategies", category="Talent", title="Apprenticeship Success Strategies",
         h1="What Drives 95% Completion and 100% Funding Compliance",
         hero_sub="Apprenticeship completion is largely an operations and progress-management problem, not a teaching quality problem — and treating it that way is what actually moves the numbers.",
         sections=[
             ("Completion is an operations problem",
              ["When apprenticeship completion rates are low, the instinctive response is often to look at teaching quality or content. In practice, drop-off is far more often driven by weak progress management and support than by learner ability or programme design.",
               "Treating completion as an operations problem — are people being tracked, supported and intervened with early enough — moves the numbers faster than redesigning the curriculum."]),
             ("Where drop-off actually happens",
              ["Apprentices rarely drop out at a single dramatic moment. More often, disengagement builds gradually — missed milestones that nobody flagged, unclear next steps, or a loss of visible progress — until leaving feels like the only option.",
               "Identifying the specific points in your own pipeline where this pattern shows up is more useful than assuming it's evenly distributed across the whole programme."]),
             ("Progress management vs teaching quality",
              ["The Defence Apprenticeship Success Programme achieved 95% completion and 100% funding compliance through coaching, active progress management and structured development pathways — not through a change in what was being taught.",
               "Early-warning triggers, regular check-ins and visible milestones give a programme the chance to intervene before disengagement becomes dropout."]),
             ("Funding compliance as a byproduct, not a separate exercise",
              ["Funding compliance is often treated as a parallel administrative exercise, bolted onto delivery. In practice, the same progress-management discipline that drives completion also produces the audit trail that protects funding — because you're tracking exactly the evidence a funding audit will ask for anyway.",
               "Organisations that separate 'delivering the programme' from 'proving compliance' usually end up doing both worse than they need to."]),
         ],
         faqs=[
             ("What's the single biggest factor in apprenticeship completion, in your experience?", "Active, early progress management — noticing disengagement before it becomes dropout — makes more difference than any change to programme content."),
             ("Does this approach apply outside Defence apprenticeships?", "Yes — funding rules differ by sector, but the discipline of active progress management and early intervention applies to any apprenticeship or funded training programme."),
             ("How do you build a funding compliance audit trail without it becoming a separate administrative burden?", "By designing progress tracking so it captures the evidence funding audits require as a natural byproduct of managing the programme well — rather than running two separate systems."),
         ],
         related_slug="apprenticeships", related_title="Apprenticeships",
         related_reading=[
             ("Skills Frameworks: The Complete Guide", "skills-frameworks-complete-guide"),
             ("What Is a Skills Framework? And How It Differs from a Capability Framework", "what-is-a-skills-framework"),
             ("Skills Frameworks for Workforce Planning and Succession", "skills-frameworks-workforce-planning-succession"),
         ]),
    dict(slug="defence-training-governance", category="Defence", title="Defence Training Governance",
         h1="Making Governance Audit-Ready and Useful — Not Just for Inspectors",
         hero_sub="Governance that only exists to satisfy an auditor is governance that's failing the people who need it most: the leaders trying to make good decisions day to day.",
         sections=[
             ("Two kinds of governance",
              ["There's governance built to satisfy an auditor, and governance built to help leaders make better decisions — and far too often, organisations only have the first. Evidence gets assembled reactively, under pressure, once an audit is announced, rather than existing as a natural byproduct of how decisions are made.",
               "Governance that's genuinely useful day to day is, almost by definition, also audit-ready — because the evidence trail was never separate from the decision-making itself."]),
             ("The evidence-on-demand test",
              ["A simple test of whether governance is working: could you produce defensible evidence for the last significant decision within a day, or would it take weeks of reconstruction? If it's the latter, the risk isn't hypothetical — it's sitting there right now, waiting for the next audit request."]),
             ("Decision rights, not just paperwork",
              ["Good governance clarifies who has the authority to make which decisions, and ensures that authority is exercised with visible evidence — not just that a form was completed somewhere. Confusion about decision rights is often the real root cause behind governance that 'exists' on paper but doesn't actually inform anything."]),
             ("What this looked like on DS4D",
              ["Training governance embedded across the Digital Skills for Defence programme and related operational training gave decision-makers evidence they could defend, rather than assumptions they hoped would hold — turning governance into something that supported enterprise-wide investment decisions, not just something that got checked at the end."]),
         ],
         faqs=[
             ("How do we know if our governance is audit-ready?", "Test it directly: pick a recent significant training decision and see how long it takes to produce defensible evidence for it. If the answer is weeks rather than a day, that's your current risk exposure."),
             ("Is this only about surviving external audits?", "No — the same governance that survives an external audit also gives internal leaders better, faster evidence for their own decisions. The two are meant to be the same system, not separate ones."),
             ("Can governance be improved without adding bureaucracy?", "Yes — the goal is governance that's useful enough that people want to use it, not process added on top of existing work. Where governance feels like pure overhead, that's usually a sign it was designed for the auditor, not the decision-maker."),
         ],
         related_slug="training-governance-assurance", related_title="Training Governance &amp; Assurance",
         related_reading=[
             ("Training Governance: The Complete Guide", "training-governance-complete-guide"),
             ("Governance vs Compliance: Why the Distinction Matters", "governance-vs-compliance"),
             ("Building an Audit-Ready Evidence Trail Without Extra Admin", "audit-ready-evidence-trail-without-extra-admin"),
         ]),
    dict(slug="from-training-to-readiness", category="Readiness", title="From Training to Readiness",
         h1="Connecting Learning Investment to the Outcomes Leaders Are Measured On",
         hero_sub="Completion rates measure activity. Readiness measures whether the organisation can actually deliver when it matters — and the two are not the same thing.",
         sections=[
             ("The measurement gap",
              ["Most learning functions report on activity: courses run, hours completed, satisfaction scores. Most leaders are measured on outcomes: readiness, performance, compliance that holds up, retention. The gap between the two is where learning investment quietly loses credibility with the people who control its budget.",
               "Closing that gap means measuring learning against the same outcomes leaders are actually accountable for, not against a parallel set of activity metrics that only make sense within L&D."]),
             ("What readiness actually means",
              ["Readiness isn't a training outcome — it's an organisational one, built from people, behaviours, governance, leadership, structure, assurance and learning all working together. Training is one input among several, which is exactly why training completion, on its own, rarely predicts readiness reliably.",
               "This is the thinking behind the Prelude Capability Model — tracing performance from mission and outcomes down through required capability, behaviours, skills and knowledge, governance and assurance, to the evidence that proves it's actually working."]),
             ("Applying the model",
              ["In practice, this means starting any capability investment by asking what the mission actually requires, then tracing backwards through which layer is genuinely missing — rather than starting from an assumption that training is the fix and working forwards.",
               "Where any layer in that chain is missing — unclear mission link, undefined capability requirement, absent governance — no amount of training closes the gap, because training was never the layer that was broken."]),
             ("Measuring what leaders actually care about",
              ["Across the case studies referenced throughout this site, the metrics that mattered to leaders were never course completion in isolation — they were operational readiness, compliance gaps closed, response effectiveness, time-to-competence, and pass rates. Learning investment earns credibility by being measured against those outcomes, not against its own activity."]),
         ],
         faqs=[
             ("How do you measure readiness if it isn't a training metric?", "Against the operational outcomes the mission actually depends on — compliance that holds up under audit, response effectiveness, time-to-competence, retention — with training's contribution assessed as one input among several, not the whole story."),
             ("Isn't completion still a useful metric at all?", "It's useful as a delivery metric — did the intended audience actually receive the intervention — but it's a poor proxy for readiness on its own, which is why it shouldn't be the only number reported to leadership."),
             ("Where should an organisation start if it wants to shift from activity to outcome measurement?", "With the Capability Readiness Review — establishing where the real gap sits (capability, leadership, process, governance, workforce or training) before deciding what to measure and invest in next."),
         ],
         related_slug="capability-readiness-review", related_title="Take the Capability Readiness Review",
         related_reading=[
             ("Performance Consulting: The Complete Guide", "performance-consulting-complete-guide"),
             ("The Training vs Capability Decision Model, Explained", "training-vs-capability-decision-model-explained"),
             ("How to Tell If Your Performance Problem Is Really a Training Problem", "is-your-performance-problem-really-a-training-problem"),
         ]),
    dict(slug="training-needs-analysis-complete-guide", category="Method", kind="Complete Guide",
         title="Training Needs Analysis: The Complete Guide for Defence & Public Sector",
         h1="Training Needs Analysis: The Complete Guide for Defence &amp; Public Sector",
         hero_sub="Everything you need to know about running a TNA that survives audit, finds the real gap, and gives leaders evidence they can act on — from first principles through to board reporting.",
         sections=[
             ("What a Training Needs Analysis actually is",
              ["A Training Needs Analysis is the structured process of testing whether a performance gap is genuinely a training gap, or whether it's being held back by something else entirely — unclear roles, weak governance, a structure working against the outcome, or expectations nobody actually agreed.",
               "That last part matters more than most organisations treat it: a properly run TNA can, and sometimes should, conclude that training isn't the answer. If it can't reach that conclusion, it isn't a needs analysis — it's a justification exercise for a decision someone already made."]),
             ("Why TNA matters more in Defence and regulated public sector",
              ["Outside regulated environments, a weak TNA wastes budget on training that doesn't work. Inside Defence and regulated public sector environments, it does that and creates an audit problem — because DSAT, set out in JSP 822, requires the analysis behind a training decision to be defensible, not just the training itself.",
               "That's the real link between TNA and DSAT: DSAT's Analysis phase is where a TNA lives, and an audit will test whether the capability requirement was genuinely established before design and development work began."]),
             ("The TNA process, step by step",
              ["A defensible TNA moves through five stages: establishing the capability requirement, gathering evidence on current performance against it, testing whether the gap is genuinely a training gap, prioritising findings by evidenced impact, and reporting in a form leaders can act on.",
               "Each stage produces something the next stage depends on. Skip the evidence-gathering stage and jump to recommendations, and there's nothing defensible underpinning the report — just opinion dressed up as analysis."]),
             ("TNA vs skills gap analysis",
              ["The two get used interchangeably, but they answer different questions. A skills gap analysis maps what skills a person or role has against what a role requires. A TNA asks the broader and more important question first: is a skills gap even what's causing the performance problem, or is something structural getting in the way.",
               "Run a skills gap analysis before that question is answered, and you risk mapping gaps against a requirement that was never the real constraint. See the dedicated article for the full distinction and when each tool is the right one."]),
             ("Where TNAs go wrong — and what it costs",
              ["The same handful of mistakes account for most of the wasted budget: starting from an assumed answer, treating stakeholder wishlists as evidence, skipping the baseline so nobody can prove impact afterwards, and treating every request as equally urgent regardless of evidenced impact.",
               "None of these are complicated to avoid. They're avoided by discipline — insisting on evidence before recommendation — not by a more sophisticated methodology. The dedicated article on this walks through each one with what it actually costs."]),
             ("Presenting findings so leaders act on them",
              ["A TNA that never gets acted on has usually failed at the reporting stage, not the analysis stage — buried in methodology when the board needed a decision, or silent on cost of inaction when that's exactly what would have moved budget. Presenting findings well is a distinct skill from running the analysis, and it's covered in full in the dedicated article."]),
             ("What a defensible TNA looks like in practice",
              ["The NATO and Royal Navy Training Modernisation case study is the clearest example on this site: a DSAT-compliant TNA pinpointed the specific points in the training pipeline where learners were being set up to fail, rather than recommending a wholesale redesign — lifting pass rates by 17% and cutting failures by 20%.",
               "The Senior Information Officer Rapid TNA case study makes the companion point: run properly, as a decision framework rather than a process to endure, a TNA accelerates good decisions instead of delaying them. The constraint in that engagement wasn't methodology — it was unclear requirements, resolved quickly once the right questions were asked."]),
         ],
         faqs=[
             ("Is a TNA always the right starting point for a performance problem?", "It's the right starting point whenever training is being considered as part of the solution — its job is precisely to test that assumption before budget is committed, rather than to confirm a decision already made."),
             ("How does a TNA relate to DSAT and JSP 822?", "DSAT's Analysis phase is effectively where a TNA lives — see the DSAT Explained article for the full methodology, and this guide for how to run the analysis itself so it holds up to audit."),
             ("What's the difference between this guide and the Best Practice article?", "This guide is the comprehensive reference — process, common failure modes, board reporting and DSAT alignment in one place. The Best Practice article and the other pieces linked below go deeper on specific parts of that process."),
             ("Do we need external support to run a defensible TNA, or can it be done in-house?", "Many organisations can run one in-house with the right structure and discipline. External support tends to add most value where independence, evidence rigour or DSAT-specific experience is the limiting factor, not where the process itself is unfamiliar."),
         ],
         related_slug="training-needs-analysis", related_title="Training Needs Analysis service",
         related_reading=[
             ("Training Needs Analysis: Best Practice", "training-needs-analysis-best-practice"),
             ("How to Run a DSAT-Compliant TNA, Step by Step", "dsat-compliant-tna-step-by-step"),
             ("TNA vs Skills Gap Analysis: What's the Difference", "tna-vs-skills-gap-analysis"),
             ("Common TNA Mistakes That Waste Budget", "common-tna-mistakes"),
             ("How to Present TNA Findings to a Board", "presenting-tna-findings-to-a-board"),
         ]),
    dict(slug="dsat-compliant-tna-step-by-step", category="Method",
         title="How to Run a DSAT-Compliant TNA, Step by Step",
         h1="How to Run a DSAT-Compliant TNA, Step by Step",
         hero_sub="A practical walkthrough of running a Training Needs Analysis that will stand up to DSAT audit and assurance — not just produce a report nobody can defend.",
         sections=[
             ("Start with the capability requirement, not the training request",
              ["A DSAT-compliant TNA starts by establishing the capability requirement in Defence terms — what does the role or unit actually need to be able to do, and against what standard — before any conversation about training format or content.",
               "Requests that arrive already framed as a training request (\"we need a course on X\") should be treated as a hypothesis to test, not a scope to deliver against."]),
             ("Building the evidence base DSAT auditors expect",
              ["Assurance auditors look for evidence, not assertion: performance data, error or incident rates, structured observation, and a clear baseline of current performance against the capability requirement. Interviews are useful context, but on their own they don't satisfy an auditor asking how the gap was established.",
               "The evidence base should be gathered and recorded in a form that survives being read months later by someone who wasn't in the room — that's the practical test of whether it's audit-ready."]),
             ("Testing whether the gap is a training gap at all",
              ["With a capability requirement and an evidence base in place, the analysis explicitly tests alternative explanations — unclear roles, absent governance, a structure working against the outcome — before concluding training is the right intervention. Recording that this test happened, and what ruled out the alternatives, is what makes the eventual recommendation defensible."]),
             ("Structuring the analysis for defensibility",
              ["A defensible structure links every recommendation back to a specific piece of evidence and a specific element of the capability requirement — not a general narrative about what would probably help. If a reviewer can't trace a recommendation back to the evidence that produced it, the structure has failed, regardless of how good the recommendation actually is."]),
             ("Handing off to design without losing the audit trail",
              ["The handoff from Analysis to Design is where audit trails most often get lost — the TNA report gets summarised into a brief, and the evidence base behind each finding quietly disappears. Keeping the full analysis attached and referenced, not just a summary, is what lets Design and Evaluation later be tested against what Analysis actually found."]),
         ],
         faqs=[
             ("Does DSAT require a specific template for TNA reporting?", "JSP 822 sets out requirements rather than a fixed template — the priority is that the evidence base, the capability requirement and the reasoning connecting them are all traceable, however the report is formatted."),
             ("How much evidence is enough to satisfy an audit?", "Enough that a reviewer unfamiliar with the engagement could follow the reasoning from capability requirement to evidence to recommendation without having to take any step on trust."),
             ("What's the biggest reason DSAT-compliant TNAs fail audit?", "Losing the audit trail at handoff to Design — the recommendation survives, but the evidence that justified it doesn't get carried forward in a traceable way."),
         ],
         related_slug="dsat-consultancy", related_title="DSAT Consultancy",
         related_reading=[
             ("Training Needs Analysis: The Complete Guide", "training-needs-analysis-complete-guide"),
             ("Training Needs Analysis: Best Practice", "training-needs-analysis-best-practice"),
             ("Common TNA Mistakes That Waste Budget", "common-tna-mistakes"),
         ]),
    dict(slug="tna-vs-skills-gap-analysis", category="Method",
         title="TNA vs Skills Gap Analysis: What's the Difference",
         h1="TNA vs Skills Gap Analysis: What's the Difference",
         hero_sub="The two are often used interchangeably, but they answer different questions — and reaching for the wrong one wastes budget on the wrong diagnosis.",
         sections=[
             ("Two different questions",
              ["A skills gap analysis asks: what skills does this person or role have, compared with what the role requires? A Training Needs Analysis asks a broader and prior question: is a skills gap actually what's causing the performance problem in the first place, or is something structural getting in the way?",
               "Confusing the two leads to a specific failure mode — running a skills gap analysis against a performance problem that was never really about skill, and getting a precise, well-evidenced answer to the wrong question."]),
             ("Where a skills gap analysis is the right tool",
              ["When the capability requirement is already well defined and agreed, and the question is genuinely which individuals or teams fall short of it, a skills gap analysis is the right, efficient tool — it maps current state against an already-trusted standard."]),
             ("Where only a TNA will do",
              ["When the performance problem itself is still in question — when it isn't yet clear whether the gap is skill, structure, governance or something else — a TNA has to come first. Running a skills gap analysis at this stage assumes the answer before testing it."]),
             ("Running both without duplicating effort",
              ["In practice, a TNA that concludes the gap genuinely is a skills gap can flow directly into a skills gap analysis against the confirmed capability requirement — using the same evidence base rather than starting again from scratch. The sequencing, not the tooling, is what prevents wasted effort."]),
         ],
         faqs=[
             ("Can a skills gap analysis substitute for a TNA?", "Only if the underlying question — is this genuinely a skills problem — has already been reliably answered elsewhere. Otherwise it risks producing a precise answer to a question that was never the real one."),
             ("Which should come first if we're not sure?", "Default to the TNA. It's built to test the broader question, and a confirmed skills gap can feed straight into a skills gap analysis afterwards without wasted effort."),
             ("Is this distinction relevant outside Defence and public sector?", "Yes — the same confusion causes wasted training spend in any sector; Defence and regulated public sector environments simply make the cost of skipping the question more visible, because it also shows up at audit."),
         ],
         related_slug="training-needs-analysis", related_title="Training Needs Analysis service",
         related_reading=[
             ("Training Needs Analysis: The Complete Guide", "training-needs-analysis-complete-guide"),
             ("Training Needs Analysis: Best Practice", "training-needs-analysis-best-practice"),
             ("How to Run a DSAT-Compliant TNA, Step by Step", "dsat-compliant-tna-step-by-step"),
         ]),
    dict(slug="common-tna-mistakes", category="Method",
         title="Common TNA Mistakes That Waste Budget",
         h1="Common TNA Mistakes That Waste Budget",
         hero_sub="The same handful of mistakes account for most of the money wasted on Training Needs Analyses that should never have recommended training in the first place.",
         sections=[
             ("Starting from the answer, not the question",
              ["The single most expensive mistake is beginning a TNA with training already assumed as the outcome, and using the analysis to justify it rather than to test it. Every subsequent step of an analysis run this way is biased toward the predetermined conclusion, however rigorous it looks on paper."]),
             ("Wishlist syndrome",
              ["Asking stakeholders what training they'd like, then packaging the answers as a needs analysis, reliably produces a wishlist rather than a diagnosis — people asked what training they want will describe training, because that's the question they were asked. It doesn't test whether training is the right answer at all."]),
             ("No baseline, no way to prove it worked",
              ["Without a documented baseline of current performance, there's no way to demonstrate afterwards that an intervention actually closed the gap it was funded to close. This is usually discovered at the worst possible time — when a leader asks what the training achieved, and the honest answer is that nobody can say."]),
             ("Treating every request as equally urgent",
              ["Without evidence-based prioritisation, budget tends to go to whoever asked loudest or most recently, rather than to the gap with the largest evidenced impact on performance. A TNA that doesn't rank findings by impact hasn't finished its job."]),
             ("Skipping the evidence base",
              ["Interviews and stakeholder opinion are useful context but are not, on their own, evidence of a performance gap. Performance data, error rates, incident reports and structured observation are what turn a set of opinions into a defensible finding — and their absence is the single easiest thing for a sceptical reviewer to challenge."]),
         ],
         faqs=[
             ("Which of these mistakes is the most expensive?", "Starting from the answer rather than the question — it doesn't just waste the cost of the analysis, it commits budget to an intervention that was never properly tested against the actual problem."),
             ("Can these mistakes be fixed partway through a TNA that's already underway?", "Often, yes — introducing a baseline or broadening the evidence base partway through is better than not doing it at all, though it's more efficient to build them in from the start."),
             ("Is wishlist syndrome always obvious when it's happening?", "Not always — a well-written wishlist can look like a rigorous needs analysis. The tell is whether the report could ever have concluded training wasn't needed; if that outcome was never possible, the process wasn't testing anything."),
         ],
         related_slug="training-needs-analysis", related_title="Training Needs Analysis service",
         related_reading=[
             ("Training Needs Analysis: The Complete Guide", "training-needs-analysis-complete-guide"),
             ("How to Run a DSAT-Compliant TNA, Step by Step", "dsat-compliant-tna-step-by-step"),
             ("How to Present TNA Findings to a Board", "presenting-tna-findings-to-a-board"),
         ]),
    dict(slug="presenting-tna-findings-to-a-board", category="Method",
         title="How to Present TNA Findings to a Board",
         h1="How to Present TNA Findings to a Board",
         hero_sub="A TNA that leaders can act on has to be presented differently from one that just gets filed — here's what a board actually needs to see.",
         sections=[
             ("Boards don't need the methodology, they need the decision",
              ["A board reading a TNA report isn't assessing whether the methodology was sound — that's what the underlying evidence base is for, and it should be available on request, not on the first slide. What a board needs upfront is the finding, its evidenced confidence, and the decision it implies."]),
             ("Leading with evidence, not activity",
              ["Reports that lead with how many people were interviewed or how many workshops were run are answering the wrong question. Leading with the performance gap, its evidenced size, and its cost of inaction gets a board to a decision far faster than a description of the process used to find it."]),
             ("Framing training vs non-training recommendations",
              ["When a TNA concludes training isn't the answer, that finding needs to be framed as clearly and confidently as one that recommends training — it's not a lesser outcome, it's the analysis doing exactly what it was commissioned to do. Boards can act on a clear \"not training\" finding; they can't act on a hedge."]),
             ("What a board-ready TNA summary looks like",
              ["In practice, a board-ready summary fits on one page: the performance gap, the evidence behind it, whether it's a training gap or something else, the recommended action, and the cost of not acting. Everything else belongs in an appendix the board can request, not in the opening pages they're actually going to read."]),
         ],
         faqs=[
             ("How long should a board-facing TNA summary be?", "One page for the findings and recommendation; the full evidence base and methodology can sit in an appendix for anyone who wants to interrogate it further."),
             ("What if the board pushes back on a 'training isn't needed' finding?", "That's exactly what the evidence base is for — a defensible TNA can show its working, which is what turns pushback into a productive conversation rather than a stalemate."),
             ("Should the person who ran the TNA present it, or should it go through a manager?", "Whoever can answer detailed questions about the evidence confidently should present it — credibility on the evidence matters more than seniority in the room."),
         ],
         related_slug="training-needs-analysis", related_title="Training Needs Analysis service",
         related_reading=[
             ("Training Needs Analysis: The Complete Guide", "training-needs-analysis-complete-guide"),
             ("Common TNA Mistakes That Waste Budget", "common-tna-mistakes"),
             ("Training Needs Analysis: Best Practice", "training-needs-analysis-best-practice"),
         ]),
    dict(slug="learning-strategy-complete-guide", category="Strategy", kind="Complete Guide",
         title="Learning Strategy: Aligning Capability Investment to Organisational Performance",
         h1="Learning Strategy: Aligning Capability Investment to Organisational Performance",
         hero_sub="Everything you need to know about building a learning strategy that gets funded, survives scrutiny, and actually connects capability investment to organisational performance.",
         sections=[
             ("What a learning strategy actually is",
              ["A learning strategy is the document connecting capability investment to organisational goals — what's being invested in, why, and how impact will be measured. That's a different job from a training plan, which simply lists what's being delivered and when.",
               "The test of whether a document is genuinely a strategy: does it explain why this investment, in this order, against this outcome — or does it just catalogue activity? Most documents labelled 'learning strategy' are, on inspection, detailed training plans wearing a strategy's title."]),
             ("Why a training plan isn't a strategy",
              ["A training plan can be executed perfectly and still fail the organisation, because execution was never the question a strategy is meant to answer. The plan tells you what's happening; the strategy is what justifies it happening at all, and in that order rather than another.",
               "This distinction matters most at budget review, when a training plan has no answer to 'why this, why now, why this much' beyond 'it's what we planned' — while a real strategy was built to answer exactly that."]),
             ("Building a strategy leadership will actually fund",
              ["Strategies get funded when they're framed in outcomes leadership is already accountable for — compliance risk, operational readiness, retention, cost of failure — rather than in learning-specific language that has to be translated before it means anything to a budget holder.",
               "That reframing has to happen at the design stage, not retrofitted into a slide deck once the document already exists. The dedicated article on funding walks through how to build the investment case in, from the start."]),
             ("Learning strategy vs training plan",
              ["Beyond the definitional difference, the practical tell is durability: a genuine strategy survives a change of budget holder or leadership team, because it's anchored to organisational outcomes that don't change with personnel. A training plan dressed up as a strategy usually doesn't survive that transition intact. The dedicated article covers this distinction in full, including how to convert a plan-shaped document into a real one."]),
             ("Measuring impact beyond completion rates",
              ["Completion rates measure whether an activity happened, not whether it changed anything. A strategy that reports success in completions alone hasn't demonstrated impact — it's demonstrated delivery. Building a measurement plan into the strategy from day one, rather than bolting one on when a board asks for evidence, is what separates credible reporting from activity theatre. The dedicated article sets out what to measure instead."]),
             ("Learning strategy for multi-site or multi-sector organisations",
              ["A strategy built for a single site or a single part of the business rarely survives being rolled out across several without modification — local variation that was invisible at one site becomes a governance problem at five. Designing for common ground and genuine local difference from the outset avoids a costly redesign later. The dedicated article covers what to build in from the start."]),
             ("What alignment looks like in practice",
              ["The MOD Digital Skills for Defence (DS4D) programme is a direct example of what this looks like done well: rather than commissioning courses against an undefined digital capability requirement, the work started by defining what digital capability Defence actually needed, then aligned learning architecture to that requirement rather than the other way round.",
               "The result was measurable: a clear, evidence-based view of future capability requirements, and 'progress in ten weeks that had stalled for twelve months' — because the strategy answered the right question before any training was designed, not after."]),
         ],
         faqs=[
             ("How is a learning strategy different from an L&D operating plan?", "An operating plan describes how the L&D function runs day to day. A learning strategy sits above that — it justifies what's being invested in and why, against organisational outcomes, with the operating plan as one of the things it informs."),
             ("How often should a learning strategy be reviewed?", "At minimum whenever the organisation's mission or operating model shifts significantly — a strategy anchored to outcomes that have since changed will lose relevance quickly, regardless of how well it was originally built."),
             ("Does a small organisation need a formal learning strategy, or is that overkill?", "Scale the document down, not the discipline — even a single page connecting a handful of investment decisions to clear outcomes and a measurement plan delivers the same value as a longer document does for a larger organisation."),
             ("What's the fastest way to tell if an existing 'strategy' is actually just a training plan?", "Ask what happens to the document if the budget holder changes. If it has no independent justification beyond 'this is what we scheduled,' it's a plan wearing a strategy's title."),
         ],
         related_slug="learning-strategy", related_title="Learning Strategy service",
         related_reading=[
             ("Building a Learning Strategy Leadership Will Actually Fund", "learning-strategy-leadership-will-fund"),
             ("Learning Strategy vs Training Plan: Why the Difference Matters", "learning-strategy-vs-training-plan"),
             ("How to Measure Learning Strategy Impact Beyond Completion Rates", "measuring-learning-strategy-impact"),
             ("Learning Strategy for Multi-Site or Multi-Sector Organisations", "learning-strategy-multi-site-multi-sector"),
         ]),
    dict(slug="learning-strategy-leadership-will-fund", category="Strategy",
         title="Building a Learning Strategy Leadership Will Actually Fund",
         h1="Building a Learning Strategy Leadership Will Actually Fund",
         hero_sub="Learning strategies get rejected or quietly ignored for predictable reasons — here's what actually makes leadership commit budget.",
         sections=[
             ("Why most learning strategies get rejected or ignored",
              ["Rejection is rarely about the quality of the thinking. It's usually about language: a strategy written in learning-specific terms — courses, pathways, modules — asks a budget holder to do the translation into outcomes they're accountable for themselves, and busy leaders often simply don't."]),
             ("Speaking in outcomes leadership is already accountable for",
              ["A strategy framed around compliance risk, operational readiness, retention or cost of failure doesn't need translating — it's already in the language the budget holder reports upward in. That reframing is often the single highest-leverage change to a strategy document that never touches the underlying plan."]),
             ("Costing it like an investment case, not a wishlist",
              ["A wishlist lists what would help. An investment case states the cost of inaction, the expected return, and the evidence behind both — and it's the second one that survives a budget round, because it gives a decision-maker something to defend upward, not just something to approve."]),
             ("Building in the evidence trail before you ask for budget",
              ["Waiting until after approval to think about how impact will be evidenced is a common and avoidable mistake — by the time someone asks 'did it work,' the baseline needed to answer the question is often long gone. Building the evidence trail into the strategy before it's funded means the next budget conversation starts from proof, not assertion."]),
         ],
         faqs=[
             ("What's the single biggest change that gets a strategy funded?", "Reframing it in outcomes the budget holder is already accountable for, rather than in learning-specific language they have to translate themselves."),
             ("Should cost of inaction always be quantified?", "Wherever possible — even an approximate figure gives a decision-maker something concrete to weigh against the investment, which a purely qualitative argument doesn't."),
             ("How early should measurement planning start?", "Before the strategy is approved, not after — a baseline captured after the fact can't answer the question 'did this work' with any confidence."),
         ],
         related_slug="learning-strategy", related_title="Learning Strategy service",
         related_reading=[
             ("Learning Strategy: The Complete Guide", "learning-strategy-complete-guide"),
             ("How to Measure Learning Strategy Impact Beyond Completion Rates", "measuring-learning-strategy-impact"),
             ("Learning Strategy vs Training Plan: Why the Difference Matters", "learning-strategy-vs-training-plan"),
         ]),
    dict(slug="learning-strategy-vs-training-plan", category="Strategy",
         title="Learning Strategy vs Training Plan: Why the Difference Matters",
         h1="Learning Strategy vs Training Plan: Why the Difference Matters",
         hero_sub="A training plan lists what's being delivered. A learning strategy explains why — and only one of those survives a change of budget holder.",
         sections=[
             ("What each document actually does",
              ["A training plan schedules delivery — what's running, for whom, and when. A learning strategy justifies that schedule against organisational outcomes — why this investment, in this order, against this measure of success. They're not competing documents; a good plan should follow from a strategy, not substitute for one."]),
             ("The tell: does it survive a change of leadership",
              ["The clearest practical test is durability. Hand a training plan to a new budget holder and its only defence is 'this is what was scheduled.' Hand over a genuine strategy and it still explains itself, because it was built on outcomes that don't change just because the person reviewing it did."]),
             ("Why organisations default to a plan and call it a strategy",
              ["Plans are easier to write — they describe what's already been decided. Strategy requires deciding, and defending, why one investment takes priority over another against evidence, which is a harder and more exposed exercise. Under time pressure, it's common to produce the easier document and label it the harder one."]),
             ("Building the strategy first, then letting the plan follow",
              ["The more durable sequence is strategy first: agree the outcomes, the priorities, and how impact will be measured, and let the training plan fall out of those decisions. Done in reverse — plan first, strategy retrofitted to justify it — the strategy tends to read as exactly what it is: a rationalisation."]),
         ],
         faqs=[
             ("Can a training plan be turned into a strategy after the fact?", "It's possible, but it usually means going back to first principles — establishing the outcomes and priorities the plan should have been built from — rather than lightly editing the existing document."),
             ("Do we need both documents, or just the strategy?", "Both, typically — the strategy sets direction and priority; the plan is the operational detail of executing it. The risk is having only the plan and mistaking it for the other."),
             ("Is this distinction just semantics?", "No — it shows up concretely at budget review, when a plan-only document has no independent answer to 'why this, why now' beyond the schedule itself."),
         ],
         related_slug="learning-strategy", related_title="Learning Strategy service",
         related_reading=[
             ("Learning Strategy: The Complete Guide", "learning-strategy-complete-guide"),
             ("Building a Learning Strategy Leadership Will Actually Fund", "learning-strategy-leadership-will-fund"),
             ("Learning Strategy for Multi-Site or Multi-Sector Organisations", "learning-strategy-multi-site-multi-sector"),
         ]),
    dict(slug="measuring-learning-strategy-impact", category="Strategy",
         title="How to Measure Learning Strategy Impact Beyond Completion Rates",
         h1="How to Measure Learning Strategy Impact Beyond Completion Rates",
         hero_sub="Completion rates measure activity, not impact — here's what to measure instead if you want leadership to actually trust the numbers.",
         sections=[
             ("Why completion rates are the wrong headline metric",
              ["Completion tells you the intended audience received the intervention. It says nothing about whether behaviour, performance or risk changed as a result — which is the question a learning strategy exists to answer. Reporting completion as the headline metric answers a question nobody senior was actually asking."]),
             ("Metrics that connect learning to performance",
              ["Useful measures link directly to the outcome the strategy was built to move — compliance gaps closed, error or incident rates, time-to-competence, retention, operational readiness. These numbers mean something to a board without translation, because they're already the numbers the organisation is accountable for elsewhere."]),
             ("Building a measurement plan before the strategy launches, not after",
              ["A baseline captured before an intervention starts is what makes any later claim of impact defensible. Waiting until someone asks for evidence to start thinking about measurement means the baseline needed to answer the question no longer exists — it has to be built in from day one."]),
             ("What credible reporting looks like to a board",
              ["Credible reporting leads with the outcome metric, not the activity metric — compliance gap closed, not courses completed — and is honest about what the data can and can't yet show. A report that only ever shows good news, with no visible baseline or method, tends to earn scepticism rather than trust."]),
         ],
         faqs=[
             ("Is completion data worth tracking at all?", "Yes, as an operational delivery metric — it confirms the intervention reached its intended audience — but it shouldn't be the headline measure of whether the strategy is working."),
             ("What if the organisation has no existing baseline data?", "Start capturing one now, even a rough one — an imperfect baseline established today is more useful than a perfect one that doesn't exist because measurement was never planned for."),
             ("How often should impact be reported to leadership?", "Frequently enough to catch problems early, but not so often that noise gets mistaken for signal — typically aligned to existing board or governance reporting cycles rather than a separate calendar."),
         ],
         related_slug="learning-strategy", related_title="Learning Strategy service",
         related_reading=[
             ("Learning Strategy: The Complete Guide", "learning-strategy-complete-guide"),
             ("Building a Learning Strategy Leadership Will Actually Fund", "learning-strategy-leadership-will-fund"),
             ("Learning Strategy vs Training Plan: Why the Difference Matters", "learning-strategy-vs-training-plan"),
         ]),
    dict(slug="learning-strategy-multi-site-multi-sector", category="Strategy",
         title="Learning Strategy for Multi-Site or Multi-Sector Organisations",
         h1="Learning Strategy for Multi-Site or Multi-Sector Organisations",
         hero_sub="A strategy that works for one site or one part of the business often breaks the moment it's rolled out across several — here's what to design for instead.",
         sections=[
             ("Why a single-site strategy doesn't scale as-is",
              ["A strategy built around one site's constraints and culture tends to carry hidden assumptions that were invisible at that scale — a reporting line, a local exception, an informal workaround — which surface as friction the moment the same strategy is rolled out somewhere those assumptions don't hold."]),
             ("Common ground vs genuine local difference",
              ["Scaling a strategy well means deliberately separating what should be consistent everywhere — governance, measurement, core priorities — from what genuinely needs to flex locally, such as delivery format or sequencing against local operational pressure. Treating everything as either fully standard or fully local both fail, for different reasons."]),
             ("Governance across multiple sites or sectors",
              ["Without a single governance structure spanning every site or sector involved, local versions of the strategy tend to drift independently, until 'the strategy' means something different depending on who you ask. Clear ownership of what can and can't be varied locally prevents that drift before it starts."]),
             ("Sequencing a multi-site rollout without losing momentum",
              ["Rolling out everywhere at once magnifies any design flaw across the whole organisation simultaneously; rolling out too cautiously loses momentum before value is visible anywhere. A staged sequence — proving the model at one or two sites, then scaling with what was learned — tends to balance both risks better than either extreme."]),
         ],
         faqs=[
             ("How many sites should a strategy be piloted at before wider rollout?", "Enough to expose genuine variation — often two sites with meaningfully different contexts reveal more than piloting at several similar ones."),
             ("Who should own governance across sites or sectors?", "A single accountable owner for what's standard versus locally flexible, even if delivery itself is devolved — without that, drift is close to inevitable."),
             ("Does multi-sector mean multi-sector within one organisation, or across client types?", "Both apply — the same discipline of separating common ground from genuine difference holds whether the variation is between sites, business units, or sectors served."),
         ],
         related_slug="learning-strategy", related_title="Learning Strategy service",
         related_reading=[
             ("Learning Strategy: The Complete Guide", "learning-strategy-complete-guide"),
             ("Learning Strategy vs Training Plan: Why the Difference Matters", "learning-strategy-vs-training-plan"),
             ("How to Measure Learning Strategy Impact Beyond Completion Rates", "measuring-learning-strategy-impact"),
         ]),
    dict(slug="leadership-development-complete-guide", category="Leadership", kind="Complete Guide",
         title="Leadership Development for High-Stakes Environments",
         h1="Leadership Development for High-Stakes Environments",
         hero_sub="Everything you need to know about building leaders who hold up under real pressure — from promotion decisions, through onboarding, to succession.",
         sections=[
             ("What leadership development for high-stakes environments actually means",
              ["High-stakes leadership development is aimed at a specific outcome: leaders whose judgement holds up when hesitation or unclear communication has a real cost, and there's rarely time to reason a decision through from first principles. That's a different target from general leadership training aimed at competent, comfortable-conditions management.",
               "Operational leadership — in the Royal Navy, in Defence programmes, in genuine crisis response — is built for exactly this, and the discipline transfers to any organisation where a leadership failure has real operational, financial or reputational cost."]),
             ("Why generic leadership training doesn't transfer under pressure",
              ["Generic leadership training tends to teach a model, a framework, a set of steps — useful scaffolding in calm conditions. Under real pressure, what actually determines outcomes is judgement: reading a situation, prioritising correctly, and acting despite incomplete information. That's built through deliberate practice under realistic pressure, coaching and honest feedback, not through a single workshop, however well designed."]),
             ("The promotion trap",
              ["The most common failure pattern in this cluster is promoting technically excellent people into leadership roles on the strength of their technical ability, then giving them little real support for the very different demands of leading a team under pressure. The dedicated article on this walks through why the logic feels sound and where it breaks down."]),
             ("Onboarding new leaders properly",
              ["New leaders left to work out what's expected of them through trial and error, while already carrying a team, tend to default to whatever leadership style they last experienced — good or bad. Explicit onboarding in the first days sets a trajectory that's expensive to correct later. The dedicated article sets out what week one needs to cover."]),
             ("Succession planning for critical roles",
              ["Waiting for a vacancy to start thinking about who's ready to fill it turns succession into crisis management. Identifying critical roles — not just senior ones — and building the pipeline before it's needed is a distinct discipline from general leadership development, covered in the dedicated article."]),
             ("What this looks like in practice",
              ["The Housing Leadership &amp; Onboarding Transformation case study is a direct example of the whole cluster working together: values-based onboarding and defined leadership pathways cut time-to-competence by 20%, precisely because expectations were designed in from day one rather than left to chance.",
               "None of that required waiting for a crisis to reveal the gap — it was built before the pressure arrived, which is the point of this entire cluster."]),
         ],
         faqs=[
             ("Is this only relevant to organisations with genuinely high-stakes operations?", "The discipline transfers even where the stakes are lower — any organisation promoting technical experts into leadership roles without deliberate support faces the same underlying gap, just with a smaller blast radius when it goes wrong."),
             ("Can leadership judgement really be taught, or is it innate?", "It can be built deliberately through realistic practice, coaching and honest feedback — but it rarely develops from classroom instruction alone."),
             ("Where should an organisation start if it wants to build this deliberately?", "With whichever gap is most exposed right now — a promotion decision, a new-manager onboarding process, or an undefined succession pipeline for a critical role — the three dedicated articles below cover each in depth."),
             ("How long does it take to see a difference in leadership consistency?", "It depends on the starting point, but the Housing case study saw a measurable 20% reduction in time-to-competence, which reflects how quickly deliberate onboarding and pathway design can change outcomes versus leaving development to chance."),
         ],
         related_slug="leadership-development", related_title="Leadership Development service",
         related_reading=[
             ("Leadership in High-Pressure Environments", "leadership-in-high-pressure-environments"),
             ("Why Promoting Your Best Technical Expert Often Fails", "why-promoting-technical-experts-fails"),
             ("Leadership Onboarding: What New Managers Need in Week One", "leadership-onboarding-week-one"),
             ("Succession Planning for Critical Roles", "succession-planning-critical-roles"),
         ]),
    dict(slug="why-promoting-technical-experts-fails", category="Leadership",
         title="Why Promoting Your Best Technical Expert Often Fails",
         h1="Why Promoting Your Best Technical Expert Often Fails",
         hero_sub="Promoting on technical ability alone is a reasonable-sounding decision that fails for a predictable, avoidable reason.",
         sections=[
             ("The logic that leads to the mistake",
              ["Promoting the strongest technical performer into a leadership role feels like rewarding merit, and it's rarely challenged at the time — the person has visibly earned it through results. The flaw isn't the reward; it's the assumption that the skills which produced those results are the same skills the new role requires."]),
             ("What technical excellence doesn't teach",
              ["Being excellent at the work is not the same as being able to prioritise a team's competing demands, hold a difficult conversation, or make a judgement call under pressure with incomplete information and a team watching how you handle it. None of that is taught by being good at the underlying technical discipline, however deep that expertise runs."]),
             ("The cost when it goes wrong",
              ["The visible cost is usually inconsistent leadership — not because the person lacks capability, but because nobody built the specific judgement and confidence the new role actually requires. The less visible cost is losing a strong technical contributor to a role they were never properly set up to succeed in, while the technical function loses its best performer."]),
             ("What to do instead",
              ["Assess leadership potential as a distinct question from technical performance before promoting, and treat the transition itself as something to actively support — explicit onboarding, coaching, and honest early feedback — rather than assuming competence will follow automatically from the promotion."]),
         ],
         faqs=[
             ("Does this mean technical experts shouldn't be promoted into leadership?", "No — many make excellent leaders. The point is that technical excellence shouldn't be the only signal used to decide, and the transition needs deliberate support rather than an assumption that it will look after itself."),
             ("How can leadership potential be assessed separately from technical skill?", "Structured observation of how someone handles ambiguity, prioritisation and difficult conversations — ideally before the promotion decision, not discovered afterwards."),
             ("What's the fastest fix if this mistake has already been made?", "Deliberate onboarding and coaching now, rather than waiting for performance to correct itself — see the dedicated article on leadership onboarding for what week one should cover, even retroactively."),
         ],
         related_slug="leadership-development", related_title="Leadership Development service",
         related_reading=[
             ("Leadership Development: The Complete Guide", "leadership-development-complete-guide"),
             ("Leadership Onboarding: What New Managers Need in Week One", "leadership-onboarding-week-one"),
             ("Succession Planning for Critical Roles", "succession-planning-critical-roles"),
         ]),
    dict(slug="leadership-onboarding-week-one", category="Leadership",
         title="Leadership Onboarding: What New Managers Need in Week One",
         h1="Leadership Onboarding: What New Managers Need in Week One",
         hero_sub="New leaders left to work out expectations through trial and error tend to default to whatever leadership style they last experienced — good or bad. Week one can prevent that.",
         sections=[
             ("Why week one sets the trajectory",
              ["A new manager's early decisions and habits tend to calcify quickly, because a team forms its impression of what's normal from what it sees first. Leaving those first days to chance means the trajectory gets set by accident rather than by design — and correcting an established pattern later is far harder than setting the right one from day one."]),
             ("What most organisations leave to chance",
              ["It's common to onboard a new manager into the administrative side of the role — systems, reporting lines, budgets — while leaving the leadership expectations themselves implicit: how decisions should be made, how the team should be communicated with, what 'good' looks like in this specific organisation's culture."]),
             ("What actually needs to be explicit from day one",
              ["Explicit expectations on decision-making authority, communication norms, and what support is available when judgement calls get hard remove the guesswork a new leader would otherwise have to resolve alone, often at the exact moment they can least afford to get it wrong."]),
             ("Building a repeatable onboarding pathway",
              ["The Housing Leadership &amp; Onboarding Transformation case study is a direct example: a defined, values-based onboarding pathway for new leaders cut time-to-competence by 20%, because expectations were designed in rather than left for each new manager to discover independently."]),
         ],
         faqs=[
             ("Does this apply equally to internal promotions and external hires?", "Both need it, though internal promotions often get it skipped entirely on the assumption that familiarity with the organisation is enough — it isn't, for the leadership-specific expectations covered here."),
             ("How formal does a week-one onboarding pathway need to be?", "Formal enough to be consistent and repeatable across every new manager, not so bureaucratic that it becomes a checklist exercise rather than genuine early support."),
             ("What's the single highest-value thing to make explicit in week one?", "Decision-making authority — what a new manager can decide alone, what needs escalation, and who to go to when it's unclear — removes the single biggest source of early hesitation or overreach."),
         ],
         related_slug="leadership-development", related_title="Leadership Development service",
         related_reading=[
             ("Leadership Development: The Complete Guide", "leadership-development-complete-guide"),
             ("Why Promoting Your Best Technical Expert Often Fails", "why-promoting-technical-experts-fails"),
             ("Succession Planning for Critical Roles", "succession-planning-critical-roles"),
         ]),
    dict(slug="succession-planning-critical-roles", category="Leadership",
         title="Succession Planning for Critical Roles",
         h1="Succession Planning for Critical Roles",
         hero_sub="Waiting for a vacancy to start thinking about who's ready to fill it turns succession into crisis management — here's how to build the pipeline before it's needed.",
         sections=[
             ("Why succession planning gets deprioritised until it's urgent",
              ["Succession planning competes for attention with problems that feel more immediate, and a critical role that's currently filled doesn't feel urgent — until the person in it leaves, at which point the organisation is planning under exactly the time pressure succession planning exists to avoid."]),
             ("Identifying critical roles, not just senior ones",
              ["Seniority and criticality aren't the same thing — a specific technical or operational role several levels below the board can be more critical to continuity than a senior generalist position. Identifying genuinely critical roles means asking what would actually stop the organisation functioning if the role were vacant tomorrow, not just reading the org chart from the top down."]),
             ("Building the pipeline before the vacancy",
              ["Once critical roles are identified, the pipeline is built by deliberately developing likely successors against the judgement and capability the role requires — not by hoping someone suitable happens to be available when the vacancy arises. This is where succession planning and leadership onboarding meet: a successor who's been deliberately prepared needs a much shorter onboarding runway when the moment comes."]),
             ("Succession planning as risk management",
              ["Treated as an HR administrative exercise, succession planning tends to get deprioritised. Treated as risk management — what's the organisation's actual exposure if this specific role becomes vacant with no notice — it tends to get the attention and resource it needs from leadership."]),
         ],
         faqs=[
             ("How many potential successors should a critical role have?", "More than one where possible — a single named successor is still a single point of failure if their own circumstances change."),
             ("Should potential successors know they've been identified?", "Generally yes, in some form — development that's kept secret is harder to act on deliberately, and transparency tends to support retention rather than undermine it."),
             ("How does succession planning fit with leadership onboarding?", "A successor who's been deliberately developed in advance needs a shorter, more targeted onboarding when the transition happens — the two disciplines compound rather than duplicate each other."),
         ],
         related_slug="leadership-development", related_title="Leadership Development service",
         related_reading=[
             ("Leadership Development: The Complete Guide", "leadership-development-complete-guide"),
             ("Why Promoting Your Best Technical Expert Often Fails", "why-promoting-technical-experts-fails"),
             ("Leadership Onboarding: What New Managers Need in Week One", "leadership-onboarding-week-one"),
         ]),
    dict(slug="capability-development-complete-guide", category="Capability", kind="Complete Guide",
         title="Capability Development: What It Means, and Why It Isn't Training",
         h1="Capability Development: What It Means, and Why It Isn't Training",
         hero_sub="Everything you need to know about capability development — what it actually means, how it differs from training, and how to build it deliberately rather than by accident.",
         sections=[
             ("What capability development actually means",
              ["Capability development is the discipline of ensuring an organisation — not just its individuals — can reliably deliver a required outcome. That means people, but it also means governance, structure, process and evidence all working together. An organisation can be full of competent, well-trained individuals and still lack capability, if those other layers are missing."]),
             ("Why it isn't training",
              ["Training is one possible input into capability, not a synonym for it. Where the missing layer is unclear roles, absent governance, or a structure working against the outcome, training doesn't close the gap — because training was never the layer that was broken. This is the core idea behind everything in this cluster, and behind this site: training is rarely the problem, capability is."]),
             ("What is a capability framework?",
              ["A capability framework is the practical tool that makes capability development possible at scale — a defined, consistent standard of competence used for assessment, development and workforce planning. Unlike a job description, it's meant to be applied the same way by every assessor, not interpreted locally by every team. The dedicated article gives the full working definition."]),
             ("Capability vs competency",
              ["The two get used interchangeably but describe different things: competency usually describes an individual's skill or behaviour, while capability describes whether the organisation as a whole can reliably deliver the outcome. An organisation can have competent individuals and still lack capability — see the dedicated article for where confusing the two causes real problems."]),
             ("Running a Capability Readiness Review",
              ["Before investing in any capability-building intervention, it's worth identifying which of six areas — capability, leadership, process, governance, workforce or training — a performance problem actually sits in. That's what the Capability Readiness Review tests, and the dedicated article explains how to run one properly."]),
             ("Multi-specialisation capability frameworks",
              ["Organisations with multiple specialisations or role types often end up with inconsistent, locally-invented standards, because nobody owns a framework spanning all of them. Multi-specialisation design deliberately maps common ground across roles while preserving genuine differences — the dedicated article covers how."]),
             ("What this looks like in practice",
              ["The Defence Capability Framework Design case study is the clearest evidence on this site: before the framework, 'ready' meant different things in different teams — an operational risk, not just an administrative inconvenience. The multi-specialisation framework and skills mapping exercise that followed lifted operational readiness by 20%, because it was designed from the outset to be usable for assessment, development and workforce planning, and was actually adopted as a result."]),
         ],
         faqs=[
             ("Is capability development just a rebrand of training and development?", "No — it's a broader discipline that includes training as one possible input, alongside governance, structure, process and evidence. Where those other layers are missing, more training doesn't build capability."),
             ("How do we know if our problem is capability or just a skills gap?", "The Capability Readiness Review is designed for exactly this — testing which of six areas a performance problem actually sits in before committing to an intervention."),
             ("Does capability development apply outside Defence and public sector?", "Yes — the discipline of tracing performance back to the layer that's genuinely missing applies to any organisation, though Defence and regulated public sector environments tend to make the cost of getting it wrong more visible."),
             ("Where should we start if we're new to thinking about capability this way?", "With whichever of the four dedicated articles below answers the most pressing question right now — what a framework actually is, how capability differs from competency, how to run a readiness review, or how to design for multiple specialisations."),
         ],
         related_slug="capability-framework-design", related_title="Capability Framework Design service",
         related_reading=[
             ("Building Capability Frameworks People Actually Use", "building-capability-frameworks"),
             ("What Is a Capability Framework? A Practical Definition", "what-is-a-capability-framework"),
             ("Capability vs Competency: Are They the Same Thing?", "capability-vs-competency-explained"),
             ("How to Run a Capability Readiness Review", "how-to-run-a-capability-readiness-review"),
             ("Multi-Specialisation Capability Frameworks Explained", "multi-specialisation-capability-frameworks"),
         ]),
    dict(slug="what-is-a-capability-framework", category="Capability",
         title="What Is a Capability Framework? A Practical Definition",
         h1="What Is a Capability Framework? A Practical Definition",
         hero_sub="A capability framework is one of the most misused terms in workforce development — here's a definition you can actually apply.",
         sections=[
             ("A working definition",
              ["A capability framework is a defined, consistent standard of competence for a role or specialisation, used for assessment, development and workforce planning. The word doing the real work in that definition is 'consistent' — a framework that different assessors apply differently isn't providing the thing it exists to provide."]),
             ("What it isn't",
              ["It isn't a job description — job descriptions describe duties and responsibilities, not the standard of competence expected. It isn't a simple competency list either, unless that list has been designed for consistent assessment, development and workforce planning use — a list on its own is a starting point, not a finished framework."]),
             ("What it needs to do to earn its keep",
              ["A working framework needs to let a manager assess someone fairly, let HR plan the workforce against it, and let an individual understand what progression actually requires — all from the same document, applied consistently. If it can't do all three, it's not yet doing its job."]),
             ("Where to start if you don't have one yet",
              ["Start from the roles or specialisations with the clearest operational risk if 'ready' is inconsistently defined, rather than trying to build an enterprise-wide framework in one pass. A framework that's used and trusted for a handful of critical roles is worth more than a comprehensive one that's published and never opened."]),
         ],
         faqs=[
             ("How is this different from a skills matrix?", "A skills matrix typically tracks which individuals have which skills. A capability framework defines the standard those skills are being assessed against in the first place — the matrix can sit on top of the framework, not replace it."),
             ("Who should be involved in building one?", "The people who'll actually use it — managers who'll assess against it, and representative role-holders — tested against real assessment scenarios during development, not finalised in isolation."),
             ("How do you know if an existing framework is actually working?", "Ask whether two different managers assessing the same person against it would reach the same conclusion. If the answer varies by manager, it isn't providing the consistency it was built for."),
         ],
         related_slug="capability-framework-design", related_title="Capability Framework Design service",
         related_reading=[
             ("Capability Development: The Complete Guide", "capability-development-complete-guide"),
             ("Capability vs Competency: Are They the Same Thing?", "capability-vs-competency-explained"),
             ("Building Capability Frameworks People Actually Use", "building-capability-frameworks"),
         ]),
    dict(slug="capability-vs-competency-explained", category="Capability",
         title="Capability vs Competency: Are They the Same Thing?",
         h1="Capability vs Competency: Are They the Same Thing?",
         hero_sub="Related, frequently confused, and genuinely different — and confusing them leads to solving the wrong problem.",
         sections=[
             ("The individual/organisational distinction",
              ["Competency usually describes an individual's skill or behaviour — can this person do this thing, to this standard. Capability describes something broader: whether the organisation as a whole, including its people, governance, structure and process together, can reliably deliver the required outcome."]),
             ("Why the difference matters in practice",
              ["An organisation can have entirely competent individuals and still lack capability, if governance is unclear, structure works against the outcome, or process doesn't support what those individuals are trying to do. Conversely, capability can't exceed the competency of the people delivering it — the two have to be built together, not treated as substitutes."]),
             ("Where confusing them causes real problems",
              ["The most common failure is diagnosing a capability problem — organisational, structural, governance-related — as a competency problem, and responding with more individual training. The individuals get more skilled; the organisational gap that was actually causing the performance problem remains exactly where it was."]),
             ("Using both together properly",
              ["A useful diagnostic sequence tests competency and capability separately: are the individuals equipped to do what's asked of them, and separately, does the organisation around them support them in doing it. The Capability Readiness Review is built to test exactly this distinction before recommending an intervention."]),
         ],
         faqs=[
             ("Can you have high competency and low capability at the same time?", "Yes, and it's a common pattern — highly skilled individuals working inside unclear roles, weak governance or a structure that undermines what they're trying to do."),
             ("Does building capability always require building competency too?", "Usually both need attention together — capability can't exceed the underlying competency of the people involved, even once the organisational layers are fixed."),
             ("How do we test which one is actually the problem?", "The Capability Readiness Review is designed for this — testing across capability, leadership, process, governance, workforce and training to identify where the real gap sits."),
         ],
         related_slug="capability-framework-design", related_title="Capability Framework Design service",
         related_reading=[
             ("Capability Development: The Complete Guide", "capability-development-complete-guide"),
             ("What Is a Capability Framework? A Practical Definition", "what-is-a-capability-framework"),
             ("How to Run a Capability Readiness Review", "how-to-run-a-capability-readiness-review"),
         ]),
    dict(slug="how-to-run-a-capability-readiness-review", category="Capability",
         title="How to Run a Capability Readiness Review",
         h1="How to Run a Capability Readiness Review",
         hero_sub="Before investing in any capability-building intervention, it's worth establishing exactly where the real gap sits — here's how the review works.",
         sections=[
             ("What the review actually tests",
              ["A Capability Readiness Review is a structured diagnostic for identifying which of six areas a performance problem genuinely sits in, before any solution is designed. Its purpose is to prevent the single most expensive mistake in this field: committing budget to an intervention before establishing what's actually causing the gap."]),
             ("The six areas it covers",
              ["The review tests capability, leadership, process, governance, workforce and training as distinct possible sources of a performance problem — because a gap that presents the same way on the surface can come from any of these, and each requires a genuinely different response."]),
             ("Running it properly: self vs facilitated",
              ["A self-assessment version gives a quick, honest first read on where an organisation likely sits — useful for framing the conversation. A facilitated review goes further, gathering evidence and stakeholder input to produce a prioritised, board-ready picture of the real problem, which matters more where the answer needs to survive scrutiny."]),
             ("What to do with the findings",
              ["The output should point directly at what to do next, not just describe the problem — if the review identifies a training gap, that's a mandate for TNA and design; if it identifies governance or structural issues, training was never going to be the answer, and the findings should redirect the conversation accordingly."]),
         ],
         faqs=[
             ("How long does a Capability Readiness Review take?", "The self-assessment version takes minutes. A full facilitated review, with evidence-gathering and stakeholder input, is typically a matter of weeks depending on scope."),
             ("Can the review conclude that training is the right answer?", "Yes — that's a legitimate outcome. The point isn't to rule out training, it's to test the assumption properly before committing budget to it."),
             ("Is the free self-assessment enough on its own, or do we need the facilitated version?", "The self-assessment is a strong starting point for framing the problem; the facilitated version is worth it where the finding needs to be defensible to a board or funder, not just directionally useful internally."),
         ],
         related_slug="capability-readiness-review", related_title="Take the free self-assessment",
         related_reading=[
             ("Capability Development: The Complete Guide", "capability-development-complete-guide"),
             ("Capability vs Competency: Are They the Same Thing?", "capability-vs-competency-explained"),
             ("Multi-Specialisation Capability Frameworks Explained", "multi-specialisation-capability-frameworks"),
         ]),
    dict(slug="multi-specialisation-capability-frameworks", category="Capability",
         title="Multi-Specialisation Capability Frameworks Explained",
         h1="Multi-Specialisation Capability Frameworks Explained",
         hero_sub="Organisations with multiple specialisations often end up with inconsistent, locally-invented standards — here's how to design a framework that spans all of them properly.",
         sections=[
             ("The problem multi-specialisation frameworks solve",
              ["Where multiple specialisations or role types exist without a single owned framework spanning all of them, standards tend to be invented locally, team by team. The result is a workforce where 'ready' means something different depending which part of the organisation you're standing in — an operational risk, not just an inconsistency."]),
             ("Common ground vs genuine specialisation difference",
              ["Good multi-specialisation design deliberately separates what should be consistent across every specialisation — core standards, assessment approach, progression logic — from what's genuinely distinct about each one. Treating everything as either fully shared or fully separate both fail, in different ways."]),
             ("Building consistency without flattening real distinctions",
              ["The design challenge is making cross-specialisation comparison possible — so workforce planning and assessment mean the same thing everywhere — without erasing what's genuinely different about each specialisation's actual requirements. That balance is the entire point of the exercise; either extreme is easier and less useful."]),
             ("Proof it works",
              ["The Defence Capability Framework Design case study is direct evidence: before the framework, 'ready' meant different things in different teams. The multi-specialisation framework and skills mapping exercise that followed lifted operational readiness by 20%, and made cross-specialisation workforce planning possible for the first time."]),
         ],
         faqs=[
             ("How many specialisations justify a multi-specialisation framework?", "There's no fixed threshold — the trigger is inconsistent local standards across roles that should be comparable, which can show up with as few as two or three specialisations."),
             ("Does this replace specialisation-specific standards entirely?", "No — it sits above them, providing common ground for comparison and workforce planning while preserving what's genuinely distinct about each specialisation."),
             ("How long does building a multi-specialisation framework typically take?", "It depends on scope and the number of specialisations involved, but it's typically a matter of months rather than weeks, given the stakeholder mapping required to get common ground right."),
         ],
         related_slug="capability-framework-design", related_title="Capability Framework Design service",
         related_reading=[
             ("Capability Development: The Complete Guide", "capability-development-complete-guide"),
             ("What Is a Capability Framework? A Practical Definition", "what-is-a-capability-framework"),
             ("How to Run a Capability Readiness Review", "how-to-run-a-capability-readiness-review"),
         ]),
    dict(slug="digital-learning-complete-guide", category="Digital Learning", kind="Complete Guide",
         title="Digital Learning That Actually Changes Behaviour",
         h1="Digital Learning That Actually Changes Behaviour",
         hero_sub="Everything you need to know about digital learning that actually changes behaviour — not just delivers content — from format choice through rollout to what happens after week one.",
         sections=[
             ("What digital learning is actually for",
              ["Digital learning succeeds or fails on the same test as any other intervention: did it change behaviour or performance, not whether it was accessed. Format — digital, blended, face-to-face — is a delivery decision that should follow from the audience and the outcome required, not a strategy in its own right."]),
             ("Blended vs fully digital: choosing the right mix",
              ["Fully digital delivery suits content that's stable, individually paced and doesn't depend on practising a skill with others. Blended delivery earns its extra complexity where judgement, interaction or hands-on practice genuinely matter to the outcome. The dedicated article sets out how to make that call per audience rather than as a single organisation-wide policy."]),
             ("Why rollouts stall after launch",
              ["A strong launch is not the same as adoption — most digital learning rollouts that underdeliver do so weeks after go-live, not on day one. The dedicated article covers the specific pattern: what stalling looks like in the data, and the manager-level gap that usually causes it."]),
             ("Designing for shift workers and distributed teams",
              ["Standard digital learning design quietly assumes a desk, a stable login window and a manager physically present to reinforce it — assumptions that don't hold for shift workers or distributed teams. The dedicated article covers what to design around instead."]),
             ("What happens after week one",
              ["Week-one access numbers are the most misleading metric in digital learning, because they measure curiosity, not adoption. What happens in the weeks after is what actually determines whether the investment pays off — the dedicated article covers the levers that drive or kill sustained use."]),
             ("What this looks like in practice",
              ["The Healthcare Learning Transformation case study demonstrates the underlying discipline: cutting compliance gaps by 18% came largely from configuration, dashboard design and information management on an existing platform — not from the platform or format itself, but from designing deliberately for how people would actually use it, week after week."]),
         ],
         faqs=[
             ("Is fully digital always cheaper than blended delivery?", "Usually cheaper to deliver, but cost of delivery isn't the right comparison if the fully digital version doesn't achieve the required behaviour change — cheaper delivery of the wrong format isn't a saving."),
             ("How soon after launch should we expect to see adoption problems, if any?", "Most stalling shows up within the first few weeks, which is exactly why week-one metrics alone are a poor signal of whether a rollout is actually working."),
             ("Do shift and distributed teams need a completely different platform?", "Not necessarily a different platform — usually different design decisions around access windows, format length and manager reinforcement, layered onto the same underlying system."),
             ("Where should we start if our current digital learning already feels like it's stalling?", "With the adoption article below — it covers what's actually driving drop-off and the manager-level lever that's usually the fastest fix."),
         ],
         related_slug="digital-learning", related_title="Digital Learning service",
         related_reading=[
             ("Blended Learning vs Fully Digital: Choosing the Right Mix", "blended-vs-fully-digital-learning"),
             ("Why Digital Learning Rollouts Stall After Launch", "why-digital-learning-rollouts-stall"),
             ("Designing Digital Learning for Shift Workers and Distributed Teams", "digital-learning-shift-workers-distributed-teams"),
             ("Digital Learning Adoption: What Happens After Week One", "digital-learning-adoption-after-week-one"),
         ]),
    dict(slug="blended-vs-fully-digital-learning", category="Digital Learning",
         title="Blended Learning vs Fully Digital: Choosing the Right Mix",
         h1="Blended Learning vs Fully Digital: Choosing the Right Mix",
         hero_sub="The right format decision follows from the audience and the outcome required — not from a preference for one delivery mode over another.",
         sections=[
             ("The question that actually decides it",
              ["The right question isn't 'digital or face-to-face' in the abstract — it's whether the outcome depends on practising a skill under realistic conditions with other people, or whether it's content that can be absorbed individually at an individual pace. That single question resolves most format decisions."]),
             ("Where fully digital works well",
              ["Fully digital delivery suits stable, individually-paced content — policy updates, compliance knowledge, reference material — where the goal is consistent understanding rather than practised judgement under pressure."]),
             ("Where blended is worth the extra complexity",
              ["Where the outcome genuinely depends on interaction, hands-on practice or judgement under realistic conditions, blended delivery is worth its additional cost and complexity — digital components handle the stable knowledge, freeing face-to-face time for the parts that actually need it."]),
             ("Making the choice per audience, not organisation-wide",
              ["A single format policy applied across an entire organisation usually serves some audiences well and others badly. The more durable approach makes this decision per audience and per outcome, rather than settling it once at a strategic level and applying it everywhere."]),
         ],
         faqs=[
             ("Is blended learning always more effective than fully digital?", "Not always — it's more effective specifically where interaction or hands-on practice matters to the outcome. For stable, individually-absorbed content, fully digital can be equally effective and considerably more efficient."),
             ("How do we decide this for a large, varied workforce?", "Segment by outcome type rather than by department — group content by whether it depends on interaction or practice, not by which team happens to need it."),
             ("Does blended always cost more to deliver?", "Generally yes, in delivery cost — the case for it rests on whether that additional cost is earned back in improved outcomes, not on cost alone."),
         ],
         related_slug="digital-learning", related_title="Digital Learning service",
         related_reading=[
             ("Digital Learning: The Complete Guide", "digital-learning-complete-guide"),
             ("Why Digital Learning Rollouts Stall After Launch", "why-digital-learning-rollouts-stall"),
             ("Digital Learning Adoption: What Happens After Week One", "digital-learning-adoption-after-week-one"),
         ]),
    dict(slug="why-digital-learning-rollouts-stall", category="Digital Learning",
         title="Why Digital Learning Rollouts Stall After Launch",
         h1="Why Digital Learning Rollouts Stall After Launch",
         hero_sub="A strong launch is not the same as adoption — most digital learning rollouts that underdeliver do so weeks after go-live, not on day one.",
         sections=[
             ("Launch success is not adoption success",
              ["Launch day numbers measure curiosity and initial compliance — people logging in because it's new, or because they were told to. They say very little about whether the platform will still be used, as intended, a month later. Treating a strong launch as proof of success is the first mistake."]),
             ("The manager gap",
              ["The single biggest predictor of sustained adoption is whether a learner's direct manager visibly expects and reinforces use of the platform. Where that reinforcement is missing, usage tends to decay quickly once the initial novelty and top-down messaging fade."]),
             ("What stalling actually looks like in the data",
              ["Stalling rarely looks like a dramatic drop-off — it looks like a slow, steady decline in logins and completions over several weeks, easy to miss if the only metric being tracked is cumulative access since launch rather than active use in the current period."]),
             ("Designing for week two, not just launch day",
              ["Rollouts that sustain adoption are designed with week two, four and twelve in mind from the start — manager reinforcement built into the plan, not left to chance, and a way of tracking active use rather than just cumulative reach."]),
         ],
         faqs=[
             ("What's the single most effective fix for a stalling rollout?", "Enlisting direct managers as visible reinforcers of use — it consistently matters more than platform features or additional launch communications."),
             ("How would we know if our rollout is already stalling?", "Track active use in the current period, not cumulative access since launch — a platform can show impressive total numbers while active weekly use quietly declines."),
             ("Is it too late to fix a rollout that's already stalled?", "No — reintroducing manager reinforcement and refreshing relevance for the current period can revive adoption, though it's easier to design in from the start than to retrofit."),
         ],
         related_slug="digital-learning", related_title="Digital Learning service",
         related_reading=[
             ("Digital Learning: The Complete Guide", "digital-learning-complete-guide"),
             ("Digital Learning Adoption: What Happens After Week One", "digital-learning-adoption-after-week-one"),
             ("Blended Learning vs Fully Digital: Choosing the Right Mix", "blended-vs-fully-digital-learning"),
         ]),
    dict(slug="digital-learning-shift-workers-distributed-teams", category="Digital Learning",
         title="Designing Digital Learning for Shift Workers and Distributed Teams",
         h1="Designing Digital Learning for Shift Workers and Distributed Teams",
         hero_sub="Standard digital learning design quietly assumes a desk and a manager physically present — assumptions that don't hold for shift workers or distributed teams.",
         sections=[
             ("Why standard digital learning design assumes a desk",
              ["Most off-the-shelf digital learning design assumes stable working hours, reliable device access, and a manager in the same physical space to reinforce it. Shift workers and distributed teams routinely have none of these, which is why standard rollouts to these audiences underperform even when the content itself is sound."]),
             ("Designing around access, not around content",
              ["The design question for these audiences starts with access, not content: what device do they realistically have, in what window of time, with what connectivity — and the format follows from the honest answer, rather than from what's easiest to build centrally."]),
             ("Distributed teams need distributed governance too",
              ["Where teams are spread across sites or locations, reinforcement and governance need a local presence too — a single central push rarely lands consistently across every site. Nominating local reinforcement, even informally, closes a gap that central communication alone can't."]),
             ("What good looks like for these audiences",
              ["Good design for shift workers and distributed teams tends to mean shorter, mobile-first content, flexible access windows that don't assume a fixed shift pattern, and locally nominated reinforcement rather than relying solely on a central manager or communication channel."]),
         ],
         faqs=[
             ("Does this mean building a completely separate platform for these teams?", "Not usually — it's more often a design and access-window change on the existing platform than a parallel system."),
             ("How do we handle reinforcement without a manager on every shift?", "Nominate local reinforcement at site or team level, even informally, rather than relying on a single manager who isn't physically present for every shift pattern."),
             ("Is mobile-first design enough on its own?", "It helps, but access windows and local reinforcement matter as much as device format — mobile content still fails if it assumes a stable block of time nobody on shift actually has."),
         ],
         related_slug="digital-learning", related_title="Digital Learning service",
         related_reading=[
             ("Digital Learning: The Complete Guide", "digital-learning-complete-guide"),
             ("Why Digital Learning Rollouts Stall After Launch", "why-digital-learning-rollouts-stall"),
             ("Blended Learning vs Fully Digital: Choosing the Right Mix", "blended-vs-fully-digital-learning"),
         ]),
    dict(slug="digital-learning-adoption-after-week-one", category="Digital Learning",
         title="Digital Learning Adoption: What Happens After Week One",
         h1="Digital Learning Adoption: What Happens After Week One",
         hero_sub="Week-one access numbers are the most misleading metric in digital learning — what happens after is what actually determines whether the investment pays off.",
         sections=[
             ("Why week one numbers are misleading",
              ["Week one measures novelty and compliance with a launch instruction, not whether the platform has become part of how people actually work. Reporting week-one access as a success metric answers a question nobody senior should be asking — did people log in once."]),
             ("What drives the drop-off",
              ["Drop-off after the initial period is usually driven by the same handful of causes: no ongoing manager expectation, content that doesn't refresh or stay relevant, and no visible link between using the platform and anything the learner or their manager is actually measured on."]),
             ("Manager reinforcement as the real adoption lever",
              ["Of every lever available, ongoing manager reinforcement — checking in, referencing the platform in team conversations, expecting it to be used — has the largest measurable effect on whether use continues past the first few weeks."]),
             ("Measuring adoption, not just access",
              ["Adoption should be tracked as active use in the current period, not cumulative access since launch. A platform with a large historical access count can still be barely used today — and that's the number that actually predicts whether the investment is working."]),
         ],
         faqs=[
             ("How long after launch should we start worrying about adoption?", "Start tracking active use from week one — by week four or five, a genuine downward trend is usually visible if reinforcement isn't in place."),
             ("Is content refresh really necessary, or is reinforcement enough?", "Both matter — reinforcement without refreshed, relevant content eventually loses credibility, and refreshed content without reinforcement still tends to be ignored."),
             ("What's a realistic target for sustained adoption?", "It varies by context, but the more useful target is a stable or growing trend in active current-period use, not a specific number in isolation."),
         ],
         related_slug="digital-learning", related_title="Digital Learning service",
         related_reading=[
             ("Digital Learning: The Complete Guide", "digital-learning-complete-guide"),
             ("Why Digital Learning Rollouts Stall After Launch", "why-digital-learning-rollouts-stall"),
             ("Designing Digital Learning for Shift Workers and Distributed Teams", "digital-learning-shift-workers-distributed-teams"),
         ]),
    dict(slug="training-governance-complete-guide", category="Governance", kind="Complete Guide",
         title="Training Governance: Making It Audit-Ready and Useful",
         h1="Training Governance: Making It Audit-Ready and Useful",
         hero_sub="Everything you need to know about training governance that survives audit and actually helps leaders make better decisions — including what DSAT and JSP 822 really require.",
         sections=[
             ("What training governance actually is",
              ["Training governance is the decision rights and evidence trail behind how training and learning are assured, audited and held accountable — who owns which decision, and what evidence proves it was made well. Done properly, it's the same system whether the audience is an internal leader making a decision or an external auditor reviewing it afterwards."]),
             ("Governance vs compliance",
              ["Governance and compliance overlap but aren't the same thing — compliance asks whether a rule was followed, governance asks whether decisions were made well and can be defended. Treating governance as purely a compliance exercise is the single most common reason it ends up feeling like bureaucracy rather than something useful. The dedicated article covers the distinction in full."]),
             ("What JSP 822 requires, in plain English",
              ["JSP 822 is the Ministry of Defence policy setting out DSAT requirements — the governance backbone behind Defence training assurance and audit. Stripped of acronym overload, it asks for evidence that training decisions were made against a real capability requirement and can be defended afterwards. The dedicated article walks through what it actually requires."]),
             ("How this connects to DSAT",
              ["DSAT — the Defence Systems Approach to Training — is the methodology JSP 822 sets out, and training governance is what makes each phase of it defensible: Analysis, Design, Development, Delivery and Evaluation all need an evidence trail, not just a completed process. See the dedicated DSAT Explained article for the full methodology."]),
             ("Building an audit-ready evidence trail without extra admin",
              ["The instinctive response to 'be audit-ready' is often to add more forms and sign-offs — which tends to produce exactly the box-ticking governance people resent. The better approach captures evidence as a natural byproduct of how decisions are already being made. The dedicated article covers how."]),
             ("Decision rights, not just paperwork",
              ["Good governance clarifies who has authority to make which decisions, and ensures that authority is exercised with visible evidence — not just that a form was completed somewhere. Confusion about decision rights is often the real root cause behind governance that exists on paper but doesn't actually inform anything."]),
             ("What this looks like in practice",
              ["Training governance embedded across the Digital Skills for Defence programme gave decision-makers evidence they could defend, rather than assumptions they hoped would hold — turning governance into something that supported enterprise-wide investment decisions, not just something checked at the end. The full story is in the Defence Training Governance article and the DS4D case study."]),
         ],
         faqs=[
             ("Is this guide specific to Defence, or does it apply more broadly?", "JSP 822 and DSAT are Defence-specific, but the underlying discipline — decision rights, evidence captured as a byproduct of decisions, governance that serves leaders as much as auditors — applies to any regulated or high-stakes training environment."),
             ("How do we know if our governance is audit-ready?", "Test it directly: pick a recent significant training decision and see how long it takes to produce defensible evidence for it. Weeks rather than a day is your current risk exposure."),
             ("Does better governance always mean more process?", "No — the most effective governance is often less process, not more, because it captures evidence as decisions are made rather than adding a separate compliance layer afterwards."),
             ("Where should we start if governance currently feels like pure overhead?", "With the audit-ready evidence trail article — overhead is usually the symptom of evidence being reconstructed after the fact rather than captured as decisions happen."),
         ],
         related_slug="training-governance-assurance", related_title="Training Governance &amp; Assurance service",
         related_reading=[
             ("Defence Training Governance", "defence-training-governance"),
             ("DSAT Explained", "dsat-explained"),
             ("What Is JSP 822? A Plain-English Explanation", "what-is-jsp-822"),
             ("Governance vs Compliance: Why the Distinction Matters", "governance-vs-compliance"),
             ("Building an Audit-Ready Evidence Trail Without Extra Admin", "audit-ready-evidence-trail-without-extra-admin"),
         ]),
    dict(slug="what-is-jsp-822", category="Governance",
         title="What Is JSP 822? A Plain-English Explanation",
         h1="What Is JSP 822? A Plain-English Explanation",
         hero_sub="The Ministry of Defence policy behind DSAT, stripped of acronym overload — what it actually asks for, and why it exists.",
         sections=[
             ("What JSP 822 actually is",
              ["JSP 822 is the Ministry of Defence Joint Service Publication that sets out the requirements for DSAT — the Defence Systems Approach to Training. It's the policy document behind Defence training governance, assurance and audit, defining what evidence and process a training decision needs to be defensible."]),
             ("What it requires in practice",
              ["In practice, JSP 822 asks for a traceable line from capability requirement, through training design and delivery, to evidence that the training worked — with each stage documented well enough to survive review by someone who wasn't involved in the original decision."]),
             ("How it relates to DSAT",
              ["DSAT is the methodology; JSP 822 is the policy that mandates and defines it. Understanding JSP 822 without understanding DSAT's five phases — Analysis, Design, Development, Delivery, Evaluation — is like reading the requirement without the method for meeting it, which is why the two are best understood together."]),
             ("Common misreadings that cause friction",
              ["The most common misreading treats JSP 822 as a checklist to complete before training can be signed off, which produces exactly the slow, bureaucratic process people associate with it. Read as a decision-support framework instead — a structured way of testing whether a proposed intervention addresses the actual capability requirement — it does the opposite: it prevents wasted spend on training that was never going to work."]),
         ],
         faqs=[
             ("Is JSP 822 only relevant to uniformed Defence training?", "It applies across Defence training more broadly, including civilian and contractor-delivered training where Defence assurance requirements apply."),
             ("Does JSP 822 mandate a specific reporting template?", "It sets out requirements rather than a fixed template — what matters is that the evidence trail is traceable, however the documentation is formatted."),
             ("Does JSP 822 compliance slow down urgent training requirements?", "Not when applied as intended — speed problems usually come from unclear requirements or treating it as sequential paperwork, not from the policy itself."),
         ],
         related_slug="training-governance-assurance", related_title="Training Governance &amp; Assurance service",
         related_reading=[
             ("Training Governance: The Complete Guide", "training-governance-complete-guide"),
             ("DSAT Explained", "dsat-explained"),
             ("Governance vs Compliance: Why the Distinction Matters", "governance-vs-compliance"),
         ]),
    dict(slug="governance-vs-compliance", category="Governance",
         title="Governance vs Compliance: Why the Distinction Matters",
         h1="Governance vs Compliance: Why the Distinction Matters",
         hero_sub="Compliance asks whether a rule was followed. Governance asks whether the decision was made well — and confusing the two is why governance so often feels like bureaucracy.",
         sections=[
             ("What each actually means",
              ["Compliance tests whether a specific rule or requirement was met — was the form completed, was the course delivered within the required timeframe. Governance is broader: it tests whether decisions were made well, with the right authority and evidence, regardless of whether a specific rule directly applied."]),
             ("Why compliance-only governance fails leaders",
              ["An organisation that only tracks compliance can pass every individual check and still make poor training investment decisions overall, because compliance says nothing about whether those decisions were good ones — only whether the required boxes were completed."]),
             ("The overlap, and where it ends",
              ["Compliance is a useful, necessary subset of governance — meeting mandatory requirements is part of making a defensible decision. But governance that stops at compliance leaves the actual quality of decision-making untested, which is where most of the real risk sits."]),
             ("Building governance that does both jobs",
              ["Effective governance treats compliance requirements as a floor, not the ceiling — meeting them while also capturing the evidence and reasoning that shows decisions were genuinely sound, not just technically permitted."]),
         ],
         faqs=[
             ("Can an organisation be fully compliant and still have poor governance?", "Yes, and it's a common pattern — every required box checked, with no real evidence that the underlying decisions were actually good ones."),
             ("Does improving governance mean adding more compliance requirements?", "No — it usually means capturing better evidence around decisions that are already being made, not adding new rules to comply with."),
             ("How can we tell if our organisation has confused the two?", "Ask whether anyone reviews the quality of training decisions, not just whether the paperwork was completed — if the answer is no, compliance has likely been mistaken for governance."),
         ],
         related_slug="training-governance-assurance", related_title="Training Governance &amp; Assurance service",
         related_reading=[
             ("Training Governance: The Complete Guide", "training-governance-complete-guide"),
             ("What Is JSP 822? A Plain-English Explanation", "what-is-jsp-822"),
             ("Building an Audit-Ready Evidence Trail Without Extra Admin", "audit-ready-evidence-trail-without-extra-admin"),
         ]),
    dict(slug="audit-ready-evidence-trail-without-extra-admin", category="Governance",
         title="Building an Audit-Ready Evidence Trail Without Extra Admin",
         h1="Building an Audit-Ready Evidence Trail Without Extra Admin",
         hero_sub="'Audit-ready' usually gets translated into more forms and more sign-offs — it doesn't have to. Here's how to capture the evidence without the extra admin.",
         sections=[
             ("Why 'audit-ready' usually means 'more paperwork' — and why it doesn't have to",
              ["The instinctive response to an audit finding is to add a new form or approval step — which usually produces exactly the box-ticking culture people resent, without necessarily producing better evidence. The alternative is designing evidence capture into decisions that are already happening, rather than bolting a new process on top of them."]),
             ("Capturing evidence as a byproduct of decisions, not a separate task",
              ["If a decision is already being made — approving a training intervention, signing off a design — the evidence that decision was sound should be captured at that moment, as part of making it, rather than reconstructed later when an audit is announced. That single shift removes most of the 'extra admin' feeling."]),
             ("What to capture, and what's unnecessary",
              ["The evidence that matters is what shows a decision was traceable to a real requirement and defensible against alternatives — not every email or draft version along the way. Capturing everything is as unhelpful as capturing too little, because it buries the evidence that actually matters in noise."]),
             ("Testing whether it's actually working",
              ["The practical test is the same one used to judge any governance system: pick a recent decision and see how quickly defensible evidence can be produced for it. If it takes weeks of reconstruction rather than a day, the evidence trail isn't actually being captured at the point of decision — it's still being manufactured after the fact."]),
         ],
         faqs=[
             ("Does this require new software or systems?", "Not necessarily — it's often more a change in when and how evidence is recorded than a new system, though existing tools can make capture easier if used deliberately."),
             ("Who should be responsible for capturing this evidence?", "Whoever is making the decision, as part of making it — evidence captured by a third party after the fact is inherently less reliable and more effort to produce."),
             ("How much evidence is 'enough' for audit purposes?", "Enough that an independent reviewer could follow the reasoning from requirement to decision without having to take any step on trust — no more, no less."),
         ],
         related_slug="training-governance-assurance", related_title="Training Governance &amp; Assurance service",
         related_reading=[
             ("Training Governance: The Complete Guide", "training-governance-complete-guide"),
             ("Governance vs Compliance: Why the Distinction Matters", "governance-vs-compliance"),
             ("What Is JSP 822? A Plain-English Explanation", "what-is-jsp-822"),
         ]),
    dict(slug="evaluating-learning-investment-complete-guide", category="Evaluation", kind="Complete Guide",
         title="Evaluating Learning and Capability Investment: Beyond Completion Rates",
         h1="Evaluating Learning and Capability Investment: Beyond Completion Rates",
         hero_sub="Everything you need to know about evaluating learning and capability investment properly — beyond completion rates, beyond satisfaction scores, and into evidence a board will actually trust.",
         sections=[
             ("Why completion rates aren't evaluation",
              ["Completion confirms an intervention reached its intended audience. It says nothing about whether behaviour, performance or risk actually changed as a result — which is the only question evaluation exists to answer. Reporting completion as if it were evaluation is one of the most common and costly habits in this field."]),
             ("Kirkpatrick's model in practice",
              ["Kirkpatrick's four levels — reaction, learning, behaviour, results — remain the standard reference model for evaluation, and for good reason: they force a distinction between how people felt and what actually changed. The dedicated article covers where the model is genuinely useful and where it breaks down in practice."]),
             ("Why satisfaction scores don't prove impact",
              ["High satisfaction and zero measurable impact can and do coexist — people can enjoy an intervention that changed nothing about their subsequent performance. Satisfaction is worth tracking, but it answers a different, much narrower question than 'did this work.' The dedicated article explains why the two get conflated so often."]),
             ("Building an evaluation plan before a programme starts",
              ["Evaluation planned after a programme has already launched is mostly guesswork, because the baseline needed to prove anything changed no longer exists. The dedicated article covers what needs deciding — and measuring — before day one."]),
             ("Measuring ROI on capability investment for board reporting",
              ["Capability investment ROI is harder to quantify than financial ROI, but that doesn't mean it can't be credibly reported — it means being honest about what can be quantified, what should be reported qualitatively, and presenting both in a form a board will actually trust. The dedicated article covers how."]),
             ("What good evaluation actually requires",
              ["Good evaluation requires a baseline captured before the intervention, a defined measure of the outcome that actually matters, and a realistic timeframe for that outcome to show up. Skip any of the three, and the resulting evaluation — however sophisticated the model behind it — is not defensible."]),
             ("What this looks like in practice",
              ["The Healthcare Learning Transformation case study is direct evidence of evaluation done well: cutting compliance gaps by 18% was measurable precisely because dashboards and reporting were designed around the outcome that mattered to leaders, not around whatever the platform generated by default."]),
         ],
         faqs=[
             ("Is completion data worth tracking at all?", "Yes, as an operational delivery metric confirming the intended audience was reached — but it shouldn't be reported as evidence that the intervention worked."),
             ("Which evaluation approach should a small organisation start with?", "A simple before-and-after measure of the specific outcome the intervention targets, captured before launch — sophistication in the model matters less than having a genuine baseline."),
             ("How long after an intervention should impact be measured?", "It depends on the outcome — some behaviours change quickly, others take months to show up in the data. The evaluation plan should set this expectation before launch, not guess at it afterwards."),
             ("Where should we start if we've never formally evaluated a training investment before?", "With the evaluation planning article below — most of the value in evaluation comes from decisions made before a programme starts, not from the analysis done afterwards."),
         ],
         related_slug="learning-strategy", related_title="Learning Strategy service",
         related_reading=[
             ("Kirkpatrick's Model in Practice: Strengths and Limitations", "kirkpatricks-model-in-practice"),
             ("How to Build an Evaluation Plan Before a Programme Starts", "building-an-evaluation-plan-before-programme-starts"),
             ("Measuring ROI on Capability Investment for Board Reporting", "measuring-roi-capability-investment"),
             ("Why Satisfaction Scores Don't Prove Impact", "why-satisfaction-scores-dont-prove-impact"),
         ]),
    dict(slug="kirkpatricks-model-in-practice", category="Evaluation",
         title="Kirkpatrick's Model in Practice: Strengths and Limitations",
         h1="Kirkpatrick's Model in Practice: Strengths and Limitations",
         hero_sub="The standard reference model for training evaluation is genuinely useful — and genuinely limited. Knowing where each applies matters more than the model itself.",
         sections=[
             ("The four levels, briefly",
              ["Kirkpatrick's model evaluates across four levels: reaction (did people find it valuable), learning (did knowledge or skill increase), behaviour (did on-the-job behaviour change), and results (did the organisational outcome improve). Each level answers a different, progressively harder question."]),
             ("Where it's genuinely useful",
              ["The model's real value is structural — it forces a distinction between reaction and results that's otherwise easy to blur, and stops an organisation mistaking a good reaction score for proof of impact. As a checklist for what to measure and when, it holds up well."]),
             ("Where it breaks down in practice",
              ["The model is far more often applied at level one or two than at level three or four, because reaction and learning are easy to measure immediately, while behaviour and results take longer and require a baseline most organisations never captured. In practice, 'we use Kirkpatrick' frequently means 'we measure reaction' — which defeats the model's actual purpose."]),
             ("Using it as a starting point, not the whole answer",
              ["Kirkpatrick tells you what to measure; it doesn't build the baseline, the timeframe, or the organisational will to measure at levels three and four. Treating it as a complete evaluation methodology, rather than a useful frame that still needs a proper evaluation plan behind it, is where most of the disappointment with the model actually comes from."]),
         ],
         faqs=[
             ("Is Kirkpatrick still the right model to use?", "It remains a useful frame, particularly for distinguishing reaction from actual impact — the limitation is in how it's typically applied, not in the model itself."),
             ("Do all four levels need to be measured every time?", "Not necessarily, but stopping at level one or two and calling it evaluation is the specific mistake to avoid — at minimum, behaviour change should be considered where it's the outcome that actually matters."),
             ("Are there better alternatives to Kirkpatrick?", "Several newer models exist, but most share the same underlying requirement — a baseline and a defined timeframe — so the practical fix is usually building an evaluation plan properly, whichever model frames it."),
         ],
         related_slug="learning-strategy", related_title="Learning Strategy service",
         related_reading=[
             ("Evaluating Learning Investment: The Complete Guide", "evaluating-learning-investment-complete-guide"),
             ("Why Satisfaction Scores Don't Prove Impact", "why-satisfaction-scores-dont-prove-impact"),
             ("How to Build an Evaluation Plan Before a Programme Starts", "building-an-evaluation-plan-before-programme-starts"),
         ]),
    dict(slug="building-an-evaluation-plan-before-programme-starts", category="Evaluation",
         title="How to Build an Evaluation Plan Before a Programme Starts",
         h1="How to Build an Evaluation Plan Before a Programme Starts",
         hero_sub="Evaluation planned after a programme has already launched is mostly guesswork — here's what needs deciding before day one.",
         sections=[
             ("Why evaluation planned after the fact is mostly guesswork",
              ["Without a baseline captured before an intervention starts, any later claim about impact rests on assumption, not evidence — there's no honest way to know what would have happened anyway. This single gap, more than any analytical sophistication, is what makes most after-the-fact evaluation unreliable."]),
             ("What needs deciding before day one",
              ["Before launch, an evaluation plan should fix what outcome is being measured, what the current baseline is, and what timeframe is realistic for change to show up. Deciding these after launch means guessing retroactively at what 'before' looked like."]),
             ("Building the baseline",
              ["A baseline doesn't need to be elaborate — a clear measure of current performance against the specific outcome the intervention targets is enough, provided it's captured before anything changes. An imperfect baseline captured now beats a perfect one that doesn't exist because nobody thought to measure before launch."]),
             ("Keeping the plan realistic",
              ["An evaluation plan that tries to measure everything usually measures nothing well. Fixing on the one or two outcomes that actually matter to the decision this investment was meant to support keeps the plan achievable and the eventual findings credible."]),
         ],
         faqs=[
             ("What if we're already partway through a programme with no baseline?", "Capture one now — it's less reliable than a pre-launch baseline, but still far better than trying to reconstruct impact with nothing to compare against."),
             ("Who should own the evaluation plan?", "Whoever is accountable for the outcome the investment is meant to affect — evaluation designed in isolation by L&D, disconnected from the accountable owner, tends to measure the wrong thing."),
             ("How detailed does the plan need to be?", "Detailed enough to fix the outcome, baseline and timeframe clearly — beyond that, simplicity helps rather than hurts, since an overcomplicated plan is less likely to actually get followed."),
         ],
         related_slug="learning-strategy", related_title="Learning Strategy service",
         related_reading=[
             ("Evaluating Learning Investment: The Complete Guide", "evaluating-learning-investment-complete-guide"),
             ("Kirkpatrick's Model in Practice: Strengths and Limitations", "kirkpatricks-model-in-practice"),
             ("Measuring ROI on Capability Investment for Board Reporting", "measuring-roi-capability-investment"),
         ]),
    dict(slug="measuring-roi-capability-investment", category="Evaluation",
         title="Measuring ROI on Capability Investment for Board Reporting",
         h1="Measuring ROI on Capability Investment for Board Reporting",
         hero_sub="Capability investment ROI is harder to quantify than financial ROI — that's a reason to be precise about what can be measured, not a reason to avoid measuring it at all.",
         sections=[
             ("Why ROI on capability investment is harder than financial ROI",
              ["Financial ROI compares a cost against a directly measurable return. Capability investment often produces its return indirectly — through reduced risk, faster time-to-competence, or improved readiness — which makes the calculation genuinely harder, not impossible."]),
             ("What can be credibly quantified",
              ["Cost of the intervention, cost of the status quo it addresses, and a specific measurable proxy for improvement — compliance gaps closed, error rates reduced, time-to-competence — can usually be quantified credibly, provided a baseline exists to compare against."]),
             ("What should be reported qualitatively instead",
              ["Not every benefit reduces cleanly to a number — improved confidence in a decision, reduced reputational exposure, or stronger succession depth are real but resist precise quantification. Reported honestly as qualitative benefits alongside the quantified figures, they add credibility rather than undermining it; forced into an artificially precise number, they do the opposite."]),
             ("Presenting ROI a board will actually trust",
              ["Credible ROI reporting shows its working — the baseline, the method, and what's quantified versus what's qualitative — rather than presenting a single confident figure with no visible basis. A board that can see how a number was built tends to trust it more than one that's simply asked to accept it."]),
         ],
         faqs=[
             ("Is it dishonest to include qualitative benefits in an ROI case?", "No, provided they're clearly labelled as qualitative rather than folded into the quantified figure — the dishonesty risk is in blurring the two, not in reporting both."),
             ("What's the most common mistake in capability ROI reporting?", "Presenting a single confident number with no visible baseline or method — it invites scepticism rather than earning trust, however accurate the underlying work actually was."),
             ("Can ROI be calculated without a baseline?", "Not credibly — without a baseline, any ROI figure is an estimate of what might have happened, not a measured comparison against what actually did."),
         ],
         related_slug="learning-strategy", related_title="Learning Strategy service",
         related_reading=[
             ("Evaluating Learning Investment: The Complete Guide", "evaluating-learning-investment-complete-guide"),
             ("How to Build an Evaluation Plan Before a Programme Starts", "building-an-evaluation-plan-before-programme-starts"),
             ("Why Satisfaction Scores Don't Prove Impact", "why-satisfaction-scores-dont-prove-impact"),
         ]),
    dict(slug="why-satisfaction-scores-dont-prove-impact", category="Evaluation",
         title="Why Satisfaction Scores Don't Prove Impact",
         h1="Why Satisfaction Scores Don't Prove Impact",
         hero_sub="High satisfaction and zero measurable impact can coexist — satisfaction is worth tracking, but it answers a much narrower question than 'did this work.'",
         sections=[
             ("What satisfaction scores actually measure",
              ["A satisfaction score measures how participants felt about an intervention immediately afterwards — engagement, relevance, quality of delivery. It's a genuinely useful signal about delivery quality. It is not a measure of whether behaviour, performance or risk subsequently changed."]),
             ("Why high satisfaction and zero impact can coexist",
              ["People can enjoy an intervention, rate it highly, and return to exactly the same behaviour afterwards — enjoyment doesn't require change to have occurred. Satisfaction and impact are correlated in general, but weakly enough that one cannot substitute for the other in any specific case."]),
             ("The seduction of an easy positive number",
              ["Satisfaction scores are fast to collect and reliably positive, which makes them an attractive headline metric — especially compared with behaviour or results data, which take longer to gather and are less guaranteed to be favourable. That asymmetry is exactly why satisfaction gets over-reported relative to its actual evidential value."]),
             ("What to measure alongside satisfaction, not instead of it",
              ["Satisfaction remains worth tracking as a delivery-quality signal, alongside — never instead of — a measure of the actual outcome the intervention targeted. Reported together, satisfaction explains part of the story; reported alone, it's frequently mistaken for the whole of it."]),
         ],
         faqs=[
             ("Should satisfaction surveys be scrapped?", "No — they're a legitimate and useful measure of delivery quality. The issue is reporting them as if they answer the impact question, not their existence."),
             ("Can low satisfaction still coincide with real impact?", "Yes — content people found difficult or uncomfortable can still be exactly what changed behaviour, which is another reason satisfaction alone is a poor proxy for impact."),
             ("What's a better headline metric than satisfaction?", "Whatever specific outcome the intervention was funded to move — compliance gap closed, error rate reduced, time-to-competence — measured against a baseline, not a feelings-based proxy for it."),
         ],
         related_slug="learning-strategy", related_title="Learning Strategy service",
         related_reading=[
             ("Evaluating Learning Investment: The Complete Guide", "evaluating-learning-investment-complete-guide"),
             ("Kirkpatrick's Model in Practice: Strengths and Limitations", "kirkpatricks-model-in-practice"),
             ("Measuring ROI on Capability Investment for Board Reporting", "measuring-roi-capability-investment"),
         ]),
    dict(slug="performance-consulting-complete-guide", category="Performance", kind="Complete Guide",
         title="Performance Consulting: Diagnosing the Real Problem Before Prescribing Training",
         h1="Performance Consulting: Diagnosing the Real Problem Before Prescribing Training",
         hero_sub="Everything you need to know about performance consulting — diagnosing why performance is falling short before prescribing training, restructuring, or anything else.",
         sections=[
             ("What performance consulting actually is",
              ["Performance consulting is the discipline of diagnosing why organisational performance is falling short before recommending a fix — testing whether the cause is genuinely a skills gap, or something structural, rather than defaulting to whichever intervention is easiest to commission."]),
             ("The Training vs Capability Decision Model",
              ["The core diagnostic question is simple to state and easy to skip under pressure: is the knowledge or skill genuinely missing, or is something else — structure, governance, leadership, process — holding performance back? The dedicated article sets out how to apply this test properly."]),
             ("How to tell if your performance problem is really a training problem",
              ["Beyond the model itself, there are concrete signs that distinguish a genuine training gap from a structural one — evidence that's often available internally but rarely gathered before training gets commissioned. The dedicated article walks through what to look for."]),
             ("Performance consulting for the public sector",
              ["Public sector performance problems carry constraints private-sector diagnosis rarely has to account for — budget scrutiny, political visibility, and the requirement that recommendations survive audit, not just internal review. The dedicated article covers what's genuinely different."]),
             ("From training to readiness — measuring what matters",
              ["Diagnosis is only half the discipline; the other half is measuring the right outcome afterwards. The From Training to Readiness article covers why completion rates are the wrong headline metric, and what readiness actually looks like when it's measured properly."]),
             ("What this looks like in practice",
              ["The Operational Role Architecture Redesign (Op Isotrope) case study is direct evidence of performance consulting under the most extreme time pressure imaginable: role ambiguity, not individual skill or resource shortage, was the real drag on effectiveness. Clarifying roles — not training anyone further — improved response effectiveness by 15%, without additional headcount."]),
         ],
         faqs=[
             ("Is performance consulting the same as a Training Needs Analysis?", "Related but broader — a TNA specifically tests whether a gap is a training gap. Performance consulting is the wider diagnostic discipline that a TNA sits inside, applicable even where training was never seriously being considered as the answer."),
             ("Can performance consulting recommend no intervention at all?", "Yes, in principle — if performance is actually within acceptable bounds once measured properly, the honest finding is that no intervention is needed, which is itself valuable information."),
             ("How is this different from general management consulting?", "The specific focus here is the capability and training angle — testing whether a performance gap is a skills problem before it's treated as one, which general management consulting doesn't always distinguish clearly."),
             ("Where should we start if we're not sure whether our problem is training-related?", "With the Capability Readiness Review — it's built specifically to test across capability, leadership, process, governance, workforce and training before anything is prescribed."),
         ],
         related_slug="capability-readiness-review", related_title="Take the Capability Readiness Review",
         related_reading=[
             ("From Training to Readiness", "from-training-to-readiness"),
             ("The Training vs Capability Decision Model, Explained", "training-vs-capability-decision-model-explained"),
             ("How to Tell If Your Performance Problem Is Really a Training Problem", "is-your-performance-problem-really-a-training-problem"),
             ("Performance Consulting for the Public Sector: What's Different", "performance-consulting-public-sector"),
         ]),
    dict(slug="training-vs-capability-decision-model-explained", category="Performance",
         title="The Training vs Capability Decision Model, Explained",
         h1="The Training vs Capability Decision Model, Explained",
         hero_sub="One question decides whether a performance gap needs training or something structural — here's how to apply it properly.",
         sections=[
             ("The one question the model asks",
              ["The model reduces to a single test: is the knowledge or skill required to perform genuinely missing? Not 'would more training help' — almost anything can be marginally helped by more training — but whether its specific absence is what's actually causing the performance gap."]),
             ("If the answer is yes: it's a training problem",
              ["Where the required knowledge or skill genuinely doesn't exist yet, training is the correct intervention, and the next step is a proper Training Needs Analysis to define exactly what's needed and how to build it defensibly."]),
             ("If the answer is no: what it usually is instead",
              ["Where the skill or knowledge already exists but performance still falls short, the cause is usually structural: unclear roles, weak governance, a process working against the outcome, or leadership not creating the conditions for people to apply what they already know. None of these are fixed by more training, however well-intentioned."]),
             ("Using the model without overcomplicating it",
              ["The model is deliberately simple, and that's the point — it's meant to be applied quickly, before budget is committed, not turned into its own lengthy analytical exercise. Where the answer isn't obvious, that uncertainty itself is the signal to run a proper diagnostic, like the Capability Readiness Review, rather than guessing."]),
         ],
         faqs=[
             ("Can a performance gap be partly training and partly structural?", "Yes, and it's a common finding — the model doesn't require a single cause, only that each contributing cause is honestly tested rather than training being assumed as the whole answer by default."),
             ("Who should apply this test — L&D or the business?", "Ideally both together — L&D alone may be biased toward finding a training answer, and the business alone may lack the framework to test the alternative structural explanations systematically."),
             ("Does this model replace a Training Needs Analysis?", "No — it's the test that decides whether a TNA is the right next step at all, not a substitute for the analysis itself once training is confirmed as relevant."),
         ],
         related_slug="capability-readiness-review", related_title="Take the Capability Readiness Review",
         related_reading=[
             ("Performance Consulting: The Complete Guide", "performance-consulting-complete-guide"),
             ("How to Tell If Your Performance Problem Is Really a Training Problem", "is-your-performance-problem-really-a-training-problem"),
             ("From Training to Readiness", "from-training-to-readiness"),
         ]),
    dict(slug="is-your-performance-problem-really-a-training-problem", category="Performance",
         title="How to Tell If Your Performance Problem Is Really a Training Problem",
         h1="How to Tell If Your Performance Problem Is Really a Training Problem",
         hero_sub="Concrete signs that distinguish a genuine training gap from a structural one — evidence that's usually available internally but rarely gathered before training gets commissioned.",
         sections=[
             ("The test that actually answers this",
              ["The most reliable test asks whether people who clearly have the relevant knowledge or skill still underperform in the same role or conditions. If they do, the gap isn't training — something in the role, structure or governance is holding performance back regardless of individual capability."]),
             ("Signs it's genuinely a training gap",
              ["Consistent underperformance across people with varying experience levels, performance that improves markedly once specific instruction is given, and an absence of structural or governance red flags all point toward a genuine training gap."]),
             ("Signs it isn't",
              ["Experienced, clearly capable people underperforming in the same way, performance that doesn't move despite prior training investment, and visible confusion about roles, authority or expectations are all signs the real constraint sits outside training."]),
             ("What to do once you know",
              ["A confirmed training gap should move into a proper Training Needs Analysis. A confirmed structural gap should be redirected toward whichever area it actually sits in — governance, leadership, process or workforce — rather than being addressed with training as a default, lower-friction response."]),
         ],
         faqs=[
             ("What if we're still not sure after applying this test?", "That uncertainty is itself useful information — it's the signal to run a more structured diagnostic, such as the Capability Readiness Review, rather than defaulting to training because it's the easier decision."),
             ("Does prior training investment that didn't work prove it's not a training problem?", "It's a strong signal, though worth checking whether the prior training actually addressed the specific gap — the wrong training failing doesn't rule out the right training working."),
             ("Can this diagnosis be done without external help?", "Often yes, with honest internal evidence-gathering — the discipline matters more than who runs it, though independence can help where internal politics make an honest answer harder to reach."),
         ],
         related_slug="capability-readiness-review", related_title="Take the Capability Readiness Review",
         related_reading=[
             ("Performance Consulting: The Complete Guide", "performance-consulting-complete-guide"),
             ("The Training vs Capability Decision Model, Explained", "training-vs-capability-decision-model-explained"),
             ("Performance Consulting for the Public Sector: What's Different", "performance-consulting-public-sector"),
         ]),
    dict(slug="performance-consulting-public-sector", category="Performance",
         title="Performance Consulting for the Public Sector: What's Different",
         h1="Performance Consulting for the Public Sector: What's Different",
         hero_sub="The same diagnostic discipline applies, but public sector performance problems carry constraints private-sector consulting rarely has to account for.",
         sections=[
             ("The same diagnosis, different constraints",
              ["The underlying question — is this a training problem or something structural — doesn't change in the public sector. What changes is the environment the answer has to survive: budget scrutiny, political and reputational visibility, and audit requirements that private-sector diagnosis rarely faces in the same form."]),
             ("Why public sector recommendations need to survive scrutiny",
              ["A recommendation that can't be defended to a scrutiny committee or auditor, however sound the underlying diagnosis, doesn't survive contact with the public sector budget process. That makes the evidence base behind a diagnosis non-negotiable, not just good practice."]),
             ("Headcount thinking vs capability thinking",
              ["Under budget pressure, the public sector default is often to think in headcount — how many posts can be afforded — rather than in capability requirement and structure. Headcount thinking treats every role as interchangeable, which breaks down precisely when a genuine performance problem needs specific capability, not just bodies."]),
             ("What this looks like in practice",
              ["The Operational Role Architecture Redesign (Op Isotrope), delivered during a national crisis response, is the clearest example: role ambiguity, not headcount or individual skill, was the real drag on effectiveness. Clarity of role improved response effectiveness by 15% without any additional resource — exactly the kind of finding that needs to survive scrutiny, and did."]),
         ],
         faqs=[
             ("Does public sector performance consulting take longer because of scrutiny requirements?", "The diagnosis itself doesn't need to take longer, but the evidence base needs to be built to survive scrutiny from the outset, rather than assembled retroactively if challenged."),
             ("Can this approach reduce headcount, or is it purely about effectiveness?", "It can go either way — sometimes the finding is that existing headcount is misallocated rather than insufficient, which can reduce pressure for additional posts rather than increase it."),
             ("Does this apply equally to central government, local government and public bodies?", "Yes — the scrutiny and evidence requirements vary in form, but the underlying discipline of defensible, evidence-based diagnosis applies across all of them."),
         ],
         related_slug="capability-readiness-review", related_title="Take the Capability Readiness Review",
         related_reading=[
             ("Performance Consulting: The Complete Guide", "performance-consulting-complete-guide"),
             ("The Training vs Capability Decision Model, Explained", "training-vs-capability-decision-model-explained"),
             ("How to Tell If Your Performance Problem Is Really a Training Problem", "is-your-performance-problem-really-a-training-problem"),
         ]),
    dict(slug="defence-learning-capability-guide", category="Defence", kind="Complete Guide",
         title="Defence Learning and Capability: A Practical Guide for Programme Leaders",
         h1="Defence Learning and Capability: A Practical Guide for Programme Leaders",
         hero_sub="Everything Defence programme leaders need on training and capability — DSAT and JSP 822 in context, enterprise-wide capability analysis, front line TNA, and working with primes.",
         sections=[
             ("What Defence learning and capability programmes are actually managing",
              ["Defence learning and capability programmes sit at the intersection of operational requirement, assurance obligation and delivery constraint — rarely a simple training commission. Managing them well means holding all three at once: what capability the mission genuinely requires, what DSAT and JSP 822 require to make that defensible, and what's realistic to deliver against real operational tempo."]),
             ("DSAT and JSP 822, in context",
              ["DSAT and JSP 822 aren't paperwork layered on top of Defence training — they're the methodology and policy that make a training decision defensible under audit. The DSAT Explained article covers the full methodology; this guide focuses on what programme leaders specifically need to apply it well."]),
             ("Lessons from enterprise-wide capability analysis",
              ["The Digital Skills for Defence (DS4D) programme is the clearest evidence of what enterprise-wide capability analysis looks like done well — defining the digital capability requirement before commissioning any training, rather than the other way round. The dedicated article draws out the lessons that transfer to other large-scale Defence capability programmes."]),
             ("TNA for front line commands",
              ["Front line commands face constraints back-office TNA rarely has to account for — operational tempo, limited access windows, and evidence-gathering that can't wait for a quiet period. The dedicated article covers how to keep a TNA DSAT-defensible without it becoming a drag on operational readiness."]),
             ("Working with Defence primes on capability programmes",
              ["Where a prime contractor is delivering a programme, capability requirement ownership needs to stay with Defence, not be quietly absorbed into delivery. The dedicated article covers where this goes wrong and what good collaboration between Defence and prime actually looks like."]),
             ("What this looks like in practice",
              ["Across the case studies referenced on this site — DS4D, the Senior Information Officer Rapid TNA, and the NATO &amp; Royal Navy Training Modernisation programme — the common thread is the same: defining the real requirement first, and using DSAT as a decision framework rather than a process to endure, consistently outperforms starting from an assumed training solution."]),
         ],
         faqs=[
             ("Is this guide relevant outside the Ministry of Defence?", "The specific DSAT/JSP 822 content is MOD-specific, but the discipline of defining capability requirements before commissioning training transfers to NATO allies and other Defence-adjacent organisations facing similar assurance requirements."),
             ("How does this guide relate to the DSAT Explained article?", "DSAT Explained covers the methodology in full; this guide applies it specifically to programme leadership — enterprise-wide analysis, front line delivery, and working with primes."),
             ("Do all Defence learning programmes need to go through a prime contractor?", "No — many are delivered directly, but where a prime is involved, capability requirement ownership needs deliberate attention, which the dedicated article covers."),
             ("Where should a programme leader start if a Defence learning programme feels stalled?", "With whichever of the three dedicated articles below matches the stage the programme is at — enterprise-wide analysis, front line TNA, or the prime relationship."),
         ],
         related_slug="dsat-consultancy", related_title="DSAT Consultancy",
         related_reading=[
             ("DSAT Explained", "dsat-explained"),
             ("Digital Skills for Defence (DS4D): Lessons from Enterprise-Wide Capability Analysis", "digital-skills-for-defence-lessons"),
             ("Training Needs Analysis for Front Line Commands", "tna-for-front-line-commands"),
             ("Working with Defence Primes on Capability Programmes", "working-with-defence-primes-capability-programmes"),
         ]),
    dict(slug="digital-skills-for-defence-lessons", category="Defence",
         title="Digital Skills for Defence (DS4D): Lessons from Enterprise-Wide Capability Analysis",
         h1="Digital Skills for Defence (DS4D): Lessons from Enterprise-Wide Capability Analysis",
         hero_sub="What an enterprise-wide digital capability programme teaches about defining the requirement before commissioning any training.",
         sections=[
             ("What made DS4D an enterprise-wide problem, not a training problem",
              ["Digital Skills for Defence started life looking like a training commissioning question — which courses should be bought for which audiences. The real question underneath it was enterprise-wide: what digital capability did Defence actually need across the workforce, and what was the current state against that requirement? Answering the training question first would have meant guessing at the capability question."]),
             ("The mistake of commissioning courses against an undefined requirement",
              ["Commissioning digital training at enterprise scale without first defining the capability requirement risks spending heavily and still missing the mission — because the courses get selected against assumptions about what's needed, not evidence. That's precisely the risk this programme was designed to avoid."]),
             ("What changed once the capability requirement was defined",
              ["Once the digital capability requirement was defined against mission and outcomes, and skills, behaviours and workforce needs were mapped against it, learning architecture could be aligned to strategic outcomes rather than the other way round — and decision-makers had an evidence-based view to plan and defend investment, in place of a stalled twelve-month conversation resolved in ten weeks."]),
             ("Lessons that transfer to other enterprise-wide Defence programmes",
              ["The transferable lesson isn't specific to digital skills: define the capability requirement against mission and outcomes before designing the learning architecture, embed governance so decisions stay defensible, and treat the workforce and skills mapping as the foundation the learning design sits on, not an afterthought to it."]),
         ],
         faqs=[
             ("Was DS4D primarily a training procurement exercise?", "No — its core value came from capability requirement definition and workforce mapping; the resulting training and learning architecture followed from that work rather than preceding it."),
             ("How long did it take to move from stalled to resolved?", "The programme made progress in ten weeks that had stalled for twelve months, once the capability requirement was properly defined rather than assumed."),
             ("Does this approach apply to non-digital capability areas?", "Yes — the method of defining capability requirement before designing learning architecture applies to any large-scale Defence capability question, digital or otherwise."),
         ],
         related_slug="dsat-consultancy", related_title="DSAT Consultancy",
         related_reading=[
             ("Defence Learning and Capability: The Complete Guide", "defence-learning-capability-guide"),
             ("Training Needs Analysis for Front Line Commands", "tna-for-front-line-commands"),
             ("Learning Strategy: The Complete Guide", "learning-strategy-complete-guide"),
         ]),
    dict(slug="tna-for-front-line-commands", category="Defence",
         title="Training Needs Analysis for Front Line Commands",
         h1="Training Needs Analysis for Front Line Commands",
         hero_sub="Front line commands face constraints back-office TNA rarely has to account for — here's how to keep the analysis DSAT-defensible without it dragging on operational readiness.",
         sections=[
             ("Why front line TNA has different constraints than back-office TNA",
              ["A TNA run against a back-office function can draw on stable schedules, accessible stakeholders and time to gather evidence properly. Front line commands rarely offer any of that — operational tempo, deployment cycles and limited access windows mean the analysis has to be designed around constraints a back-office TNA never faces."]),
             ("Operational tempo vs analytical rigour",
              ["The temptation under operational tempo is to shortcut evidence-gathering entirely, producing a fast but indefensible analysis. The better approach scopes tightly — analysing the specific, highest-impact question rather than attempting comprehensive coverage — so rigour survives even where time doesn't allow for a lengthy process."]),
             ("What good evidence gathering looks like at the front line",
              ["Performance data, incident reports and structured observation captured opportunistically during existing operational windows — rather than requiring dedicated stand-alone sessions — tend to work better than an evidence-gathering plan that assumes front line personnel have spare capacity to give."]),
             ("Keeping DSAT-defensible under time pressure",
              ["Speed and DSAT-defensibility aren't in conflict when the analysis is scoped correctly — the Senior Information Officer Rapid TNA case study demonstrated this directly: the real constraint wasn't the methodology, it was unclear requirements, resolved quickly once the right, tightly-scoped questions were asked."]),
         ],
         faqs=[
             ("Can a front line TNA really be both fast and DSAT-defensible?", "Yes, provided it's scoped tightly to the specific question that matters most, rather than attempting comprehensive coverage under time pressure that was never available for it."),
             ("How should evidence be gathered without pulling personnel off task?", "By building evidence capture into existing operational windows and reporting — performance data and structured observation that's already happening, rather than requiring new dedicated sessions."),
             ("Does front line TNA require a different template from other Defence TNAs?", "Not a different template — the same DSAT-aligned structure applies, but the evidence-gathering approach needs to be realistic about front line access and tempo."),
         ],
         related_slug="dsat-consultancy", related_title="DSAT Consultancy",
         related_reading=[
             ("Defence Learning and Capability: The Complete Guide", "defence-learning-capability-guide"),
             ("How to Run a DSAT-Compliant TNA, Step by Step", "dsat-compliant-tna-step-by-step"),
             ("Working with Defence Primes on Capability Programmes", "working-with-defence-primes-capability-programmes"),
         ]),
    dict(slug="working-with-defence-primes-capability-programmes", category="Defence",
         title="Working with Defence Primes on Capability Programmes",
         h1="Working with Defence Primes on Capability Programmes",
         hero_sub="Where a prime contractor is delivering a programme, capability requirement ownership needs to stay with Defence — here's where that goes wrong, and what good collaboration looks like.",
         sections=[
             ("Where prime-led programmes typically underweight capability",
              ["Primes are typically measured on delivery milestones — systems built, training delivered, timelines met — which can quietly deprioritise the capability requirement itself, especially where that requirement was never clearly defined and owned before the prime was engaged."]),
             ("The interface between prime delivery and capability requirement ownership",
              ["The healthiest arrangement treats the prime as responsible for delivery against a capability requirement that Defence continues to own and can independently assess — rather than the requirement itself being defined, interpreted and effectively owned by the delivery organisation."]),
             ("Keeping capability requirements owned by Defence, not just delivered by the prime",
              ["Where Defence loses ownership of the capability requirement, evaluation of whether the programme actually succeeded ends up relying on the prime's own delivery metrics — measures that describe activity, not necessarily the capability outcome the programme was funded to achieve."]),
             ("What good collaboration looks like",
              ["Effective collaboration keeps the capability requirement, its evidence base and its evaluation criteria independently owned and understood by Defence, while the prime focuses on what it does well — delivery — against a requirement it didn't get to define alone."]),
         ],
         faqs=[
             ("Does this mean Defence should avoid using primes for capability programmes?", "No — primes bring genuine delivery capability. The point is ensuring the capability requirement itself stays independently owned and evaluated by Defence, not absorbed into delivery."),
             ("How early should Defence define the capability requirement relative to prime engagement?", "Ideally before the prime is engaged, or in close parallel — defining it after delivery has started risks the requirement being shaped by what's already being delivered, rather than the reverse."),
             ("Who should evaluate whether the programme actually achieved its capability outcome?", "Defence, using criteria defined independently of the prime's own delivery metrics — otherwise the evaluation risks measuring activity rather than the capability outcome that was funded."),
         ],
         related_slug="dsat-consultancy", related_title="DSAT Consultancy",
         related_reading=[
             ("Defence Learning and Capability: The Complete Guide", "defence-learning-capability-guide"),
             ("Digital Skills for Defence (DS4D): Lessons from Enterprise-Wide Capability Analysis", "digital-skills-for-defence-lessons"),
             ("Training Needs Analysis for Front Line Commands", "tna-for-front-line-commands"),
         ]),
    dict(slug="skills-frameworks-complete-guide", category="Skills", kind="Complete Guide",
         title="Skills Frameworks: Building Standards People Actually Use",
         h1="Skills Frameworks: Building Standards People Actually Use",
         hero_sub="Everything you need to know about skills frameworks — what they are, how they differ from capability frameworks, and how to build one people actually use.",
         sections=[
             ("What a skills framework actually is",
              ["A skills framework maps the specific skills required for particular roles — narrower and more operational than a capability framework, which sets the broader standard a role needs to meet. The dedicated article gives the full working definition and shows where each tool is the right one."]),
             ("How it differs from a capability framework",
              ["Skills frameworks and capability frameworks are frequently confused, but they answer different questions: a skills framework asks what specific skills a role requires; a capability framework asks whether the organisation as a whole can reliably deliver against a standard. Used together, they're powerful — used interchangeably, they cause real confusion in assessment and workforce planning."]),
             ("Mapping skills to roles across multiple specialisations",
              ["Organisations with several specialisations or role types often end up with skills maps that don't compare across teams, because each was built locally. The dedicated article covers how to build a mapping that's genuinely comparable across specialisations without flattening real differences between them."]),
             ("Skills frameworks for workforce planning and succession",
              ["A skills framework only earns its keep once it's actually used for workforce planning and succession — identifying gaps against future need, not just assessing current performance. The dedicated article covers how to make that connection real rather than aspirational."]),
             ("Where apprenticeships fit in",
              ["Apprenticeship programmes are one of the clearest places a skills framework proves its worth — giving structure to what 'progressing' actually means and evidence for funding compliance. The Apprenticeship Success Strategies article covers what drove 95% completion and 100% funding compliance on one such programme."]),
             ("What this looks like in practice",
              ["The Defence Apprenticeship Success Programme is direct evidence: coaching, active progress management and structured development pathways — underpinned by clear skills standards — achieved 95% completion and 100% funding compliance, not through a change in course content but through giving progression a clear, trackable structure."]),
         ],
         faqs=[
             ("Do we need both a skills framework and a capability framework?", "Often, yes — they serve different purposes and work well together, with the skills framework providing the operational detail underneath the capability framework's broader standard."),
             ("Is a skills framework the same as a skills matrix?", "A skills matrix is typically a tracking tool showing who has which skills. A skills framework defines the standard being tracked against in the first place — the matrix sits on top of it."),
             ("How often does a skills framework need updating?", "Whenever roles or the operating model change meaningfully — a framework built against roles that have since evolved will lose accuracy and usefulness quickly."),
             ("Where should we start if we don't have a skills framework yet?", "With the dedicated definition article below, then the mapping article if multiple specialisations are involved — building a lightweight version for a handful of critical roles is a reasonable starting point."),
         ],
         related_slug="capability-framework-design", related_title="Capability Framework Design service",
         related_reading=[
             ("What Is a Skills Framework? And How It Differs from a Capability Framework", "what-is-a-skills-framework"),
             ("Apprenticeship Success Strategies", "apprenticeship-success-strategies"),
             ("Mapping Skills to Roles Across Multiple Specialisations", "mapping-skills-to-roles-multiple-specialisations"),
             ("Skills Frameworks for Workforce Planning and Succession", "skills-frameworks-workforce-planning-succession"),
         ]),
    dict(slug="what-is-a-skills-framework", category="Skills",
         title="What Is a Skills Framework? And How It Differs from a Capability Framework",
         h1="What Is a Skills Framework? And How It Differs from a Capability Framework",
         hero_sub="The two terms get used interchangeably, but they answer different questions — and knowing which one you need matters.",
         sections=[
             ("A working definition",
              ["A skills framework maps the specific skills required for particular roles — a practical, operational tool for assessing what someone can currently do against what a role needs, and for planning how to close the gap."]),
             ("Skills framework vs capability framework",
              ["A capability framework sets the broader standard of competence a role or specialisation needs to meet, used consistently across assessors. A skills framework operates one level more granular — the specific skills that, together, add up to meeting that broader standard."]),
             ("Where each is the right tool",
              ["When the question is 'does this organisation reliably deliver the outcome required,' a capability framework is the right tool. When the question is 'what specific skills does this person or role have, and what's missing,' a skills framework answers it more directly and operationally."]),
             ("Using both together",
              ["Used together, a capability framework sets the standard and a skills framework provides the granular detail for assessing progress toward it — which is what makes workforce planning and succession genuinely actionable, rather than aspirational."]),
         ],
         faqs=[
             ("Can an organisation have a skills framework without a capability framework?", "Yes, particularly for narrower operational purposes — but without the broader capability framework, it's harder to ensure consistency in what 'meeting the standard' actually means across the organisation."),
             ("Which should be built first?", "Generally the capability framework, since it defines the standard the skills framework's detail should map against — though a lightweight skills map can also surface what the capability framework needs to cover."),
             ("Is 'skills matrix' the same thing as a skills framework?", "A skills matrix is usually the tracking tool that sits on top of a skills framework, showing who currently has which skills — the framework itself defines what's being tracked."),
         ],
         related_slug="capability-framework-design", related_title="Capability Framework Design service",
         related_reading=[
             ("Skills Frameworks: The Complete Guide", "skills-frameworks-complete-guide"),
             ("Capability vs Competency: Are They the Same Thing?", "capability-vs-competency-explained"),
             ("Mapping Skills to Roles Across Multiple Specialisations", "mapping-skills-to-roles-multiple-specialisations"),
         ]),
    dict(slug="mapping-skills-to-roles-multiple-specialisations", category="Skills",
         title="Mapping Skills to Roles Across Multiple Specialisations",
         h1="Mapping Skills to Roles Across Multiple Specialisations",
         hero_sub="Skills maps built locally, specialisation by specialisation, rarely compare with each other — here's how to build one that does.",
         sections=[
             ("The mapping problem multiple specialisations create",
              ["Where each specialisation builds its own skills map independently, the results rarely compare — the same skill might be named differently, assessed at different thresholds, or simply not mapped consistently, making cross-specialisation workforce planning close to impossible."]),
             ("Building a map that's comparable across specialisations",
              ["A comparable map requires deliberately separating skills that are genuinely common across specialisations from those that are specialisation-specific, and defining both using consistent language and assessment thresholds, rather than letting each specialisation invent its own."]),
             ("Keeping it usable, not just comprehensive",
              ["A skills map that tries to capture every possible skill in exhaustive detail tends to become too unwieldy for managers to actually use for assessment or planning. The more valuable map is comprehensive enough to be accurate and simple enough to be used consistently."]),
             ("What good looks like",
              ["A working multi-specialisation skills map lets workforce planners compare readiness across specialisations meaningfully — the same underlying discipline behind the Defence Capability Framework Design case study, which made cross-specialisation workforce planning possible for the first time by mapping common ground while preserving genuine differences."]),
         ],
         faqs=[
             ("How many specialisations justify building a shared skills map?", "There's no fixed threshold — the signal is inconsistent local mapping that's already making cross-specialisation comparison difficult, which can show up with just two or three specialisations."),
             ("Does a shared map erase genuine differences between specialisations?", "It shouldn't — the goal is separating common ground from genuine specialisation-specific skills, not flattening everything into a single generic list."),
             ("Who should be involved in building a multi-specialisation map?", "Representatives from each specialisation, to ensure genuine differences are correctly captured rather than assumed by whoever leads the mapping exercise centrally."),
         ],
         related_slug="capability-framework-design", related_title="Capability Framework Design service",
         related_reading=[
             ("Skills Frameworks: The Complete Guide", "skills-frameworks-complete-guide"),
             ("Multi-Specialisation Capability Frameworks Explained", "multi-specialisation-capability-frameworks"),
             ("Skills Frameworks for Workforce Planning and Succession", "skills-frameworks-workforce-planning-succession"),
         ]),
    dict(slug="skills-frameworks-workforce-planning-succession", category="Skills",
         title="Skills Frameworks for Workforce Planning and Succession",
         h1="Skills Frameworks for Workforce Planning and Succession",
         hero_sub="A skills framework only earns its keep once it's actually used for workforce planning and succession — here's how to make that connection real.",
         sections=[
             ("Why workforce planning needs a skills framework underneath it",
              ["Workforce planning that isn't grounded in a defined skills framework tends to default to headcount thinking — how many people, rather than what skills — which breaks down exactly when a genuine skills gap needs to be closed, not just a body count filled."]),
             ("Using the framework for succession, not just assessment",
              ["A skills framework used only for current-state assessment misses half its value. Applied to succession, it identifies specifically what a potential successor still needs to develop against a defined role's requirements — turning succession planning from a subjective judgement call into an evidenced development plan."]),
             ("Keeping the framework current as roles change",
              ["A skills framework tied to roles that have since evolved loses accuracy quickly, and workforce plans built on a stale framework inherit that inaccuracy. Reviewing the framework whenever roles or the operating model shift meaningfully keeps workforce planning and succession decisions genuinely evidence-based."]),
             ("What this looks like in practice",
              ["Succession planning built on a current, well-used skills framework can identify a shortfall — and the specific development needed to close it — well before a vacancy forces a decision, which is the entire point of doing succession planning deliberately rather than reactively."]),
         ],
         faqs=[
             ("Can workforce planning work without a formal skills framework?", "It can work at a basic level, but tends to default to headcount thinking without a framework defining what skills actually matter — which limits how precisely gaps can be identified and closed."),
             ("How does this connect to succession planning for critical roles?", "Directly — a skills framework gives succession planning its evidence base, turning 'who might be ready' into a specific, developable gap against a defined standard."),
             ("How often should workforce plans be revisited against the framework?", "At minimum whenever the framework itself is reviewed, and additionally whenever significant workforce changes — restructuring, new specialisations — occur."),
         ],
         related_slug="workforce-planning", related_title="Workforce Planning service",
         related_reading=[
             ("Skills Frameworks: The Complete Guide", "skills-frameworks-complete-guide"),
             ("Succession Planning for Critical Roles", "succession-planning-critical-roles"),
             ("Mapping Skills to Roles Across Multiple Specialisations", "mapping-skills-to-roles-multiple-specialisations"),
         ]),
    dict(slug="learning-technology-complete-guide", category="Technology", kind="Complete Guide",
         title="Learning Technology: Getting Value from Your LMS",
         h1="Learning Technology: Getting Value from Your LMS",
         hero_sub="Everything you need to know about getting real value from your LMS — what it is, what it can't do, choosing a platform, and building dashboards leaders actually trust.",
         sections=[
             ("What an LMS is actually for",
              ["An LMS is the platform used to deliver, track and report on training — it produces data by default, but data isn't the same as trustworthy reporting or genuine capability. The dedicated article gives the full working definition and covers what an LMS can't do for you, however well it's configured."]),
             ("Why re-platforming is usually the wrong first move",
              ["The default response to a frustrating LMS is often to replace it — but a new platform inherits the same configuration and information management problems unless those are fixed first. Testing whether the current platform has ever been properly configured for actual reporting and pathway needs usually comes before any replacement decision."]),
             ("Totara vs off-the-shelf platforms",
              ["Where a platform decision genuinely is needed, the choice between something like Totara and an off-the-shelf alternative comes down to how much configuration flexibility your reporting and pathway needs actually require — not brand preference. The dedicated article covers what to weigh."]),
             ("Building dashboards leaders actually trust",
              ["An LMS's default reports rarely earn the confidence needed to put a number in a board report unchecked. Building dashboards leaders actually trust is a deliberate design exercise, not a platform feature — the dedicated article covers how to do it properly."]),
             ("Adoption is the real project, not the platform",
              ["Whether you configure an existing platform or genuinely need a new one, the harder and more important project is adoption — making sure managers, learners and administrators actually use the system as intended, week after week, not just during launch."]),
             ("What this looks like in practice",
              ["The Healthcare Learning Transformation case study cut compliance gaps by 18% largely through configuration, dashboard redesign and information management on an existing Totara platform — proof that most LMS value comes from how a platform is used, not which platform is chosen."]),
         ],
         faqs=[
             ("How do we know if our problem is the platform or the configuration?", "Test whether current reporting is trustworthy and whether pathways match how people actually work — if not, that's usually a configuration and information management gap, fixable without replacing the platform."),
             ("Does this guide apply to LMS platforms other than Totara?", "Yes — Totara features in the case studies referenced here, but the underlying discipline of configuration, dashboard design and information management transfers to most modern LMS platforms."),
             ("How long does an LMS optimisation project typically take compared to a re-platform?", "A focused configuration and dashboard project is typically a matter of months; a full re-platform is a much longer, higher-risk undertaking — which is exactly why it's worth ruling out the cheaper fix first."),
             ("Where should we start if our LMS currently feels like it's underdelivering?", "With the dashboard article below if reporting is the pain point, or the platform comparison article if a genuine replacement decision is on the table — re-platforming should be the last resort, not the first response."),
         ],
         related_slug="lms-optimisation", related_title="LMS Optimisation service",
         related_reading=[
             ("Learning Technology Lessons", "learning-technology-lessons"),
             ("What Is an LMS? And What It Can't Do for You", "what-is-an-lms"),
             ("Totara vs Off-the-Shelf LMS Platforms: What to Consider", "totara-vs-off-the-shelf-lms"),
             ("Building Dashboards Leaders Actually Trust", "building-dashboards-leaders-trust"),
         ]),
    dict(slug="what-is-an-lms", category="Technology",
         title="What Is an LMS? And What It Can't Do for You",
         h1="What Is an LMS? And What It Can't Do for You",
         hero_sub="An LMS is the platform, not the strategy — understanding what it genuinely can and can't do prevents a lot of wasted procurement.",
         sections=[
             ("A working definition",
              ["A Learning Management System is the platform used to deliver, track and report on training — assigning content, recording completion, and generating data on activity across an organisation's learners."]),
             ("What an LMS does well",
              ["An LMS is genuinely good at consistent delivery, automated tracking, and generating raw activity data at scale — things that would be impractical to do manually across any meaningfully sized workforce."]),
             ("What it can't do — and what people mistakenly expect it to",
              ["An LMS can't define what capability an organisation actually needs, can't guarantee behaviour changes because content was completed, and can't produce trustworthy board-level reporting without deliberate dashboard design layered on top of its raw data. Expecting the platform itself to solve these is where many LMS investments disappoint."]),
             ("Where the real value comes from",
              ["The real value of an LMS comes from what's built around it — configuration matched to genuine reporting and pathway needs, dashboards designed around what leaders actually need to see, and adoption sustained well past launch. The platform is necessary infrastructure, not the strategy itself."]),
         ],
         faqs=[
             ("Is a more expensive LMS automatically better?", "Not necessarily — cost doesn't predict whether a platform will be configured and adopted well, which is where most of the real value or disappointment comes from."),
             ("Can an LMS replace the need for a learning strategy?", "No — the platform delivers and tracks whatever strategy defines, but doesn't generate the strategy itself. See the Learning Strategy guide for that separate discipline."),
             ("Why do LMS rollouts so often disappoint despite a good platform choice?", "Because the platform was expected to solve problems — configuration, dashboard trust, adoption — that require deliberate design work the platform itself doesn't provide automatically."),
         ],
         related_slug="lms-optimisation", related_title="LMS Optimisation service",
         related_reading=[
             ("Learning Technology: The Complete Guide", "learning-technology-complete-guide"),
             ("Learning Technology Lessons", "learning-technology-lessons"),
             ("Building Dashboards Leaders Actually Trust", "building-dashboards-leaders-trust"),
         ]),
    dict(slug="totara-vs-off-the-shelf-lms", category="Technology",
         title="Totara vs Off-the-Shelf LMS Platforms: What to Consider",
         h1="Totara vs Off-the-Shelf LMS Platforms: What to Consider",
         hero_sub="The right platform choice comes down to how much configuration flexibility your reporting and pathway needs actually require — not brand preference.",
         sections=[
             ("What actually differs between platforms",
              ["The meaningful differences between LMS platforms are configuration flexibility, reporting depth, and how well the platform can be adapted to genuinely unusual compliance or pathway requirements — not surface-level features that most platforms now offer in some form."]),
             ("Where Totara's flexibility earns its complexity",
              ["Totara's open-source, highly configurable architecture earns its additional complexity where compliance reporting or pathway requirements are genuinely unusual — which is common across healthcare and public sector organisations with specific regulatory reporting needs."]),
             ("Where an off-the-shelf platform is the better choice",
              ["Where requirements are closer to standard — conventional compliance tracking, common pathway structures — an off-the-shelf platform with lower configuration overhead can deliver equivalent value with less implementation complexity and ongoing maintenance burden."]),
             ("Making the decision based on your reporting and pathway needs, not brand",
              ["The right starting point for this decision is a clear-eyed audit of what your actual reporting and pathway requirements are, tested against what each platform can deliver out of the box versus what would need custom configuration — not which platform is best-known or most recently reviewed favourably."]),
         ],
         faqs=[
             ("Is Totara always the better choice for regulated sectors?", "Often a strong fit given its configuration flexibility, but 'regulated sector' alone isn't sufficient justification — the decision should rest on your specific reporting and pathway requirements."),
             ("How much does implementation complexity differ between platform types?", "Generally, more configurable platforms require more upfront implementation effort in exchange for closer fit to unusual requirements — a genuine trade-off, not a free upgrade."),
             ("Can we switch from an off-the-shelf platform to Totara later if needs become more complex?", "Yes, though migration has its own cost and disruption — which is why it's worth being realistic about likely future reporting complexity at the outset, not just current needs."),
         ],
         related_slug="lms-optimisation", related_title="LMS Optimisation service",
         related_reading=[
             ("Learning Technology: The Complete Guide", "learning-technology-complete-guide"),
             ("What Is an LMS? And What It Can't Do for You", "what-is-an-lms"),
             ("Learning Technology Lessons", "learning-technology-lessons"),
         ]),
    dict(slug="building-dashboards-leaders-trust", category="Technology",
         title="Building Dashboards Leaders Actually Trust",
         h1="Building Dashboards Leaders Actually Trust",
         hero_sub="A dashboard leaders trust enough to put in a board report unchecked is a design exercise, not a platform feature.",
         sections=[
             ("Why default platform reports don't earn trust",
              ["Most LMS platforms generate reports by default, but those reports are built around what the platform tracks easily, not around what a specific leader needs to know to make a decision. That mismatch is why default reports are often technically accurate but practically unused."]),
             ("Designing around what leaders actually need to see",
              ["Trustworthy dashboard design starts with the decision the dashboard is meant to support — compliance risk, readiness, budget justification — and works backwards to the specific metrics that answer it, rather than starting from whatever data the platform makes easiest to display."]),
             ("The credibility test",
              ["A dashboard earns credibility when a leader can trace a headline number back to its underlying source and method without needing to ask someone to check it first. Dashboards that require regular caveats or manual verification before use haven't yet earned that trust, however sophisticated they look."]),
             ("What this looks like in practice",
              ["The Healthcare Learning Transformation case study cut compliance gaps by 18% largely because dashboards were redesigned around what leaders actually needed to see and trust — not around what the platform generated by default. That redesign, not a platform change, was where the value came from."]),
         ],
         faqs=[
             ("How many metrics should a leadership dashboard show?", "As few as answer the specific decision it's meant to support — a dashboard trying to show everything tends to be trusted less than one that shows the right few things clearly."),
             ("Who should be involved in designing a trustworthy dashboard?", "The leaders who'll actually use it, from the start — a dashboard designed in isolation by the platform administrator tends to reflect what's easy to build, not what's actually needed."),
             ("Does dashboard redesign require new software?", "Not necessarily — much of the value in the Healthcare Learning Transformation case study came from redesigning what an existing platform already generated, not from new tooling."),
         ],
         related_slug="lms-optimisation", related_title="LMS Optimisation service",
         related_reading=[
             ("Learning Technology: The Complete Guide", "learning-technology-complete-guide"),
             ("What Is an LMS? And What It Can't Do for You", "what-is-an-lms"),
             ("Totara vs Off-the-Shelf LMS Platforms: What to Consider", "totara-vs-off-the-shelf-lms"),
         ]),
    dict(slug="organisational-change-capability-complete-guide", category="Change", kind="Complete Guide",
         title="Building Capability Into Organisational Change and Transformation",
         h1="Building Capability Into Organisational Change and Transformation",
         hero_sub="Everything you need to know about building capability into organisational change — role architecture, why transformation stalls after go-live, and where change management and capability building overlap.",
         sections=[
             ("Why organisational change needs capability building, not just change management",
              ["Change management handles the human and structural side of transformation — communication, adoption, sequencing. It doesn't, on its own, ensure the organisation actually has the capability to operate under the new structure once the change lands. Transformation that manages the change well but skips capability building tends to look successful at go-live and struggle soon after."]),
             ("Role architecture redesign during rapid scaling or crisis",
              ["Role clarity is often the first thing to break down under rapid scaling or crisis conditions — not because people lack skill, but because who does what, with what authority, stops being clear exactly when clarity matters most. The dedicated article covers how to redesign role architecture under genuine time pressure."]),
             ("Why transformation programmes stall after go-live",
              ["Go-live is a milestone, not a finish line, and many transformation programmes that look successful on launch day stall within months. The dedicated article covers what actually causes the stall and how to design against it from the start."]),
             ("Change management vs capability building",
              ["The two disciplines overlap but aren't substitutes — change management without capability building often produces a workforce that's been communicated with well but still can't operate the new model; capability building without change management can produce a technically capable workforce that never adopts the change. The dedicated article covers where each is needed and how to sequence them."]),
             ("Public sector constraints on transformation",
              ["Public sector transformation carries constraints — budget scrutiny, political visibility, defensibility to auditors — that shape how both change management and capability building need to be applied. The Public Sector Workforce Development article covers what's genuinely different."]),
             ("What this looks like in practice",
              ["The Operational Role Architecture Redesign (Op Isotrope), delivered during a national crisis response, is direct evidence: role ambiguity, not skill or headcount, was the real drag on effectiveness. Clarifying roles improved response effectiveness by 15%, without additional resource — exactly the kind of capability-building work that has to sit alongside change management, not be replaced by it."]),
         ],
         faqs=[
             ("Is change management unnecessary if capability building is done well?", "No — both are needed. Capability building without change management risks a technically capable workforce that never adopts the new way of working."),
             ("How soon after go-live should we expect problems if capability wasn't built in?", "Often within weeks to a few months — the dedicated article on post-go-live stalling covers the specific pattern and how to catch it early."),
             ("Does role architecture redesign only apply during a crisis?", "No — the discipline applies to any period of rapid scaling or restructuring, though crisis conditions make the cost of role ambiguity most visible."),
             ("Where should we start if a transformation programme already feels stalled?", "With the post-go-live stalling article — most stalls trace back to a specific, identifiable gap rather than a general loss of momentum."),
         ],
         related_slug="workforce-planning", related_title="Workforce Planning service",
         related_reading=[
             ("Public Sector Workforce Development", "public-sector-workforce-development"),
             ("Role Architecture Redesign During Rapid Scaling or Crisis Response", "role-architecture-redesign-rapid-scaling-crisis"),
             ("Why Transformation Programmes Stall After Go-Live", "why-transformation-programmes-stall-after-go-live"),
             ("Change Management vs Capability Building: Where They Overlap", "change-management-vs-capability-building"),
         ]),
    dict(slug="role-architecture-redesign-rapid-scaling-crisis", category="Change",
         title="Role Architecture Redesign During Rapid Scaling or Crisis Response",
         h1="Role Architecture Redesign During Rapid Scaling or Crisis Response",
         hero_sub="Role clarity is often the first thing to break down under rapid scaling or crisis conditions — here's how to redesign it under genuine time pressure.",
         sections=[
             ("Why role architecture breaks first under rapid scaling or crisis",
              ["Under stable conditions, role ambiguity is an inconvenience that gets worked around informally. Under rapid scaling or crisis conditions, there's no time for informal workarounds — unclear authority and overlapping responsibility show up immediately as delay, duplicated effort or dropped accountability."]),
             ("The redesign discipline under time pressure",
              ["Role architecture redesign under pressure has to be faster and more targeted than a standard organisational design exercise — focused on who has authority for the highest-stakes decisions first, rather than attempting a comprehensive redesign of every role simultaneously."]),
             ("What good role clarity delivers operationally",
              ["Clear role architecture doesn't add capability that wasn't already there — it removes the friction and hesitation caused by not knowing who's authorised to act. That's often enough, on its own, to materially improve effectiveness without any additional headcount or skill."]),
             ("Proof it works",
              ["The Operational Role Architecture Redesign (Op Isotrope), delivered during a national crisis response, is direct evidence: role ambiguity, not individual skill or resource shortage, was the biggest drag on effectiveness. Clarifying roles improved response effectiveness by 15%, without requiring additional headcount."]),
         ],
         faqs=[
             ("How fast can a role architecture redesign realistically happen under crisis conditions?", "The Op Isotrope programme demonstrated meaningful improvement is achievable quickly when the redesign is tightly scoped to the highest-stakes decisions first, rather than attempting comprehensive coverage."),
             ("Does this require formal organisational design expertise?", "It helps, but the core discipline — identifying where authority is genuinely unclear and resolving it deliberately — can be applied by experienced operational leaders under the right facilitation."),
             ("Is this only relevant during an actual crisis?", "No — the same discipline applies to any period of rapid scaling, though crisis conditions make the cost of role ambiguity most visible and urgent to fix."),
         ],
         related_slug="workforce-planning", related_title="Workforce Planning service",
         related_reading=[
             ("Building Capability Into Organisational Change: The Complete Guide", "organisational-change-capability-complete-guide"),
             ("Public Sector Workforce Development", "public-sector-workforce-development"),
             ("Why Transformation Programmes Stall After Go-Live", "why-transformation-programmes-stall-after-go-live"),
         ]),
    dict(slug="why-transformation-programmes-stall-after-go-live", category="Change",
         title="Why Transformation Programmes Stall After Go-Live",
         h1="Why Transformation Programmes Stall After Go-Live",
         hero_sub="Go-live is a milestone, not the finish line — many transformation programmes that look successful on launch day stall within months.",
         sections=[
             ("Go-live is a milestone, not the finish line",
              ["Programme teams and leadership attention both tend to peak around go-live, then disperse quickly afterwards — precisely when the new model needs the most reinforcement to bed in. Treating go-live as the finish line, rather than the start of the hardest phase, is where many transformations begin to unravel."]),
             ("What actually causes post-go-live stall",
              ["The common causes are consistent: capability that was assumed rather than actually built before launch, reinforcement and support that disappears once the programme team disbands, and a new structure that technically exists but that people quietly revert away from under pressure to deliver."]),
             ("Designing for the months after go-live",
              ["Programmes that sustain change design explicitly for the post-go-live period — sustained reinforcement, a defined point at which the programme team hands over to business-as-usual ownership, and monitoring that catches reversion early rather than discovering it months later."]),
             ("What good looks like",
              ["Sustained transformation treats capability building and change management as running through go-live, not stopping at it — the same discipline behind the Op Isotrope example, where clarity of role had to actually hold under continued operational pressure, not just look right on the day it was announced."]),
         ],
         faqs=[
             ("How long after go-live should reinforcement continue?", "Long enough to see the new model survive a genuine period of operational pressure, not just an initial calm period — this varies by context but is typically months, not weeks."),
             ("What's the earliest warning sign of post-go-live stall?", "Quiet reversion to old ways of working under pressure to deliver, often before it's formally reported — active monitoring for this in the weeks after go-live catches it earliest."),
             ("Whose responsibility is it to prevent stalling after the programme team disbands?", "This needs deciding explicitly before go-live — a defined business-as-usual owner, not an assumption that the new model will simply sustain itself."),
         ],
         related_slug="workforce-planning", related_title="Workforce Planning service",
         related_reading=[
             ("Building Capability Into Organisational Change: The Complete Guide", "organisational-change-capability-complete-guide"),
             ("Role Architecture Redesign During Rapid Scaling or Crisis Response", "role-architecture-redesign-rapid-scaling-crisis"),
             ("Change Management vs Capability Building: Where They Overlap", "change-management-vs-capability-building"),
         ]),
    dict(slug="change-management-vs-capability-building", category="Change",
         title="Change Management vs Capability Building: Where They Overlap",
         h1="Change Management vs Capability Building: Where They Overlap",
         hero_sub="The two disciplines overlap but aren't substitutes — knowing where each is needed prevents transformation that manages the change well but can't actually operate the new model.",
         sections=[
             ("What each discipline actually does",
              ["Change management handles the human and structural side of transformation — communication, adoption, sequencing, managing resistance. Capability building ensures the organisation can actually operate under the new structure once the change lands — the skills, governance, and standards required to deliver against it."]),
             ("Where they need each other",
              ["A well-communicated, well-sequenced change that lands on an organisation lacking the capability to operate the new model will produce compliance without competence — people doing what they're told, without being genuinely equipped to do it well. Capability building without change management risks the reverse: a capable workforce that resists or reverts because the change itself was poorly managed."]),
             ("What happens when only one is applied",
              ["Change management alone tends to produce transformations that look successful at go-live and struggle within months, once the gap between the new structure's requirements and the workforce's actual capability becomes visible under real operating pressure. Capability building alone tends to produce resistance and slow adoption, because the human side of the change was never properly managed."]),
             ("Sequencing both properly",
              ["The more reliable sequence builds required capability in parallel with, not after, the change management workstream — so that by go-live, the workforce is both willing and actually able to operate the new model, rather than one lagging behind the other."]),
         ],
         faqs=[
             ("Which should be planned first?", "Neither in isolation — they need to be planned together from the outset, since sequencing one without the other is exactly what causes the gaps this article covers."),
             ("Can a small transformation skip formal capability building?", "Scale the effort to the transformation's size, not the discipline — even a lightweight capability check before go-live catches gaps that pure change management wouldn't surface."),
             ("How do we know if we've under-invested in capability building relative to change management?", "A workforce that says the right things about the new model but struggles to actually operate it under pressure is the clearest sign — that gap is capability, not communication."),
         ],
         related_slug="workforce-planning", related_title="Workforce Planning service",
         related_reading=[
             ("Building Capability Into Organisational Change: The Complete Guide", "organisational-change-capability-complete-guide"),
             ("Why Transformation Programmes Stall After Go-Live", "why-transformation-programmes-stall-after-go-live"),
             ("Role Architecture Redesign During Rapid Scaling or Crisis Response", "role-architecture-redesign-rapid-scaling-crisis"),
         ]),
]

for _art in INSIGHTS_FULL:
    insight_article_page(_art["slug"], _art["category"], _art["title"], _art["h1"], _art["hero_sub"],
                          _art["sections"], _art["faqs"], _art["related_slug"], _art["related_title"],
                          kind=_art.get("kind", "Insight"), related_reading=_art.get("related_reading"))

# ================================================================== INSIGHTS
RES = [
    ("assets/icons/insight.svg", "The Capability Readiness Playbook&trade;", "Our consultancy-grade guide: the Prelude Capability Model&trade;, the Capability Readiness Review&trade;, common capability mistakes and the diagnostic questions we use."),
    ("assets/icons/readiness.svg", "Capability Readiness Review", "The full ten-point diagnostic as a printable workbook — with scoring and guidance to find the real problem."),
    ("assets/icons/assurance.svg", "Defence Training Needs Analysis Checklist", "A practical checklist for running a DSAT-aligned TNA that finds the real gap, not just the symptom."),
    ("assets/icons/governance.svg", "Learning Governance Health Check", "Twelve questions to test whether your training governance would stand up to audit."),
    ("assets/icons/capability.svg", "Workforce Capability Assessment", "A structured way to map workforce capability against what the mission actually demands."),
]
res_cards = ""
for ic, t, d in RES:
    res_cards += f'''      <div class="resource reveal"><img class="r-ic" src="{ic}" alt=""><div class="r-body"><span class="gated">Free · email required</span><h3>{t}</h3><p>{d}</p><a class="read" href="#get-resources">Request this resource →</a></div></div>
'''
_res_opts = "".join(f"<option>{t}</option>" for _, t, _ in RES)
insights_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">Insights &amp; Resources</div>
    <h1 class="reveal in" data-d="1">Practical tools, not just opinions.</h1>
    <p class="hero-sub reveal in" data-d="2">Download diagnostics and templates you can use today — and read plain-English thinking on the problems Defence and public sector leaders actually face.</p>
  </div>
</header>

<div class="divider"></div>

<section style="padding-top:64px">
  <div class="wrap">
    <div class="eyebrow reveal">Free resources</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Diagnostics and templates to get you started.</p>
    <div class="resource-grid">
{res_cards}    </div>
    <div class="capture reveal" id="get-resources">
      <div class="capture-copy">
        <h3>Get the resource</h3>
        <p class="muted">Tell me where to send it. You'll get the resource by email, plus the occasional practical note on capability and readiness — no spam, unsubscribe anytime.</p>
      </div>
      <form class="capture-form" action="https://formspree.io/f/xeeyazed" method="POST">
        <input type="hidden" name="_subject" value="Prelude website: Resource request">
        <input type="hidden" name="_next" value="{SITE_URL}/thank-you.html?from=resource">
        <div class="field"><label for="r-resource">Resource</label><select id="r-resource" name="resource">{_res_opts}</select></div>
        <div class="field"><label for="r-email">Work email</label><input id="r-email" name="email" type="email" required placeholder="you@organisation.gov.uk"><span class="field-error">Please enter a valid email address.</span></div>
        <button type="submit" class="btn btn-primary">Send it to me {ARROW}</button>
      </form>
    </div>
  </div>
</section>

<div class="divider"></div>

<section style="padding-top:30px">
  <div class="wrap">
    <div class="eyebrow reveal">Featured</div>
    <article class="featured-insight reveal" data-d="1">
      <div>
        <span class="ic-cat">Manifesto</span>
        <h2>Why Training Isn't the Problem</h2>
        <p>Most failed "training" was never a training problem. The course did its job; the capability gap sat somewhere else — in unclear roles, weak governance, missing pathways or standards no one agreed on.</p>
        <p>This is the idea behind everything I do: training is rarely the problem — capability is. Diagnosis has to come before prescription.</p>
        <a class="read" href="why-training-isnt-the-problem.html">Read the manifesto →</a>
      </div>
      <div class="fi-visual"><img src="assets/icons/capability.svg" alt=""></div>
    </article>
  </div>
</section>

<section style="padding-top:30px">
  <div class="wrap">
    <article class="featured-insight reveal" data-d="1">
      <div>
        <span class="ic-cat">Reference</span>
        <h2>Capability &amp; Learning Glossary</h2>
        <p>New to DSAT, TNA or capability frameworks? Start with the glossary — plain-English definitions of every term used across this site, each linking through to the article or service page that covers it properly.</p>
        <a class="read" href="glossary.html">Browse the glossary →</a>
      </div>
      <div class="fi-visual"><img src="assets/icons/insight.svg" alt=""></div>
    </article>
  </div>
</section>

<section style="padding-top:30px">
  <div class="wrap">
    <div class="eyebrow reveal">More insights</div>
    <div class="insight-grid">
      <article class="insight-card reveal"><div class="ic-top"><img src="assets/icons/governance.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Defence</span><h3>DSAT Explained</h3><p>What JSP 822 actually asks of you — without the acronym overload.</p><a class="read" href="dsat-explained.html">Read the article &rarr;</a></div></article>
      <article class="insight-card reveal" data-d="1"><div class="ic-top"><img src="assets/icons/assurance.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Method</span><h3>Training Needs Analysis: Best Practice</h3><p>How to run a TNA that finds the real gap and gives leaders evidence.</p><a class="read" href="training-needs-analysis-best-practice.html">Read the article &rarr;</a></div></article>
      <article class="insight-card reveal" data-d="2"><div class="ic-top"><img src="assets/icons/capability.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Capability</span><h3>Building Capability Frameworks</h3><p>Designing competency frameworks people actually use.</p><a class="read" href="building-capability-frameworks.html">Read the article &rarr;</a></div></article>
      <article class="insight-card reveal"><div class="ic-top"><img src="assets/icons/leadership.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Leadership</span><h3>Leadership in High-Pressure Environments</h3><p>What the military teaches about leaders who hold up when it counts.</p><a class="read" href="leadership-in-high-pressure-environments.html">Read the article &rarr;</a></div></article>
      <article class="insight-card reveal" data-d="1"><div class="ic-top"><img src="assets/icons/sector-public.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Public Sector</span><h3>Public Sector Workforce Development</h3><p>Building capability and pipelines under real budget pressure.</p><a class="read" href="public-sector-workforce-development.html">Read the article &rarr;</a></div></article>
      <article class="insight-card reveal" data-d="2"><div class="ic-top"><img src="assets/icons/development.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Technology</span><h3>Learning Technology Lessons</h3><p>Why so many LMS investments underdeliver — and how to get value.</p><a class="read" href="learning-technology-lessons.html">Read the article &rarr;</a></div></article>
      <article class="insight-card reveal"><div class="ic-top"><img src="assets/icons/systems.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Talent</span><h3>Apprenticeship Success Strategies</h3><p>What drives 95% completion and 100% funding compliance.</p><a class="read" href="apprenticeship-success-strategies.html">Read the article &rarr;</a></div></article>
      <article class="insight-card reveal" data-d="1"><div class="ic-top"><img src="assets/icons/sector-defence.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Defence</span><h3>Defence Training Governance</h3><p>Making governance audit-ready and useful — not just for inspectors.</p><a class="read" href="defence-training-governance.html">Read the article &rarr;</a></div></article>
      <article class="insight-card reveal" data-d="2"><div class="ic-top"><img src="assets/icons/readiness.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Readiness</span><h3>From Training to Readiness</h3><p>Connecting learning investment to the outcomes leaders are measured on.</p><a class="read" href="from-training-to-readiness.html">Read the article &rarr;</a></div></article>
    </div>
  </div>
</section>

{cta("Want this thinking applied to your organisation?", "Insight is useful. Applied insight changes outcomes. Let's talk about yours.", secondary=("See the evidence", "case-studies.html"))}'''

# ================================================================== CONTACT
contact_body = f'''<header class="page-hero" id="book">
  <div class="wrap">
    <div class="eyebrow reveal in">Contact</div>
    <h1 class="reveal in" data-d="1">Discuss your capability challenge.</h1>
    <p class="hero-sub reveal in" data-d="2">A practical, problem-first conversation — no sales pitch. Tell me what's going on and we'll work out what's really driving it, and whether I'm the right person to help.</p>
  </div>
</header>

<div class="divider"></div>

<section style="padding-top:64px">
  <div class="wrap contact-grid">
    <div class="reveal">
      <h2 style="font-size:1.5rem;font-weight:500;margin-bottom:8px">Send a message</h2>
      <p class="muted" style="margin-bottom:26px">I read every enquiry personally and aim to reply within one working day.</p>
      <form class="form" action="https://formspree.io/f/xeeyazed" method="POST">
        <input type="hidden" name="_subject" value="Prelude website: New capability enquiry">
        <input type="hidden" name="_next" value="{SITE_URL}/thank-you.html?from=contact">
        <div class="row">
          <div class="field"><label for="name">Name</label><input id="name" name="name" type="text" required placeholder="Your name"><span class="field-error">Please enter your name.</span></div>
          <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" required placeholder="you@organisation.gov.uk"><span class="field-error">Please enter a valid email address.</span></div>
        </div>
        <div class="row">
          <div class="field"><label for="org">Organisation</label><input id="org" name="organisation" type="text" placeholder="Your organisation"></div>
          <div class="field"><label for="sector">Sector</label>
            <select id="sector" name="sector"><option>Defence</option><option>Healthcare / NHS</option><option>Housing</option><option>Public sector / Government</option><option>Other</option></select>
          </div>
        </div>
        <div class="field"><label for="message">What capability challenge are you facing?</label><textarea id="message" name="message" required placeholder="A few lines on the problem you're trying to solve..."></textarea><span class="field-error">Please tell me a little about the challenge you're facing.</span></div>
        <button type="submit" class="btn btn-primary">Send enquiry {ARROW}</button>
        <p class="form-note">Prefer email? Write to <a href="mailto:jason.smith@prelude-learning.com" style="color:var(--gold)">jason.smith@prelude-learning.com</a>.</p>
      </form>
    </div>
    <div class="reveal" data-d="2">
      <div class="contact-info">
        <div class="ci-item"><h4>No sales pitch</h4><p>A practical conversation about your problem — not a pitch for a product.</p></div>
        <div class="ci-item"><h4>Problem-first</h4><p>We start with what's really going on, then talk about whether and how I can help.</p></div>
        <div class="ci-item"><h4>Email</h4><a href="mailto:jason.smith@prelude-learning.com">jason.smith@prelude-learning.com</a></div>
        <div class="ci-item"><h4>Based in</h4><p>United Kingdom. Working with Defence and public sector organisations nationally.</p></div>
        <div class="ci-item"><h4>Clearance</h4><p>Active SC clearance held (former DV). Comfortable in secure, regulated environments.</p></div>
      </div>
      <div class="cred-strip" style="margin-top:30px">
        <div class="cred-badge">{CHECK}Active SC Clearance</div>
        <div class="cred-badge">{CHECK}DSAT Specialist</div>
        <div class="cred-badge">{CHECK}PRINCE2 Practitioner</div>
      </div>
    </div>
  </div>
</section>

{cta('"Jason understands my environment, my problem, and has solved this before."', "That's the conversation I want to have with you.")}'''

# ================================================================== CRR
CRR_QUESTIONS = [
    "We can clearly state the problem we're actually trying to solve.",
    "We know which behaviours need to change.",
    "We're clear on the impact we're trying to achieve.",
    "We've defined what 'good' looks like.",
    "We know how success will be measured.",
    "We have evidence supporting our view of the current position.",
    "We've genuinely tested whether training is the real problem.",
    "We understand the organisational barriers in the way.",
    "We understand the risks if nothing changes.",
    "We know what capability is required to achieve the outcome.",
]
CRR_OPTS = [("Yes, clearly", "3"), ("Partly", "2"), ("Not really", "1"), ("Not sure", "0")]
_crr_q = ""
for i, q in enumerate(CRR_QUESTIONS, 1):
    opts = "".join(f'<label class="crr-opt"><input type="radio" name="q{i}" value="{s}"><span>{l}</span></label>' for l, s in CRR_OPTS)
    _crr_q += f'<div class="crr-q"><div class="q"><span class="qn">{i:02d}</span><span>{q}</span></div><div class="crr-opts">{opts}</div></div>\n      '

crr_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">The Capability Readiness Review&trade;</div>
    <h1 class="reveal in" data-d="1">Find the real problem before you invest in the solution.</h1>
    <p class="hero-sub reveal in" data-d="2">The first step before investing in training, consultancy or capability development. Most organisations know something isn't working — few know whether it's a capability, leadership, process, governance, workforce or training issue. This is the structured diagnosis I run with every client, now available free as a self-assessment.</p>
  </div>
</header>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">What it is</div>
    <p class="lead reveal" data-d="1">A diagnostic, not a sales tool. <span class="dim">The Capability Readiness Review tests how clearly you can answer the ten questions that determine whether an intervention will actually work — and shows where the risk really sits. It's built on the Prelude Capability Model&trade;.</span></p>
    {fw_prelude_model()}
    {fw_readiness_review()}
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Three levels</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">A clear path from free self-check to full diagnosis.</p>
    <div class="ladder reveal" data-d="2">
      <div class="rung"><div class="rung-tag">Free</div><h3>Capability Readiness Self-Assessment</h3><p>The ten-question self-assessment on this page. An immediate, honest read on where your readiness gaps sit — in two minutes, in your browser.</p><a class="read" href="#crr">Start below →</a></div>
      <div class="rung featured"><div class="rung-tag">Facilitated</div><h3>Capability Readiness Review&trade;</h3><p>A facilitated review with evidence-gathering and stakeholder input, producing a prioritised, board-ready picture of the real problem and what to do about it.</p><a class="read" href="contact.html#book">Enquire →</a></div>
      <div class="rung"><div class="rung-tag">Consultancy</div><h3>Capability Diagnostic&trade;</h3><p>A full diagnostic engagement — root-cause analysis, capability mapping and an evidence-based plan aligned to the Prelude Capability Model&trade;.</p><a class="read" href="contact.html#book">Enquire →</a></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">The self-assessment</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Ten questions. Two minutes. An honest read on your readiness.</p>
    <div class="crr reveal" data-d="2" id="crr">
      <div class="crr-progress"><span id="crr-bar"></span></div>
      <div class="crr-progress-label" id="crr-count">0 of 10 answered</div>
      {_crr_q}
      <div class="crr-actions">
        <button class="btn btn-primary" id="crr-calc" type="button">See my Capability Readiness Score {ARROW}</button>
        <button class="btn btn-ghost" id="crr-print" type="button">Download / print</button>
        <span class="crr-hint" id="crr-hint">Answer all ten, then calculate.</span>
      </div>
      <div class="crr-result" id="crr-result">
        <div class="crr-score-wrap">
          <div class="score-ring" id="crr-ring"><div class="inner"><span class="sf" id="crr-score">0%</span><span class="sl">Readiness</span></div></div>
          <div class="crr-band"><h3 id="crr-bandtitle"></h3><p id="crr-bandtext"></p></div>
        </div>
        <div class="crr-cols">
          <div class="crr-card"><h4>Areas of risk</h4><ul id="crr-risks"></ul></div>
          <div class="crr-card"><h4>Potential root causes</h4><ul id="crr-causes"></ul></div>
          <div class="crr-card"><h4>Recommended next steps</h4><ul id="crr-steps"></ul></div>
        </div>
        <div style="margin-top:30px"><a href="contact.html#book" class="btn btn-primary">Discuss Your Capability Challenge {ARROW}</a></div>
      </div>
    </div>
    <p class="placeholder-note reveal" style="margin-top:22px">This self-assessment runs entirely in your browser — nothing is sent or stored. A full, facilitated Capability Readiness Review goes deeper, with evidence-gathering and stakeholder input.</p>
  </div>
</section>

<div class="divider"></div>

{cta("Want the full, facilitated Review?", "The self-assessment is the starting point. The full Capability Readiness Review brings evidence, stakeholder input and a prioritised plan.", secondary=("How I work", "how-i-work.html"))}'''

# ================================================================== HOW I WORK
HIW_STAGES = [
    ("01", "Discovery &amp; Capability Review", "We start with the Capability Readiness Review&trade; — understanding your mission, the problem, and what 'good' looks like before anything else."),
    ("02", "Analysis &amp; Diagnosis", "Evidence-based analysis to separate the real capability gap from the symptoms — and to find the root cause, not just the loudest complaint."),
    ("03", "Design &amp; Recommendation", "A practical, prioritised recommendation: learning where it helps, and structure, governance or workforce design where it doesn't."),
    ("04", "Implementation Support", "Hands-on support to put the recommendation into practice — at whatever level of involvement suits you and your team."),
    ("05", "Measurement &amp; Sustainability", "Measuring the outcomes that matter, and embedding the change so capability keeps improving long after I've left."),
]
_hiw = "".join(f'<div class="mstep reveal"><div class="mnum">{n}</div><h3>{t}</h3><p>{p}</p></div>' for n, t, p in HIW_STAGES)
howiwork_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">How I Work</div>
    <h1 class="reveal in" data-d="1">Know exactly what to expect.</h1>
    <p class="hero-sub reveal in" data-d="2">Bringing in an external adviser is a risk. Here's how I reduce it — a clear, five-stage approach with senior delivery, evidence at every step, and no lock-in.</p>
  </div>
</header>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">The engagement</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Five stages, from first conversation to lasting capability.</p>
    <div class="method-steps">{_hiw}</div>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">The method behind it</div>
    {fw_improvement_approach()}
    {fw_maturity_model()}
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">What you can expect</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">No surprises. No junior hand-offs. No lock-in.</p>
    <div class="feature-grid cols-2">
      <div class="feature-card reveal"><h3>Clear scope &amp; milestones</h3><p>You'll know what's being done, by when, and what each stage delivers — agreed up front.</p></div>
      <div class="feature-card reveal" data-d="1"><h3>Senior delivery throughout</h3><p>You work directly with me. The person you meet is the person who does the work.</p></div>
      <div class="feature-card reveal"><h3>Evidence at every stage</h3><p>Recommendations are backed by analysis you can see, question and take to your board.</p></div>
      <div class="feature-card reveal" data-d="1"><h3>No lock-in</h3><p>I build your capability to stand on its own — not a dependency on me.</p></div>
    </div>
    {photo_grid([
      ("public-sector-stakeholder-roundtable.jpeg", "Strategic planning session — leaders reviewing options around a table", 540, 360),
      ("defence-military-operations-room.jpeg", "Capability review workshop in a headquarters environment", 596, 335),
      ("capability-framework-review.jpeg", "One-to-one advisory conversation reviewing a capability framework", 540, 360),
    ], cols="3")}
  </div>
</section>

<div class="divider"></div>

{trust()}
{cta("Ready to see what the first stage looks like?", "Start with the Capability Readiness Review, or just tell me what's going on.", secondary=("Take the Capability Review", "capability-readiness-review.html"))}'''

# ================================================================== MANIFESTO
manifesto_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">Manifesto</div>
    <h1 class="reveal in" data-d="1">Why training isn't the problem.</h1>
    <p class="hero-sub reveal in" data-d="2">The single idea behind everything I do: training is rarely the problem. Capability is. Here's what that means — and why diagnosis has to come before prescription.</p>
  </div>
</header>

<div class="divider"></div>

<section>
  <div class="wrap article">
    <h2 class="reveal">Performance gaps are not the same as training gaps</h2>
    <p class="reveal">When something isn't working, the reflex is to assume people need training. Sometimes they do. Far more often, the knowledge and skill are already there — and performance is being held back by something else entirely: unclear roles, weak governance, missing standards, or a structure that quietly works against the outcome.</p>

    <h2 class="reveal">Training is commissioned before the problem is understood</h2>
    <p class="reveal">Courses are easy to buy and easy to count. So organisations commission them early — before anyone has defined the problem, what good looks like, or how success will be measured. The result is activity that feels like progress but rarely moves the outcome.</p>

    <h2 class="reveal">Capability is a system, not a course</h2>
    <p class="reveal">Real capability comes from people, behaviours, governance, leadership, structure, assurance and learning working together. Training is one part of that system. When the other parts are missing, no amount of training will deliver the result — which is exactly why so much training appears to "fail".</p>
    {fw_prelude_model()}

    <h2 class="reveal">Diagnosis before prescription</h2>
    <p class="reveal">No serious adviser prescribes before they diagnose. The same discipline applies to capability: understand the mission, find the real gap, separate cause from symptom — and only then decide what the right intervention is. Sometimes it's learning. Often it's something more structural.</p>
    {fw_decision_model()}

    <h2 class="reveal">Root causes beat symptoms — every time</h2>
    <p class="reveal">Organisations improve fastest when they understand root causes rather than chasing symptoms. It's less comfortable than booking a course, but it's the difference between spending money and building capability that lasts.</p>
  </div>
</section>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">Go deeper</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Take the thinking further.</p>
    <div class="resource-grid">
      <div class="resource reveal"><img class="r-ic" src="assets/icons/readiness.svg" alt=""><div class="r-body"><span class="gated">Free · email required</span><h3>The Capability Readiness Playbook&trade;</h3><p>A consultancy-grade guide to the Prelude Capability Model&trade;, the Capability Readiness Review&trade;, common capability mistakes and the diagnostic questions I use.</p><a class="read" href="insights.html#get-resources">Get the Playbook →</a></div></div>
      <div class="resource reveal" data-d="1"><img class="r-ic" src="assets/icons/insight.svg" alt=""><div class="r-body"><span class="gated">Coming soon</span><h3>Watch the talk</h3><p>"Why Training Isn't the Problem" — the manifesto as a short talk for leadership teams. Video coming soon.</p><span class="read" style="opacity:.6">In production →</span></div></div>
    </div>
  </div>
</section>

{cta("Think you might have a capability problem?", "Start with the free Capability Readiness Self-Assessment, or just tell me what's going on.", secondary=("Take the Capability Review", "capability-readiness-review.html"))}'''

# ================================================================== WHO I HELP
_buyers = (
    buyer_acc("01", "Defence Programme Leaders",
        ["Capability requirements that aren't clearly defined","Programmes judged on activity, not readiness","Pressure to deliver at pace without losing governance"],
        "Commissioning training and tooling before the capability requirement is defined — then struggling to show the programme moved readiness.",
        ["A defined, evidence-based capability requirement","Readiness you can measure and defend","Pace without sacrificing DSAT defensibility"],
        "I define what capability the mission requires, diagnose the real gap, and turn analysis into action your board can stand behind.", is_open=True)
    + buyer_acc("02", "Capability Managers",
        ["Symptoms reported as capability gaps","No consistent way to measure capability","Operational demand outpacing the workforce"],
        "Treating every performance issue as a skills issue, so structural and governance causes go unaddressed.",
        ["Root causes separated from symptoms","A consistent capability picture","Targeted, affordable interventions"],
        "I bring a model and method to map capability against mission, so you invest where it actually moves performance.")
    + buyer_acc("03", "Heads of Learning &amp; Development",
        ["Being handed 'training' requests that aren't training problems","Proving L&amp;D's impact on performance","A learning estate that's grown without strategy"],
        "Saying yes to course requests without diagnosing the problem — and being measured on completion, not outcomes.",
        ["A defensible 'is this really training?' filter","Learning aligned to organisational performance","Evidence of impact, not just activity"],
        "I help you reposition L&amp;D as a capability function — diagnosing first, and using learning as one tool among several.")
    + buyer_acc("04", "Training Governance Leads",
        ["Governance treated as box-ticking","Assurance that doesn't reassure","Audit risk hidden until inspection"],
        "Running DSAT as a process to complete rather than a framework to support decisions — which slows everything down.",
        ["Governance that's audit-ready and useful","DSAT used to speed good decisions","Defensible evidence on demand"],
        "I make governance and assurance both compliant and practical, so it supports pace instead of blocking it.")
    + buyer_acc("05", "Defence Digital Programme Managers",
        ["Digital problems framed as training problems","Unclear future role requirements","Skills, behaviours and workforce needs unmapped"],
        "Buying digital learning against an undefined capability requirement — a course catalogue, not capability.",
        ["Defined digital capability requirements","Workforce and roles mapped to them","Learning architecture aligned to outcomes"],
        "I define the digital capability the mission needs and align the workforce and learning estate to deliver it — as on DS4D.")
    + buyer_acc("06", "NHS Workforce Leads",
        ["Compliance reporting that can't be trusted","Mandatory training that doesn't change practice","Leadership capability under pressure"],
        "Adding more mandatory training to fix behaviour, when the data and governance are the real gap.",
        ["Reliable compliance visibility","Training that changes practice","Stronger leadership capability"],
        "I diagnose where compliance and capability really break down, then fix the system — not just the course.")
    + buyer_acc("07", "People Directors",
        ["People strategy disconnected from performance","Succession and capability risk","Investment hard to justify to the board"],
        "Investing in programmes before defining the capability the organisation needs and how success will be measured.",
        ["People strategy tied to performance","Capability and succession risk understood","Board-ready evidence for investment"],
        "I connect workforce capability to organisational outcomes, with evidence your board will back.")
    + buyer_acc("08", "Housing Leadership Teams",
        ["Inconsistent manager capability","Slow, inconsistent onboarding","Culture and service expectations left unwritten"],
        "Sending managers on courses while the real gaps sit in structure, onboarding and expectations.",
        ["Consistent leadership standards","Faster time-to-competence","Culture and expectations made explicit"],
        "I build manager and onboarding capability that lifts service and retention — grounded in how housing actually operates.")
    + buyer_acc("09", "Transformation Leaders",
        ["Change that stalls after launch","Capability gaps surfacing mid-programme","Benefits that are hard to evidence"],
        "Designing the solution before diagnosing the capability the change actually requires.",
        ["Capability designed into the change","Fewer mid-programme surprises","Evidenced, sustained benefits"],
        "I diagnose the capability your transformation needs and embed it, so change sticks after the programme ends.")
)
whoihelp_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">Who I Help</div>
    <h1 class="reveal in" data-d="1">You identify with your role faster than your sector.</h1>
    <p class="hero-sub reveal in" data-d="2">Find your role below for the challenges I see most often, the mistakes worth avoiding, the outcomes you're really after — and how I help you get there.</p>
  </div>
</header>

<div class="divider"></div>

<section style="padding-top:50px">
  <div class="wrap">
    <div class="accordion">
{_buyers}    </div>
  </div>
</section>

<div class="divider"></div>

{comparison_section()}
{cta("Sound familiar?", "If any of that is your world right now, let's talk about what's really driving it — no sales pitch.", secondary=("Take the Capability Review", "capability-readiness-review.html"))}'''

# ------------------------------------------------------------------ write
page("index.html", "Jason Smith — Capability, Readiness &amp; Workforce Development Advisor | Prelude",
     "Training is rarely the problem. Capability is. Jason Smith is a capability, readiness and workforce development advisor helping Defence and public sector organisations diagnose the real problem and build capability. DSAT specialist, 23+ years, Active SC.",
     home_body, "home")

page("defence.html", "DSAT Consultant | JSP 822 &amp; Defence Training Governance | Prelude",
     "Defence capability and DSAT consultancy for MOD, Defence Digital, DE&S, Front Line Commands and prime contractors. JSP 822, Training Needs Analysis, capability frameworks, training governance and readiness.",
     defence_body, "defence",
     keywords="DSAT Consultant, JSP 822 Consultant, Defence Training Governance, Training Needs Analysis, Defence Capability Development",
     breadcrumb="Defence", faq=DEFENCE_FAQ)

page("healthcare.html", "Healthcare &amp; NHS Capability Consultancy | Prelude",
     "Healthcare and NHS capability consultancy: compliance assurance, Totara and LMS optimisation, workforce capability planning and leadership development for clinical and operational managers.",
     healthcare_body, "healthcare",
     keywords="NHS consultant, healthcare learning and development, Totara LMS optimisation, NHS compliance training, healthcare workforce capability",
     breadcrumb="Healthcare", faq=HEALTHCARE_FAQ)

page("housing.html", "Housing Association Capability Consultancy | Prelude",
     "Housing association capability consultancy: manager onboarding, values-based induction, succession planning and workforce capability for housing associations, ALMOs and local authority housing teams.",
     housing_body, "housing",
     keywords="housing association consultant, housing leadership development, manager onboarding housing, ALMO workforce development",
     breadcrumb="Housing", faq=HOUSING_FAQ)

page("public-sector.html", "Public Sector Capability &amp; Workforce Consultancy | Prelude",
     "Public sector capability consultancy: workforce and role architecture redesign, transformation capability, leadership development and training governance for local and central government.",
     public_sector_body, "public-sector",
     keywords="public sector workforce consultant, local government capability, role architecture redesign, public sector training governance",
     breadcrumb="Public Sector", faq=PUBLIC_SECTOR_FAQ)

page("professional-services.html", "Professional Services Capability Consultancy | Prelude",
     "Professional services capability consultancy: leadership and partner-track development, talent retention, onboarding and capability frameworks for law firms, accountancy and consulting practices.",
     professional_services_body, "professional-services",
     keywords="professional services leadership development, partner track development, law firm talent development, accountancy firm leadership training",
     breadcrumb="Professional Services", faq=PROFESSIONAL_SERVICES_FAQ)

page("about.html", "About Jason Smith — Royal Navy Leader &amp; Capability Advisor | Prelude",
     "23+ years building capability where the stakes are real: Royal Navy operational leadership, Defence capability specialism, Korn Ferry consultant, independent capability advisor.",
     about_body, "about", og="profile", breadcrumb="About")

page("services.html", "Services — Capability &amp; Governance, Leadership &amp; Workforce, Learning Transformation | Prelude",
     "Capability consultancy grouped around your problem: DSAT, TNA, capability frameworks and governance; leadership, talent, workforce planning and apprenticeships; digital learning, LMS, learning operations and strategy.",
     services_body, "services", breadcrumb="Services")

page("case-studies.html", "Case Studies — Defence, Healthcare &amp; Housing Capability Projects | Prelude",
     "Capability, governance and learning projects across Defence, Healthcare and Housing — the problem, why it mattered, what I did, the results and the client benefit.",
     cs_body, "case-studies", breadcrumb="Case Studies")

page("insights.html", "Insights &amp; Resources — DSAT, TNA, Capability &amp; Governance Tools | Prelude",
     "Free diagnostics and templates plus plain-English thinking on DSAT, training needs analysis, capability frameworks, leadership and defence training governance.",
     insights_body, "insights",
     keywords="DSAT, JSP 822, Training Needs Analysis checklist, capability framework template, learning governance health check, leadership diagnostic",
     breadcrumb="Insights")

page("contact.html", "Contact — Discuss Your Capability Challenge | Jason Smith, Prelude",
     "Discuss your capability, readiness or training governance challenge with Jason Smith. A practical, problem-first conversation — no sales pitch. Defence, Healthcare, Housing and public sector.",
     contact_body, "contact", breadcrumb="Contact")

# ================================================================== THANK YOU
thank_you_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">Sent</div>
    <h1 class="reveal in" data-d="1" id="ty-heading">Message sent.</h1>
    <p class="hero-sub reveal in" data-d="2" id="ty-sub">Thanks — I read every enquiry personally and aim to reply within one working day.</p>
  </div>
</header>

<div class="divider"></div>

<section>
  <div class="wrap">
    <div class="eyebrow reveal">While you wait</div>
    <p class="section-intro lead reveal" data-d="1" style="font-size:clamp(1.4rem,2.6vw,2rem)">Some places to keep exploring.</p>
    <div class="feature-grid">
      <div class="feature-card reveal"><h3>Case studies</h3><p>See the evidence behind the claims — real capability, governance and learning projects across Defence, Healthcare and Housing.</p></div>
      <div class="feature-card reveal" data-d="1"><h3>Capability Readiness Review</h3><p>Not sure where your own problem sits? Take the ten-question self-assessment.</p></div>
      <div class="feature-card reveal" data-d="2"><h3>Insights</h3><p>Practical thinking on DSAT, capability frameworks, leadership and readiness.</p></div>
    </div>
    <div style="margin-top:40px" class="reveal">
      <a href="case-studies.html" class="btn btn-primary">View case studies {ARROW}</a>
      <a href="index.html" class="btn btn-ghost" style="margin-left:14px">Back to homepage</a>
    </div>
  </div>
</section>
<script>
(function(){{
  var params = new URLSearchParams(location.search);
  if (params.get('from') === 'resource') {{
    document.getElementById('ty-heading').textContent = 'Resource on its way.';
    document.getElementById('ty-sub').textContent = "Thanks — check your inbox shortly. If it doesn't arrive in a few minutes, check your spam folder or email jason.smith@prelude-learning.com directly.";
  }}
}})();
</script>'''

page("thank-you.html", "Thank You | Prelude Learning &amp; Consultancy",
     "Your message has been sent to Prelude Learning &amp; Consultancy.",
     thank_you_body, "", noindex=True)

page("capability-readiness-review.html", "The Capability Readiness Review&trade; — Free Diagnostic | Prelude",
     "Find the real problem before you invest. A 10-question Capability Readiness Review self-assessment for Defence and public sector leaders — capability, leadership, process, governance, workforce or training.",
     crr_body, "crr", extra_body='<script src="crr.js"></script>\n', breadcrumb="Capability Readiness Review")

page("how-i-work.html", "How I Work — A Clear Five-Stage Capability Engagement | Prelude",
     "Exactly what to expect when you work with Jason Smith: discovery and Capability Review, analysis and diagnosis, design, implementation support, and measurement — senior delivery, evidence-led, no lock-in.",
     howiwork_body, "how-i-work", breadcrumb="How I Work")

page("why-training-isnt-the-problem.html", "Why Training Isn't the Problem — The Prelude Manifesto",
     "Training is rarely the problem. Capability is. The Prelude manifesto on why performance gaps aren't training gaps, why diagnosis must come before prescription, and how the Prelude Capability Model works.",
     manifesto_body, "insights",
     keywords="capability not training, performance gap, training needs analysis, capability diagnosis, Prelude Capability Model",
     breadcrumb="Why Training Isn't the Problem")

page("who-i-help.html", "Who I Help — Capability Support by Role | Prelude",
     "Capability, readiness and workforce development support for Defence Programme Leaders, Capability Managers, Heads of L&D, Training Governance Leads, NHS Workforce Leads, People Directors, Housing leadership and Transformation Leaders.",
     whoihelp_body, "who-i-help", breadcrumb="Who I Help")

privacy_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">Legal</div>
    <h1 class="reveal in" data-d="1">Privacy Policy.</h1>
    <p class="hero-sub reveal in" data-d="2">How Prelude Learning &amp; Consultancy Ltd collects, uses and protects the personal data you share through this website.</p>
  </div>
</header>

<div class="divider"></div>

<section>
  <div class="wrap article">
    <p class="reveal" style="color:var(--stone-dim);font-size:14px">Last updated: 11 July 2026</p>

    <h2 class="reveal">Who we are</h2>
    <p class="reveal">This website is operated by Prelude Learning &amp; Consultancy Ltd, a company registered in England and Wales (Company No. 16918049). For the purposes of UK data protection law, Prelude Learning &amp; Consultancy Ltd is the data controller for personal data submitted through this site. Contact: <a href="mailto:jason.smith@prelude-learning.com" style="color:var(--gold)">jason.smith@prelude-learning.com</a>.</p>

    <h2 class="reveal">What we collect</h2>
    <p class="reveal">We only collect personal data you choose to give us, through two forms on this site:</p>
    <ul style="color:var(--stone);line-height:1.75;margin:0 0 8px 20px">
      <li>The <strong>contact form</strong> — name, email address, organisation, sector, and the message you write.</li>
      <li>The <strong>resource request form</strong> — email address and the resource you've asked for.</li>
    </ul>
    <p class="reveal">We do not use analytics, advertising or tracking cookies on this site. No personal data is collected automatically beyond what you submit directly.</p>

    <h2 class="reveal">How we use it</h2>
    <p class="reveal">We use the information you provide to respond to your enquiry, to send the specific resource you requested, and — only where you've asked for it — to send occasional, practical follow-up notes on capability and readiness. You can unsubscribe from those at any time. We do not sell or rent your data, and we do not use it for any purpose other than the one you gave it to us for.</p>

    <h2 class="reveal">Legal basis</h2>
    <p class="reveal">We process enquiry and resource-request data on the basis of legitimate interests — responding to a business enquiry you've initiated — and, for any ongoing email updates, on the basis of your consent, which you can withdraw at any time.</p>

    <h2 class="reveal">Who we share it with</h2>
    <p class="reveal">Form submissions are processed by Formspree (Formspree, Inc., a US-based form-handling provider) acting as our data processor, which delivers your submission to us by email. This involves a transfer of your data outside the UK; Formspree's own privacy policy is available at <a href="https://formspree.io/legal/privacy-policy" style="color:var(--gold)" target="_blank" rel="noopener">formspree.io/legal/privacy-policy</a>. We do not share your data with any other third party, and we do not sell it. If the specific provider we use changes, this policy will be updated to reflect it.</p>

    <h2 class="reveal">How long we keep it</h2>
    <p class="reveal">We keep enquiry and resource-request data only as long as necessary to respond to you and maintain a reasonable business record of the correspondence — in practice, no longer than 24 months from your last contact with us, unless you ask us to delete it sooner or we're required to keep it longer by law.</p>

    <h2 class="reveal">Your rights</h2>
    <p class="reveal">Under UK GDPR, you have the right to ask for access to, correction of, or deletion of your personal data; to object to or restrict how we use it; and to receive a copy of it in a portable format. To exercise any of these rights, email <a href="mailto:jason.smith@prelude-learning.com" style="color:var(--gold)">jason.smith@prelude-learning.com</a>. If you're unhappy with how we've handled your data, you can also complain to the UK Information Commissioner's Office (ico.org.uk).</p>

    <h2 class="reveal">Children</h2>
    <p class="reveal">This site and its services are intended for business use by adults and are not directed at children.</p>

    <h2 class="reveal">Changes to this policy</h2>
    <p class="reveal">We'll update this page if how we collect or use data changes, and update the date at the top accordingly.</p>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <h2 class="reveal">Questions about your data?</h2>
    <p class="reveal" data-d="1">Email us directly and we'll get back to you personally.</p>
    <div class="cta-actions reveal" data-d="2">
      <a href="mailto:jason.smith@prelude-learning.com" class="btn btn-primary">Email jason.smith@prelude-learning.com {ARROW}</a>
    </div>
  </div>
</section>'''

page("privacy.html", "Privacy Policy | Prelude Learning &amp; Consultancy",
     "How Prelude Learning &amp; Consultancy Ltd collects, uses and protects personal data submitted through this website, and your rights under UK GDPR.",
     privacy_body, "", breadcrumb="Privacy Policy")

# ------------------------------------------------------------------ sitemap.xml
SITEMAP_PAGES = [
    ("index.html", "1.0", "monthly"),
    ("defence.html", "0.9", "monthly"),
    ("healthcare.html", "0.9", "monthly"),
    ("housing.html", "0.9", "monthly"),
    ("public-sector.html", "0.9", "monthly"),
    ("professional-services.html", "0.9", "monthly"),
    ("services.html", "0.9", "monthly"),
    ("dsat-consultancy.html", "0.8", "monthly"),
    ("training-needs-analysis.html", "0.8", "monthly"),
    ("capability-framework-design.html", "0.8", "monthly"),
    ("training-governance-assurance.html", "0.8", "monthly"),
    ("leadership-development.html", "0.8", "monthly"),
    ("talent-development.html", "0.8", "monthly"),
    ("workforce-planning.html", "0.8", "monthly"),
    ("apprenticeships.html", "0.8", "monthly"),
    ("digital-learning.html", "0.8", "monthly"),
    ("lms-optimisation.html", "0.8", "monthly"),
    ("learning-operations.html", "0.8", "monthly"),
    ("learning-strategy.html", "0.8", "monthly"),
    ("who-i-help.html", "0.8", "monthly"),
    ("how-i-work.html", "0.7", "monthly"),
    ("case-studies.html", "0.9", "monthly"),
    ("mod-digital-skills-for-defence.html", "0.7", "yearly"),
    ("sio-course-rapid-tna.html", "0.7", "yearly"),
    ("defence-capability-framework-design.html", "0.7", "yearly"),
    ("op-isotrope-role-architecture-redesign.html", "0.7", "yearly"),
    ("healthcare-learning-transformation.html", "0.7", "yearly"),
    ("housing-leadership-onboarding-transformation.html", "0.7", "yearly"),
    ("defence-apprenticeship-success-programme.html", "0.7", "yearly"),
    ("nato-royal-navy-training-modernisation.html", "0.7", "yearly"),
    ("capability-readiness-review.html", "0.8", "monthly"),
    ("insights.html", "0.7", "monthly"),
    ("glossary.html", "0.7", "monthly"),
    ("dsat-explained.html", "0.7", "monthly"),
    ("training-needs-analysis-best-practice.html", "0.7", "monthly"),
    ("building-capability-frameworks.html", "0.7", "monthly"),
    ("leadership-in-high-pressure-environments.html", "0.7", "monthly"),
    ("public-sector-workforce-development.html", "0.7", "monthly"),
    ("learning-technology-lessons.html", "0.7", "monthly"),
    ("apprenticeship-success-strategies.html", "0.7", "monthly"),
    ("defence-training-governance.html", "0.7", "monthly"),
    ("from-training-to-readiness.html", "0.7", "monthly"),
    ("training-needs-analysis-complete-guide.html", "0.8", "monthly"),
    ("dsat-compliant-tna-step-by-step.html", "0.7", "monthly"),
    ("tna-vs-skills-gap-analysis.html", "0.7", "monthly"),
    ("common-tna-mistakes.html", "0.7", "monthly"),
    ("presenting-tna-findings-to-a-board.html", "0.7", "monthly"),
    ("learning-strategy-complete-guide.html", "0.8", "monthly"),
    ("learning-strategy-leadership-will-fund.html", "0.7", "monthly"),
    ("learning-strategy-vs-training-plan.html", "0.7", "monthly"),
    ("measuring-learning-strategy-impact.html", "0.7", "monthly"),
    ("learning-strategy-multi-site-multi-sector.html", "0.7", "monthly"),
    ("leadership-development-complete-guide.html", "0.8", "monthly"),
    ("why-promoting-technical-experts-fails.html", "0.7", "monthly"),
    ("leadership-onboarding-week-one.html", "0.7", "monthly"),
    ("succession-planning-critical-roles.html", "0.7", "monthly"),
    ("capability-development-complete-guide.html", "0.8", "monthly"),
    ("what-is-a-capability-framework.html", "0.7", "monthly"),
    ("capability-vs-competency-explained.html", "0.7", "monthly"),
    ("how-to-run-a-capability-readiness-review.html", "0.7", "monthly"),
    ("multi-specialisation-capability-frameworks.html", "0.7", "monthly"),
    ("digital-learning-complete-guide.html", "0.8", "monthly"),
    ("blended-vs-fully-digital-learning.html", "0.7", "monthly"),
    ("why-digital-learning-rollouts-stall.html", "0.7", "monthly"),
    ("digital-learning-shift-workers-distributed-teams.html", "0.7", "monthly"),
    ("digital-learning-adoption-after-week-one.html", "0.7", "monthly"),
    ("training-governance-complete-guide.html", "0.8", "monthly"),
    ("what-is-jsp-822.html", "0.7", "monthly"),
    ("governance-vs-compliance.html", "0.7", "monthly"),
    ("audit-ready-evidence-trail-without-extra-admin.html", "0.7", "monthly"),
    ("evaluating-learning-investment-complete-guide.html", "0.8", "monthly"),
    ("kirkpatricks-model-in-practice.html", "0.7", "monthly"),
    ("building-an-evaluation-plan-before-programme-starts.html", "0.7", "monthly"),
    ("measuring-roi-capability-investment.html", "0.7", "monthly"),
    ("why-satisfaction-scores-dont-prove-impact.html", "0.7", "monthly"),
    ("performance-consulting-complete-guide.html", "0.8", "monthly"),
    ("training-vs-capability-decision-model-explained.html", "0.7", "monthly"),
    ("is-your-performance-problem-really-a-training-problem.html", "0.7", "monthly"),
    ("performance-consulting-public-sector.html", "0.7", "monthly"),
    ("defence-learning-capability-guide.html", "0.8", "monthly"),
    ("digital-skills-for-defence-lessons.html", "0.7", "monthly"),
    ("tna-for-front-line-commands.html", "0.7", "monthly"),
    ("working-with-defence-primes-capability-programmes.html", "0.7", "monthly"),
    ("skills-frameworks-complete-guide.html", "0.8", "monthly"),
    ("what-is-a-skills-framework.html", "0.7", "monthly"),
    ("mapping-skills-to-roles-multiple-specialisations.html", "0.7", "monthly"),
    ("skills-frameworks-workforce-planning-succession.html", "0.7", "monthly"),
    ("learning-technology-complete-guide.html", "0.8", "monthly"),
    ("what-is-an-lms.html", "0.7", "monthly"),
    ("totara-vs-off-the-shelf-lms.html", "0.7", "monthly"),
    ("building-dashboards-leaders-trust.html", "0.7", "monthly"),
    ("organisational-change-capability-complete-guide.html", "0.8", "monthly"),
    ("role-architecture-redesign-rapid-scaling-crisis.html", "0.7", "monthly"),
    ("why-transformation-programmes-stall-after-go-live.html", "0.7", "monthly"),
    ("change-management-vs-capability-building.html", "0.7", "monthly"),
    ("why-training-isnt-the-problem.html", "0.6", "yearly"),
    ("about.html", "0.7", "monthly"),
    ("contact.html", "0.8", "yearly"),
    ("privacy.html", "0.2", "yearly"),
]

def build_sitemap():
    urls = ""
    for filename, priority, changefreq in SITEMAP_PAGES:
        loc = SITE_URL + "/" if filename == "index.html" else f"{SITE_URL}/{filename}"
        urls += f'''  <url>
    <loc>{loc}</loc>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
'''
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>
'''
    with open("sitemap.xml", "w") as f:
        f.write(xml)
    print("wrote sitemap.xml")

build_sitemap()

print("done")
