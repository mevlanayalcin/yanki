#!/usr/bin/env python3
"""Build the bilingual website and Yankı product showcase from local sources."""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
import shutil
from urllib.parse import quote

from site_copy import COPY

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / 'dist'
DOMAIN = 'mevlanayalcin.com.tr'
POSTA = 'info@' + DOMAIN
DEPO = 'https://github.com/mevlanayalcin/yanki'
PROFIL = 'https://github.com/mevlanayalcin'
LINKEDIN = 'https://www.linkedin.com/in/mevlanayalcin'
CONTENT_UPDATED = '2026-11-16'
SLUG = {
    'en': {
        'home': '/', 'services': '/services/', 'products': '/products/', 'approach': '/process/',
        'company': '/company/', 'privacy': '/privacy/', 'yanki': '/work/yanki/',
        'contact': '/contact/', 'terms': '/terms/', 'audit': '/work/inference-audit/', 'notes': '/notes/',
    },
    'tr': {
        'home': '/tr/', 'services': '/tr/hizmetler/', 'products': '/tr/urunler/', 'approach': '/tr/surec/',
        'company': '/tr/kurumsal/', 'privacy': '/tr/gizlilik/', 'yanki': '/tr/calismalar/yanki/',
        'contact': '/tr/iletisim/', 'terms': '/tr/sartlar/', 'audit': '/tr/calismalar/inference-denetimi/', 'notes': '/tr/notlar/',
    },
}
E = html.escape
ARROW = '<span class="arrow" aria-hidden="true">↗</span>'
MARK = '<svg class="brandmark" aria-hidden="true" viewBox="0 0 40 40" fill="none"><path d="M2 34V6h8l10 15L30 6h8v28h-8V20L20 35 10 20v14H2Z" fill="currentColor"/><path d="M31 30h7v7h-7z" fill="#d95535"/></svg>'

QUICKSTART_SNIPPET = """git clone https://github.com/mevlanayalcin/yanki.git && cd yanki
pip install -e ".[dev]"

# 1. Verify a Turkish quote span with U+0130 (İ/i) offset preservation
python3 -m yanki.cli verify \\
  --source "İSTANBUL veri merkezinde tutulan birincil yedekler Ankara bölgesine çoğaltılır." \\
  --quote "istanbul veri merkezinde tutulan birincil yedekler"

# 2. Run the 24-case TR/EN deterministic benchmark suite (offline CI gate)
python3 -m yanki.eval --offline --strict-thresholds"""


def link(text, href, cls='text-link', external=False):
    extra = ' target="_blank" rel="noopener noreferrer"' if external else ''
    return f'<a class="{cls}" href="{E(href, quote=True)}"{extra}>{E(text)}{ARROW}</a>'


def brand(lang):
    home_label = 'Ana sayfa' if lang == 'tr' else 'Home'
    sub = 'AI mühendisliği' if lang == 'tr' else 'AI engineering'
    return f'<a class="brand" href="{SLUG[lang]["home"]}" aria-label="Mevlana Yalçın — {home_label}">{MARK}<span class="brand-name">Mevlana Yalçın<small>{sub}</small></span></a>'


def heading(eyebrow, title, body='', compact=False):
    intro = f'<p class="section-intro">{E(body)}</p>' if body else ''
    cls = ' compact' if compact else ''
    return f'<div class="section-top{cls}"><p class="eyebrow">{E(eyebrow)}</p><div><h2>{E(title)}</h2>{intro}</div></div>'


def service_list(lang):
    rows = []
    for s in COPY[lang]['services']['items']:
        tags = ''.join(f'<span class="tag">{E(t)}</span>' for t in s['tags'])
        fiyat = (COPY[lang].get('prices') or {}).get('items', {}).get(s['number'], '')
        if fiyat:
            tags += f'<span class="tag price">{E(fiyat)}</span>'
        label = f'{s["title"]} — {COPY[lang]["contact"]["cta"]}'
        rows.append(
            f'<article class="service-row"><span class="service-number">{s["number"]}</span>'
            f'<h3>{E(s["title"])}</h3><div class="service-body"><p>{E(s["body"])}</p><div class="tags">{tags}</div></div>'
            f'<a class="row-arrow" href="#contact" aria-label="{E(label, quote=True)}">{ARROW}</a></article>'
        )
    return '<div class="service-list">' + ''.join(rows) + '</div>'


