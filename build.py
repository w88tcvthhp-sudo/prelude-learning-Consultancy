#!/usr/bin/env python3
"""Generates the static HTML pages for the Prelude site from shared parts.
Run:  python3 build.py   (outputs *.html into this folder)."""
import os

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2.4" aria-hidden="true"><path d="M4 12l5 5L20 6"/></svg>'
CROSS = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2.4" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

NAVLINKS = [
    ("defence.html", "Defence", "defence"),
    ("services.html", "Services", "services"),
    ("how-i-work.html", "How I Work", "how-i-work"),
    ("case-studies.html", "Case Studies", "case-studies"),
    ("insights.html", "Insights", "insights"),
    ("about.html", "About", "about"),
    ("contact.html", "Contact", "contact"),
]

def head(title, desc, keywords="", og="website"):
    kw = f'\n<meta name="keywords" content="{keywords}">' if keywords else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#081D16">
<title>{title}</title>
<meta name="description" content="{desc}">{kw}
<meta property="og:type" content="{og}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&f[]=general-sans@400,500,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
'''

def nav(active):
    links = ""
    for href, label, key in NAVLINKS:
        cls = ' class="active"' if key == active else ""
        links += f'      <a href="{href}"{cls}>{label}</a>\n'
    return f'''<nav id="nav">
  <div class="wrap nav-inner">
    <a href="index.html" class="logo" aria-label="Prelude home">
      <img src="assets/logo/prelude-icon.svg" alt="Prelude" width="34" height="34">
      <span class="mark">PRELUDE<span>Learning &amp; Consultancy</span></span>
    </a>
    <div class="nav-links" id="navLinks">
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
        <span>Explore</span>
        <a href="defence.html">Defence</a>
        <a href="who-i-help.html">Who I Help</a>
        <a href="services.html">Services</a>
        <a href="how-i-work.html">How I Work</a>
        <a href="capability-readiness-review.html">Capability Review</a>
        <a href="case-studies.html">Case Studies</a>
        <a href="why-training-isnt-the-problem.html">Manifesto</a>
        <a href="insights.html">Insights</a>
        <a href="about.html">About</a>
        <a href="contact.html">Contact</a>
      </div>
      <div class="foot-domains">
        <span>Contact</span>
        <a href="mailto:jason.smith@prelude-learning.com">jason.smith@prelude-learning.com</a>
        <a href="https://prelude-learning.com">prelude-learning.com</a>
      </div>
    </div>
    <div class="foot-bottom">
      <p>© <span id="yr"></span> Prelude Learning &amp; Consultancy Ltd. All rights reserved.</p>
      <p>Learning Designed for Impact</p>
    </div>
  </div>
</footer>

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

def photo(cap, tag, ratio="wide"):
    return f'''<div class="photo-frame {ratio}"><img class="ph-mark" src="assets/logo/prelude-icon.svg" alt=""><div class="ph-cap">{cap}</div><div class="ph-tag">{tag}</div></div>'''

def photo_grid(items, cols="3"):
    cells = "".join(photo(c, t, "tall") for c, t in items)
    cls = "photo-grid" + (" cols-2" if cols == "2" else "")
    return f'<div class="{cls} reveal">{cells}</div>'

def page(filename, title, desc, body, active, keywords="", og="website", extra_body=""):
    html = head(title, desc, keywords, og) + nav(active) + body + extra_body + footer()
    with open(filename, "w") as f:
        f.write(html)
    print("wrote", filename)

