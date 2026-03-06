"""CV template renderer - generates HTML from CV data using templates."""
from jinja2 import Environment, BaseLoader
from typing import Optional

# ============================================================
# TEMPLATE REGISTRY
# ============================================================

TEMPLATES = {}


def _register(name: str, display: str, description: str, preview_color: str, html: str):
    TEMPLATES[name] = {
        "id": name,
        "name": display,
        "description": description,
        "preview_color": preview_color,
        "html": html,
    }


def get_available_templates() -> list[dict]:
    return [
        {"id": t["id"], "name": t["name"], "description": t["description"], "preview_color": t["preview_color"]}
        for t in TEMPLATES.values()
    ]


def render_cv_html(template_id: str, cv_data: dict) -> str:
    template = TEMPLATES.get(template_id, TEMPLATES.get("modern"))
    env = Environment(loader=BaseLoader())
    tmpl = env.from_string(template["html"])
    return tmpl.render(**cv_data, template_id=template_id)


# ============================================================
# SHARED CSS HELPERS
# ============================================================

_RESET = """
* { margin: 0; padding: 0; box-sizing: border-box; }
html { font-size: 14px; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; color: #1a1a1a; line-height: 1.5; }
a { color: inherit; text-decoration: none; }
ul { list-style: none; }
.page { max-width: 850px; margin: 0 auto; padding: 40px 50px; background: #fff; }
@media print { .page { padding: 30px 40px; } }
"""

# ============================================================
# TEMPLATE 1: MODERN
# ============================================================
_register("modern", "Modern", "Clean modern design with accent color sidebar header", "#2563eb", """
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width">
<style>
""" + _RESET + """
.header { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 30px 40px; margin: -40px -50px 25px; }
.header h1 { font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; }
.header .title { font-size: 1.1rem; opacity: 0.9; margin-top: 4px; }
.contact { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 12px; font-size: 0.85rem; opacity: 0.85; }
.contact span::before { content: '·'; margin-right: 6px; }
.contact span:first-child::before { content: ''; margin: 0; }
.section { margin-bottom: 20px; }
.section-title { font-size: 1rem; font-weight: 700; color: #2563eb; text-transform: uppercase; letter-spacing: 1.5px; border-bottom: 2px solid #2563eb; padding-bottom: 4px; margin-bottom: 12px; }
.summary { color: #374151; font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px; }
.exp-item { margin-bottom: 14px; }
.exp-header { display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; }
.exp-header h3 { font-size: 1rem; font-weight: 600; }
.exp-header .company { color: #2563eb; }
.exp-header .dates { font-size: 0.85rem; color: #6b7280; }
.exp-bullets li { padding-left: 16px; position: relative; margin-bottom: 3px; font-size: 0.9rem; color: #374151; }
.exp-bullets li::before { content: '▸'; position: absolute; left: 0; color: #2563eb; }
.skills-grid { display: flex; flex-wrap: wrap; gap: 6px; }
.skill-tag { background: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500; }
.edu-item { margin-bottom: 8px; }
.edu-item h3 { font-size: 0.95rem; font-weight: 600; }
.edu-item .school { color: #6b7280; font-size: 0.85rem; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
@media (max-width: 600px) { .two-col { grid-template-columns: 1fr; } .header { padding: 20px; margin: -40px -50px 20px; } }
</style></head><body><div class="page">
<div class="header">
  <h1>{{ full_name }}</h1>
  {% if title %}<div class="title">{{ title }}</div>{% endif %}
  <div class="contact">
    {% if email %}<span>{{ email }}</span>{% endif %}
    {% if phone %}<span>{{ phone }}</span>{% endif %}
    {% if location %}<span>{{ location }}</span>{% endif %}
    {% if linkedin %}<span>{{ linkedin }}</span>{% endif %}
    {% if github %}<span>{{ github }}</span>{% endif %}
    {% if portfolio %}<span>{{ portfolio }}</span>{% endif %}
  </div>
</div>

{% if summary %}<div class="summary">{{ summary }}</div>{% endif %}

{% if experience %}
<div class="section">
  <div class="section-title">Experience</div>
  {% for job in experience %}
  <div class="exp-item">
    <div class="exp-header">
      <h3>{{ job.title }} <span class="company">@ {{ job.company }}</span></h3>
      <span class="dates">{{ job.start }} – {{ job.end or 'Present' }}</span>
    </div>
    {% if job.bullets %}
    <ul class="exp-bullets">{% for b in job.bullets %}<li>{{ b }}</li>{% endfor %}</ul>
    {% endif %}
  </div>
  {% endfor %}
</div>
{% endif %}

<div class="two-col">
<div>
{% if skills %}
<div class="section">
  <div class="section-title">Skills</div>
  <div class="skills-grid">{% for s in skills %}<span class="skill-tag">{{ s }}</span>{% endfor %}</div>
</div>
{% endif %}

{% if languages %}
<div class="section">
  <div class="section-title">Languages</div>
  {% for l in languages %}<div>{{ l.language }} – {{ l.level }}</div>{% endfor %}
</div>
{% endif %}
</div>

<div>
{% if education %}
<div class="section">
  <div class="section-title">Education</div>
  {% for e in education %}
  <div class="edu-item">
    <h3>{{ e.degree }}</h3>
    <div class="school">{{ e.school }}{% if e.year %} · {{ e.year }}{% endif %}{% if e.gpa %} · GPA: {{ e.gpa }}{% endif %}</div>
  </div>
  {% endfor %}
</div>
{% endif %}

{% if certifications %}
<div class="section">
  <div class="section-title">Certifications</div>
  {% for c in certifications %}<div>{{ c.name }}{% if c.issuer %} – {{ c.issuer }}{% endif %}{% if c.year %} ({{ c.year }}){% endif %}</div>{% endfor %}
</div>
{% endif %}
</div>
</div>

{% if projects %}
<div class="section">
  <div class="section-title">Projects</div>
  {% for p in projects %}
  <div class="exp-item">
    <h3>{{ p.name }}{% if p.url %} <a href="{{ p.url }}" style="color:#2563eb;font-size:0.85rem">↗</a>{% endif %}</h3>
    <p style="font-size:0.9rem;color:#374151">{{ p.description }}</p>
    {% if p.tech %}<div style="font-size:0.8rem;color:#6b7280;margin-top:2px">Tech: {{ p.tech if p.tech is string else p.tech | join(', ') }}</div>{% endif %}
  </div>
  {% endfor %}
</div>
{% endif %}
</div></body></html>
""")