def product_art(lang, slug='yanki'):
    tr = lang == 'tr'
    if slug == 'yanki-engine':
        cap = '1:1 UNICODE VE ÇOK KAYNAKLI RAG KANITI' if tr else '1:1 UNICODE & MULTI-SOURCE RAG PROVENANCE'
        return (
            '<div class="product-art engine" aria-hidden="true">'
            '<span class="artifact-label">YANKI 0.2.0 / MIT PYTHON CORE</span>'
            '<div class="engine-preview">'
            '<div class="engine-bar"><span>src/yanki/grounding.py</span><b>24/24 CI PASS</b></div>'
            '<code>verify_multi_source_citations(chunks, cites)</code>'
            '<code>-&gt; span [0, 50) · 0.14 ms · deterministic</code>'
            f'<small>{cap}</small>'
            '</div></div>'
        )
    badge = 'ÖZEL ÖNİZLEME · YAPIM AŞAMASINDA' if tr else 'PRIVATE PREVIEW · IN DEVELOPMENT'
    small = ' MODEL-BAĞIMSIZ DOĞRULAMA VEKİLİ' if tr else 'MODEL-AGNOSTIC VERIFICATION GATEWAY'
    line_txt = 'Her model alıntısı teslimden önce kaynak kesitiyle doğrulanır.' if tr else 'Every cited span verified against source offsets before delivery.'
    return (
        f'<div class="product-art yanki" aria-hidden="true">'
        f'<span class="artifact-label">{badge}</span>'
        f'<div class="note-preview"><div class="preview-brand">yankı<i></i></div>'
        f'<p>{line_txt}</p><div class="note-line"></div><small>{small}</small></div></div>'
    )


def products(lang):
    items = []
    for p in COPY[lang]['products']['items']:
        href = SLUG[lang]['yanki'] if p['slug'] == 'yanki' else p['href']
        art = product_art(lang, p['slug'])
        items.append(
            f'<article class="product-card">{art}<div class="product-copy">'
            f'<div class="product-topline"><span class="product-name">{E(p["name"])}</span><span class="product-status">{E(p["status"])}</span></div>'
            f'<h3>{E(p["title"])}</h3><p>{E(p["body"])}</p>'
            f'{link(p["cta"], href, external=href.startswith("https:"))}'
            f'<span class="product-category">{E(p["category"])}</span></div></article>'
        )
    grid_cls = 'product-grid' if len(items) > 1 else 'product-grid one'
    return f'<div class="{grid_cls}">' + ''.join(items) + '</div>'


def verification_evidence(lang):
    v = COPY[lang]['verification']
    items = ''.join(
        f'<article class="step"><span class="step-number">0{i+1}</span><h3>{E(item["title"])}</h3><p>{E(item["body"])}</p></article>'
        for i, item in enumerate(v['items'])
    )
    examples_href = SLUG[lang]['yanki'] + '#examples'
    return (
        f'<section class="section wrap verification-evidence" id="verification">'
        f'{heading(v["eyebrow"], v["title"], v["body"])}'
        f'<div class="approach-grid">{items}</div>'
        f'<div class="actions">{link(v["cta"], examples_href, "button")}{link(v["source_label"], DEPO, external=True)}</div>'
        f'</section>'
    )


def process(lang):
    rows = ''.join(
        f'<article class="step"><span class="step-number">{s["number"]}</span><h3>{E(s["title"])}</h3><p>{E(s["body"])}</p></article>'
        for s in COPY[lang]['process']['steps']
    )
    return f'<div class="approach-grid">{rows}</div>'


def contact(lang):
    c = COPY[lang]['contact']
    subject = 'Mühendislik ve Yankı özel önizleme' if lang == 'tr' else 'Engineering & Yankı private preview'
    mailto_href = 'mailto:' + POSTA + '?subject=' + quote(subject)
    return (
        f'<section class="contact" id="contact"><div class="wrap contact-top">'
        f'<div><p class="eyebrow">{E(c["eyebrow"])}</p><h2>{E(c["title"])}</h2><p>{E(c["body"])}</p></div>'
        f'<div class="contact-action">{link(c["cta"], mailto_href, "button light")}'
        f'<a class="contact-email" href="mailto:{POSTA}">{POSTA}</a></div></div></section>'
    )


def telemetry_strip(lang):
    cells = ''.join(
        f'<div class="telemetry-cell"><strong>{E(m["value"])}</strong><span>{E(m["label"])}</span></div>'
        for m in COPY[lang]['hero']['metrics']
    )
    return f'<div class="telemetry-strip">{cells}</div>'


