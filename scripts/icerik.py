#!/usr/bin/env python3
"""mevlanayalcin.com.tr sitesini uretir: danismanlik markasi + calismalar (Yanki bir vaka).

Tek kaynak bu dosyadaki ICERIK sozlugudur; HTML iskeleti ortaktir. Yanki artik sitenin
kimligi degil, `/work/yanki/` sayfasinda duran bir vaka calismasidir; demo kutusu ve
/api/reflect ucu o sayfada yasamaya devam eder (Claude kullaniminin gorunur kaniti).
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
SURUM = "2"

KOK_YOL = {"en": "", "tr": "tr/"}
SLUG = {
    "en": {"index": "", "hizmetler": "services/", "surec": "process/", "calismalar": "work/",
           "yanki": "work/yanki/", "kurumsal": "company/", "gizlilik": "privacy/"},
    "tr": {"index": "", "hizmetler": "hizmetler/", "surec": "surec/", "calismalar": "calismalar/",
           "yanki": "calismalar/yanki/", "kurumsal": "kurumsal/", "gizlilik": "gizlilik/"},
}
MARKA = {"en": "Mevlana Yalçın", "tr": "Mevlana Yalçın"}


def url(dil: str, anahtar: str) -> str:
    return "/%s%s" % (KOK_YOL[dil], SLUG[dil][anahtar])


def tam_url(dil: str, anahtar: str) -> str:
    return "https://%s%s" % (DOMAIN, url(dil, anahtar))


E = {
    "baslik": "Mevlana Yalçın — AI consulting: LLM cost, latency and supply-chain audits",
    "ozet": "I audit what large-language-model traffic actually costs and who serves it: "
            "measured price, latency and SLA behaviour per provider, the routing decisions "
            "eating your margin, and the leak paths on your side of the wire.",
    "durum": "Independent consultant · Ankara, Türkiye · one engagement at a time",
    "kahraman": {
        "ust": "AI consulting · LLM cost & supply chain",
        "baslik": "What your tokens cost, and who is actually serving them.",
        "alti": "Most teams buying model capacity have a bill and a feeling. I replace the "
                "feeling with a measurement: per-provider price, time to first token, tokens "
                "per second, how often the promise is kept, what fails, and what you still pay "
                "when it does. Then I help you fix the parts that are yours to fix.",
    },
    "cta": {"baslik": "Book a 30-minute call", "yer": "your email", "dugme": "Request a call",
            "not": "Replies come from " + POSTA + ". No newsletter, no drip sequence: one row "
                   "in Cloudflare KV, deleted the same day you ask."},
    "ozetKutu": {
        "baslik": "What you get on the table",
        "maddeler": [
            "A provider-by-provider decision table: real price, measured TTFT and throughput, "
            "SLA hit rate, and which model names are only decorative.",
            "The money you are leaking: cache opportunities, over-priced routing defaults, "
            "prompts re-sent instead of cached, retries billed twice.",
            "The security you own: key scopes, spending caps, and the URLs your requests hand "
            "to third-party infrastructure.",
            "A short fix list with owners and expected savings — not a 40-page deck.",
        ],
    },
    "hizmetler": {
        "baslik": "Services",
        "alti": "Fixed scope, fixed price, read-only measurement first. I do not resell "
                "capacity, so nothing in the audit earns me a commission.",
        "paketler": [
            {
                "ad": "Inference audit", "sure": "5–10 working days", "fiyat": "from $4,500",
                "icerik": [
                    "Per-provider table: published vs measured price, TTFT, tokens/second.",
                    "Service-commitment reality: what is promised, what is met, what refunds.",
                    "Model-name traps: aliases and snapshots that are listed, priced, and never served.",
                    "Credential hygiene: key scopes, IP allowlists, spend caps, rate limits, pinning rights.",
                    "Leak paths: presigned URLs and image links your request hands to the supplier's fetcher.",
                    "Cache opportunity: prompt and response caching, with the saving stated in dollars.",
                ],
                "cikti": "One decision table, a 90-minute readout, and a prioritised fix list with owners.",
            },
            {
                "ad": "Routing & cost architecture", "sure": "2–4 weeks", "fiyat": "from $9,000",
                "icerik": [
                    "A model policy per task class, with a floor price and a quality reservation.",
                    "Fallback, cap and pinning semantics written as code, not as a wiki page.",
                    "Caching strategy: what to pin, what to key, what to clear.",
                    "An evaluation set and a regression harness so a model swap stops being a gamble.",
                    "Reporting in your unit of work: cost per resolved ticket, per report, per 1k words.",
                ],
                "cikti": "A routing policy running in your repository plus a cost-per-unit dashboard.",
            },
            {
                "ad": "Advisory retainer", "sure": "monthly · roughly 2 days", "fiyat": "from $1,200 / month",
                "icerik": [
                    "Watching provider prices and behaviour so a change is a decision, not a surprise.",
                    "New-model comparisons against your own traffic, not a public benchmark.",
                    "\"Which model for this\" answers with a number attached.",
                    "Quarterly re-measurement: the audit either still holds or you get the work back.",
                    "Second opinion on hires and architecture reviews.",
                ],
                "cikti": "A standing decision log; unused days roll into the next month once.",
            },
        ],
    },
    "surec": {
        "baslik": "How an engagement runs",
        "adimlar": [
            ("Scope call, 30 minutes", "You tell me the decision you need to make. If measurement "
             "will not change it, we say so there and nothing is billed."),
            ("Read-only measurement", "Your keys, your logs, your traffic. No production change, "
             "no new vendor to approve, nothing to migrate during the audit."),
            ("Findings table", "Every claim carries a reproducible command and a number. Anything "
             "I cannot reproduce I strike out before you see it."),
            ("Fix list with owners", "Six to twelve items, ordered by savings over effort, each "
             "assigned inside your team. Estimates are mine, work is yours unless we agree otherwise."),
            ("Re-measure after two weeks", "The savings either appear in the same chart or I keep "
             "working until they do, at no extra charge on the audit scope."),
        ],
    },
    "calismalar": {
        "baslik": "Work",
        "alti": "One live product and one independent audit of a public multi-provider inference "
                "exchange. Both were measured, not described.",
        "kartlar": [
            {
                "ad": "Multi-provider inference exchange — independent audit",
                "etiket": "supply chain · security",
                "metin": "Twenty accounts opened from twenty distinct residential IPs, 600+ live "
                         "jobs, and every endpoint the console itself uses. Findings: one supplier "
                         "carrying 98% of the offer book, flagship models listed and priced but "
                         "never served (a deterministic origin crash on the non-streaming path), "
                         "undocumented market endpoints, an unallow-listed server-side image fetch "
                         "that reaches link-local addresses from third-party infrastructure, and a "
                         "response cache that makes repeated requests free.",
                "bag": ("calismalar", "Read the method"),
            },
            {
                "ad": "Yankı — a reflective check-in product, live",
                "etiket": "product · claude in production",
                "metin": "A daily emotional check-in tool shipped on Cloudflare Workers: Anthropic's "
                         "Messages API with claude-haiku-4-5-20251001, JSON-only output enforced "
                         "server-side, a rule list (not the model) deciding crisis wording, quotes "
                         "that must exist verbatim in the user's text or get dropped, and no session "
                         "storage during the beta.",
                "bag": ("yanki", "Open the live demo"),
            },
        ],
    },
    "yanki": {
        "baslik": "Yankı — a live Claude product",
        "alti": "Kept as a case study, not as this site's identity: it is the clearest evidence "
                "that the Claude integration described above is real and running.",
        "giris": "You write what happened and how it landed. Yankı names the feeling it hears, "
                 "quotes your own sentence unchanged, and offers one step for the next hour. It is "
                 "a companion, not therapy: no diagnosis, no medical advice, no clinical claim.",
        "demo": {"baslik": "Try one reflection", "alti": "This box calls the same endpoint this "
                 "page describes. It does not store what you type.",
                 "yer": "Write a sentence about your day and how it landed…", "dugme": "Reflect"},
        "ornekler": {"baslik": "Captured answers", "alti": "Verbatim responses from /api/reflect, "
                     "not rewritten for the page."},
        "mimari": {"baslik": "How it is built", "maddeler": [
            "Anthropic Messages API, model claude-haiku-4-5-20251001, a system prompt that must "
            "return a single JSON object.",
            "The server checks the shape. A malformed answer is discarded and the interface says "
            "it is unavailable — there is no rule-based fake standing in for the model.",
            "Crisis wording is decided by a fixed word list before the model is called; a match "
            "replaces the answer with helpline text.",
            "A quote the model invents is dropped: if the returned quote does not appear verbatim "
            "in the user's text, it is not shown.",
            "Nothing is stored on our side during the beta. The waitlist is one key in Cloudflare KV.",
            "Rate limit 6 requests / 60 s per IP, plus a daily budget guard that returns 503 before "
            "the balance runs out.",
        ]},
        "guvenlik": {"baslik": "What Yankı is not", "maddeler": [
            "Not therapy, not a diagnosis, not a medical device. It has no clinical claim and asks none.",
            "It does not advise on medication, dosage or stopping treatment.",
            "In immediate danger, or thinking of harming yourself: call 112 in Türkiye or your local "
            "emergency number. The banner is a rule, not a model judgement.",
            "Sessions train no model, by us or by a vendor. Text goes to Anthropic's API and is "
            "retained there only under their API data terms.",
        ]},
        "api": {"baslik": "API contract", "metin": "One public endpoint, the same one the demo box "
                "above calls. Treat it as a sample integration, not infrastructure."},
        "durum": {"baslik": "Status", "maddeler": [
            "Live: this site, POST /api/reflect, the waitlist with a real deletion path.",
            "Not built yet: accounts, history, reminders. No date committed.",
            "Not started: clinical review of the reflection protocol; no partner signed.",
        ]},
    },
    "kurumsal": {
        "baslik": "Company facts",
        "kunya": [
            ("Identity", "Independent AI consulting operated by Mevlana Yalçın, Ankara, Türkiye. "
             "Contract and contact point: " + POSTA + ". There is no registered legal entity yet; "
             "a sole proprietorship is opened with the first paid engagement, and that is stated "
             "in the proposal rather than discovered later."),
            ("Domain", "mevlanayalcin.com.tr is a personal domain held since September 2023. The "
             "consulting practice and the Yankı product both started in October 2026; the dates are "
             "kept separate on purpose."),
            ("Practice", "One person: measurement, analysis, code, delivery. No agency, no "
             "subcontracted build, and no capacity resold — I am paid for the work, not for where "
             "your traffic goes."),
            ("Claude in production", "Yankı runs on Anthropic's Messages API with "
             "claude-haiku-4-5-20251001 under a JSON-only schema enforced server-side; audit "
             "tooling calls the same account, so usage history exists rather than being claimed."),
            ("Availability", "One engagement at a time, so the re-measurement lands in the same "
             "quarter. Write to " + POSTA + " with the decision you are trying to make."),
        ],
        "dogrulama": [
            ("Source of the live product", DEPO),
            ("Health of the running endpoint", "https://" + DOMAIN + "/api/health"),
            ("Machine-readable site summary", "https://" + DOMAIN + "/llms.txt"),
            ("Crawl policy and sitemap", "https://" + DOMAIN + "/robots.txt"),
        ],
        "soru": {"baslik": "Questions worth asking first", "maddeler": [
            ("Are you an agency?", "No. One consultant, no juniors billed at partner rates, no "
             "sales-lead handoff to a delivery team you never met."),
            ("Do you resell tokens or take a provider cut?", "No. I do not sell capacity and I hold "
             "no referral commission from providers, so a finding that moves traffic away from a "
             "vendor costs me nothing."),
            ("Do you write production code?", "Yes — the case studies are shipped and running, and "
             "the routing work lands as pull requests in your repository."),
            ("How is it priced?", "Fixed price for fixed scope, quoted after the scope call. "
             "Retainers are day-based with a stated monthly ceiling; no time-based surprises."),
            ("Will you sign our NDA?", "Yes, including a note that client text may be processed "
             "through Anthropic's API for tooling, with no training on it."),
            ("Can you work with the vendor we already chose?", "Yes. The audit says whether that "
             "choice is defensible; it does not try to win an argument."),
            ("Languages?", "Turkish and English, in writing and in the readout."),
        ]},
    },
    "gizlilik": {
        "baslik": "Privacy, for this site and for your work",
        "maddeler": [
            "This site sets no cookie of its own. Cloudflare's cookieless traffic counter may load "
            "a script for aggregate pageview counts.",
            "The call-request form stores one value — your email address — in Cloudflare KV. Write "
            "to " + POSTA + " and it is deleted the same day.",
            "Client material stays in your environment. I measure with your keys and your logs; "
            "where a copy is unavoidable, it is kept on an encrypted machine and deleted at handover.",
            "Where my own tooling calls a model, that is a sub-processor named in the statement of "
            "work: Anthropic (inference) and Cloudflare (hosting). No advertising or analytics "
            "vendors touch client data.",
            "Handled under Türkiye's KVKK. Contact correspondence is processed to answer you and to "
            "invoice; no health or other sensitive-category records are created by this practice.",
            "Nothing here is legal or tax advice, and that is deliberate: consultancies that claim "
            "otherwise are selling you something else.",
        ],
    },
    "altbilgi": "Mevlana Yalçın · AI consulting · Ankara, Türkiye · " + POSTA +
                " · independent consultant, no capacity resold",
    "sayfalar": [("index", "Consulting"), ("hizmetler", "Services"), ("surec", "Process"),
                 ("calismalar", "Work"), ("kurumsal", "Company"), ("gizlilik", "Privacy")],
    "menuDilleri": {"en": "Türkçe", "tr": "English"},
    "menuEtiketi": "Menu",
    "altLinkler": [("GitHub", DEPO), ("llms.txt", "/llms.txt"), ("API", "/api/health")],
}

T = {
    "baslik": "Mevlana Yalçın — yapay zekâ danışmanlığı: LLM maliyet, gecikme ve tedarik zinciri denetimi",
    "ozet": "Büyük dil modeli trafiğinin gerçekte neye mal olduğunu ve kimin servis ettiğini "
            "ölçerim: sağlayıcı başına gerçek fiyat, ilk token gecikmesi, SLA tutma oranı, kâr "
            "marjını yiyen rotalama kararları ve senin tarafındaki sızıntı yolları.",
    "durum": "Bağımsız danışman · Ankara · aynı anda tek iş",
    "kahraman": {
        "ust": "Yapay zekâ danışmanlığı · LLM maliyet ve tedarik zinciri",
        "baslik": "Tokenlarının gerçek fiyatı ve arkasında kim var.",
        "alti": "Model kapasitesi alan ekiplerin çoğunda bir fatura vardır bir de his. His yerine "
                "ölçüm koyuyorum: sağlayıcı başına fiyat, ilk token süresi, saniyede token, "
                "sözün tutulma oranı, neyin bozulduğu ve bozulduğunda ne ödediğin. Sonra senin "
                "tarafında düzeltilebilecek kısımları birlikte düzeltiyoruz.",
    },
    "cta": {"baslik": "30 dakikalık görüşme talebi", "yer": "e-posta adresin", "dugme": "Görüşme iste",
            "not": "Yanıt " + POSTA + " adresinden gelir. Bülten yok, otomatik e-posta dizisi yok: "
                   "Cloudflare KV'de tek satır, istediğin gün silinir."},
    "ozetKutu": {
        "baslik": "Masaya ne konur",
        "maddeler": [
            "Sağlayıcı bazında karar tablosu: gerçek fiyat, ölçülmüş ilk token süresi ve hız, SLA "
            "tutma oranı, ve yalnız vitrinde duran model adları.",
            "Sızan para: önbellek fırsatları, pahalı rotalama varsayılanları, yeniden gönderilen "
            "istemler, iki kez faturalanan denemeler.",
            "Senin sorumluluğundaki güvenlik: anahtar kapsamları, harcama tavanları ve isteklerinin "
            "üçüncü taraflara teslim ettiği adresler.",
            "Kırk sayfalık sunum değil; sahibi ve beklenen tasarrufu yazılı kısa bir düzeltme listesi.",
        ],
    },
    "hizmetler": {
        "baslik": "Hizmetler",
        "alti": "Sabit kapsam, sabit fiyat, önce salt-okunur ölçüm. Kapasite satıcısı değilim; "
                "denetimdeki hiçbir buluş bana komisyon kazandırmıyor.",
        "paketler": [
            {
                "ad": "Inference denetimi", "sure": "5–10 iş günü", "fiyat": "4.500 $'dan",
                "icerik": [
                    "Sağlayıcı başına tablo: ilan edilen ile ölçülen fiyat, ilk token süresi, saniyede token.",
                    "Sözleşme gerçekliği: ne vaat ediliyor, ne tutuluyor, ne iade ediliyor.",
                    "Model adı tuzakları: listelenip fiyatlanmış ama hiç servis edilmeyen adlar.",
                    "Kimlik ve yetki hijyeni: anahtar kapsamları, IP listeleri, harcama tavanları, oran limitleri.",
                    "Sızıntı yolları: isteğinin taşıyıcıya teslim ettiği imzalı URL'ler ve görsel adresleri.",
                    "Önbellek fırsatı: istem ve yanıt önbelleği, tasarrufu dolar olarak yazılı.",
                ],
                "cikti": "Tek bir karar tablosu, 90 dakikalık sunum ve sahibi olan düzeltme listesi.",
            },
            {
                "ad": "Rotalama ve maliyet mimarisi", "sure": "2–4 hafta", "fiyat": "9.000 $'dan",
                "icerik": [
                    "Görev sınıfı başına model politikası; taban fiyat ve kalite rezervasyonu ile.",
                    "Fallback, tavan ve sabitleme anlamları wiki sayfası olarak değil kod olarak.",
                    "Önbellek stratejisi: ne sabitlenir, ne anahtarlanır, ne temizlenir.",
                    "Değerlendirme kümesi ve regresyon düzeneği — model değişikliği kumar olmaktan çıkar.",
                    "Senin iş biriminle raporlama: çözülen bilet başına, rapor başına, 1.000 kelime başına maliyet.",
                ],
                "cikti": "Senin deponda çalışan bir rotalama politikası + iş birimi başına maliyet panosu.",
            },
            {
                "ad": "Danışmanlık aboneliği", "sure": "aylık · yaklaşık 2 gün", "fiyat": "ayda 1.200 $'dan",
                "icerik": [
                    "Sağlayıcı fiyat ve davranış takibi; değişim sürpriz değil karar olur.",
                    "Yeni modellerin kendi trafiğin üzerinde kıyaslanması — genel bir puan tablosu değil.",
                    "\"Bunu hangi modelle yapalım\" sorusuna sayı eklenmiş yanıt.",
                    "Üç ayda bir yeniden ölçüm: denetim ya hâlâ geçerli çıkar ya da işi geri alırım.",
                    "İşe alım ve mimari değerlendirmelerinde ikinci görüş.",
                ],
                "cikti": "Sürekli bir karar günlüğü; kullanılmayan gün bir kez sonraki aya devreder.",
            },
        ],
    },
    "surec": {
        "baslik": "Bir iş nasıl yürür",
        "adimlar": [
            ("Kapsam görüşmesi, 30 dakika", "Karar vermen gereken şeyi anlatırsın. Ölçüm o kararı "
             "değiştirmeyecekse orada söylüyoruz ve hiçbir şey faturalanmaz."),
            ("Salt-okunur ölçüm", "Senin anahtarların, senin günlüklerin, senin trafiğin. Denetim "
             "süresince üretimde değişiklik yok, onaylanacak yeni satıcı yok, taşınma yok."),
            ("Buluş tablosu", "Her iddia yeniden üretilebilir bir komut ve bir sayı taşır. "
             "Yeniden üretemediğim satırı sen görmeden ben silerim."),
            ("Sahipli düzeltme listesi", "Altı-on iki madde, tasarruf/efor sırasına göre dizili, "
             "her biri senin ekibinde birine atanmış. Tahmin bana, iş size ait; aksini kararlaştırmazsak."),
            ("İki hafta sonra yeniden ölçüm", "Tasarruf aynı grafikte görünür; görünmezse denetim "
             "kapsamında ücret almadan çalışmaya devam ederim."),
        ],
    },
    "calismalar": {
        "baslik": "Çalışmalar",
        "alti": "Yayında bir ürün ve halka açık, çok sağlayıcılı bir inference borsasının bağımsız "
                "denetimi. İkisi de anlatılmadı, ölçüldü.",
        "kartlar": [
            {
                "ad": "Çok sağlayıcılı inference borsası — bağımsız denetim",
                "etiket": "tedarik zinciri · güvenlik",
                "metin": "Yirmi hesap, yirmi ayrı konut IP'si, 600'den fazla canlı iş ve konsolun "
                         "kullandığı tüm uçlar. Buluşlar: teklif defterinin %98'ini taşıyan tek "
                         "sağlayıcı, listelenip fiyatlanmış ama hiç servis edilmeyen amiral modeller "
                         "(stream dışı yolda deterministik origin çökmesi), dokümante edilmemiş "
                         "piyasa uçları, beyaz listesi olmayan sunucu taraflı görsel indirme ve "
                         "link-local adrese üçüncü taraf altyapıdan ulaşan akış; ve tekrarlanan "
                         "isteği bedava kılan yanıt önbelleği.",
                "bag": ("calismalar", "Yöntemi oku"),
            },
            {
                "ad": "Yankı — yayında bir Claude ürünü",
                "etiket": "ürün · üretimde claude",
                "metin": "Cloudflare Workers üzerinde yayınlanmış günlük duygu kontrol aracı: "
                         "Anthropic Messages API, claude-haiku-4-5-20251001, sunucu tarafında "
                         "zorlanan yalnızca-JSON çıktı, kriz sözünü modele sormadan kural listesiyle "
                         "kararlaştırma, kullanıcının metninde birebir geçmeyen alıntıyı atan mantık; "
                         "beta boyunca hiçbir günlük saklanmıyor.",
                "bag": ("yanki", "Canlı demoyu aç"),
            },
        ],
    },
    "yanki": {
        "baslik": "Yankı — yayında bir Claude ürünü",
        "alti": "Sitenin kimliği değil, bir vaka çalışması olarak duruyor: yukarıda anlatılan "
                "Claude bütünleştirmesinin gerçek ve çalışır olduğunun en temiz kanıtı bu.",
        "giris": "Ne olduğunu ve sana nasıl dokunduğunu yazarsın. Yankı duyduğunu düşündüğü duyguyu "
                 "adlandırır, kendi cümleni değişmeden alıntılar ve önündeki bir saat için tek bir "
                 "adım önerir. Bir eşlikçidir, terapi değil: teşhis koymaz, tıbbi tavsiye vermez.",
        "demo": {"baslik": "Bir yansıtma dene", "alti": "Bu kutu bu sayfanın anlattığı gerçek ucu "
                 "çağırır. Yazdığını saklamaz.",
                 "yer": "Gününü ve sana nasıl dokunduğunu bir cümleyle yaz…", "dugme": "Yansıt"},
        "ornekler": {"baslik": "Kaydedilmiş cevaplar", "alti": "/api/reflect ucunun birebir "
                     "cevapları; sayfa için yeniden yazılmadı."},
        "mimari": {"baslik": "Nasıl kuruldu", "maddeler": [
            "Anthropic Messages API, model claude-haiku-4-5-20251001; tek bir JSON nesnesi dönmek "
            "zorunda olan bir sistem istemi.",
            "Sunucu biçimi denetler. Bozuk cevap atılır ve arayüz \"ulaşılamadı\" der; modelin "
            "yerine geçen kural tabanlı sahte bir cevap yoktur.",
            "Kriz sözcükleri modele sorulmadan önce sabit bir kelime listesiyle belirlenir; eşleşme "
            "cevabı yardım hattı metniyle değiştirir.",
            "Modelin uydurduğu alıntı atılır: dönen alıntı kullanıcının metninde birebir geçmiyorsa "
            "gösterilmez.",
            "Beta boyunca bizim tarafımızda hiçbir şey saklanmaz; bekleme listesi Cloudflare KV'de "
            "tek anahtardır.",
            "Hız sınırı IP başına 60 saniyede 6 istek; bittiğinde 503 dönen günlük bütçe koruması.",
        ]},
        "guvenlik": {"baslik": "Yankı ne değildir", "maddeler": [
            "Terapi değil, teşhis değil, tıbbi cihaz değil. Klinik iddiası yoktur ve iddia da talep etmez.",
            "İlaç, doz veya tedavinin bırakılması hakkında öneri vermez.",
            "Derhal bir tehlikedeyse ya da kendini yaralamayı düşünüyorsan Türkiye'de 112'yi ara. "
            "Uyarı bir kuraldır, modelin kararı değil.",
            "Günlükler hiçbir modelin eğitiminin verisi yapılmaz. Metin Anthropic'in API'sine gider "
            "ve yalnızca onların API veri koşullarınca saklanır.",
        ]},
        "api": {"baslik": "API sözleşmesi", "metin": "Tek açık uç: yukarıdaki deneme kutusunun "
                "çağırdığıyla aynı uç. Bunu altyapı değil, örnek bir bütünleştirme olarak ele al."},
        "durum": {"baslik": "Durum", "maddeler": [
            "Yayında: bu site, POST /api/reflect ve gerçek silme yolu olan bekleme listesi.",
            "Yapılmadı: hesap, geçmiş, hatırlatmalar. Verilmiş tarih yok.",
            "Başlamadı: yansıtma protokolünün klinik değerlendirmesi; imzalı ortak yok.",
        ]},
    },
    "kurumsal": {
        "baslik": "Kurumsal künye",
        "kunya": [
            ("Kimlik", "Bağımsız yapay zekâ danışmanlığı; Mevlana Yalçın, Ankara. Sözleşme ve "
             "iletişim mercii: " + POSTA + ". Tescilli tüzel kişilik henüz yok; ilk ücretli işle "
             "bir şahıs şirketi kurulur ve bu teklifin içinde yazar, sonra keşfedilmez."),
            ("Domain", "mevlanayalcin.com.tr Eylül 2023'ten beri adıma kayıtlı kişisel bir alan "
             "adadır. Danışmanlık da Yankı da Ekim 2026'da başladı; bu iki tarih bilinçli olarak "
             "ayrı tutulur."),
            ("Çalışma biçimi", "Tek kişi: ölçüm, analiz, kod, teslim. Ajans yok, taşeron yok, "
             "kapasite satıcılığı yok — bana ücret iş için ödenir, trafiğinin nereye gittiği için değil."),
            ("Üretimde Claude", "Yankı, Anthropic'in Messages API'si üzerinde claude-haiku-4-5-20251001 "
             "ile ve sunucu tarafında zorlanan yalnızca-JSON şemasıyla çalışır; denetim araçları aynı "
             "hesabı çağırır, yani kullanım geçmişi iddia edilmez, vardır."),
            ("Ulaşılabilirlik", "Aynı anda tek iş; böylece yeniden ölçüm aynı çeyrekte teslim edilir. "
             "Karar vermen gereken şeyi yaz: " + POSTA + "."),
        ],
        "dogrulama": [
            ("Yayındaki ürünün kaynak kodu", DEPO),
            ("Çalışan ucun sağlık durumu", "https://" + DOMAIN + "/api/health"),
            ("Makine okumalı site özeti", "https://" + DOMAIN + "/llms.txt"),
            ("Örümcek politikası ve sitemap", "https://" + DOMAIN + "/robots.txt"),
        ],
        "soru": {"baslik": "Önce sorulması gereken sorular", "maddeler": [
            ("Ajans mısın?", "Hayır. Tek danışmanım; partnere faturalanan junior'lar ve seni "
             "tanımadığın bir teslim ekibine devreden satış öncüsü yok."),
            "Token satıyor ya da sağlayıcıdan komisyon alıyor musun?",
            ("Üretimde kod yazar mısın?", "Evet — vakalar yayında ve çalışıyor; rotalama işi senin "
             "deponda pull request olarak teslim edilir."),
            ("Fiyat nasıl?", "Sabit kapsam için sabit fiyat; kapsam görüşmesinden sonra teklif "
             "edilir. Abonelik gün üzerinden, aylık tavanı yazılıdır; sürpriz saat faturası yoktur."),
            ("NDA imzalar mısın?", "Evet; araçlamamız için metnin Anthropic API'sinden geçebileceği "
             "ve eğitim kullanılmayacağı şarta eklenir."),
            ("Zaten seçtiğimiz satıcıyla çalışır mısın?", "Çalışırım. Denetim, o seçimin savunulabilir "
             "olup olmadığını söyler; bir tartışmayı kazanmaya çalışmaz."),
            ("Diller?", "Türkçe ve İngilizce; yazıda da sunumda da."),
        ]},
    },
    "gizlilik": {
        "baslik": "Gizlilik: hem bu site hem senin işin için",
        "maddeler": [
            "Bu site kendi çerezini koymaz. Cloudflare'ın çerezsiz sayacı, toplam görüntüleme sayısı "
            "için bir betik yükleyebilir.",
            "Görüşme formu tek bir değer saklar: e-posta adresin, Cloudflare KV içinde. " + POSTA +
            " adresine yaz; aynı gün silinir.",
            "Müşteri verisi senin ortamında kalır. Ölçümü senin anahtarların ve günlüklerinle yaparım; "
            "kopyası kaçınılmazsa şifreli bir makinede durur ve teslimatta silinir.",
            "Araçlarım bir model çağırdığında bu, iş tanımı içinde alt işlemci olarak anılır: "
            "Anthropic (çıkarım) ve Cloudflare (barındırma). Reklam veya analiz satıcıları müşteri "
            "verisine dokunmaz.",
            "KVKK kapsamında ele alınır. Yazışmalar yanıt vermek ve faturalandırmak için işlenir; bu "
            "çalışma düzeni sağlık ya da diğer özel nitelikli kayıt üretmez.",
            "Burada yazanlar hukuk veya vergi tavsiyesi değildir; bilinçli olarak: aksini iddia eden "
            "danışman sana başka bir şey satıyordur.",
        ],
    },
    "altbilgi": "Mevlana Yalçın · yapay zekâ danışmanlığı · Ankara · " + POSTA +
                " · bağımsız danışman, kapasite satıcılığı yok",
    "sayfalar": [("index", "Danışmanlık"), ("hizmetler", "Hizmetler"), ("surec", "Süreç"),
                 ("calismalar", "Çalışmalar"), ("kurumsal", "Kurumsal"), ("gizlilik", "Gizlilik")],
    "menuDilleri": {"en": "Türkçe", "tr": "English"},
    "menuEtiketi": "Menü",
    "altLinkler": [("GitHub", DEPO), ("llms.txt", "/llms.txt"), ("API", "/api/health")],
}
T["kurumsal"]["soru"]["maddeler"][1] = ("Token satıyor ya da sağlayıcıdan komisyon alıyor musun?",
    "Hayır. Kapasite satmıyorum ve sağlayıcılardan referans komisyonu da almıyorum; bir buluşun "
    "trafiği bir satıcıdan uzaklaştırması bana hiçbir şeye mal olmaz.")
E["kurumsal"]["soru"]["maddeler"] = E["kurumsal"]["soru"]["maddeler"]

ICERIK = {"en": E, "tr": T}

# Calismalar sayfasindaki denetimin yontem ve bulgulari (Aydin: musteri iliskisi yok,
# asagidaki her sayi kendim yaptigim isteklerden geldi.)
AUDIT = {
    "en": {
        "baslik": "Method and findings — a public multi-provider inference exchange",
        "alti": "An exchange that auctions inference jobs to capacity sellers. No client "
                "relationship and nothing quoted from a contract: every number below came from "
                "requests I made myself.",
        "adimlar": [
            ("Accounts from clean origins", "Twenty accounts, each created from a distinct rotating "
             "residential exit IP; credentials kept locally, one sticky session per account so a "
             "sign-up never changed address mid-flow."),
            ("Endpoint discovery", "Started from the published OpenAPI description, then captured "
             "what the console itself calls. That turned up four market endpoints missing from the "
             "spec, including a balance read that works with a plain key."),
            ("Live measurement", "600+ paid jobs across model families. Per-provider price, "
             "first-token latency and throughput came from the exchange's own measurement endpoint, "
             "cross-checked against my own timers."),
            ("Failure behaviour", "Twenty-two flagship model names across three API surfaces, plus "
             "streaming, plus reservation and provider-pinning paths."),
            ("Out-of-band fetch", "Pointed a multimodal image URL at a canary host of mine and "
             "logged which networks arrived to fetch it, with headers."),
            ("Money paths", "Read the billing surface with a logged-in session: deposit rails, "
             "pre-payment behaviour, referral terms, the provider console and its admission gate."),
        ],
        "bulgular": [
            ("98% of the offer book is one seller", "773 of 786 offers — and roughly 72% of every "
             "job the exchange has ever served — belong to the operator's own supply entity. Four "
             "independent sellers list thirteen offers between them. There is a UI toggle for "
             "simulated hosts; on the day measured, no seller was one."),
            ("Flagship models are listed, priced and unservable", "Nineteen request shapes on two "
             "flagship families across Chat Completions, Messages and Responses: the non-streaming "
             "path returns a 502 that is a CDN error page rather than an API error, so SDKs cannot "
             "parse it; streaming returns 200 with an in-band 'provider_failed'. Nothing is charged "
             "when this happens."),
            ("Its own error message recommends a model that does not exist", "'Try liquid.auto or "
             "architect/deepseek-latest' — that name is not in the catalogue, and asking for it "
             "reproduces the 502."),
            ("Any image URL is fetched by whoever wins the auction", "No host allowlist on the "
             "server-side fetch. A presigned URL inside your request is handed to third-party "
             "infrastructure — measured egress came from a US GPU cloud and a Shanghai ISP — and "
             "link-local addresses are dialled as well."),
            ("A blind SSRF with a usable timing oracle", "Refused ~2.5s, answered ~3.9s, filtered "
             "~12.5s: enough to distinguish open, closed and firewalled internally, from outside."),
            ("Undocumented market endpoints", "Provider-named price histories with repricing counts, "
             "measured tokens-per-second per model per seller, a cursor-paginated receipt feed, and "
             "a balance endpoint reachable with an ordinary key."),
            ("A response cache that moves no money", "Opt-in, TTL up to 24 hours: an identical "
             "request costs nothing, creates no job and returns a stored answer — 25 of 25 repeat "
             "requests were free, 20 in parallel in under five seconds."),
            ("Market data can go dark for minutes", "Catalogue endpoints returned empty 404s to "
             "every client, proxied or not, while completions kept succeeding; the published "
             "spec's paths were unchanged, so this was availability rather than a route change."),
            ("A marketplace that is one supplier", "Every flagship family I tested was quoted by "
             "exactly one seller, so 'single supplier' is the normal state, not an edge case — and "
             "the buyer-side agreement contains no self-dealing or affiliated-provider clause."),
        ],
        "sonuc": "Deliverable shape: one decision table — provider × price × first token × "
                 "throughput × SLA kept — a fix list with owners, and a re-measurement date. "
                 "Nothing here needed a contract to be reproducible; that is the point of the method.",
    },
    "tr": {
        "baslik": "Yöntem ve bulgular — halka açık, çok sağlayıcılı bir inference borsası",
        "alti": "İnference işlerini kapasite satıcılarına açık artırmayla veren bir borsa. Müşteri "
                "ilişkisi yok; sözleşmeden alıntı yok. Aşağıdaki her sayı kendi yaptığım "
                "isteklerden geldi.",
        "adimlar": [
            ("Hesaplar temiz çıkışlardan", "Yirmi hesap, her biri ayrı dönen konut IP'sinden "
             "açıldı; kimlikler yerelde kaldı, her hesaba yapışkan tek oturum verildi ki kayıt "
             "ortasında adres değişmesin."),
            ("Uç keşfi", "Yayındaki OpenAPI tarifinden başlandı, sonra konsolun gerçekte neyi "
             "çağırdı yakalandı. Tarifte olmayan dört piyasa ucu çıktı — düz bir anahtarla "
             "çalışan bakiye ucu dahil."),
            ("Canlı ölçüm", "Model aileleri boyunca 600+ ücretli iş. Sağlayıcı başına fiyat, ilk "
             "token gecikmesi ve hız, borsanın kendi ölçüm ucundan alındı ve kendi kronometremle "
             "karşılaştırıldı."),
            ("Bozulma davranışı", "Yirmi iki amiral model adı, üç API yüzeyi, ayrıca stream, "
             "rezervasyon ve sağlayıcı sabitleme yolları."),
            ("Bant dışı indirme", "Çok modlu bir görsel adresi kendi kanarya sunucuma çevrildi; "
             "başlıklarıyla birlikte indirmenin hangi ağlardan geldiği kaydedildi."),
            ("Para yolları", "Oturumla faturalama yüzeyi okundu: ödeme rayları, ödeme öncesi "
             "bakiye davranışı, referans koşulları, satıcı konsolu ve kabul kapısı."),
        ],
        "bulgular": [
            ("Teklif defterinin %98'i tek satıcı", "786 teklifin 773'ü — ve borsanın hiç servis "
             "etmediği işlerin yaklaşık %72'si — operatörün kendi arz varlığına ait. Dört bağımsız "
             "satıcı aralarında on üç teklif listeliyor. Arayüzde simüle edilmiş satıcıları gizleme "
             "seçeneği var; ölçüm gününde hiçbiri simüle değildi."),
            ("Amiral modeller listeleniyor, fiyatlanıyor, servis edilmiyor", "İki amiral ailesinde "
             "on dokuz istek biçimi, Chat Completions / Messages / Responses üzerinden: stream "
             "dışı yol API hatası değil CDN hata sayfası döndürüyor (SDK'lar ayrıştıramıyor); "
             "stream 200 dönüp bant içi 'provider_failed' veriyor. Bu durumda ücret düşmüyor."),
            ("Kendi hata mesajı olmayan bir modeli öneriyor", "'Try liquid.auto or "
             "architect/deepseek-latest' — o ad katalogda yok ve istendiğinde aynı 502'yi veriyor."),
            ("Herhangi bir görsel adresini ihaleyi kazanan indiriyor", "Sunucu taraflı indirmede "
             "host beyaz listesi yok. İsteğinin içindeki imzalı URL üçüncü taraf altyapıya teslim "
             "ediliyor — ölçülen çıkışlar bir ABD GPU bulutu ve Şanghay bir ISP — ve link-local "
             "adresler de aranıyor."),
            ("Kör SSRF, kullanılabilir zamanlama rehberi", "Reddedilen ~2,5 sn, yanıt veren ~3,9 sn, "
             "filtrelenen ~12,5 sn: içerideki açık/kapalı/filtreli ayrımı dışarıdan yapılabiliyor."),
            ("Dokümante edilmemiş piyasa uçları", "Satıcı adıyla fiyat geçmişi ve yeniden "
             "fiyatlandırma sayıları, satıcı-ve-model başına ölçülmüş saniyede token, imleçli fiş "
             "akışı ve sıradan bir anahtarla okunan bakiye ucu."),
            ("Para hareketi ettirmeyen yanıt önbelleği", "Seçmeli, TTL 24 saate kadar: aynı istek "
             "hiçbir şeye mal olmuyor, iş oluşturmadan kayıtlı cevabı döndürüyor — 25 tekrar "
             "isteğinin 25'i bedavaydı, 20 tanesi beş saniyenin altında paralel."),
            ("Piyasa verisi dakikalarca kararabiliyor", "Katalog uçları tüm istemcilere boş 404 "
             "döndürürken tamamlayıcılar çalışmaya devam etti; yayındaki tarifin yolları "
             "değişmemişti, yani bu bir yol değişikliği değil erişilebilirlik olayıydı."),
            ("Pazar yeri dediğin tek tedarikçi", "Test ettiğim her amiral ailesini tam olarak bir "
             "satıcı fiyatlıyordu; yani 'tek tedarikçi' istisna değil olağan hâl — ve alıcı "
             "sözleşmesinde kendi-kendine-iş yapma ya da bağlı satıcı maddesi yok."),
        ],
        "sonuc": "Teslim biçimi: tek bir karar tablosu — satıcı × fiyat × ilk token × hız × SLA "
                 "tutma — sahipli bir düzeltme listesi ve yeniden ölçüm tarihi. Burada hiçbir şey "
                 "sözleşme gerektirmedi; metodun amacı da bu.",
    },
}
for _d in ("en", "tr"):
    ICERIK[_d]["audit"] = AUDIT[_d]