# ============================================================
# TEMPLATE 2: CLASSIC
# ============================================================
_register("classic", "Classic", "Traditional professional layout, timeless and elegant", "#1f2937", """
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width">
<style>
""" + _RESET + """
body { font-family: 'Georgia', 'Times New Roman', serif; }
.header { text-align: center; border-bottom: 2px solid #1f2937; padding-bottom: 15px; margin-bottom: 20px; }
.header h1 { font-size: 2rem; font-weight: 400; letter-spacing: 3px; text-transform: uppercase; }
.header .title { font-size: 1rem; color: #4b5563; margin-top: 4px; font-style: italic; }
.contact { display: flex; justify-content: center; flex-wrap: wrap; gap: 15px; margin-top: 8px; font-size: 0.85rem; color: #4b5563; }
.section { margin-bottom: 18px; }
.section-title { font-size: 0.95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; border-bottom: 1px solid #d1d5db; padding-bottom: 3px; margin-bottom: 10px; }
.summary { font-style: italic; color: #374151; line-height: 1.6; margin-bottom: 18px; text-align: center; }
.exp-item { margin-bottom: 14px; }
.exp-header { display: flex; justify-content: space-between; flex-wrap: wrap; }
.exp-header h3 { font-size: 1rem; }
.exp-header .dates { font-size: 0.85rem; color: #6b7280; font-style: italic; }
.exp-bullets { margin-top: 4px; }
.exp-bullets li { padding-left: 18px; position: relative; margin-bottom: 3px; font-size: 0.9rem; }
.exp-bullets li::before { content: '—'; position: absolute; left: 0; color: #9ca3af; }
.skills-list { font-size: 0.9rem; color: #374151; }
.edu-item { margin-bottom: 6px; }
.edu-item h3 { font-size: 0.95rem; }
.edu-item .school { color: #6b7280; font-size: 0.85rem; }
</style></head><body><div class="page">
<div class="header">
  <h1>{{ full_name }}</h1>
  {% if title %}<div class="title">{{ title }}</div>{% endif %}
  <div class="contact">
    {% if email %}<span>{{ email }}</span>{% endif %}
    {% if phone %}<span>{{ phone }}</span>{% endif %}
    {% if location %}<span>{{ location }}</span>{% endif %}
    {% if linkedin %}<span>{{ linkedin }}</span>{% endif %}
    {% if github %}<span>{{ github }}</span>{% endif %}
  </div>
</div>

{% if summary %}<div class="summary">{{ summary }}</div>{% endif %}

{% if experience %}
<div class="section">
  <div class="section-title">Professional Experience</div>
  {% for job in experience %}
  <div class="exp-item">
    <div class="exp-header">
      <h3><strong>{{ job.title }}</strong>, {{ job.company }}</h3>
      <span class="dates">{{ job.start }} – {{ job.end or 'Present' }}</span>
    </div>
    {% if job.bullets %}<ul class="exp-bullets">{% for b in job.bullets %}<li>{{ b }}</li>{% endfor %}</ul>{% endif %}
  </div>
  {% endfor %}
</div>
{% endif %}

{% if education %}
<div class="section">
  <div class="section-title">Education</div>
  {% for e in education %}
  <div class="edu-item">
    <h3><strong>{{ e.degree }}</strong></h3>
    <div class="school">{{ e.school }}{% if e.year %}, {{ e.year }}{% endif %}{% if e.gpa %} — GPA: {{ e.gpa }}{% endif %}</div>
  </div>
  {% endfor %}
</div>
{% endif %}

{% if skills %}
<div class="section">
  <div class="section-title">Skills</div>
  <div class="skills-list">{{ skills | join(' · ') }}</div>
</div>
{% endif %}

{% if projects %}
<div class="section">
  <div class="section-title">Projects</div>
  {% for p in projects %}
  <div class="exp-item">
    <h3><strong>{{ p.name }}</strong></h3>
    <p style="font-size:0.9rem">{{ p.description }}</p>
  </div>
  {% endfor %}
</div>
{% endif %}

{% if certifications %}
<div class="section">
  <div class="section-title">Certifications</div>
  {% for c in certifications %}<div style="font-size:0.9rem">{{ c.name }}{% if c.issuer %}, {{ c.issuer }}{% endif %}{% if c.year %} ({{ c.year }}){% endif %}</div>{% endfor %}
</div>
{% endif %}

{% if languages %}
<div class="section">
  <div class="section-title">Languages</div>
  <div class="skills-list">{% for l in languages %}{{ l.language }} ({{ l.level }}){% if not loop.last %} · {% endif %}{% endfor %}</div>
</div>
{% endif %}
</div></body></html>
""")