def home(lang):
    c = COPY[lang]
    h = c['hero']
    names = ['Ölç', 'Doğrula', 'Yayınla'] if lang == 'tr' else ['Measure', 'Verify', 'Ship']
    caps = ''.join(f'<span><b>0{i+1}</b>{name}</span>' for i, name in enumerate(names))
    s, p, a = c['services'], c['products'], c['process']
    art_cap = 'Deterministik doğrulama katmanı' if lang == 'tr' else 'Deterministic verification layer'
    return (
        f'<section class="hero wrap">'
        f'<div class="hero-top"><p class="eyebrow">{E(h["eyebrow"])}</p><span class="location"><span class="status-dot"></span>Ankara, Türkiye</span></div>'
        f'<div class="hero-grid"><div class="hero-copy"><h1>{E(h["title"])}<span class="accent">{E(h["title_accent"])}</span></h1>'
        f'<p>{E(h["body"])}</p><div class="actions">{link(h["primary"], SLUG[lang]["yanki"], "button")}{link(h["secondary"], "#verification")}</div></div>'
        f'<div class="hero-art"><img src="/assets/structure.svg" width="620" height="620" alt="" fetchpriority="high">'
        f'<div class="art-caption"><span>{art_cap}</span><span>YANKI / v0.2</span></div></div></div>'
        f'{telemetry_strip(lang)}'
        f'<div class="hero-bottom"><span>{E(h["note"])}</span><div class="capabilities">{caps}</div></div></section>'
        f'<section class="intro wrap">{heading(c["intro"]["eyebrow"], c["intro"]["title"], c["intro"]["body"])}</section>'
        f'<section class="section products-section" id="products"><div class="wrap">{heading(p["eyebrow"], p["title"], p["body"])}{products(lang)}</div></section>'
        f'{verification_evidence(lang)}'
        f'<section class="section wrap" id="expertise">{heading(s["eyebrow"], s["title"], s["body"])}{service_list(lang)}<div class="section-foot">{link(c["nav"]["services"], SLUG[lang]["services"])}</div></section>'
        f'<section class="section wrap">{heading(a["eyebrow"], a["title"])}{process(lang)}</section>'
        f'<section class="company-strip wrap"><p class="eyebrow">{E(c["company"]["eyebrow"])}</p><div><h2>{E(c["company"]["title"])}</h2><p>{E(c["company"]["body"])}</p>{link(c["nav"]["company"], SLUG[lang]["company"])}</div></section>'
    )


def page_hero(lang, key, title=None, body=None):
    c = COPY[lang][key]
    lede_txt = body if body is not None else c.get('body', c.get('intro', ''))
    return f'<section class="page-hero wrap"><p class="eyebrow">{E(c["eyebrow"])}</p><h1>{E(title or c["title"])}</h1><p class="lede">{E(lede_txt)}</p></section>'


def yanki_engine_section(lang):
    ye = COPY[lang]['yanki_engine']
    mods = ''.join(
        f'<article class="step engine-card"><span class="step-number">{E(m["num"])} · <code>{E(m["name"])}</code></span>'
        f'<h3>{E(m["title"])}</h3><p>{E(m["body"])}</p></article>'
        for m in ye['modules']
    )
    h1, h2, h3, h4 = ye['bench_headers']
    thead = f'<thead><tr><th scope="col">{E(h1)}</th><th scope="col">{E(h2)}</th><th scope="col">{E(h3)}</th><th scope="col">{E(h4)}</th></tr></thead>'
    tbody_rows = ''.join(
        f'<tr><th scope="row">{E(r[0])}</th><td>{E(r[1])}</td><td><code>{E(r[2])}</code></td><td><span class="badge-pass">{E(r[3])}</span></td></tr>'
        for r in ye['bench_rows']
    )
    table_vars = f'--label-2: "{E(h2, quote=True)}"; --label-3: "{E(h3, quote=True)}"; --label-4: "{E(h4, quote=True)}";'
    snippet = E(QUICKSTART_SNIPPET)
    hpc_url = DEPO + '/tree/main/hpc'
    return (
        f'<section class="section engine-section" id="engine"><div class="wrap">'
        f'{heading(ye["eyebrow"], ye["title"], ye["body"])}'
        f'<div class="engine-grid">{mods}</div>'
        f'<figure class="code-figure">'
        f'<figcaption id="quickstart-caption">{E(ye["code_caption"])}</figcaption>'
        f'<pre role="region" aria-labelledby="quickstart-caption" tabindex="0"><code class="language-bash">{snippet}</code></pre>'
        f'</figure>'
        f'</div></section>'
        f'<section class="section wrap" id="benchmarks">'
        f'{heading(ye["bench_eyebrow"], ye["bench_title"], ye["bench_body"], compact=True)}'
        f'<div tabindex="0" role="region" aria-labelledby="bench-caption" class="table-wrapper">'
        f'<table class="bench-table" style=\'{table_vars}\'>'
        f'<caption id="bench-caption">{E(ye["bench_caption"])}</caption>'
        f'{thead}<tbody>{tbody_rows}</tbody></table></div>'
        f'<div class="actions">{link(ye["repo_cta"], DEPO, "button", external=True)}{link(ye["ci_cta"], hpc_url, external=True)}</div>'
        f'</section>'
    )


