#!/usr/bin/env python3
"""mevlanayalcin.com.tr statik sitesini uretir (dist/).

Icerigin tek kaynagi scripts/icerik.py; HTML iskeleti iki dilde ortaktir. Yanki artik
sitenin kimligi degil, /work/yanki/ (TR: /calismalar/yanki/) sayfasinda duran bir vakadir:
demo kutusu ve canli /api/reflect ucu orada yasamaya devam eder.
"""

from __future__ import annotations

import html
import json
import pathlib
import re
import sys

KOK = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "scripts"))

from icerik import (  # noqa: E402
    CIKTI, DEPO, DOMAIN, ICERIK, KOK_YOL, POSTA, SLUG, SURUM, tam_url, url,
)

C = CIKTI  # kisaltma


def _e(metin: str) -> str:
    return html.escape(str(metin), quote=True)


def _fiyat_say(ifade: str) -> str:
    """'from $4,500' / \"4.500 $'dan\" / 'ayda 1.200 $'dan' -> '4500'."""
    rakamlar = re.sub(r"[^\d]", "", ifade.replace("1.200", "1200"))
    return rakamlar[:7] or "0"


def menu(dil: str, aktif: str) -> str:
    satirlar = []
    for anahtar, ad in ICERIK[dil]["sayfalar"]:
        isaret = ' class="aktif"' if anahtar == aktif else ""
        satirlar.append('<a href="%s"%s>%s</a>' % (url(dil, anahtar), isaret, _e(ad)))
    digeri = "tr" if dil == "en" else "en"
    satirlar.append('<a class="dil" href="%s">%s</a>'
                    % (url(digeri, "index") or "/", _e(ICERIK[dil]["menuDilleri"][dil])))
    return "\n      ".join(satirlar)


def _jsonld(dil: str, canonical: str) -> dict:
    i = ICERIK[dil]
    teklifler = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": p["ad"]},
                  "priceSpecification": {"@type": "PriceSpecification",
                                         "priceCurrency": "USD", "price": _fiyat_say(p["fiyat"])}
                  } for p in i["hizmetler"]["paketler"]]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "ProfessionalService", "@id": "https://%s/#org" % DOMAIN,
             "name": "%s — AI consulting" % ("Mevlana Yalçın"), "alternateName": "Yankı",
             "url": "https://%s/" % DOMAIN, "email": POSTA,
             "description": i["ozet"],
             "founder": {"@type": "Person", "name": "Mevlana Yalçın"},
             "numberOfEmployees": {"@type": "QuantitativeValue", "value": 1},
             "areaServed": ["TR", "Global"],
             "address": {"@type": "PostalAddress", "addressLocality": "Ankara",
                         "addressCountry": "TR"},
             "codeRepository": DEPO,
             "makesOffer": teklifler},
            {"@type": "SoftwareApplication", "name": "Yankı",
             "url": tam_url(dil, "yanki"), "applicationCategory": "LifestyleApplication",
             "operatingSystem": "Web", "inLanguage": ["en", "tr"],
             "publisher": {"@id": "https://%s/#org" % DOMAIN}},
        ],
    }


def kabuk(dil: str, anahtar: str, baslik: str, aciklama: str, govde: str, canonical: str) -> str:
    i = ICERIK[dil]
    betik = ('<script src="/assets/app.js?v=%s" defer></script>' % SURUM
             if anahtar in ("index", "yanki") else "")
    return """<!DOCTYPE html>
<html lang="%(dil)s"><head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>%(baslik)s</title>
<meta name="description" content="%(aciklama)s" />
<link rel="canonical" href="%(canonical)s" />
<meta property="og:type" content="website" />
<meta property="og:title" content="%(baslik)s" />
<meta property="og:description" content="%(aciklama)s" />
<meta property="og:url" content="%(canonical)s" />
<meta property="og:site_name" content="mevlanayalcin.com.tr" />
<meta name="twitter:card" content="summary" />
<link href="/assets/site.css?v=%(surum)s" rel="stylesheet" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<script type="application/ld+json">%(jsonld)s</script>
</head><body>
<header class="ust">
  <a class="kul" href="%(anasayfa)s">Mevlana Yalçın<span class="nokta">.</span></a>
  <nav class="menu" id="menu">%(menu)s</nav>
  <button class="menudugme" id="menudugme" aria-expanded="false" aria-controls="menu">%(menuEtiket)s</button>
</header>
<main>%(govde)s</main>
<footer class="alt">
  <p class="altbilgi">%(altbilgi)s</p>
  <p class="altlinkler">%(altlinkler)s</p>
</footer>
<script src="/assets/nav.js?v=%(surum)s" defer></script>
%(betik)s
</body></html>
""" % {
        "dil": dil, "baslik": _e(baslik), "aciklama": _e(aciklama), "canonical": canonical,
        "menu": menu(dil, anahtar), "govde": govde, "altbilgi": _e(i["altbilgi"]),
        "altlinkler": " · ".join('<a href="%s">%s</a>' % (u, _e(a)) for a, u in i["altLinkler"]),
        "surum": SURUM, "anasayfa": url(dil, "index") or "/", "betik": betik,
        "menuEtiket": _e(i["menuEtiketi"]),
        "jsonld": json.dumps(_jsonld(dil, canonical), ensure_ascii=False,
                             separators=(",", ":")),
    }