# ============================================================
# TEMPLATE 3: MINIMAL
# ============================================================
_register("minimal", "Minimal", "Ultra-clean with maximum whitespace, content-focused", "#111827", """
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width">
<style>
""" + _RESET + """
body { font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif; font-size: 13px; color: #111827; }
.page { padding: 50px 60px; }
.header h1 { font-size: 1.8rem; font-weight: 300; letter-spacing: -0.5px; }
.header .title { font-size: 0.95rem; color: #6b7280; font-weight: 300; }
.contact { margin-top: 6px; font-size: 0.8rem; color: #9ca3af; }
.contact span + span::before { content: '  /  '; }
.divider { height: 1px; background: #e5e7eb; margin: 20px 0; }
.section { margin-bottom: 18px; }
.section-title { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 3px; color: #9ca3af; margin-bottom: 10px; }
.summary { color: #4b5563; line-height: 1.7; font-size: 0.9rem; }
.exp-item { margin-bottom: 14px; }
.exp-item h3 { font-size: 0.95rem; font-weight: 500; }
.exp-meta { font-size: 0.8rem; color: #9ca3af; margin-bottom: 4px; }
.exp-bullets li { font-size: 0.85rem; color: #4b5563; margin-bottom: 2px; padding-left: 12px; position: relative; }
.exp-bullets li::before { content: '–'; position: absolute; left: 0; color: #d1d5db; }
.skill-row { font-size: 0.85rem; color: #4b5563; line-height: 1.8; }
</style></head><body><div class="page">
<div class="header">
  <h1>{{ full_name }}</h1>
  {% if title %}<div class="title">{{ title }}</div>{% endif %}
  <div class="contact">
    {% if email %}<span>{{ email }}</span>{% endif %}
    {% if phone %}<span>{{ phone }}</span>{% endif %}
    {% if location %}<span>{{ location }}</span>{% endif %}
    {% if linkedin %}<span>{{ linkedin }}</span>{% endif %}
    {% if github %}<span>{{ github }}</span>{% endif %}
  </div>
</div>
<div class="divider"></div>

{% if summary %}<div class="summary">{{ summary }}</div><div class="divider"></div>{% endif %}

{% if experience %}
<div class="section">
  <div class="section-title">Experience</div>
  {% for job in experience %}
  <div class="exp-item">
    <h3>{{ job.title }}</h3>
    <div class="exp-meta">{{ job.company }} · {{ job.start }} – {{ job.end or 'Present' }}</div>
    {% if job.bullets %}<ul class="exp-bullets">{% for b in job.bullets %}<li>{{ b }}</li>{% endfor %}</ul>{% endif %}
  </div>
  {% endfor %}
</div>
{% endif %}

{% if skills %}
<div class="section">
  <div class="section-title">Skills</div>
  <div class="skill-row">{{ skills | join('  ·  ') }}</div>
</div>
{% endif %}

{% if education %}
<div class="section">
  <div class="section-title">Education</div>
  {% for e in education %}
  <div style="margin-bottom:6px">
    <strong style="font-weight:500">{{ e.degree }}</strong><br>
    <span style="color:#9ca3af;font-size:0.8rem">{{ e.school }}{% if e.year %} · {{ e.year }}{% endif %}</span>
  </div>
  {% endfor %}
</div>
{% endif %}

{% if projects %}
<div class="section">
  <div class="section-title">Projects</div>
  {% for p in projects %}
  <div style="margin-bottom:8px">
    <strong style="font-weight:500">{{ p.name }}</strong>
    <div style="font-size:0.85rem;color:#4b5563">{{ p.description }}</div>
  </div>
  {% endfor %}
</div>
{% endif %}
</div></body></html>
""")