def yanki_trace_explorer(lang):
    y = COPY[lang]['yanki']
    tab_buttons = []
    tab_panels = []
    for i, ex in enumerate(y['examples']):
        selected = 'true' if i == 0 else 'false'
        fg_start = ' focusgroupstart' if i == 0 else ''
        tab_id = f'trace-tab-{i}'
        panel_id = f'trace-panel-{i}'
        panel_state = 'tabindex="0"' if i == 0 else 'hidden="until-found"'
        in_cap_id = f'trace-in-{i}'
        dr_cap_id = f'trace-dr-{i}'
        vd_cap_id = f'trace-vd-{i}'

        tab_buttons.append(
            f'<button type="button" role="tab" class="trace-tab" id="{tab_id}" aria-selected="{selected}"{fg_start}>{E(ex["tab"])}</button>'
        )
        tab_panels.append(
            f'<div role="tabpanel" class="trace-panel" id="{panel_id}" aria-labelledby="{tab_id}" {panel_state}>'
            f'<div class="trace-panel-inner">'
            f'<div class="trace-header">'
            f'<div><h3>{E(ex["scenario"])}</h3><p>{E(ex["summary"])}</p></div>'
            f'<span class="trace-badge {E(ex["badge_tone"])}">{E(ex["badge"])}</span>'
            f'</div>'
            f'<div class="trace-columns">'
            f'<div class="trace-col"><span class="trace-step-label" id="{in_cap_id}">01 · {E(ex["input_label"])}</span>'
            f'<pre role="region" aria-labelledby="{in_cap_id}" tabindex="0"><code>{E(ex["input_code"])}</code></pre></div>'
            f'<div class="trace-col"><span class="trace-step-label" id="{dr_cap_id}">02 · {E(ex["draft_label"])}</span>'
            f'<pre role="region" aria-labelledby="{dr_cap_id}" tabindex="0"><code>{E(ex["draft_code"])}</code></pre></div>'
            f'<div class="trace-col verdict"><span class="trace-step-label" id="{vd_cap_id}">03 · {E(ex["verdict_label"])}</span>'
            f'<pre role="region" aria-labelledby="{vd_cap_id}" tabindex="0"><code>{E(ex["verdict_code"])}</code></pre></div>'
            f'</div>'
            f'</div></div>'
        )
    tabs_html = ''.join(tab_buttons)
    panels_html = ''.join(tab_panels)
    return (
        f'<section class="section wrap" id="examples">'
        f'{heading(y["examples_eyebrow"], y["examples_title"], y["examples_body"], compact=True)}'
        f'<div class="trace-tabs">'
        f'<div class="trace-tablist" role="tablist" focusgroup="tablist nomemory" aria-label="{E(y["examples_tablist_label"], quote=True)}">{tabs_html}</div>'
        f'<div class="trace-panels">{panels_html}</div>'
        f'</div></section>'
    )


def yanki(lang):
    y = COPY[lang]['yanki']
    stages = ''.join(
        f'<article class="pipeline-stage"><div class="stage-head"><span>{E(st["step"])}</span><code>{E(st["meta"])}</code></div>'
        f'<h3>{E(st["name"])}</h3><p>{E(st["desc"])}</p></article>'
        for st in y['pipeline_stages']
    )
    use_cases = ''.join(
        f'<article class="step"><span class="step-number">{E(uc["num"])}</span><h3>{E(uc["title"])}</h3><p>{E(uc["body"])}</p></article>'
        for uc in y['use_cases']
    )
    privacy_label = E(COPY[lang]['footer']['privacy'])
    pipeline_title = 'Dört aşamalı deterministik doğrulama boru hattı' if lang == 'tr' else 'Four-stage deterministic verification pipeline'
    pipeline_eyebrow = 'Sistem mimarisi' if lang == 'tr' else 'System architecture'
    return (
        page_hero(lang, 'yanki')
        + f'<section class="wrap dev-banner-wrap"><div class="dev-banner" role="note">'
        f'<div class="dev-banner-top"><span class="status-pill">{E(y["status"])}</span><code>yanki-core v0.2.0 · MIT</code></div>'
        f'<h2>{E(y["dev_banner_title"])}</h2><p>{E(y["dev_banner_body"])}</p>'
        f'<div class="actions"><a class="button" href="#early-access">{E(y["waitlist_button"])}{ARROW}</a>{link(COPY[lang]["yanki_engine"]["repo_cta"], DEPO, external=True)}</div>'
        f'</div></section>'
        + f'<section class="section wrap" id="architecture">{heading(pipeline_eyebrow, pipeline_title, compact=True)}<div class="pipeline-grid">{stages}</div></section>'
        + yanki_trace_explorer(lang)
        + f'<section class="section wrap" id="use-cases">{heading(y["use_cases_eyebrow"], y["use_cases_title"], compact=True)}<div class="engine-grid">{use_cases}</div></section>'
        + yanki_engine_section(lang)
        + f'<section class="section wrap" id="early-access"><div class="waitlist-box">'
        f'<div class="waitlist-copy"><p class="eyebrow">{E(y["waitlist_eyebrow"])}</p><h2 id="waitlist-heading">{E(y["waitlist_title"])}</h2><p>{E(y["waitlist_body"])}</p></div>'
        f'<form id="bekleme" class="waitlist-form" action="/api/waitlist" method="POST" aria-labelledby="waitlist-heading" novalidate>'
        f'<label for="preview-email">{E(y["waitlist_label"])} <span aria-hidden="true">*</span></label>'
        f'<input type="email" id="preview-email" name="email" autocomplete="email" inputmode="email" autocorrect="off" autocapitalize="none" spellcheck="false" enterkeyhint="send" required maxlength="180" placeholder="{E(y["waitlist_placeholder"], quote=True)}" aria-describedby="preview-hint beklemeyanit">'
        f'<span id="preview-hint" class="form-note">{E(y["waitlist_hint"])} · <a href="{SLUG[lang]["privacy"]}">{privacy_label} ↗</a></span>'
        f'<button class="button" type="submit">{E(y["waitlist_button"])}{ARROW}</button>'
        f'<p class="form-status" id="beklemeyanit" role="status" aria-live="polite"></p>'
        f'</form></div></section>'
    )