# ------------------------------------------------------------------ helpers
def acc_item(num, title, ch, appr, out, ex, is_open=False):
    chli = "".join(f"<li>{x}</li>" for x in ch)
    outli = "".join(f"<li>{x}</li>" for x in out)
    op = " open" if is_open else ""
    return f'''      <div class="acc-item{op}">
        <button class="acc-head"><span class="acc-num">{num}</span><span class="acc-title">{title}</span><span class="plus" aria-hidden="true"></span></button>
        <div class="acc-body"><div class="acc-body-inner">
          <div class="acc-block"><h4>Client challenges</h4><ul>{chli}</ul></div>
          <div class="acc-block"><h4>My approach</h4><p>{appr}</p></div>
          <div class="acc-block"><h4>Outcomes</h4><ul>{outli}</ul></div>
          <div class="acc-block"><h4>Example</h4><p>{ex}</p></div>
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

def case(sector_attr, sector_label, title, metric_fig, metric_label, problem, why, found, did, results, benefit, lessons, visual, count=None, suffix=""):
    didli = "".join(f"<li>{x}</li>" for x in did)
    resli = "".join(f"<li>{x}</li>" for x in results)
    if count:
        fig = f'<div class="figure" data-count="{count}" data-suffix="{suffix}">0</div>'
    else:
        fig = f'<div class="figure">{metric_fig}</div>'
    return f'''    <article class="case reveal" data-sector="{sector_attr}">
      <div class="case-aside">
        <div class="case-sector">{sector_label}</div>
        <h3>{title}</h3>
        <div class="case-metric">{fig}<div class="label">{metric_label}</div></div>
        <div class="photo-frame tall" style="margin-top:18px"><img class="ph-mark" src="assets/logo/prelude-icon.svg" alt=""><div class="ph-cap">{visual}</div><div class="ph-tag">Visual slot</div></div>
      </div>
      <div class="case-body">
        <div class="cb"><h4>The problem</h4><p>{problem}</p></div>
        <div class="cb"><h4>Why it mattered</h4><p>{why}</p></div>
        <div class="cb"><h4>What I found</h4><p>{found}</p></div>
        <div class="cb"><h4>What I did</h4><ul>{didli}</ul></div>
        <div class="cb"><h4>Results</h4><ul>{resli}</ul></div>
        <div class="cb"><h4>Client benefit</h4><p>{benefit}</p></div>
        <div class="cb"><h4>Lessons learned</h4><p>{lessons}</p></div>
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
    <p class="hero-sub reveal in" data-d="2">Training is rarely the problem. Capability is. When readiness slips, compliance fails or managers aren't performing, the cause is almost never a missing course. As a capability, readiness and workforce development advisor, I diagnose the real problem first — then use learning as one of several tools to fix it. 15+ years, DSAT specialist, Active SC clearance.</p>
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
      <div class="metric"><div class="figure" data-count="15000">0</div><div class="label">Employees supported across a single organisation</div></div>
      <div class="metric"><div class="figure" data-count="25" data-suffix="%">0</div><div class="label">Improvement in operational performance (up to)</div></div>
      <div class="metric"><div class="figure" data-count="95" data-suffix="%">0</div><div class="label">Apprenticeship completion rate</div></div>
      <div class="metric"><div class="figure" data-count="100" data-suffix="%">0</div><div class="label">Funding compliance</div></div>
      <div class="metric"><div class="figure">4 <span class="unit">sectors</span></div><div class="label">Defence, Healthcare, Housing &amp; Public Sector</div></div>
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
        <a class="ch-foot" href="services.html">How I help healthcare →</a>
      </div>
      <div class="challenge-col reveal" data-d="2">
        <div class="ch-head"><img src="assets/icons/sector-housing.svg" alt=""><h3>Housing &amp; Public Sector</h3></div>
        <ul><li>Manager development</li><li>Onboarding effectiveness</li><li>Succession planning</li><li>Cultural transformation</li><li>Workforce capability</li></ul>
        <a class="ch-foot" href="services.html">How I help housing &amp; public sector →</a>
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
    {photo_grid([("Senior leaders reviewing operational plans","Defence environment"),("Defence headquarters / planning room","Defence environment"),("Training governance workshop in session","Defence environment")], cols="3")}
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
{cta("Need DSAT or capability support?", "Tell me what you're facing — JSP 822, governance, TNA or readiness. A practical conversation, no sales pitch.", secondary=("View services", "services.html"))}'''

# ================================================================== ABOUT
about_body = f'''<header class="page-hero">
  <div class="wrap">
    <div class="eyebrow reveal in">About</div>
    <h1 class="reveal in" data-d="1">15+ years building capability where the stakes are real.</h1>
    <p class="hero-sub reveal in" data-d="2">I'm Jason Smith. From Royal Navy operational leadership to advising large organisations on capability, readiness and assurance — I solve the problems training alone never fixes.</p>
  </div>