# ============================================================
# TEMPLATE 4: CREATIVE
# ============================================================
_register("creative", "Creative", "Bold design with color blocks, perfect for designers and creatives", "#7c3aed", """
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width">
<style>
""" + _RESET + """
body { font-family: 'Segoe UI', system-ui, sans-serif; }
.page { display: grid; grid-template-columns: 280px 1fr; min-height: 100vh; padding: 0; max-width: 900px; }
.sidebar { background: linear-gradient(180deg, #7c3aed 0%, #5b21b6 100%); color: white; padding: 40px 25px; }
.sidebar h1 { font-size: 1.5rem; font-weight: 700; margin-bottom: 4px; }
.sidebar .title { font-size: 0.9rem; opacity: 0.8; }
.sidebar .section { margin-top: 25px; }
.sidebar .section-title { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; opacity: 0.6; margin-bottom: 8px; }
.sidebar .contact-item { font-size: 0.8rem; margin-bottom: 4px; opacity: 0.9; }
.sidebar .skill-tag { display: inline-block; background: rgba(255,255,255,0.15); padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; margin: 2px; }
.sidebar .lang-item { font-size: 0.8rem; margin-bottom: 3px; }
.main { padding: 40px 35px; }
.main .section { margin-bottom: 22px; }
.main .section-title { font-size: 0.85rem; font-weight: 700; color: #7c3aed; text-transform: uppercase; letter-spacing: 1.5px; padding-bottom: 4px; border-bottom: 2px solid #7c3aed; margin-bottom: 12px; }
.summary { font-size: 0.9rem; color: #4b5563; line-height: 1.6; padding: 12px; background: #faf5ff; border-left: 3px solid #7c3aed; border-radius: 0 6px 6px 0; }
.exp-item { margin-bottom: 16px; position: relative; padding-left: 15px; }
.exp-item::before { content: ''; position: absolute; left: 0; top: 8px; width: 6px; height: 6px; background: #7c3aed; border-radius: 50%; }
.exp-item h3 { font-size: 0.95rem; font-weight: 600; }
.exp-item .company { color: #7c3aed; font-weight: 500; }
.exp-item .dates { font-size: 0.8rem; color: #9ca3af; }
.exp-bullets li { font-size: 0.85rem; color: #4b5563; margin-bottom: 2px; }
.edu-item { margin-bottom: 8px; }
.edu-item h3 { font-size: 0.9rem; }
.project-card { background: #faf5ff; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; }
.project-card h3 { font-size: 0.9rem; color: #7c3aed; }
.project-card p { font-size: 0.8rem; color: #4b5563; }
@media (max-width: 650px) { .page { grid-template-columns: 1fr; } .sidebar { padding: 25px; } }
@media print { .page { grid-template-columns: 250px 1fr; } }
</style></head><body><div class="page">
<div class="sidebar">
  <h1>{{ full_name }}</h1>
  {% if title %}<div class="title">{{ title }}</div>{% endif %}

  <div class="section">
    <div class="section-title">Contact</div>
    {% if email %}<div class="contact-item">{{ email }}</div>{% endif %}
    {% if phone %}<div class="contact-item">{{ phone }}</div>{% endif %}
    {% if location %}<div class="contact-item">{{ location }}</div>{% endif %}
    {% if linkedin %}<div class="contact-item">{{ linkedin }}</div>{% endif %}
    {% if github %}<div class="contact-item">{{ github }}</div>{% endif %}
    {% if portfolio %}<div class="contact-item">{{ portfolio }}</div>{% endif %}
  </div>

  {% if skills %}
  <div class="section">
    <div class="section-title">Skills</div>
    <div>{% for s in skills %}<span class="skill-tag">{{ s }}</span>{% endfor %}</div>
  </div>
  {% endif %}

  {% if languages %}
  <div class="section">
    <div class="section-title">Languages</div>
    {% for l in languages %}<div class="lang-item">{{ l.language }} – {{ l.level }}</div>{% endfor %}
  </div>
  {% endif %}

  {% if certifications %}
  <div class="section">
    <div class="section-title">Certifications</div>
    {% for c in certifications %}<div class="contact-item">{{ c.name }}{% if c.year %} ({{ c.year }}){% endif %}</div>{% endfor %}
  </div>
  {% endif %}

  {% if education %}
  <div class="section">
    <div class="section-title">Education</div>
    {% for e in education %}
    <div style="margin-bottom:8px">
      <div style="font-size:0.85rem;font-weight:600">{{ e.degree }}</div>
      <div style="font-size:0.75rem;opacity:0.7">{{ e.school }}{% if e.year %} · {{ e.year }}{% endif %}</div>
    </div>
    {% endfor %}
  </div>
  {% endif %}
</div>

<div class="main">
  {% if summary %}
  <div class="section">
    <div class="summary">{{ summary }}</div>
  </div>
  {% endif %}

  {% if experience %}
  <div class="section">
    <div class="section-title">Experience</div>
    {% for job in experience %}
    <div class="exp-item">
      <h3>{{ job.title }} <span class="company">@ {{ job.company }}</span></h3>
      <div class="dates">{{ job.start }} – {{ job.end or 'Present' }}</div>
      {% if job.bullets %}<ul class="exp-bullets">{% for b in job.bullets %}<li>{{ b }}</li>{% endfor %}</ul>{% endif %}
    </div>
    {% endfor %}
  </div>
  {% endif %}

  {% if projects %}
  <div class="section">
    <div class="section-title">Projects</div>
    {% for p in projects %}
    <div class="project-card">
      <h3>{{ p.name }}</h3>
      <p>{{ p.description }}</p>
      {% if p.tech %}<div style="font-size:0.7rem;color:#7c3aed;margin-top:4px">{{ p.tech if p.tech is string else p.tech | join(' · ') }}</div>{% endif %}
    </div>
    {% endfor %}
  </div>
  {% endif %}
</div>
</div></body></html>
""")