def content(lang, page):
    c = COPY[lang]
    if page == 'home':
        return home(lang)
    if page == 'services':
        pr = c.get('prices') or {}
        alt = (
            (f'<div class="tech-note">{E(pr.get("retainer", ""))}</div>' if pr.get('retainer') else '')
            + (f'<p class="legal-note">{E(pr.get("note", ""))}</p>' if pr.get('note') else '')
            + (link(c['audit']['cta'], SLUG[lang]['audit']) if c.get('audit') else '')
        )
        return page_hero(lang, 'services') + f'<section class="page-content wrap">{service_list(lang)}<div class="tech-note">{E(c["services"]["body"])}</div>{alt}{link(c["nav"]["contact"], SLUG[lang]["contact"])}</section>'
    if page == 'products':
        return page_hero(lang, 'products') + f'<section class="page-content wrap">{products(lang)}</section>' + verification_evidence(lang)
    if page == 'approach':
        return page_hero(lang, 'process', body=c['services']['body']) + f'<section class="page-content wrap">{process(lang)}</section>'
    if page == 'company':
        cc = c['company']
        facts = ''.join(f'<div class="fact"><dt>{E(f["label"])}</dt><dd>{E(f["value"])}</dd></div>' for f in cc['facts'])
        arch_heading = 'Modelden bağımsız doğrulama mimarisi' if lang == 'tr' else 'Model-agnostic verification architecture'
        return (
            page_hero(lang, 'company')
            + f'<section class="page-content wrap"><dl class="facts">{facts}</dl>'
            f'<p class="legal-note">{E(cc["legal"])}</p><p class="legal-note">{E(cc["dates"])}</p>'
            f'<div class="profile-links">{link("GitHub", PROFIL, external=True)}{link("LinkedIn", LINKEDIN, external=True)}{link(c["nav"]["contact"], SLUG[lang]["contact"])}</div>'
            f'<div class="technical"><h2>{arch_heading}</h2><p class="legal-note">{E(cc["model_use"])}</p>{link(c["nav"]["products"], SLUG[lang]["products"])}</div></section>'
        )
    if page == 'privacy':
        sections = ''.join(f'<section class="prose-section"><h2>{E(s["title"])}</h2><p>{E(s["body"])}</p></section>' for s in c['privacy']['sections'])
        return page_hero(lang, 'privacy') + f'<div class="page-content wrap"><div class="prose">{sections}</div></div>'
    if page == 'contact':
        cp = c['contact_page']
        return (
            page_hero(lang, 'contact_page')
            + f'<section class="page-content wrap contact-page"><div class="contact-card"><span class="eyebrow">{E(cp["email_label"])}</span>'
            f'<a class="contact-address" href="mailto:{POSTA}">{POSTA}</a>'
            f'<dl class="contact-facts"><dt>{E(cp["founder_label"])}</dt><dd>Mevlana Yalçın</dd><dt>{E(cp["timezone_label"])}</dt><dd>{E(cp["timezone"])}</dd></dl>'
            f'<div class="profile-links">{link(cp["profile"], PROFIL, external=True)}{link(cp["linkedin"], LINKEDIN, external=True)}{link(cp["source"], DEPO, external=True)}</div></div>'
            f'<div class="contact-explanation"><h2>{E(cp["write_title"])}</h2><p>{E(cp["write_body"])}</p>'
            f'<h2>{E(cp["next_title"])}</h2><p>{E(cp["next_body"])}</p>{link(cp["terms_link"], SLUG[lang]["terms"])}</div></section>'
        )
    if page == 'terms':
        t = c['terms']
        parcalar = ''.join(f'<section class="prose-section"><h2>{E(s["title"])}</h2><p>{E(s["body"])}</p></section>' for s in t['sections'])
        return page_hero(lang, 'terms') + f'<div class="page-content wrap"><div class="prose">{parcalar}</div><div class="actions">{link(t["cta"], "mailto:" + POSTA, "button")}</div></div>'
    if page == 'notes':
        n = c['notes']
        kartlar = ''.join(
            f'<section class="prose-section"><h2>{E(m["title"])} <span class="note-date">{E(m["date"])}</span></h2><p>{E(m["body"])}</p></section>'
            for m in n['items']
        )
        return (
            page_hero(lang, 'notes')
            + f'<section class="page-content wrap"><div class="approach-grid">{kartlar}</div>'
            f'<p class="legal-note">{E(n["note"])}</p>'
            f'<div class="actions">{link(n["cta"], SLUG[lang]["audit"], "button")}{link(c["nav"]["contact"], SLUG[lang]["contact"])}</div></section>'
        )
    if page == 'audit':
        a = c['audit']
        yontem = ''.join(f'<li>{E(m)}</li>' for m in a['method'])
        bulgular = ''.join(
            f'<article class="step"><span class="step-number">0{i+1}</span><h3>{E(f["title"])}</h3><p>{E(f["body"])}</p></article>'
            for i, f in enumerate(a['findings'])
        )
        return (
            page_hero(lang, 'audit')
            + f'<section class="page-content wrap"><div class="prose"><h2>{E(a["method_title"])}</h2><ul class="method-list">{yontem}</ul>'
            f'<p class="legal-note">{E(a["evidence_note"])}</p></div>'
            f'<h2 class="findings-title">{E(a["findings_title"])}</h2><div class="approach-grid">{bulgular}</div>'
            f'<div class="prose"><h2>{E(a["outcome_title"])}</h2><p>{E(a["outcome"])}</p></div>'
            f'<div class="actions">{link(a["cta"], SLUG[lang]["contact"], "button")}{link(c["nav"]["services"], SLUG[lang]["services"])}</div></section>'
        )
    if page == 'yanki':
        return yanki(lang)
    return f'<section class="not-found wrap"><p class="eyebrow">404</p><h1>{E(c["labels"]["not_found_title"])}</h1><p>{E(c["labels"]["not_found_body"])}</p>{link(c["labels"]["back"], SLUG[lang]["home"], "button")}</section>'