def _liste(maddeler, sirali=False):
    etiket = "ol" if sirali else "ul"
    return ('<%s class="maddeler">' % etiket
            + "".join("<li>%s</li>" % _e(m) for m in maddeler)
            + "</%s>" % etiket)


def _paketler(dil, kisa=False):
    i = ICERIK[dil]
    kartlar = []
    for p in i["hizmetler"]["paketler"]:
        alt = p["icerik"][:3] if kisa else p["icerik"]
        kartlar.append(
            '<article class="paket"><h3>%s</h3>'
            '<p class="paketMeta"><span class="etiket">%s</span><span class="fiyat">%s</span></p>'
            '<ul class="maddeler">%s</ul>%s</article>'
            % (_e(p["ad"]), _e(p["sure"]), _e(p["fiyat"]),
               "".join("<li>%s</li>" % _e(x) for x in alt),
               "" if kisa else '<p class="cikti">%s</p>' % _e(p["cikti"])))
    return '<div class="paketler">%s</div>' % "".join(kartlar)


def _ornekler(dil):
    dosya = KOK / "data" / "ornekler.json"
    if not dosya.exists():
        return ""
    veri = json.loads(dosya.read_text(encoding="utf-8"))
    i = ICERIK[dil]
    ba = "<h2>%s</h2><p class=\"alt\">%s</p>" % (_e(i["yanki"]["ornekler"]["baslik"]),
                                                 _e(i["yanki"]["ornekler"]["alti"]))
    kartlar = []
    for o in veri.get(dil) or veri.get("en") or []:
        kartlar.append(
            '<article class="ornek"><p class="soru">“%s”</p><dl>'
            "<dt>%s</dt><dd>%s <span class=\"siddet\">%s</span></dd>"
            "<dt>%s</dt><dd>%s</dd>"
            "<dt>%s</dt><dd>%s</dd>"
            "<dt>%s</dt><dd>%s</dd>"
            "</dl><p class=\"motor\">%s · %s</p></article>"
            % (_e(o["girdi"]),
               _e("Feeling" if dil == "en" else "Duygu"), _e(o.get("duygu") or "—"),
               _e(o.get("siddet") or ""),
               _e("Reflection" if dil == "en" else "Yansıtma"), _e(o.get("yansitma") or "—"),
               _e("Your words" if dil == "en" else "Senin cümlen"), _e(o.get("alıntı") or "—"),
               _e("Next step" if dil == "en" else "Adım"), _e(o.get("adım") or "—"),
               _e(o.get("provider") or ""), _e(o.get("model") or "")))
    return ba + '<div class="ornekler">%s</div>' % "".join(kartlar)


API_TABLO = """
<table class="sozlesme">
<tr><th>Method</th><td>POST</td></tr>
<tr><th>Path</th><td><code>/api/reflect</code></td></tr>
<tr><th>Request</th><td><code>{"text": string, "lang": "en"|"tr"}</code> — 8–600 characters</td></tr>
<tr><th>Response</th><td><code>{duygu, siddet, yansitma, alinti, adim, disclaimer, provider, model, cache}</code></td></tr>
<tr><th>Errors</th><td><code>bad_request</code> 400 · <code>too_long</code> 413 · <code>busy</code> 429 · <code>daily_budget</code> 503 · <code>upstream</code> 502</td></tr>
<tr><th>Rate limit</th><td>6 requests / 60 s per IP (Durable Object)</td></tr>
<tr><th>Budget</th><td>A daily payment-equivalent cap stops the endpoint before the balance runs out</td></tr>
<tr><th>Crisis wording</th><td>Decided by a rule list before the model call; the answer is replaced by helpline text</td></tr>
</table>
"""