</header>

<div class="divider"></div>

<section>
  <div class="wrap split">
    <div class="reveal stack-gap">
      <div class="eyebrow">My background</div>
      <p>My career began in the Royal Navy, where I spent years in operational leadership — responsible for people, performance and readiness in demanding, high-pressure environments. There, capability isn't a slide in a deck; it's whether your team can deliver when it matters.</p>
      <p>Over 15+ years I've moved from operational leadership into capability development and workforce performance — building training and assurance to exacting Defence standards, and learning to connect what happens on the ground with what the board needs to see.</p>
      <p>Today I bring that perspective to Defence, Healthcare, Housing and the wider public sector as an independent capability advisor — someone who has actually operated inside the environments my clients work in.</p>
    </div>
    <div class="reveal" data-d="2">
      <div class="photo-frame"><img class="ph-mark" src="assets/logo/prelude-icon.svg" alt="">Professional photograph<br>of Jason Smith</div>
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
      <div class="metric"><div class="figure" data-count="15" data-suffix="+">0</div><div class="label">Years in capability, leadership &amp; readiness</div></div>
      <div class="metric"><div class="figure" data-count="15000">0</div><div class="label">Staff supported across a single organisation</div></div>
      <div class="metric"><div class="figure" data-count="95" data-suffix="%">0</div><div class="label">Apprenticeship completion rate</div></div>
      <div class="metric"><div class="figure" data-count="25" data-suffix="%">0</div><div class="label">Operational performance improvement (up to)</div></div>
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
        "DSAT-aligned analysis and governance for MOD Digital Skills for Defence.", is_open=True)
    + acc_item("02", "Training Needs Analysis",
        ["Investing in training without knowing the true gap", "Symptoms treated instead of causes", "No baseline to measure improvement"],
        "A structured TNA that separates capability problems from training problems using evidence, so investment goes where it moves performance.",
        ["Evidence-based recommendations", "A clear baseline and priorities", "Confidence that spend is targeted"],
        "DSAT-compliant TNA underpinning a 17% increase in pass rates on Royal Navy / NATO programmes.")
    + acc_item("03", "Capability Framework Design",
        ["No consistent competency standards", "Roles and skills defined differently across teams", "Hard to plan workforce or measure readiness"],
        "I design multi-specialisation capability frameworks, map skills to roles, and make them usable for assessment, development and planning.",
        ["Consistent, defensible standards", "Skills mapping and workforce planning", "Improved operational readiness"],
        "Multi-specialisation Defence framework contributing to a 20% increase in operational readiness.")
    + acc_item("04", "Training Governance &amp; Assurance",
        ["Governance that can't keep pace with delivery", "Assurance that doesn't reassure", "Risk hidden until audit"],
        "I build governance and assurance that is both audit-ready and useful — giving leaders confidence and inspectors evidence.",
        ["Trustworthy assurance evidence", "Clear governance and ownership", "Reduced compliance risk"],
        "Training governance embedded across DS4D and operational training programmes.")
)
lead_wf = (
    acc_item("05", "Leadership Development",
        ["Technically strong people promoted without support", "Inconsistent leadership under pressure", "Development that doesn't transfer to the job"],
        "Leadership and management development grounded in real operational experience and CMI-aligned coaching — building judgement and confidence.",
        ["Leaders who carry capability through change", "Consistent leadership standards", "Stronger succession and retention"],
        "Leadership pathways and values-based onboarding for a housing association, cutting time-to-competence by 20%.")
    + acc_item("06", "Talent Development",
        ["Talent leaving before it matures", "No clear development pathways", "Over-reliance on recruitment"],
        "Structured talent and development pathways that grow capability from within and give people a reason to stay.",
        ["A sustainable internal pipeline", "Clear progression", "Reduced recruitment cost and risk"],
        "Coaching and structured pathways driving 95% apprenticeship completion.")
    + acc_item("07", "Workforce Planning",
        ["Capability and demand out of step", "Roles unclear during change or scaling", "No line of sight from skills to mission"],
        "I align roles, skills and structure to operational demand — so the workforce is ready for what's coming, not just what's here.",
        ["Roles and skills aligned to demand", "Clearer structure under change", "Improved readiness"],
        "Role architecture redesign during national crisis response (OP ISOTROPE), improving response effectiveness by 15%.")
    + acc_item("08", "Apprenticeships",
        ["Low completion rates", "Funding compliance risk", "Programmes that don't build real capability"],
        "Structured pathways, coaching and active progress management that keep learners on track and funding compliant throughout.",
        ["95% completion rates", "100% funding compliance", "Genuine capability, not just certificates"],
        "Defence Apprenticeship Success Programme — 95% completion, 100% funding compliance.")
)
learn_tx = (
    acc_item("09", "Digital Learning",
        ["Digital learning bought but underused", "Content that doesn't change behaviour", "Transformation that stalls after launch"],
        "Digital and blended learning designed for outcomes and adoption — so modernisation improves performance, not just format.",
        ["Higher engagement and completion", "Measurable performance gains", "Sustainable, adopted change"],
        "Blended and e-learning interventions reducing failure rates by 20% on operational training.")
    + acc_item("10", "LMS Optimisation",
        ["An LMS that frustrates more than it helps", "Compliance reporting that can't be trusted", "Poor visibility of learning data"],
        "LMS optimisation — dashboards, pathways and information management (including Totara) that turn your platform into reliable capability intelligence.",
        ["Trustworthy compliance reporting", "Clear dashboards and pathways", "Reduced compliance gaps"],
        "Totara dashboards across 15,000 healthcare colleagues, cutting compliance gaps by 18%.")
    + acc_item("11", "Learning Operations",
        ["Learning delivery that's inconsistent or manual", "Effort spent on admin, not impact", "No reliable view of what's working"],
        "I streamline how learning is planned, delivered and measured — so the operation runs predictably and frees time for what matters.",
        ["More efficient delivery", "Consistent, repeatable processes", "Better management information"],
        "Information management improvements across a 15,000-strong workforce.")
    + acc_item("12", "Learning Strategy",
        ["Learning disconnected from organisational goals", "Activity measured instead of impact", "No coherent direction for investment"],
        "A clear learning strategy that aligns capability investment to organisational performance — with a practical, fundable roadmap.",
        ["Learning aligned to goals", "Stronger value for money", "A roadmap leaders can back"],
        "Strategic learning architecture and roadmaps for enterprise Defence capability planning.")
)
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