def page_name(lang, page):
    if page == 'home':
        return 'Ana sayfa' if lang == 'tr' else 'Home'
    if page == 'yanki':
        return 'Yankı'
    if page == 'privacy':
        return COPY[lang]['footer']['privacy']
    return COPY[lang]['nav'].get(page, page)


def breadcrumbs(lang, page):
    if page in ('home', '404'):
        return ''
    aria_lbl = 'Sayfa yolu' if lang == 'tr' else 'Breadcrumb'
    return f'<nav class="breadcrumbs wrap" aria-label="{aria_lbl}"><a href="{SLUG[lang]["home"]}">{page_name(lang, "home")}</a><span aria-hidden="true">/</span><span aria-current="page">{E(page_name(lang, page))}</span></nav>'


def structured_data(lang, page, canonical):
    root = 'https://' + DOMAIN
    founder = {
        '@type': 'Person', '@id': root + '/#founder', 'name': 'Mevlana Yalçın',
        'jobTitle': 'Founder and AI systems engineer', 'url': root + SLUG[lang]['company'], 'sameAs': [PROFIL, LINKEDIN],
    }
    service = {
        '@type': 'ProfessionalService', '@id': root + '/#business', 'name': 'Mevlana Yalçın', 'url': root,
        'description': COPY[lang]['meta']['description'], 'email': POSTA, 'founder': {'@id': root + '/#founder'},
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Ankara', 'addressCountry': 'TR'},
        'contactPoint': {'@type': 'ContactPoint', 'email': POSTA, 'url': root + SLUG[lang]['contact'], 'availableLanguage': ['en', 'tr'], 'contactType': 'business enquiries'},
        'knowsAbout': [
            'Deterministic LLM output verification', 'Multilingual RAG citation grounding',
            'vLLM and SGLang GPU inference systems', 'Adversarial AI evaluation',
        ],
    }
    graph = [founder, service, {'@type': 'WebSite', '@id': root + '/#website', 'name': 'Mevlana Yalçın', 'url': root, 'publisher': {'@id': root + '/#business'}}]
    if page in SLUG[lang]:
        graph.append({'@type': 'WebPage', '@id': canonical + '#page', 'url': canonical, 'name': page_name(lang, page), 'inLanguage': lang, 'isPartOf': {'@id': root + '/#website'}, 'dateModified': CONTENT_UPDATED})
    if page not in ('home', '404'):
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': page_name(lang, 'home'), 'item': root + SLUG[lang]['home']}, {'@type': 'ListItem', 'position': 2, 'name': page_name(lang, page), 'item': canonical}]})
    if page in ('home', 'products', 'yanki'):
        graph.append({
            '@type': 'SoftwareApplication', '@id': root + '/work/yanki/#product', 'name': 'Yankı Verification Platform',
            'softwareVersion': '0.2.0', 'url': root + SLUG[lang]['yanki'], 'applicationCategory': 'DeveloperApplication',
            'operatingSystem': 'Linux, macOS, Cloud', 'license': 'https://opensource.org/licenses/MIT',
            'codeRepository': DEPO, 'description': COPY[lang]['products']['body'], 'creator': {'@id': root + '/#founder'},
        })
        graph.append({
            '@type': 'SoftwareSourceCode', '@id': root + '/work/yanki/#engine', 'name': 'yanki', 'version': '0.2.0',
            'codeRepository': DEPO, 'license': 'https://opensource.org/licenses/MIT', 'programmingLanguage': ['Python'],
            'author': {'@id': root + '/#founder'}, 'description': COPY[lang]['yanki_engine']['body'],
        })
    return {'@context': 'https://schema.org', '@graph': graph}


