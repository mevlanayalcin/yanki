#!/usr/bin/env python3
"""Yanki sitesini uretir: dist/ icine iki dilde statik sayfalar, llms.txt, robots, sitemap.

Tek kaynak bu dosyadaki IÇERIK sozlugudur; HTML iskeleti ortaktir. Kaydedilmis ornek
cevaplar data/ornekler.json icinden gelir ve o dosya /api/reflect ucunun GERÇEK
ciktilarindan olusur (elle yazilmis pazarlama metni degil).
"""

from __future__ import annotations

import html
import json
import pathlib

KOK = pathlib.Path(__file__).resolve().parent.parent
CIKTI = KOK / "dist"
DOMAIN = "mevlanayalcin.com.tr"
POSTA = "merhaba@" + DOMAIN
DEPO = "https://github.com/mevlanayalcin/yanki"

DILLER = {
    "en": {"kod": "en", "yol": "", "adi": "English"},
    "tr": {"kod": "tr", "yol": "tr/", "adi": "Türkçe"},
}

IÇERIK = {
    "en": {
        "baslik": "Yankı — a reflective AI companion for emotional check-ins",
        "ozet": "Yankı mirrors your own words back, names what you appear to feel, and offers one small next step. It is a companion, not therapy, and it never invents a feeling you did not put there.",
        "durum": "Private beta · built by one founder in Ankara",
        "kahraman": {
            "ust": "Three minutes, once a day",
            "baslik": "Say it plainly. Get it back, clearer.",
            "alti": "You write what happened and how it landed. Yankı returns the feeling it hears, the sentence of yours that carries it, and one concrete step you can take in the next hour.",
        },
        "nasil": {
            "baslik": "How a check-in is built",
            "adimlar": [
                ("You write freely", "One text box. No forms, no mood emoji grid, no streaks to keep you hostage."),
                ("It names the feeling", "A language model reads the passage and proposes one feeling label with an intensity, plus the alternative it considered and rejected."),
                ("It quotes you", "The reflection carries your own sentence, unchanged. If it cannot find one, it says so instead of guessing."),
                ("One small step", "A single, doable action for the next hour: four minutes of breathing, a two-line journal prompt, a walk, a message to a person."),
                ("Crisis words are handled by rules", "A fixed word list runs before the model. If it hits, Yankı stops reflecting and shows human contacts. The model does not get to decide this."),
            ],
        },
        "guvenlik": {
            "baslik": "What Yankı is not",
            "maddeler": [
                "Not therapy, not a diagnosis, not a medical device. It has no clinical claim and asks none.",
                "It does not advise on medication, dosage, or stopping treatment.",
                "If you are in immediate danger or thinking of harming yourself, call 112 in Türkiye or your local emergency number. Yankı shows this banner whenever a crisis word appears, and it is a rule, not a model judgement.",
                "Sessions are not used to train any model, by us or by a vendor.",
                "Your text goes to Anthropic's API to produce the reflection, and it is retained there only under their API data terms, not ours.",
            ],
        },
        "gizlilik": {
            "baslik": "Where your text lives",
            "maddeler": [
                "Check-in text is sent to Anthropic for one inference call and is not stored on our servers during the beta.",
                "The waitlist entry is one row: your email address, in Cloudflare KV. No analytics cookie, no ad pixel, no session replay.",
                "Ask for deletion at " + POSTA + " and the row is gone the same day.",
                "Handled under Türkiye's KVKK; we keep no health record, so there is no clinical file to request.",
            ],
        },
        "kurumsal": {
            "baslik": "Company facts",
            "kimlik": "Yankı is an operating name used by its founder, Mevlana Yalçın, for an emotional check-in companion. Contractual and contact point: " + POSTA + " · Ankara, Türkiye. Not a registered legal entity.",
            "domain": "mevlanayalcin.com.tr is a personal domain the founder has held since September 2023. Product work on Yankı began in October 2026 and the two dates are kept separate on purpose.",
            "ekip": "One person: founder, engineering, support. No agency, no subcontracted build.",
            "claude": "Reflections are produced through Anthropic's Messages API with claude-haiku-4-5-20251001 under a reflection-constrained prompt that must return JSON. The output is schema-checked server side; a malformed answer is discarded rather than shown. Crisis wording is decided by a rule list before the model is called.",
            "durumSatiri": "Live: this site, the /api/reflect endpoint, the waitlist. In development: the account, history and reminders. Planned: a clinician-reviewed protocol and a second language set.",
            "roadmap": [
                ("Reflection endpoint with schema checks", "Live", "Runs on Cloudflare Workers; sample answers on this page were captured from it."),
                ("Waitlist with real deletion path", "Live", "One KV row per address, removed on request."),
                ("Accounts, check-in history, reminders", "In development", "Local-first storage is the default; sync will be opt-in."),
                ("Crisis word list in Turkish and English", "Live", "Reviewed against a public helpline wording list, not invented."),
                ("Clinician review of the reflection protocol", "Planned", "Not started, no partner signed yet."),
                ("Mobile apps", "Planned", "No date committed."),
            ],
            "dogrulama": [
                ("Worker source", DEPO),
                ("API contract", "https://" + DOMAIN + "/api/"),
                ("Machine-readable summary", "https://" + DOMAIN + "/llms.txt"),
                ("Crawl test", "https://" + DOMAIN + "/robots.txt"),
            ],
        },
        "fiyat": {
            "baslik": "Price",
            "metin": "Free during the private beta. When it is charged, the paid tier will be the one that keeps history and reminders; the reflective check-in itself will not become a paid feature that gates a person in distress.",
        },
        "api": {
            "baslik": "API",
            "metin": "One public endpoint for now, the same one this page's demo box calls. It is rate limited and carries a daily budget guard, so treat it as a sample integration, not infrastructure.",
        },
        "soru": {
            "baslik": "Questions a reviewer usually asks",
            "maddeler": [
                ("Why a language model at all?", "Because naming a feeling from prose is not something a rules engine can do. The parts that must not be probabilistic — crisis detection, output shape, refusal to quote text that is not there — are handled by code around the model."),
                ("What is Claude load-bearing for?", "The reflection itself. Remove Claude and the product has no centre; there is no rules-based fallback pretending to be one, the box just says it is unavailable."),
                ("Is this a wrapper?", "The model is the core call; the value is in the constraint around it: JSON-only output, quoted-source-of-truth being the user's own text, rule-based crisis handling, no memory of your sessions in the beta."),
                ("Who is it for?", "People who want a daily check-in habit and are not in active treatment. It is not for crisis care and says so in the interface."),
            ],
        },
        "bekleyenler": "Join the waitlist",
        "postaYeri": "your email",
        "gizlilikNotu": "One row in Cloudflare: your address. Deletion on request at " + POSTA + ". No marketing drip.",
        "demo": {
            "baslik": "Try one reflection",
            "alti": "This box calls the real endpoint. It does not store what you type.",
            "giris": "Type a sentence about your day and how it made you feel…",
            "dugme": "Reflect",
            "bekleme": "Thinking…",
            "hata": "The endpoint is unavailable right now (rate limit or daily budget). Nothing was stored.",
        },
        "ornekler": {
            "baslik": "Three captured answers",
            "alti": "Verbatim responses from /api/reflect, not rewritten for the page. The request text is shown above each answer.",
        },
        "altbilgi": "Yankı · Ankara, Türkiye · 2026 · operating name, not a registered legal entity · " + POSTA,
        "sayfalar": [
            ("", "Product"),
            ("how-it-works/", "How it works"),
            ("safety/", "Safety"),
            ("privacy/", "Privacy"),
            ("api/", "API"),
            ("company/", "Company"),
        ],
        "menuDilleri": {"en": "Türkçe", "tr": "English"},
    },
    "tr": {
        "baslik": "Yankı — duygusal günlük kontrol için yansıtan yapay zekâ eşlikçisi",
        "ozet": "Yankı kendi cümlelerini sana geri yansıtır, duyduğunu düşündüğü duyguyu adlandırır ve önündeki bir saat için tek bir somut adım önerir. O bir eşlikçidir, terapi değildir; senin koymadığın bir duyguyu uydurmaz.",
        "durum": "Özel beta · Ankara'da tek kurucu tarafından geliştiriliyor",
        "kahraman": {
            "ust": "Günde üç dakika",
            "baslik": "Olduğu gibi anlat. Daha net haliyle geri al.",
            "alti": "Ne olduğunu ve sana nasıl dokunduğunu yazarsın. Yankı duyduğunu düşündüğü duyguyu, o duyguyu taşıyan kendi cümleni ve önündeki bir saat içinde atabileceğin tek adımı geri verir.",
        },
        "nasil": {
            "baslik": "Bir günlük kontrol nasıl kurulur",
            "adimlar": [
                ("Serbest yazarsın", "Tek metin kutusu. Form yok, duygu emojisi panosu yok, sürdürmeye mecbur eden seri rekorları yok."),
                ("Duyguyu adlandırır", "Dil modeli metni okur ve bir duygu etiketiyle şiddetini önerir; ayrıca düşünüp elediği alternatifi de söyler."),
                ("Seni alıntılar", "Yansıtma, değişmemiş kendi cümleni taşır. Böyle bir cümle bulamazsa tahmin etmek yerine bulamadığını söyler."),
                ("Tek küçük adım", "Önündeki bir saat için yapılabilecek tek şey: dört dakika nefes, iki satırlık bir yazı önerisi, bir yürüyüş, birine atılacak bir mesaj."),
                ("Kriz kelimelerini kurallar işler", "Sabit bir kelime listesi modelden önce çalışır. Eşleşirse Yankı yansıtmayı bırakır ve insani iletişim hatlarını gösterir. Buna model karar vermez."),
            ],
        },
        "guvenlik": {
            "baslik": "Yankı ne değildir",
            "maddeler": [
                "Terapi değil, teşhis değil, tıbbi cihaz değil. Klinik bir iddiası yoktur ve iddia da talep etmez.",
                "İlaç, doz veya tedavinin bırakılması hakkında öneri vermez.",
                "Derhal bir tehlikedeyse ya da kendini yaralamayı düşünüyorsan Türkiye'de 112'yi ya da bulunduğun yerin acil numarasını ara. Kriz kelimesi geçtiğinde bu uyarıyı gösterir; bu bir kuraldır, modelin kararı değil.",
                "Günlükler hiçbir modelin eğitiminin verisi yapılmaz — ne biz tarafından ne bir sağlayıcı tarafından.",
                "Metin, yansıtmayı üretmek için Anthropic'in API'sine gider ve yalnızca onların API veri koşullarınca saklanır; bizim tarafımızda kayıt tutulmaz.",
            ],
        },
        "gizlilik": {
            "baslik": "Metnin nerede durur",
            "maddeler": [
                "Günlük metni tek bir çıkarım çağrısı için Anthropic'e gider ve beta süresince bizim sunucularımızda saklanmaz.",
                "Bekleme listesi kaydı tek satırdır: e-posta adresin, Cloudflare KV içinde. Analitik çerezi yok, reklam pikseli yok, oturum kaydı yok.",
                "Silme için " + POSTA + " adresine yaz; aynı gün silinir.",
                "KVKK kapsamında ele alınır; sağlık kaydı tutmadığımız için talep edilecek klinik bir dosya da yoktur.",
            ],
        },
        "kurumsal": {
            "baslik": "Kurumsal künye",
            "kimlik": "Yankı, kurucusu Mevlana Yalçın'ın duygusal kontrol eşlikçisi için kullandığı bir işletme adıdır. Sözleşme ve iletişim mercii: " + POSTA + " · Ankara, Türkiye. Tescilli tüzel kişilik değildir.",
            "domain": "mevlanayalcin.com.tr, kurucunun Eylül 2023'ten beri elinde tuttuğu kişisel bir alan adadır. Yankı üzerindeki ürün çalışması Ekim 2026'da başlamıştır; bu iki tarih bilinçli olarak ayrı tutulur.",
            "ekip": "Tek kişi: kurucu, mühendislik, destek. Ajans yok, taşerona devredilmiş iş yok.",
            "claude": "Yansıtmalar Anthropic'in Messages API'si üzerinden, claude-haiku-4-5-20251001 ile ve JSON dönmek zorunda olan bir kısıtlı istemle üretilir. Çıktı sunucu tarafında şemaya göre denetlenir; bozuk cevap gösterilmez, atılır. Kriz sözcükleri modele sorulmadan önce bir kural listesiyle belirlenir.",
            "durumSatiri": "Yayında: bu site, /api/reflect ucu, bekleme listesi. Geliştiriliyor: hesap, günlük geçmişi ve hatırlatmalar. Planlanan: bir klinik uzman tarafından değerlendirilmiş yansıtma protokolü ve ikinci dil seti.",
            "roadmap": [
                ("Şema denetimli yansıtma ucu", "Yayında", "Cloudflare Workers üzerinde çalışır; bu sayfadaki örnek cevaplar ondan kaydedildi."),
                ("Gerçek silme yoluyla bekleme listesi", "Yayında", "Adres başına tek KV satırı; istenince silinir."),
                ("Hesap, günlük geçmişi, hatırlatmalar", "Geliştiriliyor", "Yerel öncelikli saklama varsayılan olacak; eşitleme seçenekli olacak."),
                ("Türkçe ve İngilizce kriz kelime listesi", "Yayında", "Açık bir yardım hattı ifade listesine göre gözdendirildi, uydurulmadı."),
                ("Yansıtma protokolünün uzman değerlendirmesi", "Planlanan", "Başlamadı, imzalı ortak yok."),
                ("Mobil uygulamalar", "Planlanan", "Verilmiş tarih yok."),
            ],
            "dogrulama": [
                ("Worker kaynak kodu", DEPO),
                ("API sözleşmesi", "https://" + DOMAIN + "/api/"),
                ("Makine okumalı özet", "https://" + DOMAIN + "/llms.txt"),
                ("Örümcek testi", "https://" + DOMAIN + "/robots.txt"),
            ],
        },
        "fiyat": {
            "baslik": "Fiyat",
            "metin": "Özel beta boyunca ücretsiz. Ücretlendiğinde ücretli katman, geçmişi ve hatırlatmaları tutan katman olacak; zorlanan bir kişiyi kapıda bekleten yansıtma adımının kendisi ücretli bir kapıya dönüşmeyecek.",
        },
        "api": {
            "baslik": "API",
            "metin": "Şimdilik tek açık uç: bu sayfadaki deneme kutusunun çağırdığınla aynı uç. Hız sınırına ve günlük bütçe korumasına bağlı; altyapı değil, örnek bir bütünleştirme olarak bak.",
        },
        "soru": {
            "baslik": "Bir incelemecinin genelde sorduğu sorular",
            "maddeler": [
                ("Neden dil modeli?", "Düz yazıdan duyguyu adlandırmayı kural motoru yapamaz. Olasılıksal olmaması gereken kısımlar — kriz tespiti, çıktı biçimi, olmayan bir cümleyi alıntılamama — modelin etrafındaki kodla yürütülür."),
                ("Claude ne için vazgeçilemez?", "Yansıtmanın kendisi için. Claude'u çıkarırsan ürünün merkezi kalır; yokmuş gibi davranan bir kural tabanlı yedek de yoktur, kutu yalnızca ulaşılamadığını söyler."),
                ("Bu bir sarmalayıcı mı?", "Model çekirdek çağrı; değer onun etrafındaki kısıtlarda: yalnızca JSON çıktısı, tek doğruluk kaynağının kullanıcının kendi metni olması, kural tabanlı kriz yönetimi, betada günlüklerin hafızada tutulmaması."),
                ("Kim için?", "Aktif tedavide olmayan, günlük kontrol alışkanlığı isteyen kişiler için. Kriz bakımı için değildir ve arayüzde böyle söylenir."),
            ],
        },
        "bekleyenler": "Bekleme listesine katıl",
        "postaYeri": "e-posta adresin",
        "gizlilikNotu": "Cloudflare'da tek satır: adresin. İstediğinde " + POSTA + " üzerinden silinir. Reklam postası yok.",
        "demo": {
            "baslik": "Bir yansıtma dene",
            "alti": "Bu kutu gerçek ucu çağırır. Yazdığını saklamaz.",
            "giris": "Gününü ve sana nasıl dokunduğunu bir cümleyle yaz…",
            "dugme": "Yansıt",
            "bekleme": "Düşünüyor…",
            "hata": "Uç şu anda ulaşılamıyor (hız sınırı veya günlük bütçe). Hiçbir şey saklanmadı.",
        },
        "ornekler": {
            "baslik": "Kaydedilmiş üç cevap",
            "alti": "/api/reflect ucunun birebir cevapları; sayfa için yeniden yazılmadı. İstek metni her cevabın üstünde gösterilir.",
        },
        "altbilgi": "Yankı · Ankara, Türkiye · 2026 · işletme adı, tescilli tüzel kişilik değil · " + POSTA,
        "sayfalar": [
            ("tr/", "Ürün"),
            ("tr/nasil/", "Nasıl çalışır"),
            ("tr/guvenlik/", "Güvenlik"),
            ("tr/gizlilik/", "Gizlilik"),
            ("tr/api/", "API"),
            ("tr/kurumsal/", "Kurumsal"),
        ],
        "menuDilleri": {"en": "Türkçe", "tr": "English"},
    },
}