# ================================================================== CASE STUDIES
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
  "Capability map &amp; learning architecture")}
{case("defence","Defence · DSAT","Senior Information Officer (SIO) Course — Rapid TNA",None,"Speed and governance, together",
  "A Senior Information Officer course needed analysis at pace — but the team feared that moving quickly would mean cutting DSAT corners and losing defensibility.",
  "Many believe Defence change is slow because of DSAT. In reality, DSAT is often treated as a process to complete rather than a framework to support decision-making — and that, not governance itself, is what slows things down.",
  "Used as a decision-support framework rather than a box-ticking process, DSAT could move fast. The real constraints were unclear current requirements and undefined future role needs — not the methodology.",
  ["Conducted a rapid, focused Training Needs Analysis","Identified immediate improvements that could be actioned at once","Assessed future role requirements and undertook new role analysis","Developed policy recommendations from the evidence","Maintained DSAT defensibility and JSP 822 compliance throughout"],
  ["Immediate, actionable improvements identified quickly","Future role requirements defined with evidence","Policy recommendations leaders could stand behind","Full DSAT defensibility and JSP 822 compliance preserved"],
  "The organisation proved it didn't have to choose between speed and governance — with the right approach, it achieved both.",
  "DSAT is a framework to support decisions, not a process to endure. Treated that way, it accelerates good decisions rather than delaying them.",
  "Rapid TNA diagnostic output")}
{case("defence","Defence","Defence Capability Framework Design",None,"Increase in operational readiness",
  "Competency standards were inconsistent, so people couldn't be assessed, developed or planned for in a consistent way.",
  "Inconsistent standards meant readiness couldn't be measured or trusted — a real operational risk.",
  "Each team was defining roles and competence differently, so 'ready' meant different things in different places.",
  ["Multi-specialisation capability framework","Skills mapping across roles","Workforce planning support"],
  ["Consistent, defensible standards","20% increase in operational readiness"],
  "A single, trusted view of capability that underpinned assessment, development and workforce planning.",
  "A framework only changes behaviour when it's usable for assessment and planning — not simply published.",
  "Capability framework snapshot", count="20", suffix="%")}
{case("defence","Defence · Crisis response","Operational Role Architecture Redesign (OP ISOTROPE)",None,"Improvement in response effectiveness",
  "A national crisis required the organisation to scale rapidly — but roles and skills weren't clear enough to do it cleanly.",
  "In a crisis, ambiguity costs time and effectiveness the organisation didn't have.",
  "Under crisis pace, role ambiguity — not individual skill — was the biggest drag on effectiveness.",
  ["Role architecture redesign","Skills alignment to operational need","Organisational structure improvements"],
  ["15% improvement in response effectiveness","Faster, clearer scaling"],
  "The organisation scaled at pace without losing clarity of role, accountability or capability.",
  "In a crisis, clarity of role beats volume of training every time.",
  "Role architecture diagram", count="15", suffix="%")}
{case("healthcare","Healthcare","Healthcare Learning Transformation",None,"Reduction in compliance gaps",
  "Across 15,000 colleagues, learning compliance and reporting were unreliable, leaving leaders blind to risk.",
  "In healthcare, compliance gaps aren't admin — they're patient safety and regulatory exposure.",
  "Compliance data existed, but it couldn't be trusted — so leaders were managing risk blind.",
  ["Totara dashboards","Structured learning pathways","Information management improvements"],
  ["18% reduction in compliance gaps","Clear visibility of learning risk"],
  "Leaders gained confidence in compliance reporting across a 15,000-strong workforce.",
  "Reliable data changes behaviour faster than more mandatory training.",
  "Compliance dashboard example", count="18", suffix="%")}
{case("housing","Housing","Housing Leadership &amp; Onboarding Transformation",None,"Reduction in time-to-competence",
  "Onboarding was slow and leadership development inconsistent, holding back performance and retention.",
  "Slow onboarding meant new colleagues took too long to contribute — and inconsistent leadership cost engagement.",
  "Onboarding was inconsistent and leadership expectations were unwritten, so new managers learned by chance.",
  ["Leadership development pathways","Values-based onboarding","Digital learning solutions"],
  ["20% reduction in time-to-competence","More consistent leadership"],
  "New colleagues became productive faster, under a consistent leadership standard.",
  "Values and expectations have to be designed into onboarding — not left to osmosis.",
  "Onboarding journey map", count="20", suffix="%")}
{case("defence","Defence","Defence Apprenticeship Success Programme",None,"Completion rate · 100% funding compliance",
  "Apprenticeship completion and qualification rates needed to improve, with funding compliance under scrutiny.",
  "Low completion wastes investment and risks funding — and fails the people on the programme.",
  "Drop-off was driven by weak progress management and support — not by learner ability.",
  ["Coaching and learner support","Progress management","Structured development pathways"],
  ["95% completion rate","100% funding compliance"],
  "A stronger internal pipeline and protected funding, with genuine capability built — not just qualifications gained.",
  "Completion is an operations problem as much as a teaching one.",
  "Progress governance example", count="95", suffix="%")}
{case("defence","Defence · NATO &amp; Royal Navy","NATO &amp; Royal Navy Training Modernisation",None,"Increase in pass rates · 20% fewer failures",
  "Established training needed to lift operational readiness and learner performance.",
  "Pass and failure rates directly affect how quickly capable people reach the front line.",
  "A DSAT-compliant TNA pinpointed the specific points in the pipeline where learners were being set up to fail.",
  ["DSAT-compliant TNA","Blended learning design","Coaching interventions","E-learning solutions"],
  ["17% increase in pass rates","20% reduction in failure rates"],
  "Higher readiness and better learner performance, with less wasted training effort.",
  "Target the few points that move pass rates, rather than redesigning everything.",
  "Learning pathway diagram", count="17", suffix="%")}
  </div>
