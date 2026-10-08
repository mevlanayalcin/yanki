#!/usr/bin/env python3
"""Build the bilingual consulting website and product pages from local sources."""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
import shutil

from site_copy import COPY

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / 'dist'
DOMAIN = 'mevlanayalcin.com.tr'
POSTA = 'info@' + DOMAIN
DEPO = 'https://github.com/mevlanayalcin/yanki'
PROFIL = 'https://github.com/mevlanayalcin'
LINKEDIN = 'https://www.linkedin.com/in/mevlanayalcin'
OG_GORSEL = 'https://mevlanayalcin.com.tr/assets/og.png'
SLUG = {
    'en': {'home': '/', 'services': '/services/', 'products': '/products/', 'approach': '/process/', 'company': '/company/', 'privacy': '/privacy/', 'yanki': '/work/yanki/', 'audit': '/work/inference-audit/', 'terms': '/terms/'},
    'tr': {'home': '/tr/', 'services': '/tr/hizmetler/', 'products': '/tr/urunler/', 'approach': '/tr/surec/', 'company': '/tr/kurumsal/', 'privacy': '/tr/gizlilik/', 'yanki': '/tr/calismalar/yanki/', 'audit': '/tr/calismalar/inference-denetimi/', 'terms': '/tr/sartlar/'},
}
E = html.escape
ARROW = '<span class="arrow" aria-hidden="true">↗</span>'
MARK = '<svg class="brandmark" aria-hidden="true" viewBox="0 0 40 40" fill="none"><path d="M2 34V6h8l10 15L30 6h8v28h-8V20L20 35 10 20v14H2Z" fill="currentColor"/><path d="M31 30h7v7h-7z" fill="#d95535"/></svg>'


def link(text, href, cls='text-link', external=False):
    extra = ' target="_blank" rel="noopener noreferrer"' if external else ''
    return f'<a class="{cls}" href="{E(href, quote=True)}"{extra}>{E(text)}{ARROW}</a>'


def brand(lang):
    return f'<a class="brand" href="{SLUG[lang]["home"]}" aria-label="Mevlana Yalçın — {"Ana sayfa" if lang == "tr" else "Home"}">{MARK}<span class="brand-name">Mevlana Yalçın<small>AI consulting</small></span></a>'


def heading(eyebrow, title, body='', compact=False):
    return f'<div class="section-top{" compact" if compact else ""}"><p class="eyebrow">{E(eyebrow)}</p><div><h2>{E(title)}</h2>{f"<p class=\"section-intro\">{E(body)}</p>" if body else ""}</div></div>'


def service_list(lang):
    rows = []
    for s in COPY[lang]['services']['items']:
        tags = ''.join(f'<span class="tag">{E(t)}</span>' for t in s['tags'])
        fiyat = (COPY[lang].get('prices') or {}).get('items', {}).get(s['number'], '')
        if fiyat:
            tags += f'<span class="tag price">{E(fiyat)}</span>'
        label = f'{s["title"]} — {COPY[lang]["contact"]["cta"]}'
        rows.append(f'<article class="service-row"><span class="service-number">{s["number"]}</span><h3>{E(s["title"])}</h3><div class="service-body"><p>{E(s["body"])}</p><div class="tags">{tags}</div></div><a class="row-arrow" href="#contact" aria-label="{E(label, quote=True)}">{ARROW}</a></article>')
    return '<div class="service-list">' + ''.join(rows) + '</div>'


def product_art(lang):
    line = 'Bugün, kendi kelimelerinle.' if lang == 'tr' else 'Today, in your own words.'
    small = 'CLAUDE İLE YANSITMA' if lang == 'tr' else 'REFLECTION WITH CLAUDE'
    return f'<div class="product-art yanki" aria-hidden="true"><span class="artifact-label">YANKI / CLAUDE API</span><div class="note-preview"><div class="preview-brand">yankı<i></i></div><p>{line}</p><div class="note-line"></div><small>{small}</small></div></div>'


def products(lang):
    items = []
    for p in COPY[lang]['products']['items']:
        href = SLUG[lang]['yanki'] if p['slug'] == 'yanki' else p['href']
        items.append(f'<article class="product-card">{product_art(lang)}<div class="product-copy"><div class="product-topline"><span class="product-name">{E(p["name"])}</span><span class="product-status">{E(p["status"])}</span></div><h3>{E(p["title"])}</h3><p>{E(p["body"])}</p>{link(p["cta"],href,external=href.startswith("https:"))}<span class="product-category">{E(p["category"])}</span></div></article>')
    return '<div class="product-grid one">' + ''.join(items) + '</div>'