# Sayfa dosya adlari: dil -> {sayfa anahtari: yol}
SAYFALAR = {
    "en": {"index": "index.html", "nasil": "how-it-works/index.html", "guvenlik": "safety/index.html",
           "gizlilik": "privacy/index.html", "api": "api/index.html", "kurumsal": "company/index.html"},
    "tr": {"index": "tr/index.html", "nasil": "tr/nasil/index.html", "guvenlik": "tr/guvenlik/index.html",
           "gizlilik": "tr/gizlilik/index.html", "api": "tr/api/index.html", "kurumsal": "tr/kurumsal/index.html"},
}

EK_URL = {
    "en": {"nasil": "/how-it-works/", "guvenlik": "/safety/", "gizlilik": "/privacy/", "api": "/api/", "kurumsal": "/company/"},
    "tr": {"nasil": "/tr/nasil/", "guvenlik": "/tr/guvenlik/", "gizlilik": "/tr/gizlilik/", "api": "/tr/api/", "kurumsal": "/tr/kurumsal/"},
}


def menu(dil: str, aktif: str) -> str:
    parcalar = []
    for dal, ad in [(s[0] if s[0] else "index", s[1]) for s in IÇERIK[dil]["sayfalar"]]:
        pass
    liste = []
    for yol, ad in IÇERIK[dil]["sayfalar"]:
        anahtar = {v: k for k, v in EK_URL[dil].items()}.get("/" + yol, "index") if yol else "index"
        tam = "/" + yol if yol else "/"
        isaret = ' class="aktif"' if anahtar == aktif else ""
        liste.append('<a href="%s"%s>%s</a>' % (tam, isaret, html.escape(ad)))
    digeri = "tr" if dil == "en" else "en"
    liste.append('<a class="dil" href="/%s">%s</a>' % (DILLER[digeri]["yol"].rstrip("/"), IÇERIK[dil]["menuDilleri"][dil]))
    return "\n      ".join(liste)