# ============================================================
# TEMPLATE 5: TECH
# ============================================================
_register("tech", "Tech", "Developer-focused with monospace accents, dark header, code-inspired", "#0f172a", """
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width">
<style>
""" + _RESET + """
body { font-family: 'Segoe UI', system-ui, sans-serif; }
.header { background: #0f172a; color: #e2e8f0; padding: 30px 40px; margin: -40px -50px 25px; }
.header h1 { font-size: 1.8rem; font-weight: 700; font-family: 'SF Mono', 'Fira Code', monospace; }
.header h1 .accent { color: #38bdf8; }
.header .title { font-family: monospace; color: #94a3b8; font-size: 0.9rem; }
.header .title::before { content: '> '; color: #38bdf8; }
.contact { display: flex; flex-wrap: wrap; gap: 15px; margin-top: 10px; font-size: 0.8rem; font-family: monospace; color: #94a3b8; }
.section { margin-bottom: 20px; }
.section-title { font-family: monospace; font-size: 0.85rem; color: #0f172a; font-weight: 700; margin-bottom: 10px; padding: 4px 10px; background: #f1f5f9; border-left: 3px solid #38bdf8; }
.summary { font-size: 0.9rem; color: #475569; line-height: 1.6; padding: 10px; background: #f8fafc; border-radius: 4px; font-family: monospace; font-size: 0.85rem; }
.exp-item { margin-bottom: 14px; border-left: 2px solid #e2e8f0; padding-left: 14px; }
.exp-item h3 { font-size: 0.95rem; font-weight: 600; }
.exp-item .company { color: #38bdf8; }
.exp-item .dates { font-family: monospace; font-size: 0.8rem; color: #94a3b8; }
.exp-bullets li { font-size: 0.85rem; color: #475569; margin-bottom: 2px; padding-left: 14px; position: relative; }
.exp-bullets li::before { content: '→'; position: absolute; left: 0; color: #38bdf8; }
.skills-grid { display: flex; flex-wrap: wrap; gap: 6px; }
.skill-tag { font-family: monospace; font-size: 0.75rem; background: #0f172a; color: #38bdf8; padding: 3px 10px; border-radius: 3px; }
.edu-item h3 { font-size: 0.9rem; }
.edu-item .school { font-size: 0.8rem; color: #94a3b8; font-family: monospace; }
.project-item { background: #f8fafc; padding: 10px 14px; border-radius: 4px; margin-bottom: 8px; border: 1px solid #e2e8f0; }
.project-item h3 { font-family: monospace; font-size: 0.9rem; color: #0f172a; }
.project-item p { font-size: 0.8rem; color: #475569; }
.project-item .tech { font-family: monospace; font-size: 0.7rem; color: #38bdf8; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
@media (max-width: 600px) { .two-col { grid-template-columns: 1fr; } }
</style></head><body><div class="page">
<div class="header">
  <h1><span class="accent">{</span> {{ full_name }} <span class="accent">}</span></h1>
  {% if title %}<div class="title">{{ title }}</div>{% endif %}
  <div class="contact">
    {% if email %}<span>{{ email }}</span>{% endif %}
    {% if phone %}<span>{{ phone }}</span>{% endif %}
    {% if location %}<span>{{ location }}</span>{% endif %}
    {% if linkedin %}<span>{{ linkedin }}</span>{% endif %}
    {% if github %}<span>{{ github }}</span>{% endif %}
  </div>
</div>

{% if summary %}<div class="summary">{{ summary }}</div>{% endif %}

{% if experience %}
<div class="section">
  <div class="section-title">// Experience</div>
  {% for job in experience %}
  <div class="exp-item">
    <h3>{{ job.title }} <span class="company">@ {{ job.company }}</span></h3>
    <div class="dates">{{ job.start }} – {{ job.end or 'Present' }}</div>
    {% if job.bullets %}<ul class="exp-bullets">{% for b in job.bullets %}<li>{{ b }}</li>{% endfor %}</ul>{% endif %}
  </div>
  {% endfor %}
</div>
{% endif %}

{% if skills %}
<div class="section">
  <div class="section-title">// Tech Stack</div>
  <div class="skills-grid">{% for s in skills %}<span class="skill-tag">{{ s }}</span>{% endfor %}</div>
</div>
{% endif %}

<div class="two-col">
<div>
{% if education %}
<div class="section">
  <div class="section-title">// Education</div>
  {% for e in education %}
  <div class="edu-item" style="margin-bottom:8px">
    <h3>{{ e.degree }}</h3>
    <div class="school">{{ e.school }}{% if e.year %} | {{ e.year }}{% endif %}</div>
  </div>
  {% endfor %}
</div>
{% endif %}
</div>
<div>
{% if certifications %}
<div class="section">
  <div class="section-title">// Certs</div>
  {% for c in certifications %}<div style="font-size:0.85rem;font-family:monospace">{{ c.name }}{% if c.year %} ({{ c.year }}){% endif %}</div>{% endfor %}
</div>
{% endif %}
</div>
</div>

{% if projects %}
<div class="section">
  <div class="section-title">// Projects</div>
  {% for p in projects %}
  <div class="project-item">
    <h3>{{ p.name }}{% if p.url %} <a href="{{ p.url }}" style="color:#38bdf8">↗</a>{% endif %}</h3>
    <p>{{ p.description }}</p>
    {% if p.tech %}<div class="tech">{{ p.tech if p.tech is string else p.tech | join(' · ') }}</div>{% endif %}
  </div>
  {% endfor %}
</div>
{% endif %}
</div></body></html>
""")