def claude_evidence(lang):
    c = COPY[lang]['claude']
    items = ''.join(f'<article class="step"><span class="step-number">0{i+1}</span><h3>{E(item["title"])}</h3><p>{E(item["body"])}</p></article>' for i,item in enumerate(c['items']))
    return f'<section class="section wrap claude-evidence" id="claude">{heading(c["eyebrow"],c["title"],c["body"])}<div class="approach-grid">{items}</div><div class="actions">{link(c["cta"],SLUG[lang]["yanki"],"button")}{link(c["source_label"],DEPO,external=True)}</div></section>'


def process(lang):
    rows = ''.join(f'<article class="step"><span class="step-number">{s["number"]}</span><h3>{E(s["title"])}</h3><p>{E(s["body"])}</p></article>' for s in COPY[lang]['process']['steps'])
    return f'<div class="approach-grid">{rows}</div>'


def contact(lang):
    c = COPY[lang]['contact']
    subject = 'Proje görüşmesi' if lang == 'tr' else 'Project enquiry'
    from urllib.parse import quote
    return f'<section class="contact" id="contact"><div class="wrap contact-top"><div><p class="eyebrow">{E(c["eyebrow"])}</p><h2>{E(c["title"])}</h2><p>{E(c["body"])}</p></div><div class="contact-action">{link(c["cta"], "mailto:"+POSTA+"?subject="+quote(subject), "button light")}<a class="contact-email" href="mailto:{POSTA}">{POSTA}</a></div></div></section>'


def home(lang):
    c = COPY[lang]; h = c['hero']
    names = ['Düşün', 'Geliştir', 'Yayınla'] if lang == 'tr' else ['Think', 'Build', 'Ship']
    caps = ''.join(f'<span><b>0{i+1}</b>{name}</span>' for i, name in enumerate(names))
    s,p,a = c['services'],c['products'],c['process']
    return f'''<section class="hero wrap">
<div class="hero-top"><p class="eyebrow">{E(h['eyebrow'])}</p><span class="location"><span class="status-dot"></span>Ankara, Türkiye</span></div>
<div class="hero-grid"><div class="hero-copy"><h1>{E(h['title'])}<span class="accent">{E(h['title_accent'])}</span></h1><p>{E(h['body'])}</p><div class="actions">{link(h['primary'],SLUG[lang]['yanki'],'button')}{link(h['secondary'],'#claude')}</div></div>
<div class="hero-art"><img src="/assets/structure.svg" width="620" height="620" alt="" fetchpriority="high"><div class="art-caption"><span>{'Fikirden sisteme' if lang=='tr' else 'From possibility to practice'}</span><span>MY / 01</span></div></div></div>
<div class="hero-bottom"><span>{E(h['note'])}</span><div class="capabilities">{caps}</div></div></section>
<section class="intro wrap">{heading(c['intro']['eyebrow'],c['intro']['title'],c['intro']['body'])}</section>
<section class="section products-section" id="products"><div class="wrap">{heading(p['eyebrow'],p['title'],p['body'])}{products(lang)}</div></section>
{claude_evidence(lang)}
<section class="section wrap" id="expertise">{heading(s['eyebrow'],s['title'],s['body'])}{service_list(lang)}<div class="section-foot">{link(c['nav']['services'],SLUG[lang]['services'])}</div></section>
<section class="section wrap">{heading(a['eyebrow'],a['title'])}{process(lang)}</section>
<section class="company-strip wrap"><p class="eyebrow">{E(c['company']['eyebrow'])}</p><div><h2>{E(c['company']['title'])}</h2><p>{E(c['company']['body'])}</p>{link(c['nav']['company'],SLUG[lang]['company'])}</div></section>'''


def page_hero(lang, key, title=None, body=None):
    c = COPY[lang][key]
    return f'<section class="page-hero wrap"><p class="eyebrow">{E(c["eyebrow"])}</p><h1>{E(title or c["title"])}</h1><p class="lede">{E(body if body is not None else c.get("body",c.get("intro","")))}</p></section>'