def shell(lang, page, version):
    c = COPY[lang]
    other = 'tr' if lang == 'en' else 'en'
    canonical = 'https://' + DOMAIN + SLUG[lang].get(page, '/404.html')
    nav = ''.join(
        f'<a href="{SLUG[lang][key]}"' + (' aria-current="page"' if key == page else '') + f'>{E(c["nav"][key])}</a>'
        for key in ['services', 'products', 'approach', 'company']
    )
    other_aria = 'Türkçe' if other == 'tr' else 'English'
    nav += f'<a class="lang" href="{SLUG[other].get(page, SLUG[other]["home"])}" lang="{other}" aria-label="{other_aria}">{c["nav"]["language"]}</a>'
    nav += f'<a class="nav-cta" href="{SLUG[lang]["contact"]}">{E(c["nav"]["contact"])}{ARROW}</a>'
    if page == 'home':
        title = c['meta']['title']
    elif page == 'yanki':
        title = c['yanki']['title'] + ' — Yankı'
    else:
        fallback_lbl = c['footer']['privacy'] if page == 'privacy' else '404'
        title = c['nav'].get(page, fallback_lbl) + ' — Mevlana Yalçın'
    description = c['meta']['description'] if page in ['home', 'approach'] else c.get(page, {}).get('body', c['meta']['description'])
    schema = structured_data(lang, page, canonical)
    og_image = 'https://' + DOMAIN + ('/og-tr.png' if lang == 'tr' else '/og.png')
    og_alt = 'Mevlana Yalçın — ' + ('Yankı AI Doğrulama Platformu ve Sistem Mühendisliği' if lang == 'tr' else 'Yankı AI Verification Platform & Systems Engineering')
    alts = ''.join(f'<link rel="alternate" hreflang="{d}" href="https://{DOMAIN}{SLUG[d].get(page, SLUG[d]["home"])}">' for d in SLUG)
    footer_aria = 'Alt bağlantılar' if lang == 'tr' else 'Footer'
    src_label = 'Kaynak kodu (MIT)' if lang == 'tr' else 'Source code (MIT)'
    footer = (
        f'<footer class="footer wrap"><div class="footer-top">{brand(lang)}'
        f'<p class="footer-copy">{E(c["footer"]["description"])}<br>{E(c["footer"]["location"])}</p></div>'
        f'<div class="footer-bottom"><span>© 2026 Mevlana Yalçın</span>'
        f'<nav class="footer-links" aria-label="{footer_aria}">'
        f'<a href="{SLUG[lang]["company"]}">{E(c["footer"]["legal"])}</a>'
        f'<a href="{SLUG[lang]["contact"]}">{E(c["nav"]["contact"])}</a>'
        f'<a href="{SLUG[lang]["privacy"]}">{E(c["footer"]["privacy"])}</a>'
        f'<a href="{SLUG[lang]["terms"]}">{E(c["nav"]["terms"])}</a>'
        f'<a href="{SLUG[lang]["notes"]}">{E(c["nav"]["notes"])}</a>'
        f'<a href="{SLUG[lang]["audit"]}">{E(c["audit"]["eyebrow"])}</a>'
        f'<a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>'
        f'<a href="{PROFIL}" target="_blank" rel="noopener noreferrer">GitHub ↗</a>'
        f'<a href="{DEPO}" target="_blank" rel="noopener noreferrer">{src_label} ↗</a>'
        f'<a href="mailto:{POSTA}" class="email-link">{POSTA}</a></nav></div></footer>'
    )
    locale_str = 'tr_TR' if lang == 'tr' else 'en_US'
    skip_str = 'İçeriğe geç' if lang == 'tr' else 'Skip to content'
    menu_aria = 'Ana menü' if lang == 'tr' else 'Main navigation'
    menu_btn = 'Menü' if lang == 'tr' else 'Menu'
    extra_js = f'<script src="/assets/app.js?v={version}" defer></script>' if page == 'yanki' else ''
    return (
        f'<!DOCTYPE html>\n<html lang="{lang}"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{E(title)}</title><meta name="description" content="{E(description, quote=True)}">'
        f'<meta name="theme-color" content="#f4f3ee"><link rel="canonical" href="{canonical}">{alts}'
        f'<link rel="alternate" hreflang="x-default" href="https://{DOMAIN}{SLUG["en"].get(page, "/")}">'
        f'<meta property="og:type" content="website"><meta property="og:title" content="{E(title, quote=True)}">'
        f'<meta property="og:description" content="{E(description, quote=True)}"><meta property="og:url" content="{canonical}">'
        f'<meta property="og:site_name" content="Mevlana Yalçın"><meta name="twitter:card" content="summary_large_image">'
        f'<meta property="og:image" content="{og_image}"><meta property="og:image:type" content="image/png">'
        f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
        f'<meta property="og:image:alt" content="{E(og_alt, quote=True)}"><meta property="og:locale" content="{locale_str}">'
        f'<meta name="twitter:image" content="{og_image}"><meta name="twitter:image:alt" content="{E(og_alt, quote=True)}">'
        f'<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">'
        f'<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/favicon.svg" type="image/svg+xml">'
        f'<link rel="stylesheet" href="/assets/site.css?v={version}">'
        f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head>\n'
        f'<body><a class="skip" href="#main">{skip_str}</a>'
        f'<header class="header wrap">{brand(lang)}<nav class="nav" id="menu" aria-label="{menu_aria}">{nav}</nav>'
        f'<button class="menu-toggle" id="menudugme" type="button" aria-expanded="false" aria-controls="menu">{menu_btn}</button></header>'
        f'<main id="main">{breadcrumbs(lang, page)}{content(lang, page)}{contact(lang)}</main>'
        f'{footer}<script src="/assets/nav.js?v={version}" defer></script>{extra_js}</body></html>'
    )