# ============================================================
# TEMPLATE 6: EXECUTIVE
# ============================================================
_register("executive", "Executive", "Premium layout for senior professionals, gold accents", "#92400e", """
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width">
<style>
""" + _RESET + """
body { font-family: 'Garamond', 'Georgia', serif; color: #1c1917; }
.page { padding: 45px 55px; }
.header { text-align: center; margin-bottom: 25px; }
.header h1 { font-size: 2.2rem; font-weight: 400; letter-spacing: 4px; text-transform: uppercase; color: #1c1917; }
.header .title { font-size: 1rem; color: #92400e; font-weight: 600; letter-spacing: 2px; margin-top: 4px; }
.header .divider { width: 80px; height: 2px; background: linear-gradient(90deg, transparent, #92400e, transparent); margin: 12px auto; }
.contact { display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; font-size: 0.8rem; color: #78716c; letter-spacing: 0.5px; }
.section { margin-bottom: 22px; }
.section-title { font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 3px; color: #92400e; border-bottom: 1px solid #d6d3d1; padding-bottom: 4px; margin-bottom: 12px; }
.summary { text-align: center; font-size: 0.95rem; color: #44403c; line-height: 1.7; font-style: italic; max-width: 600px; margin: 0 auto 22px; }
.exp-item { margin-bottom: 16px; }
.exp-header { display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; }
.exp-header h3 { font-size: 1.05rem; font-weight: 400; }
.exp-header .company { font-weight: 700; }
.exp-header .dates { font-size: 0.8rem; color: #78716c; font-style: italic; }
.exp-bullets li { font-size: 0.9rem; color: #44403c; margin-bottom: 4px; padding-left: 16px; position: relative; line-height: 1.5; }
.exp-bullets li::before { content: '◆'; position: absolute; left: 0; color: #92400e; font-size: 0.5rem; top: 5px; }
.skills-row { font-size: 0.9rem; color: #44403c; text-align: center; line-height: 2; }
.skills-row span { padding: 2px 0; }
.skills-row span + span::before { content: '  ◆  '; color: #d6d3d1; font-size: 0.6rem; }
.edu-item { text-align: center; margin-bottom: 8px; }
.edu-item h3 { font-size: 0.95rem; font-weight: 400; }
.edu-item .school { font-size: 0.85rem; color: #78716c; }
</style></head><body><div class="page">
<div class="header">
  <h1>{{ full_name }}</h1>
  {% if title %}<div class="title">{{ title }}</div>{% endif %}
  <div class="divider"></div>
  <div class="contact">
    {% if email %}<span>{{ email }}</span>{% endif %}
    {% if phone %}<span>{{ phone }}</span>{% endif %}
    {% if location %}<span>{{ location }}</span>{% endif %}
    {% if linkedin %}<span>{{ linkedin }}</span>{% endif %}
  </div>
</div>

{% if summary %}<div class="summary">{{ summary }}</div>{% endif %}

{% if experience %}
<div class="section">
  <div class="section-title">Professional Experience</div>
  {% for job in experience %}
  <div class="exp-item">
    <div class="exp-header">
      <h3><span class="company">{{ job.company }}</span> — {{ job.title }}</h3>
      <span class="dates">{{ job.start }} – {{ job.end or 'Present' }}</span>
    </div>
    {% if job.bullets %}<ul class="exp-bullets">{% for b in job.bullets %}<li>{{ b }}</li>{% endfor %}</ul>{% endif %}
  </div>
  {% endfor %}
</div>
{% endif %}

{% if skills %}
<div class="section">
  <div class="section-title">Core Competencies</div>
  <div class="skills-row">{% for s in skills %}<span>{{ s }}</span>{% endfor %}</div>
</div>
{% endif %}

{% if education %}
<div class="section">
  <div class="section-title">Education</div>
  {% for e in education %}
  <div class="edu-item">
    <h3>{{ e.degree }}</h3>
    <div class="school">{{ e.school }}{% if e.year %} · {{ e.year }}{% endif %}</div>
  </div>
  {% endfor %}
</div>
{% endif %}

{% if certifications %}
<div class="section">
  <div class="section-title">Certifications & Awards</div>
  {% for c in certifications %}<div style="text-align:center;font-size:0.9rem;margin-bottom:4px">{{ c.name }}{% if c.issuer %} — {{ c.issuer }}{% endif %}{% if c.year %} ({{ c.year }}){% endif %}</div>{% endfor %}
</div>
{% endif %}

{% if projects %}
<div class="section">
  <div class="section-title">Key Projects</div>
  {% for p in projects %}
  <div class="exp-item">
    <h3><span class="company">{{ p.name }}</span></h3>
    <p style="font-size:0.9rem;color:#44403c">{{ p.description }}</p>
  </div>
  {% endfor %}
</div>
{% endif %}
</div></body></html>
""")

