#!/usr/bin/env python3
"""Canli siteyi denetler: her URL 200 mu, canonical/og:uv birbirini tutuyor mu,
JSON-LD ayristiriliyor mu, ic baglantilar kirk mi, API ve 404 davranisi dogru mu.

Kullanim:  python3 scripts/denet.py [temel-url]
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

TEMEL = (sys.argv[1] if len(sys.argv) > 1 else "https://mevlanayalcin.com.tr").rstrip("/")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/129 Safari/537.36"


def cek(yol: str):
    istek = urllib.request.Request(TEMEL + yol, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(istek, timeout=25) as yanit:
            return yanit.status, yanit.read().decode("utf-8", "replace"), {k.lower(): v for k, v in yanit.headers.items()}
    except urllib.error.HTTPError as h:
        return h.code, h.read().decode("utf-8", "replace"), {k.lower(): v for k, v in (h.headers or {}).items()}
    except Exception as hata:  # baglanamadi
        return 0, repr(hata)[:80], {}


def main() -> int:
    sorunlar = []
    kod, sitemap, _ = cek("/sitemap.xml")
    adresler = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    yollar = sorted({urllib.parse.urlparse(a).path for a in adresler})
    print("sitemap:", len(adresler), "URL,", len(yollar), "benzersiz yol")
    if kod != 200:
        sorunlar.append("sitemap okunamadi: %s" % kod)

    linkler = set()
    for yol in yollar:
        kod, govde, bas = cek(yol)
        tip = bas.get("content-type", "")
        if kod != 200 or "text/html" not in tip:
            sorunlar.append("%s -> http=%s tip=%s" % (yol, kod, tip[:30]))
            continue
        kanonik = (re.search(r'<link rel="canonical" href="([^"]+)"', govde) or [None, ""])[1]
        og = (re.search(r'property="og:url" content="([^"]+)"', govde) or [None, ""])[1]
        dil = (re.search(r'<html lang="([^"]+)"', govde) or [None, ""])[1]
        if kanonik != TEMEL + yol:
            sorunlar.append("%s -> canonical %s degil" % (yol, kanonik))
        if og != kanonik:
            sorunlar.append("%s -> og:url (%s) canonical ile ayrisiyor" % (yol, og))
        if dil not in ("en", "tr"):
            sorunlar.append("%s -> html lang=%s" % (yol, dil))
        if dil == "tr" and not yol.startswith("/tr/"):
            sorunlar.append("%s -> icerik Turkce ama yol /tr/ altında degil" % yol)
        if "info@mevlanayalcin.com.tr" not in govde:
            sorunlar.append("%s -> iletisim adresi yok" % yol)
        for blok in re.findall(r'<script type="application/ld\+json">(.*?)</script>', govde, re.S):
            try:
                json.loads(blok)
            except Exception as hata:
                sorunlar.append("%s -> JSON-LD bozuk: %s" % (yol, str(hata)[:60]))
        for href in re.findall(r'href="(/[^"#]*|https?:[^"]+)"', govde):
            if href.startswith("http") and urllib.parse.urlparse(href).netloc != urllib.parse.urlparse(TEMEL).netloc:
                continue
            linkler.add(href.split("#")[0])

    print("sayfada bulunan kendi ic linkleri:", len(linkler))
    for href in sorted(linkler):
        yol = href if href.startswith("/") else urllib.parse.urlparse(href).path
        kod, _, _ = cek(yol)
        if kod not in (200, 201):
            sorunlar.append("kirik baglanti: %s -> %s" % (yol, kod))

    kod, govde, _ = cek("/su-TEST-404/")
    if kod != 404 or len(govde) < 800:
        sorunlar.append("404 davranisi: http=%s govde=%s bayt (tasarimli 404 beklenir)" % (kod, len(govde)))

    kod, govde, _ = cek("/api/health")
    try:
        saglik = json.loads(govde)
        if not saglik.get("ok"):
            sorunlar.append("api/health ok=false")
        print("api/health:", kod, saglik)
    except Exception:
        sorunlar.append("api/health ayristirilamadi: %s %s" % (kod, govde[:60]))

    for statik in ("/robots.txt", "/llms.txt", "/favicon.svg", "/assets/site.css", "/assets/nav.js", "/assets/app.js"):
        kod, govde, bas = cek(statik)
        tip = bas.get("content-type", "")
        if kod != 200 or not govde:
            sorunlar.append("%s -> http=%s tip=%s bayt=%s" % (statik, kod, tip[:24], len(govde)))
        elif statik.endswith(".css") and "text/css" not in tip:
            sorunlar.append("%s -> tip %s" % (statik, tip))
        elif statik.endswith(".js") and "javascript" not in tip:
            sorunlar.append("%s -> tip %s" % (statik, tip))

    # botlar ve duz tarayici ayni cevabi vermeli
    UALAR = ["", "python-requests/2.31", "curl/8.5.0",
             "Mozilla/5.0 (compatible; Googlebot/2.1)",
             "Mozilla/5.0 (compatible; ClaudeBot/1.0; +noreply@anthropic.com)"]
    for ua in UALAR:
        istek = urllib.request.Request(TEMEL + "/", headers={"User-Agent": ua or "none"})
        try:
            with urllib.request.urlopen(istek, timeout=25) as y:
                if y.status != 200:
                    sorunlar.append("bot UA %r -> %s" % (ua[:22], y.status))
        except Exception as hata:
            sorunlar.append("bot UA %r -> %s" % (ua[:22], repr(hata)[:40]))

    print()
    if sorunlar:
        print("SORUNLAR (%d):" % len(sorunlar))
        for s in sorunlar:
            print("  -", s)
        return 1
    print("temiz: %d sayfa, %d ic link, api, statikler ve botlar gecti" % (len(yollar), len(linkler)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