def yanki(lang):
    c = COPY[lang]['yanki']; tr = lang == 'tr'
    features = ''.join(f'<div class="feature"><h3>{E(f["title"])}</h3><p>{E(f["body"])}</p></div>' for f in c['features'])
    tech_title = 'Claude entegrasyonu ve API' if tr else 'Claude integration & API'
    tech_body = ('Yansıtma için Anthropic Messages API ve claude-haiku-4-5-20251001 kullanılır. Yanıt biçimi ve alıntılar uygulamada kontrol edilir. Kriz sözcükleri için model çağrısından önce ayrı bir kural kontrolü yapılır. Bu kontrol tüm acil durumları tespit edemez.' if tr else 'Reflections use the Anthropic Messages API and claude-haiku-4-5-20251001. The application checks the response format and quotes. A separate rule checks for crisis words before calling the model. This check cannot identify every emergency.')
    return page_hero(lang,'yanki') + f'''<section class="page-content wrap"><div class="yanki-layout"><div class="product-description"><h2>{E(c['cta'])}</h2>{features}<p class="tech-note">{E(c['safety'])}</p></div><div class="reflection-box"><div class="product-topline"><span class="product-name">yankı</span><span class="product-status">{E(c['status'])}</span></div><label for="girdi">{E(c['input_label'])}</label><textarea id="girdi" minlength="8" maxlength="600" rows="5" placeholder="{E(c['input_placeholder'],quote=True)}" aria-describedby="reflection-privacy"></textarea><button class="button" id="yansit" type="button">{E(c['input_button'])}{ARROW}</button><p class="form-status" id="durum" role="status" aria-live="polite"></p><div class="reflection-result" id="sonuc" aria-live="polite" hidden></div><p class="form-note" id="reflection-privacy">{E(c['privacy_note'])} <a href="{SLUG[lang]['privacy']}">{E(COPY[lang]['nav'].get('privacy',COPY[lang]['footer']['privacy']))} ↗</a></p></div></div><details class="technical" id="api"><summary>{tech_title}</summary><div class="technical-content"><p>{tech_body}</p><p><code>POST /api/reflect</code> · <code>{{"text": "…", "lang": "en|tr"}}</code> · 8–600 {'karakter' if tr else 'characters'}</p><p>{'İstek ve günlük kullanım sınırları uygulanır. Hizmet kullanılamıyorsa arayüz hata gösterir.' if tr else 'Request and daily usage limits apply. The interface shows an error when the service is unavailable.'}</p><p> · <a href="/api/health">{'Servis bilgisi' if tr else 'Service metadata'}</a></p></div></details></section>'''


def content(lang, page):
    c = COPY[lang]
    if page == 'home': return home(lang)
    if page == 'services':
        pr = c.get('prices') or {}
        ek_not = (f'<div class="tech-note">{E(pr.get("retainer",""))}</div>' if pr.get('retainer') else '') + \
                 (f'<p class="legal-note">{E(pr.get("note",""))}</p>' if pr.get('note') else '')
        return page_hero(lang,'services') + f'<section class="page-content wrap">{service_list(lang)}<div class="tech-note">{E(c["services"]["body"])}</div>{ek_not}{link(c["audit"]["cta"], SLUG[lang]["audit"])}</section>'
    if page == 'products':
        return page_hero(lang,'products') + f'<section class="page-content wrap">{products(lang)}</section>' + claude_evidence(lang)
    if page == 'approach':
        return page_hero(lang,'process',body=c['services']['body']) + f'<section class="page-content wrap">{process(lang)}</section>'
    if page == 'company':
        cc = c['company']
        facts = ''.join(f'<div class="fact"><dt>{E(f["label"])}</dt><dd>{E(f["value"])}</dd></div>' for f in cc['facts'])
        return page_hero(lang,'company') + f'<section class="page-content wrap"><dl class="facts">{facts}</dl><p class="legal-note">{E(cc["legal"])}</p><p class="legal-note">{E(cc["dates"])}</p><div class="technical"><h2>{"Yankı’da Claude kullanımı" if lang=="tr" else "Claude in Yankı"}</h2><p class="legal-note">{E(cc["model_use"])}</p>{link(c["nav"]["products"],SLUG[lang]["products"])}</div></section>'
    if page == 'privacy':
        sections = ''.join(f'<section class="prose-section"><h2>{E(s["title"])}</h2><p>{E(s["body"])}</p></section>' for s in c['privacy']['sections'])
        return page_hero(lang,'privacy') + f'<div class="page-content wrap"><div class="prose">{sections}</div></div>'
    if page == 'audit':
        a = c['audit']
        yontem = ''.join(f'<li>{E(m)}</li>' for m in a['method'])
        bulgular = ''.join(f'<article class="step"><span class="step-number">0{i+1}</span><h3>{E(f["title"])}</h3><p>{E(f["body"])}</p></article>'
                           for i, f in enumerate(a['findings']))
        return page_hero(lang, 'audit') + f"""<section class="page-content wrap">
<div class="prose"><h2>{E(a['method_title'])}</h2><ul class="method-list">{yontem}</ul>
<p class="legal-note">{E(a['evidence_note'])}</p></div>
<h2 class="findings-title">{E(a['findings_title'])}</h2><div class="approach-grid">{bulgular}</div>
<div class="prose"><h2>{E(a['outcome_title'])}</h2><p>{E(a['outcome'])}</p></div>
<div class="actions">{link(a['cta'], '#contact', 'button')}{link(c['nav']['services'], SLUG[lang]['services'])}</div>
</section>"""
    if page == 'terms':
        t = c['terms']
        parcalar = ''.join(f'<section class="prose-section"><h2>{E(s["title"])}</h2><p>{E(s["body"])}</p></section>'
                           for s in t['sections'])
        return page_hero(lang, 'terms') + f'<div class="page-content wrap"><div class="prose">{parcalar}</div><div class="actions">{link(t["cta"], "mailto:" + POSTA, "button")}</div></div>'
    if page == 'yanki': return yanki(lang)
    return f'<section class="not-found wrap"><p class="eyebrow">404</p><h1>{E(c["labels"]["not_found_title"])}</h1><p>{E(c["labels"]["not_found_body"])}</p>{link(c["labels"]["back"],SLUG[lang]["home"],"button")}</section>'