# ============================================================
# TEMPLATE 7: COMPACT
# ============================================================
_register("compact", "Compact", "Dense single-page layout, fits maximum content", "#059669", """
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width">
<style>
""" + _RESET + """
html { font-size: 12px; }
body { font-family: 'Segoe UI', system-ui, sans-serif; }
.page { padding: 25px 35px; }
.header { display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #059669; padding-bottom: 8px; margin-bottom: 12px; }
.header h1 { font-size: 1.6rem; font-weight: 700; color: #059669; }
.header .title { font-size: 0.9rem; color: #4b5563; }
.contact-col { text-align: right; font-size: 0.8rem; color: #6b7280; line-height: 1.4; }
.section { margin-bottom: 10px; }
.section-title { font-size: 0.8rem; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; background: #f0fdf4; padding: 2px 6px; }
.summary { font-size: 0.85rem; color: #374151; line-height: 1.4; margin-bottom: 10px; }
.exp-item { margin-bottom: 8px; }
.exp-line { display: flex; justify-content: space-between; font-size: 0.85rem; }
.exp-line h3 { font-weight: 600; }
.exp-line .dates { color: #9ca3af; font-size: 0.8rem; }
.exp-bullets { margin-top: 2px; }
.exp-bullets li { font-size: 0.8rem; color: #4b5563; margin-bottom: 1px; padding-left: 10px; position: relative; }
.exp-bullets li::before { content: '•'; position: absolute; left: 0; color: #059669; }
.skills-inline { font-size: 0.8rem; color: #374151; line-height: 1.6; }
.bottom-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
@media (max-width: 500px) { .bottom-grid { grid-template-columns: 1fr; } .header { flex-direction: column; } .contact-col { text-align: left; margin-top: 6px; } }
</style></head><body><div class="page">
<div class="header">
  <div>
    <h1>{{ full_name }}</h1>
    {% if title %}<div class="title">{{ title }}</div>{% endif %}
  </div>
  <div class="contact-col">
    {% if email %}<div>{{ email }}</div>{% endif %}
    {% if phone %}<div>{{ phone }}</div>{% endif %}
    {% if location %}<div>{{ location }}</div>{% endif %}
    {% if linkedin %}<div>{{ linkedin }}</div>{% endif %}
    {% if github %}<div>{{ github }}</div>{% endif %}
  </div>
</div>

{% if summary %}<div class="summary">{{ summary }}</div>{% endif %}

{% if experience %}
<div class="section">
  <div class="section-title">Experience</div>
  {% for job in experience %}
  <div class="exp-item">
    <div class="exp-line">
      <h3>{{ job.title }}, {{ job.company }}</h3>
      <span class="dates">{{ job.start }}–{{ job.end or 'Present' }}</span>
    </div>
    {% if job.bullets %}<ul class="exp-bullets">{% for b in job.bullets %}<li>{{ b }}</li>{% endfor %}</ul>{% endif %}
  </div>
  {% endfor %}
</div>
{% endif %}

{% if skills %}
<div class="section">
  <div class="section-title">Skills</div>
  <div class="skills-inline">{{ skills | join(' · ') }}</div>
</div>
{% endif %}

<div class="bottom-grid">
<div>
{% if education %}
<div class="section">
  <div class="section-title">Education</div>
  {% for e in education %}
  <div style="margin-bottom:4px;font-size:0.8rem">
    <strong>{{ e.degree }}</strong><br>
    <span style="color:#9ca3af">{{ e.school }}{% if e.year %}, {{ e.year }}{% endif %}</span>
  </div>
  {% endfor %}
</div>
{% endif %}
</div>
<div>
{% if certifications %}
<div class="section">
  <div class="section-title">Certifications</div>
  {% for c in certifications %}<div style="font-size:0.8rem">{{ c.name }}{% if c.year %} ({{ c.year }}){% endif %}</div>{% endfor %}
</div>
{% endif %}
{% if languages %}
<div class="section">
  <div class="section-title">Languages</div>
  {% for l in languages %}<div style="font-size:0.8rem">{{ l.language }} – {{ l.level }}</div>{% endfor %}
</div>
{% endif %}
</div>
</div>

{% if projects %}
<div class="section">
  <div class="section-title">Projects</div>
  {% for p in projects %}
  <div style="margin-bottom:4px;font-size:0.8rem"><strong>{{ p.name }}</strong> – {{ p.description }}</div>
  {% endfor %}
</div>
{% endif %}
</div></body></html>
""")