def main():
    assets = KOK / 'site' / 'assets'
    fingerprint = hashlib.sha256(b''.join(p.read_bytes() for p in sorted(assets.iterdir()) if p.is_file())).hexdigest()[:10]
    if CIKTI.exists():
        shutil.rmtree(CIKTI)
    shutil.copytree(assets, CIKTI / 'assets')
    for lang in SLUG:
        for page, path in SLUG[lang].items():
            target = CIKTI / path.strip('/') / 'index.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(shell(lang, page, fingerprint), encoding='utf-8')
    (CIKTI / '404.html').write_text(shell('en', '404', fingerprint), encoding='utf-8')
    tarih = CONTENT_UPDATED
    urls = sorted('https://' + DOMAIN + u for routes in SLUG.values() for u in routes.values())
    (CIKTI / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + ''.join(f'<url><loc>{u}</loc><lastmod>{tarih}</lastmod></url>' for u in urls)
        + '</urlset>'
    )
    (CIKTI / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n')
    llms = (
        '# Mevlana Yalçın — Yankı AI Verification Platform & Systems Engineering\n\n'
        + COPY['en']['meta']['description']
        + '\n\n## Identity\n'
        + COPY['en']['company']['body'] + '\n'
        + COPY['en']['company']['legal'] + '\n'
        + COPY['en']['company']['dates']
        + '\n\n## Platform & Open-Source Engine\n'
        '- **Yankı Cloud Gateway (In Active Development · Private Preview)**: Managed model-agnostic verification proxy, immutable citation audit logs, and policy console. Interactive public execution is disabled during private preview; curated production traces and early-access registration are available on `/work/yanki/`.\n'
        '- **Yankı Core Engine (`yanki` v0.2.0, MIT License)**: Dependency-free Python 3.11+ package (`src/yanki/`) providing index-preserving Turkish `İ/ı` Unicode offset mapping (`yanki.normalize`), single- & multi-source RAG citation verification (`verify_quote_grounding`, `verify_multi_source_citations`), pre-inference safety short-circuits (`yanki.guardrails`), `<think>`-aware strict JSON validation (`yanki.schema`), and unified `vLLM`/`SGLang`/OpenAI-compatible GPU benchmark harness (`24/24` passing in GitHub Actions CI).\n'
        f'- **Repository**: {DEPO}\n'
        f'- **Product & Trace Examples**: https://{DOMAIN}/work/yanki/\n\n## Pages\n'
    )
    for lang in SLUG:
        for page, path in SLUG[lang].items():
            llms += f'- [{lang}: {page}](https://{DOMAIN}{path})\n'
    (CIKTI / 'llms.txt').write_text(llms + '\nContact: ' + POSTA + '\n')
    for image in (KOK / 'site' / 'brand').iterdir():
        if image.is_file() and image.suffix in ('.png', '.ico'):
            shutil.copyfile(image, CIKTI / image.name)
    shutil.copyfile(CIKTI / 'og.png', CIKTI / 'assets' / 'og.png')
    shutil.copyfile(CIKTI / 'apple-touch-icon.png', CIKTI / 'assets' / 'apple-touch-icon.png')
    (CIKTI / 'favicon.svg').write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="6" fill="#222a27"/>'
        '<path d="M7 37V11h7l10 14 10-14h7v26h-7V24L24 38 14 24v13Z" fill="#f4f3ee"/><path d="M34 33h7v7h-7z" fill="#d95535"/></svg>'
    )
    if (KOK / 'funding.json').is_file():
        shutil.copyfile(KOK / 'funding.json', CIKTI / 'funding.json')
    if (KOK / '.well-known').is_dir():
        shutil.copytree(KOK / '.well-known', CIKTI / '.well-known', dirs_exist_ok=True)
    print(f'Built {len(urls)} bilingual pages, local assets, sitemap and 404.')


if __name__ == '__main__':
    main()