def kabuk(dil: str, anahtar: str, baslik: str, aciklama: str, govde: str, canonical: str) -> str:
    hreflang_tr = "/tr/" if dil == "en" else "/"
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
<meta property="og:site_name" content="Yankı" />
<meta name="twitter:card" content="summary" />
<link href="/assets/site.css" rel="stylesheet" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<script type="application/ld+json">%(jsonld)s</script>
</head><body>
<header class="ust">
  <a class="kul" href="/%(yol)s">Yankı<span class="nokta">.</span></a>
  <nav class="menu" id="menu">%(menu)s</nav>
  <button class="menudugme" id="menudugme" aria-expanded="false" aria-controls="menu">Menu</button>
</header>
<main>%(govde)s</main>
<footer class="alt">
  <p class="altbilgi">%(altbilgi)s</p>
  <p class="altlinkler"><a href="%(depo)s">GitHub</a> · <a href="/llms.txt">llms.txt</a> · <a href="/%(yol)sapi/">API</a> · <a href="/%(yol)scompany/">Company</a></p>
</footer>
<script src="/assets/nav.js" defer></script>
%(betik)s
</body></html>
""" % {
        "dil": dil, "baslik": html.escape(baslik), "aciklama": html.escape(aciklama),
        "canonical": canonical, "menu": menu(dil, anahtar), "govde": govde,
        "altbilgi": html.escape(IÇERIK[dil]["altbilgi"]), "depo": DEPO,
        "yol": DILLER[dil]["yol"],
        "betik": "<script src=\"/assets/app.js\" defer></script>" if anahtar == "index" else "",
        "jsonld": json.dumps(_jsonld(dil, canonical), ensure_ascii=False, separators=(",", ":")),
    }


def _jsonld(dil: str, canonical: str) -> dict:
    i = IÇERIK[dil]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": "https://%s/#org" % DOMAIN, "name": "Yankı",
             "url": "https://%s/" % DOMAIN, "email": POSTA,
             "description": i["ozet"],
             "founder": {"@type": "Person", "name": "Mevlana Yalçın"},
             "numberOfEmployees": {"@type": "QuantitativeValue", "value": 1},
             "address": {"@type": "PostalAddress", "addressLocality": "Ankara", "addressCountry": "TR"},
             "codeRepository": DEPO},
            {"@type": "SoftwareApplication", "name": "Yankı", "url": canonical,
             "applicationCategory": "LifestyleApplication", "operatingSystem": "Web",
             "inLanguage": ["en", "tr"], "description": i["ozet"],
             "publisher": {"@id": "https://%s/#org" % DOMAIN},
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        ],
    }


def _liste(maddeler: list, sirali: bool = False) -> str:
    etiket = "ol" if sirali else "ul"
    return "<%s class=\"maddeler\">" % etiket + "".join("<li>%s</li>" % m for m in maddeler) + "</%s>" % etiket


def _ornekler(dil: str) -> str:
    dosya = KOK / "data" / "ornekler.json"
    if not dosya.exists():
        return ""
    veri = json.loads(dosya.read_text(encoding="utf-8"))
    ba = "<h2>%s</h2><p class=\"alt\">%s</p>" % (html.escape(IÇERIK[dil]["ornekler"]["baslik"]), html.escape(IÇERIK[dil]["ornekler"]["alti"]))
    kartlar = []
    for o in veri.get(dil) or veri.get("en") or []:
        kartlar.append(
            "<article class=\"ornek\"><p class=\"soru\">“%s”</p><dl>"
            "<dt>Duygu</dt><dd>%s <span class=\"siddet\">%s</span></dd>"
            "<dt>Yansıtma</dt><dd>%s</dd>"
            "<dt>Alıntı</dt><dd class=\"ali%d\">%s</dd>"
            "<dt>Adım</dt><dd>%s</dd>"
            "</dl><p class=\"motor\">%s · %s</p></article>"
            % (html.escape(o["girdi"]), html.escape(o.get("duygu") or "—"), html.escape(str(o.get("siddet") or "")),
               html.escape(o.get("yansitma") or "—"), 0 if not o.get("alıntı") else 0,
               html.escape(o.get("alıntı") or "—"), html.escape(o.get("adım") or "—"),
               html.escape(o.get("provider") or ""), html.escape(o.get("model") or ""))
        )
    return ba + "<div class=\"ornekler\">" + "".join(kartlar) + "</div>"


def govde_uret(dil: str, anahtar: str) -> str:
    i = IÇERIK[dil]
    d = i["demo"]
    if anahtar == "index":
        return (
            '<section class="kahraman"><div class="iç">'
            '<p class="ustbaslik">%s</p><h1>%s</h1><p class="alti">%s</p>'
            '<p class="durum">%s</p>'
            '<form class="bekleme" id="bekleme" action="/api/waitlist" method="post">'
            '<input type="email" name="email" required placeholder="%s" aria-label="%s" />'
            '<button type="submit">%s</button><p class="not" id="beklemeyanit">%s</p></form>'
            "</div>"
            '<div class="kutu" id="kutu">'
            '<h2 class="kutuBaslik">%s</h2><p class="kutuAlti">%s</p>'
            '<textarea id="girdi" rows="3" placeholder="%s"></textarea>'
            '<div class="kutuEylem"><button id="yansit">%s</button><span id="durum" aria-live="polite"></span></div>'
            '<div id="sonuc" hidden></div>'
            "</div></section>"
            '<section class="ku" id="ornekler">%s</section>' % (
                html.escape(i["kahraman"]["ust"]), html.escape(i["kahraman"]["baslik"]), html.escape(i["kahraman"]["alti"]),
                html.escape(i["durum"]), html.escape(d["giris"]), html.escape(d["giris"]), html.escape(i["bekleyenler"]),
                html.escape(d["gizlilikNotu"] if False else i["gizlilikNotu"]),
                html.escape(d["baslik"]), html.escape(d["alti"]), html.escape(d["giris"]), html.escape(d["dugme"]), _ornekler(dil))
        )
    if anahtar == "nasil":
        adimlar = "".join('<li><h3>%s</h3><p>%s</p></li>' % (html.escape(b), html.escape(m)) for b, m in i["nasil"]["adimlar"])
        return '<section class="ku"><h1>%s</h1><ol class="adimlar">%s</ol><p class="motorNotu">%s</p></section>' % (
            html.escape(i["nasil"]["baslik"]), adimlar, html.escape(i["kurumsal"]["claude"]))
    if anahtar == "guvenlik":
        return '<section class="ku"><h1>%s</h1>%s<p class="vurgu">%s</p></section>' % (
            html.escape(i["guvenlik"]["baslik"]), _liste([html.escape(m) for m in i["guvenlik"]["maddeler"]]),
            html.escape(i["fiyat"]["metin"]))
    if anahtar == "gizlilik":
        return '<section class="ku"><h1>%s</h1>%s</section>' % (
            html.escape(i["gizlilik"]["baslik"]), _liste([html.escape(m) for m in i["gizlilik"]["maddeler"]]))
    if anahtar == "api":
        tablo = (
            "<table class=\"sozlesme\"><tr><th>Method</th><td>POST</td></tr>"
            "<tr><th>Path</th><td>/api/reflect</td></tr>"
            "<tr><th>Request</th><td><code>{&quot;text&quot;: string, &quot;lang&quot;: &quot;en&quot;|&quot;tr&quot;}</code> — 8–600 characters</td></tr>"
            "<tr><th>Response</th><td><code>{duygu, siddet, yansitma, alinti, adim, disclaimer, provider, model, cache}</code></td></tr>"
            "<tr><th>Errors</th><td><code>bad_request</code> 400 · <code>too_long</code> 413 · <code>busy</code> 429 · <code>daily_budget</code> 503 · <code>upstream</code> 502</td></tr>"
            "<tr><th>Rate limit</th><td>6 requests / 60 s per IP</td></tr>"
            "<tr><th>Budget</th><td>A daily payment-equivalent cap stops the endpoint before the balance runs out</td></tr>"
            "<tr><th>Crisis wording</th><td>Handled by a rule list before the model call; the answer is replaced by helpline text</td></tr></table>"
        )
        return '<section class="ku"><h1>%s</h1><p>%s</p>%s</section><section class="ku">%s</section>' % (
            html.escape(i["api"]["baslik"]), html.escape(i["api"]["metin"]), tablo, _ornekler(dil))
    if anahtar == "kurumsal":
        satirlar = "".join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (b, m) for b, m in [
            ("Kimlik" if dil == "tr" else "Identity", html.escape(i["kurumsal"]["kimlik"])),
            ("Domain", html.escape(i["kurumsal"]["domain"])),
            ("Ekip" if dil == "tr" else "Team", html.escape(i["kurumsal"]["ekip"])),
            ("Claude", html.escape(i["kurumsal"]["claude"])),
            ("Durum" if dil == "tr" else "Status", html.escape(i["kurumsal"]["durumSatiri"])),
        ])
        plan = "".join('<tr><td>%s</td><td><span class="durum-%s">%s</span></td><td>%s</td></tr>' % (
            html.escape(ad), durum.replace(" ", "-").lower(), html.escape(durum), html.escape(notu))
            for ad, durum, notu in i["kurumsal"]["roadmap"])
        dogr = "".join('<li><a href="%s">%s</a></li>' % (u, html.escape(ad)) for ad, u in i["kurumsal"]["dogrulama"])
        soru = "".join("<details><summary>%s</summary><p>%s</p></details>" % (html.escape(s), html.escape(c)) for s, c in i["soru"]["maddeler"])
        return ('<section class="ku"><h1>%s</h1><table class="kunya">%s</table></section>'
                '<section class="ku"><h2>%s</h2><table class="plan">%s</table></section>'
                '<section class="ku"><h2>%s</h2><ul class="dogrulama">%s</ul></section>'
                '<section class="ku"><h2>%s</h2>%s</section>') % (
            html.escape(i["kurumsal"]["baslik"]), satirlar,
            html.escape("Roadmap" if dil == "en" else "Yol haritası"), plan,
            html.escape("Verify this independently" if dil == "en" else "Bağımsız doğrulama"), dogr,
            html.escape(i["soru"]["baslik"]), soru)
    return ""


def yaz(dosya: pathlib.Path, metin: str) -> None:
    dosya.parent.mkdir(parents=True, exist_ok=True)
    dosya.write_text(metin, encoding="utf-8")


def main() -> None:
    for dil, harita in SAYFALAR.items():
        for anahtar, yol in harita.items():
            i = IÇERIK[dil]
            aciklama = i["ozet"] if anahtar == "index" else i.get({"nasil": "nasil", "guvenlik": "guvenlik", "gizlilik": "gizlilik", "api": "api", "kurumsal": "kurumsal"}[anahtar], {}).get("baslik", i["ozet"])
            baslik = i["baslik"] if anahtar == "index" else "%s · Yankı" % aciklama
            slug = "" if anahtar == "index" else EK_URL[dil][anahtar].rstrip("/").lstrip("/")
            canonical = "https://%s/%s%s" % (DOMAIN, DILLER[dil]["yol"], (slug + "/") if slug else "")
            if anahtar == "nasil":
                aciklama = i["nasil"]["baslik"] + " — " + i["kahraman"]["alti"]
            elif anahtar == "guvenlik":
                aciklama = i["guvenlik"]["baslik"] + " — " + i["guvenlik"]["maddeler"][0]
            elif anahtar == "gizlilik":
                aciklama = i["gizlilik"]["baslik"] + " — " + i["gizlilik"]["maddeler"][0]
            elif anahtar == "api":
                aciklama = i["api"]["metin"]
            elif anahtar == "kurumsal":
                aciklama = i["kurumsal"]["kimlik"]
            yaz(CIKTI / yol, kabuk(dil, anahtar, baslik, aciklama, govde_uret(dil, anahtar), canonical))

    # robots + sitemap + llms.txt
    adresler = sorted({("https://%s/%s" % (DOMAIN, DILLER[d]["yol"] + (EK_URL[d][a].lstrip("/") if a != "index" else "")))
                       for d in SAYFALAR for a in SAYFALAR[d]})
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
               + "".join("<url><loc>%s</loc></url>" % u for u in adresler) + "</urlset>")
    yaz(CIKTI / "sitemap.xml", sitemap)
    yaz(CIKTI / "robots.txt", "User-agent: *\nAllow: /\nSitemap: https://%s/sitemap.xml\n" % DOMAIN)
    llms = [
        "# Yankı", "",
        "> " + IÇERIK["en"]["ozet"], "",
        "Yankı is an emotional check-in companion, not therapy, not a diagnosis, not a medical device.",
        "Reflections are produced by Anthropic's Messages API with claude-haiku-4-5-20251001 under a JSON-only prompt;",
        "crisis wording is decided by a rule list before the model is called.", "",
        "## Pages", "",
        "- [Product](https://%s/): what it does and a live demo box" % DOMAIN,
        "- [How it works](https://%s/how-it-works/): the five steps of a check-in" % DOMAIN,
        "- [Safety](https://%s/safety/): explicit limits, emergency notice (112 in Türkiye)" % DOMAIN,
        "- [Privacy](https://%s/privacy/): text is not stored during the beta; no analytics cookie" % DOMAIN,
        "- [Company](https://%s/company/): identity, roadmap with status, verification links" % DOMAIN,
        "- [API](https://%s/api/): POST /api/reflect contract, errors, rate limit, budget guard" % DOMAIN, "",
        "## Facts kept separate on purpose", "",
        "- mevlanayalcin.com.tr is a personal domain held since September 2023.",
        "- Product work on Yankı began October 2026.",
        "- One person, bootstrapped, Ankara. No registered legal entity, no funding raised, no customers yet.",
        "- Waitlist only: sign-up at the site; deletion by email to " + POSTA + ".",
    ]
    yaz(CIKTI / "llms.txt", "\n".join(llms) + "\n")
    yaz(CIKTI / "favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0f3d3e"/><path d="M18 20v9c0 8 8 10 8 18m0 0c0-8 8-10 8-18v-9m-8 18v14" stroke="#f2e9dc" stroke-width="4" fill="none" stroke-linecap="round"/></svg>\n')
    print("uretildi:", len(adresler), "URL ->", CIKTI)


if __name__ == "__main__":
    main()