</section>

{cta("Recognise your organisation in any of these?", "If so, let's talk about what it would take to get the same result for you.", secondary=("Explore services", "services.html"))}'''

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
      <form class="capture-form" action="https://formspree.io/f/your-form-id" method="POST">
        <input type="hidden" name="_subject" value="Resource request">
        <div class="field"><label for="r-resource">Resource</label><select id="r-resource" name="resource">{_res_opts}</select></div>
        <div class="field"><label for="r-email">Work email</label><input id="r-email" name="email" type="email" required placeholder="you@organisation.gov.uk"></div>
        <button type="submit" class="btn btn-primary">Send it to me {ARROW}</button>
      </form>
    </div>
    <p class="placeholder-note reveal" style="margin-top:18px">The form posts to a Formspree placeholder — connect it to your email tool / ESP before launch to capture and deliver to leads automatically.</p>
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
    <div class="eyebrow reveal">More insights</div>
    <div class="insight-grid">
      <article class="insight-card reveal"><div class="ic-top"><img src="assets/icons/governance.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Defence</span><h3>DSAT Explained</h3><p>What JSP 822 actually asks of you — without the acronym overload.</p><span class="read">Read the article →</span></div></article>
      <article class="insight-card reveal" data-d="1"><div class="ic-top"><img src="assets/icons/assurance.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Method</span><h3>Training Needs Analysis: Best Practice</h3><p>How to run a TNA that finds the real gap and gives leaders evidence.</p><span class="read">Read the article →</span></div></article>
      <article class="insight-card reveal" data-d="2"><div class="ic-top"><img src="assets/icons/capability.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Capability</span><h3>Building Capability Frameworks</h3><p>Designing competency frameworks people actually use.</p><span class="read">Read the article →</span></div></article>
      <article class="insight-card reveal"><div class="ic-top"><img src="assets/icons/leadership.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Leadership</span><h3>Leadership in High-Pressure Environments</h3><p>What the military teaches about leaders who hold up when it counts.</p><span class="read">Read the article →</span></div></article>
      <article class="insight-card reveal" data-d="1"><div class="ic-top"><img src="assets/icons/sector-public.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Public Sector</span><h3>Public Sector Workforce Development</h3><p>Building capability and pipelines under real budget pressure.</p><span class="read">Read the article →</span></div></article>
      <article class="insight-card reveal" data-d="2"><div class="ic-top"><img src="assets/icons/development.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Technology</span><h3>Learning Technology Lessons</h3><p>Why so many LMS investments underdeliver — and how to get value.</p><span class="read">Read the article →</span></div></article>
      <article class="insight-card reveal"><div class="ic-top"><img src="assets/icons/systems.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Talent</span><h3>Apprenticeship Success Strategies</h3><p>What drives 95% completion and 100% funding compliance.</p><span class="read">Read the article →</span></div></article>
      <article class="insight-card reveal" data-d="1"><div class="ic-top"><img src="assets/icons/sector-defence.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Defence</span><h3>Defence Training Governance</h3><p>Making governance audit-ready and useful — not just for inspectors.</p><span class="read">Read the article →</span></div></article>
      <article class="insight-card reveal" data-d="2"><div class="ic-top"><img src="assets/icons/readiness.svg" alt=""></div><div class="ic-body"><span class="ic-cat">Readiness</span><h3>From Training to Readiness</h3><p>Connecting learning investment to the outcomes leaders are measured on.</p><span class="read">Read the article →</span></div></article>
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
      <form class="form" action="https://formspree.io/f/your-form-id" method="POST">
        <div class="row">
          <div class="field"><label for="name">Name</label><input id="name" name="name" type="text" required placeholder="Your name"></div>
          <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" required placeholder="you@organisation.gov.uk"></div>
        </div>
        <div class="row">
          <div class="field"><label for="org">Organisation</label><input id="org" name="organisation" type="text" placeholder="Your organisation"></div>
          <div class="field"><label for="sector">Sector</label>
            <select id="sector" name="sector"><option>Defence</option><option>Healthcare / NHS</option><option>Housing</option><option>Public sector / Government</option><option>Other</option></select>
          </div>
        </div>
        <div class="field"><label for="message">What capability challenge are you facing?</label><textarea id="message" name="message" required placeholder="A few lines on the problem you're trying to solve..."></textarea></div>
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

{cta("\\\"Jason understands my environment, my problem, and has solved this before.\\\"", "That's the conversation I want to have with you.")}'''

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
    {photo_grid([("Strategic planning session — leaders reviewing options around a table","Defence / Public sector"),("Capability review workshop in a headquarters environment","Defence"),("One-to-one advisory / coaching conversation","Leadership")], cols="3")}
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
     "Training is rarely the problem. Capability is. Jason Smith is a capability, readiness and workforce development advisor helping Defence and public sector organisations diagnose the real problem and build capability. DSAT specialist, 15+ years, Active SC.",
     home_body, "home")