def govde_uret(dil, anahtar):
    i = ICERIK[dil]
    if anahtar == "index":
        k = i["kahraman"]
        cta = i["cta"]
        kartlar = "".join(
            '<article class="vaka"><p class="etiket">%s</p><h3>%s</h3><p>%s</p>'
            '<p><a href="%s">%s</a></p></article>'
            % (_e(kart["etiket"]), _e(kart["ad"]), _e(kart["metin"]),
               url(dil, kart["bag"][0]) + ("#denetim" if kart["bag"][0] == "calismalar" and dil == "tr"
                                            else ("#audit" if kart["bag"][0] == "calismalar" else "")),
               _e(kart["bag"][1]))
            for kart in i["calismalar"]["kartlar"])
        return (
            '<section class="kahraman"><div class="iç">'
            '<p class="ustbaslik">%s</p><h1>%s</h1><p class="alti">%s</p><p class="durum">%s</p>'
            '<form class="bekleme" id="bekleme" action="/api/waitlist" method="post">'
            '<input type="email" name="email" required placeholder="%s" aria-label="%s" />'
            '<button type="submit">%s</button><p class="not" id="beklemeyanit">%s</p></form>'
            "</div>"
            '<div class="kutu"><h2 class="kutuBaslik">%s</h2>%s</div></section>'
            '<section class="ku"><h2>%s</h2><p class="alt">%s</p>%s'
            '<p><a href="%s">%s →</a></p></section>'
            '<section class="ku"><h2>%s</h2><p class="alt">%s</p><div class="paketler">%s</div>'
            '</section>'
            % (_e(k["ust"]), _e(k["baslik"]), _e(k["alti"]), _e(i["durum"]),
               _e(cta["yer"]), _e(cta["yer"]), _e(cta["dugme"]), _e(cta["not"]),
               _e(i["ozetKutu"]["baslik"]), _liste(i["ozetKutu"]["maddeler"]),
               _e(i["hizmetler"]["baslik"]), _e(i["hizmetler"]["alti"]), _paketler(dil, kisa=True),
               url(dil, "hizmetler"),
               _e("All three packages, with scope and price" if dil == "en"
                  else "Üç paketin kapsamı ve fiyatı"),
               _e(i["calismalar"]["baslik"]), _e(i["calismalar"]["alti"]), kartlar))
    if anahtar == "hizmetler":
        return ('<section class="ku"><h1>%s</h1><p class="alt">%s</p>%s</section>'
                % (_e(i["hizmetler"]["baslik"]), _e(i["hizmetler"]["alti"]), _paketler(dil)))
    if anahtar == "surec":
        adimlar = "".join('<li><h3>%s</h3><p>%s</p></li>' % (_e(b), _e(m))
                          for b, m in i["surec"]["adimlar"])
        return ('<section class="ku"><h1>%s</h1><ol class="adimlar">%s</ol>'
                '<p class="vurgu">%s</p></section>'
                % (_e(i["surec"]["baslik"]), adimlar,
                   _e(i["kurumsal"]["kunya"][2][1] if len(i["kurumsal"]["kunya"]) > 2 else "")))
    if anahtar == "calismalar":
        a = i["audit"]
        adimlar = "".join("<li><h3>%s</h3><p>%s</p></li>" % (_e(b), _e(m)) for b, m in a["adimlar"])
        bulgular = "".join("<details><summary>%s</summary><p>%s</p></details>" % (_e(b), _e(m))
                           for b, m in a["bulgular"])
        y = i["calismalar"]["kartlar"][1]
        bulgular = "".join("<details><summary>%s</summary><p>%s</p></details>" % (_e(b), _e(m))
                           for b, m in a["bulgular"])
        return (
            '<section class="ku"><h1>%s</h1><p class="alt">%s</p></section>'
            '<section class="ku" id="%s"><h2>%s</h2><p>%s</p>'
            '<h3>%s</h3><ol class="adimlar">%s</ol>'
            '<h3>%s</h3>%s<p class="motorNotu">%s</p></section>'
            '<section class="ku"><h2>%s</h2><p>%s</p><p><a href="%s">%s →</a></p></section>'
            % (_e(i["calismalar"]["baslik"]), _e(i["calismalar"]["alti"]),
               "audit" if dil == "en" else "denetim",
               _e(a["baslik"]), _e(a["alti"]),
               _e("Method" if dil == "en" else "Yöntem"), adimlar,
               _e("Findings" if dil == "en" else "Buluşlar"), bulgular, _e(a["sonuc"]),
               _e(y["ad"]), _e(y["metin"]), url(dil, "yanki"),
               _e("Open the live demo" if dil == "en" else "Canlı demoyu aç")))
    if anahtar == "yanki":
        y = i["yanki"]
        d = y["demo"]
        return (
            '<section class="ku"><p class="ustbaslik">%s</p><h1>%s</h1>'
            '<p class="alt">%s</p><p>%s</p></section>'
            '<section class="ku"><div class="kutu" id="kutu">'
            '<h2 class="kutuBaslik">%s</h2><p class="kutuAlti">%s</p>'
            '<textarea id="girdi" rows="3" placeholder="%s"></textarea>'
            '<div class="kutuEylem"><button id="yansit">%s</button>'
            '<span id="durum" aria-live="polite"></span></div>'
            '<div id="sonuc" hidden></div></div></section>'
            '<section class="ku">%s</section>'
            '<section class="ku"><h2>%s</h2>%s</section>'
            '<section class="ku"><h2>%s</h2>%s<p class="vurgu">%s</p></section>'
            '<section class="ku" id="api"><h2>%s</h2><p class="alt">%s</p>%s</section>'
            '<section class="ku"><h2>%s</h2>%s<ul class="dogrulama">%s</ul></section>'
            % (_e("Case study · live" if dil == "en" else "Vaka çalışması · yayında"),
               _e(y["baslik"]), _e(y["alti"]), _e(y["giris"]),
               _e(d["baslik"]), _e(d["alti"]), _e(d["yer"]), _e(d["dugme"]),
               _ornekler(dil),
               _e(y["mimari"]["baslik"]), _liste(y["mimari"]["maddeler"]),
               _e(y["guvenlik"]["baslik"]), _liste(y["guvenlik"]["maddeler"]),
               _e("Turkish: 112 · English: your local emergency number" if dil == "en"
                  else "Türkiye'de 112 · diğer ülkelerde kendi acil numaran"),
               _e(y["api"]["baslik"]), _e(y["api"]["metin"]), API_TABLO,
               _e(y["durum"]["baslik"]), _liste(y["durum"]["maddeler"]),
               "".join('<li><a href="%s">%s</a></li>' % (u, _e(ad))
                       for ad, u in i["kurumsal"]["dogrulama"])))
    if anahtar == "kurumsal":
        satirlar = "".join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (_e(b), _e(m))
                           for b, m in i["kurumsal"]["kunya"])
        dogr = "".join('<li><a href="%s">%s</a></li>' % (u, _e(ad))
                       for ad, u in i["kurumsal"]["dogrulama"])
        soru = "".join("<details><summary>%s</summary><p>%s</p></details>" % (_e(s), _e(c))
                       for s, c in i["kurumsal"]["soru"]["maddeler"])
        return ('<section class="ku"><h1>%s</h1><table class="kunya">%s</table></section>'
                '<section class="ku"><h2>%s</h2><ul class="dogrulama">%s</ul></section>'
                '<section class="ku"><h2>%s</h2>%s</section>'
                % (_e(i["kurumsal"]["baslik"]), satirlar,
                   _e("Verify this independently" if dil == "en" else "Bağımsız doğrulama"), dogr,
                   _e(i["kurumsal"]["soru"]["baslik"]), soru))
    if anahtar == "gizlilik":
        return '<section class="ku"><h1>%s</h1>%s</section>' % (
            _e(i["gizlilik"]["baslik"]), _liste(i["gizlilik"]["maddeler"]))
    return ""


