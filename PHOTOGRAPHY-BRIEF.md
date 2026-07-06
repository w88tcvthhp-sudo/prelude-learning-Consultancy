# Prelude — Photography / Image Brief

The site uses styled placeholder frames wherever a photograph belongs. Replace each
with real or AI-generated imagery. Keep the tone consistent: **professional,
realistic, strategic, slightly desaturated, low-key lighting**. Avoid smiling stock
photos, posed handshakes, or clichéd "teamwork" shots. Faces can be out of focus,
turned away, or implied — the subject is the environment and the work, not models.

Suggested colour treatment: cool/green-tinted, deep shadows, to sit with the Deep
Forest (#081D16) / Emerald (#0E7A5A) palette. 16:9 or 3:4. Export at 2x.

## Ready-to-use generation prompts (Midjourney / DALL·E / Firefly style)

DEFENCE
- "Senior military and civilian leaders reviewing operational plans around a table in a low-lit briefing room, large screens with maps, shot from behind, cinematic, desaturated green tone, documentary realism, no faces to camera"
- "Modern defence headquarters interior, planning room with glass partitions and subtle screen glow, empty and architectural, moody low-key lighting, wide angle"
- "Training governance workshop in progress, whiteboards and printed frameworks on the wall, people seen from behind collaborating, realistic, muted tones"
- "Digital capability programme — analysts at workstations in a secure operations centre, screen light, shallow depth of field, serious atmosphere"

HEALTHCARE
- "Healthcare leadership team in a strategy meeting in a modern NHS-style boardroom, viewed from the side, documentary style, calm muted palette, no direct eye contact"
- "Workforce planning meeting, people around a table with laptops and printed dashboards, realistic, soft daylight, restrained"
- "Learning technology environment — a clinician using an LMS on a tablet in a quiet corridor, shallow focus, professional"

HOUSING
- "Community-focused leadership meeting in a housing association office, practical and grounded, people from behind, natural light, realistic"
- "Frontline housing service delivery — a manager walking through a residential development, overcast, documentary realism"
- "Management development workshop, flip charts and notes, collaborative, candid, muted colour"

PUBLIC SECTOR
- "Public sector transformation programme working session, sticky notes and roadmaps on glass, people mid-discussion seen from behind, realistic, cool tones"
- "Capability review — two professionals examining printed competency frameworks at a desk, close, serious, shallow depth of field"
- "Stakeholder engagement session in a government building, neutral architecture, candid, low-key lighting"

## Slot locations in the build
- about.html ............ portrait of Jason (3:4) — replace the `.photo-frame`
- defence.html ......... 3 environment shots (operational plans / HQ / governance workshop)
- how-i-work.html ...... 3 shots (planning session / capability workshop / advisory conversation)
- case-studies.html .... one supporting visual per study (framework snapshot, dashboard, map, etc.)

To swap a placeholder for a real image, replace the `<div class="photo-frame ...">...</div>`
with `<img src="assets/photos/your-image.jpg" alt="..." style="width:100%;border-radius:6px">`
and drop the file into a new `assets/photos/` folder.