page("defence.html", "DSAT Consultant | JSP 822 &amp; Defence Training Governance | Prelude",
     "Defence capability and DSAT consultancy for MOD, Defence Digital, DE&S, Front Line Commands and prime contractors. JSP 822, Training Needs Analysis, capability frameworks, training governance and readiness.",
     defence_body, "defence",
     keywords="DSAT Consultant, JSP 822 Consultant, Defence Training Governance, Training Needs Analysis, Defence Capability Development")

page("about.html", "About Jason Smith — Royal Navy Leader &amp; Capability Advisor | Prelude",
     "15+ years building capability where the stakes are real: Royal Navy operational leadership, Defence capability specialism, Korn Ferry consultant, independent capability advisor.",
     about_body, "about", og="profile")

page("services.html", "Services — Capability &amp; Governance, Leadership &amp; Workforce, Learning Transformation | Prelude",
     "Capability consultancy grouped around your problem: DSAT, TNA, capability frameworks and governance; leadership, talent, workforce planning and apprenticeships; digital learning, LMS, learning operations and strategy.",
     services_body, "services")

page("case-studies.html", "Case Studies — Defence, Healthcare &amp; Housing Capability Projects | Prelude",
     "Capability, governance and learning projects across Defence, Healthcare and Housing — the problem, why it mattered, what I did, the results and the client benefit.",
     cs_body, "case-studies")