def baslik_ve_aciklama(dil, anahtar):
    i = ICERIK[dil]
    if anahtar == "index":
        return i["baslik"], i["ozet"]
    if anahtar == "hizmetler":
        return "%s · %s" % (i["hizmetler"]["baslik"], "Mevlana Yalçın"), i["hizmetler"]["alti"]
    if anahtar == "surec":
        return "%s · Mevlana Yalçın" % i["surec"]["baslik"], i["surec"]["adimlar"][0][1]
    if anahtar == "calismalar":
        return ("%s · Mevlana Yalçın" % i["calismalar"]["baslik"], i["calismalar"]["alti"])
    if anahtar == "yanki":
        return "%s · Mevlana Yalçın" % i["yanki"]["baslik"], i["yanki"]["alti"]
    if anahtar == "kurumsal":
        return "%s · Mevlana Yalçın" % i["kurumsal"]["baslik"], i["kurumsal"]["kunya"][0][1]
    return "%s · Mevlana Yalçın" % i["gizlilik"]["baslik"], i["gizlilik"]["maddeler"][0]


def yaz(dosya, metin):
    dosya.parent.mkdir(parents=True, exist_ok=True)
    dosya.write_text(metin, encoding="utf-8")


def main():
    for dil in SLUG:
        for anahtar in SLUG[dil]:
            baslik, aciklama = baslik_ve_aciklama(dil, anahtar)
            yol = "%s%sindex.html" % (KOK_YOL[dil], SLUG[dil][anahtar])
            yaz(C / yol, kabuk(dil, anahtar, baslik, aciklama,
                               govde_uret(dil, anahtar), tam_url(dil, anahtar)))

    govde404 = (
        '<section class="ku"><p class="ustbaslik">404</p><h1>Bu adres bir sayfaya denk gelmiyor.</h1>'
        '<p>Bağlantıyı elle yazdıysan yolu kontrol et; bir yerden tıkladıysan bu tarafımızdaki bir '
        'eksik — <a href="mailto:%s">%s</a> adresine yazarsan düzeltiriz.</p>'
        '<p><a href="https://%s/">English home</a> · <a href="https://%s/tr/">Türkçe ana sayfa</a> · '
        '<a href="https://%s/tr/kurumsal/">Kurumsal</a></p></section>'
    ) % (POSTA, POSTA, DOMAIN, DOMAIN, DOMAIN)
    yaz(C / "404.html", kabuk("en", "__404__", "Sayfa bulunamadı · Mevlana Yalçın",
                              ICERIK["en"]["ozet"], govde404, "https://%s/404" % DOMAIN))

    adresler = sorted({tam_url(d, a) for d in SLUG for a in SLUG[d]})
    yaz(C / "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join("<url><loc>%s</loc></url>" % u for u in adresler) + "</urlset>")
    yaz(C / "robots.txt", "User-agent: *\nAllow: /\nSitemap: https://%s/sitemap.xml\n" % DOMAIN)

    i = ICERIK["en"]
    llms = [
        "# Mevlana Yalçın — AI consulting (mevlanayalcin.com.tr)", "",
        "> " + i["ozet"], "",
        "Independent consultant in Ankara. Fixed-scope audits of LLM cost, latency, SLA behaviour",
        "and supply-chain/security exposure. No capacity is resold, so findings carry no commission.",
        "Claude is used in production on the case study below.", "",
        "## Pages", "",
        "- [Consulting](%s): positioning, what lands on the table" % tam_url("en", "index"),
        "- [Services](%s): three packages with scope, duration and price anchors" % tam_url("en", "hizmetler"),
        "- [Process](%s): five steps, read-only measurement first" % tam_url("en", "surec"),
        "- [Work](%s): method and findings of an inference exchange audit" % tam_url("en", "calismalar"),
        "- [Case study — Yankı](%s): live Claude product, demo box and API contract" % tam_url("en", "yanki"),
        "- [Company](%s): identity, verification links, questions worth asking first" % tam_url("en", "kurumsal"),
        "- [Privacy](%s): site and client-data handling, sub-processors, KVKK" % tam_url("en", "gizlilik"),
        "",
        "### Türkçe", "",
        "- [Danışmanlık](%s)" % tam_url("tr", "index"),
        "- [Hizmetler](%s)" % tam_url("tr", "hizmetler"),
        "- [Süreç](%s)" % tam_url("tr", "surec"),
        "- [Çalışmalar](%s)" % tam_url("tr", "calismalar"),
        "- [Vaka — Yankı](%s)" % tam_url("tr", "yanki"),
        "- [Kurumsal](%s)" % tam_url("tr", "kurumsal"),
        "- [Gizlilik](%s)" % tam_url("tr", "gizlilik"),
        "",
        "## Facts kept separate on purpose", "",
        "- mevlanayalcin.com.tr is a personal domain held since September 2023.",
        "- The consulting practice and the Yankı product both began in October 2026.",
        "- One person, Ankara. No registered legal entity yet; a sole proprietorship is opened with the first paid engagement.",
        "- Yankı: Anthropic Messages API, claude-haiku-4-5-20251001, JSON-only output enforced server-side, rule-based crisis handling, no session storage during the beta.",
        "- Live endpoints: POST /api/reflect, POST /api/waitlist, GET /api/health.",
        "- Contact: " + POSTA,
    ]
    yaz(C / "llms.txt", "\n".join(llms) + "\n")
    print("uretildi:", len(adresler), "URL ->", C)


if __name__ == "__main__":
    main()