def shell(lang, page, version):
    c = COPY[lang]; other = 'tr' if lang == 'en' else 'en'; canonical = 'https://' + DOMAIN + SLUG[lang].get(page,'/404.html')
    nav = ''.join(f'<a href="{SLUG[lang][key]}"'+(' aria-current="page"' if key==page else '')+f'>{E(c["nav"][key])}</a>' for key in ['services','products','approach','company'])
    nav += f'<a class="lang" href="{SLUG[other].get(page,SLUG[other]["home"])}" lang="{other}" aria-label="{ "Türkçe" if other=="tr" else "English"}">{c["nav"]["language"]}</a><a class="nav-cta" href="#contact">{E(c["nav"]["contact"])}{ARROW}</a>'
    title = c['meta']['title'] if page == 'home' else (c['yanki']['title'] + ' — Yankı' if page == 'yanki' else c['nav'].get(page,c['footer']['privacy'] if page == 'privacy' else '404') + ' — Mevlana Yalçın')
    description = c['meta']['description'] if page in ['home','approach'] else c.get(page,{}).get('body',c['meta']['description'])
    schema = {'@context':'https://schema.org','@type':'ProfessionalService','name':'Mevlana Yalçın','url':'https://'+DOMAIN,'description':c['meta']['description'],'email':POSTA,'founder':{'@type':'Person','name':'Mevlana Yalçın','jobTitle':'Founder & Principal Consultant','sameAs':[PROFIL, LINKEDIN]},"sameAs":[PROFIL, DEPO, LINKEDIN],'areaServed':['Global','TR'],'priceRange':'$$-$$$','contactPoint':{'@type':'ContactPoint','email':POSTA,'availableLanguage':['en','tr'],'contactType':'sales'},'address':{'@type':'PostalAddress','addressLocality':'Ankara','addressCountry':'TR'},'knowsAbout':['AI consulting','Product engineering','AI evaluation']}
    alts = ''.join(f'<link rel="alternate" hreflang="{d}" href="https://{DOMAIN}{SLUG[d].get(page,SLUG[d]["home"])}">' for d in SLUG)
    footer = f'''<footer class="footer wrap"><div class="footer-top">{brand(lang)}<p class="footer-copy">{E(c['footer']['description'])}<br>{E(c['footer']['location'])}</p></div><div class="footer-bottom"><span>© 2026 Mevlana Yalçın</span><nav class="footer-links" aria-label="{'Alt bağlantılar' if lang=='tr' else 'Footer'}"><a href="{SLUG[lang]['company']}">{E(c['footer']['legal'])}</a><a href="{SLUG[lang]['privacy']}">{E(c['footer']['privacy'])}</a><a href="{SLUG[lang]['terms']}">{E(c['terms']['title'])}</a><a href="{SLUG[lang]['audit']}">{E(c['audit']['eyebrow'])}</a><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a href="{PROFIL}" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="{DEPO}" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="mailto:{POSTA}" class="email-link">{POSTA}</a></nav></div></footer>'''
    return f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(description,quote=True)}"><meta name="theme-color" content="#f4f3ee"><link rel="canonical" href="{canonical}">{alts}<link rel="alternate" hreflang="x-default" href="https://{DOMAIN}{SLUG['en'].get(page,'/')}"><meta property="og:type" content="website"><meta property="og:title" content="{E(title,quote=True)}"><meta property="og:description" content="{E(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="Mevlana Yalçın"><meta name="twitter:card" content="summary_large_image"><meta property="og:image" content="{OG_GORSEL}"><meta name="twitter:image" content="{OG_GORSEL}"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css?v={version}"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head>