page("insights.html", "Insights &amp; Resources — DSAT, TNA, Capability &amp; Governance Tools | Prelude",
     "Free diagnostics and templates plus plain-English thinking on DSAT, training needs analysis, capability frameworks, leadership and defence training governance.",
     insights_body, "insights",
     keywords="DSAT, JSP 822, Training Needs Analysis checklist, capability framework template, learning governance health check, leadership diagnostic")

page("contact.html", "Contact — Discuss Your Capability Challenge | Jason Smith, Prelude",
     "Discuss your capability, readiness or training governance challenge with Jason Smith. A practical, problem-first conversation — no sales pitch. Defence, Healthcare, Housing and public sector.",
     contact_body, "contact")

page("capability-readiness-review.html", "The Capability Readiness Review&trade; — Free Diagnostic | Prelude",
     "Find the real problem before you invest. A 10-question Capability Readiness Review self-assessment for Defence and public sector leaders — capability, leadership, process, governance, workforce or training.",
     crr_body, "crr", extra_body='<script src="crr.js"></script>\n')

page("how-i-work.html", "How I Work — A Clear Five-Stage Capability Engagement | Prelude",
     "Exactly what to expect when you work with Jason Smith: discovery and Capability Review, analysis and diagnosis, design, implementation support, and measurement — senior delivery, evidence-led, no lock-in.",
     howiwork_body, "how-i-work")

page("why-training-isnt-the-problem.html", "Why Training Isn't the Problem — The Prelude Manifesto",
     "Training is rarely the problem. Capability is. The Prelude manifesto on why performance gaps aren't training gaps, why diagnosis must come before prescription, and how the Prelude Capability Model works.",
     manifesto_body, "insights",
     keywords="capability not training, performance gap, training needs analysis, capability diagnosis, Prelude Capability Model")

page("who-i-help.html", "Who I Help — Capability Support by Role | Prelude",
     "Capability, readiness and workforce development support for Defence Programme Leaders, Capability Managers, Heads of L&D, Training Governance Leads, NHS Workforce Leads, People Directors, Housing leadership and Transformation Leaders.",
     whoihelp_body, "")

print("done")