# ============================================================
# TEMPLATE 8: TWO-COLUMN
# ============================================================
_register("two-column", "Two Column", "Professional two-column layout with sidebar", "#dc2626", """
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width">
<style>
""" + _RESET + """
body { font-family: 'Segoe UI', system-ui, sans-serif; }
.page { display: grid; grid-template-columns: 1fr 240px; padding: 0; max-width: 870px; }
.main { padding: 35px 30px; }
.sidebar { background: #fafafa; padding: 35px 22px; border-left: 1px solid #e5e7eb; }
.header h1 { font-size: 1.8rem; font-weight: 700; color: #dc2626; }
.header .title { font-size: 0.95rem; color: #4b5563; margin-bottom: 15px; }
.section { margin-bottom: 18px; }
.section-title { font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #dc2626; border-bottom: 2px solid #dc2626; padding-bottom: 3px; margin-bottom: 10px; }
.sidebar .section-title { color: #374151; border-color: #d1d5db; }
.summary { font-size: 0.9rem; color: #374151; line-height: 1.6; }
.exp-item { margin-bottom: 14px; }
.exp-item h3 { font-size: 0.95rem; font-weight: 600; }
.exp-item .meta { font-size: 0.8rem; color: #dc2626; }
.exp-item .dates { font-size: 0.8rem; color: #9ca3af; }
.exp-bullets li { font-size: 0.85rem; color: #374151; margin-bottom: 2px; padding-left: 12px; position: relative; }
.exp-bullets li::before { content: '▪'; position: absolute; left: 0; color: #dc2626; }
.sidebar-item { font-size: 0.8rem; color: #374151; margin-bottom: 3px; }
.sidebar .skill-tag { display: inline-block; font-size: 0.75rem; background: #fff; border: 1px solid #e5e7eb; padding: 2px 8px; border-radius: 3px; margin: 2px; }
.project-item { margin-bottom: 10px; }
.project-item h3 { font-size: 0.9rem; font-weight: 600; }
.project-item p { font-size: 0.8rem; color: #4b5563; }
@media (max-width: 650px) { .page { grid-template-columns: 1fr; } .sidebar { border-left: none; border-top: 1px solid #e5e7eb; } }
@media print { .page { grid-template-columns: 1fr 220px; } }
</style></head><body><div class="page">
<div class="main">
  <div class="header">
    <h1>{{ full_name }}</h1>
    {% if title %}<div class="title">{{ title }}</div>{% endif %}
  </div>

  {% if summary %}
  <div class="section">
    <div class="section-title">Profile</div>
    <div class="summary">{{ summary }}</div>
  </div>
  {% endif %}

  {% if experience %}
  <div class="section">
    <div class="section-title">Experience</div>
    {% for job in experience %}
    <div class="exp-item">
      <h3>{{ job.title }}</h3>
      <div class="meta">{{ job.company }}</div>
      <div class="dates">{{ job.start }} – {{ job.end or 'Present' }}</div>
      {% if job.bullets %}<ul class="exp-bullets">{% for b in job.bullets %}<li>{{ b }}</li>{% endfor %}</ul>{% endif %}
    </div>
    {% endfor %}
  </div>
  {% endif %}

  {% if projects %}
  <div class="section">
    <div class="section-title">Projects</div>
    {% for p in projects %}
    <div class="project-item">
      <h3>{{ p.name }}</h3>
      <p>{{ p.description }}</p>
      {% if p.tech %}<div style="font-size:0.7rem;color:#dc2626;margin-top:2px">{{ p.tech if p.tech is string else p.tech | join(' · ') }}</div>{% endif %}
    </div>
    {% endfor %}
  </div>
  {% endif %}
</div>

<div class="sidebar">
  <div class="section">
    <div class="section-title">Contact</div>
    {% if email %}<div class="sidebar-item">{{ email }}</div>{% endif %}
    {% if phone %}<div class="sidebar-item">{{ phone }}</div>{% endif %}
    {% if location %}<div class="sidebar-item">{{ location }}</div>{% endif %}
    {% if linkedin %}<div class="sidebar-item">{{ linkedin }}</div>{% endif %}
    {% if github %}<div class="sidebar-item">{{ github }}</div>{% endif %}
    {% if portfolio %}<div class="sidebar-item">{{ portfolio }}</div>{% endif %}
  </div>

  {% if skills %}
  <div class="section">
    <div class="section-title">Skills</div>
    <div>{% for s in skills %}<span class="skill-tag">{{ s }}</span>{% endfor %}</div>
  </div>
  {% endif %}

  {% if education %}
  <div class="section">
    <div class="section-title">Education</div>
    {% for e in education %}
    <div style="margin-bottom:8px">
      <div style="font-size:0.8rem;font-weight:600">{{ e.degree }}</div>
      <div style="font-size:0.75rem;color:#6b7280">{{ e.school }}{% if e.year %}<br>{{ e.year }}{% endif %}</div>
    </div>
    {% endfor %}
  </div>
  {% endif %}

  {% if certifications %}
  <div class="section">
    <div class="section-title">Certifications</div>
    {% for c in certifications %}<div class="sidebar-item">{{ c.name }}{% if c.year %} ({{ c.year }}){% endif %}</div>{% endfor %}
  </div>
  {% endif %}

  {% if languages %}
  <div class="section">
    <div class="section-title">Languages</div>
    {% for l in languages %}<div class="sidebar-item">{{ l.language }} – {{ l.level }}</div>{% endfor %}
  </div>
  {% endif %}
</div>
</div></body></html>
""")