<body><a class="skip" href="#main">{'İçeriğe geç' if lang=='tr' else 'Skip to content'}</a><header class="header wrap">{brand(lang)}<nav class="nav" id="menu" aria-label="{'Ana menü' if lang=='tr' else 'Main navigation'}">{nav}</nav><button class="menu-toggle" id="menudugme" aria-expanded="false" aria-controls="menu">{'Menü' if lang=='tr' else 'Menu'}</button></header><main id="main">{content(lang,page)}{contact(lang)}</main>{footer}<script src="/assets/nav.js?v={version}" defer></script>{f'<script src="/assets/app.js?v={version}" defer></script>' if page=='yanki' else ''}</body></html>'''


def gorseller(cikti):
    """Marka gorsellerini uretir: og.png (1200x630), apple-touch-icon, favicon.ico."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        print('PIL yok: og gorseli/ico atlandi')
        return
    FON = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    zemin, metin, vurgu = (244, 243, 238), (34, 42, 39), (217, 85, 53)

    def yazi(boyut):
        return ImageFont.truetype(FON, boyut) if Path(FON).exists() else ImageFont.load_default()

    g = Image.new('RGB', (1200, 630), zemin)
    d = ImageDraw.Draw(g)
    d.text((86, 140), "Mevlana Yalçın", font=yazi(84), fill=vurgu)
    d.text((86, 258), "AI consulting with Claude", font=yazi(52), fill=metin)
    d.text((86, 342), "Audits · integration · evaluation  ·  Ankara, Türkiye", font=yazi(30), fill=(90, 96, 92))
    d.rectangle([86, 462, 156, 478], fill=vurgu)
    d.text((86, 506), "mevlanayalcin.com.tr", font=yazi(30), fill=metin)
    (cikti / 'assets').mkdir(parents=True, exist_ok=True)
    g.save(cikti / 'assets' / 'og.png')

    def kare(boyut):
        i = Image.new('RGB', (boyut, boyut), (34, 42, 39))
        dd = ImageDraw.Draw(i)
        k = max(6, boyut // 5)
        dd.text((k, int(boyut * 0.20)), "M", font=yazi(int(boyut * 0.60)), fill=(244, 243, 238))
        dd.rectangle([boyut - k - 4, boyut - k - 4, boyut - 4, boyut - 4], fill=vurgu)
        return i

    kare(180).save(cikti / 'assets' / 'apple-touch-icon.png')
    kare(64).save(cikti / 'favicon.ico')


def main():
    assets = KOK / 'site' / 'assets'
    fingerprint = hashlib.sha256(b''.join(p.read_bytes() for p in sorted(assets.iterdir()) if p.is_file())).hexdigest()[:10]
    if CIKTI.exists(): shutil.rmtree(CIKTI)
    shutil.copytree(assets, CIKTI / 'assets')
    for lang in SLUG:
        for page, path in SLUG[lang].items():
            target = CIKTI / path.strip('/') / 'index.html'
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(shell(lang,page,fingerprint),encoding='utf-8')
    (CIKTI/'404.html').write_text(shell('en','404',fingerprint),encoding='utf-8')
    import datetime
    tarih = datetime.date.today().isoformat()
    urls = sorted('https://'+DOMAIN+u for routes in SLUG.values() for u in routes.values())
    (CIKTI/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc><lastmod>{tarih}</lastmod></url>' for u in urls)+'</urlset>')
    (CIKTI/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n')
    llms = '# Mevlana Yalçın — AI consulting with Claude\n\n'+COPY['en']['meta']['description']+'\n\n## Identity\n'+COPY['en']['company']['body']+'\n'+COPY['en']['company']['legal']+'\n'+COPY['en']['company']['dates']+'\n\n## Product\n- Yankı: live beta for personal reflection. Uses Anthropic Messages API. Not therapy or medical advice.\n\n## Pages\n'
    for lang in SLUG:
        for page,path in SLUG[lang].items(): llms += f'- [{lang}: {page}](https://{DOMAIN}{path})\n'
    (CIKTI/'llms.txt').write_text(llms+'\nContact: '+POSTA+'\n')
    gorseller(CIKTI)
    (CIKTI/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="6" fill="#222a27"/><path d="M7 37V11h7l10 14 10-14h7v26h-7V24L24 38 14 24v13Z" fill="#f4f3ee"/><path d="M34 33h7v7h-7z" fill="#d95535"/></svg>')
    print(f'Built {len(urls)} bilingual pages, local assets, sitemap and 404.')

if __name__ == '__main__': main()
