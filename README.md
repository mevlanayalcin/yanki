# mevlanayalcin.com.tr

Mevlana Yalçın — yapay zekâ danışmanlığı sitesinin kaynağı. Sitenin kimliği artık bir
ürün değil: **LLM maliyet, gecikme ve tedarik zinciri denetimi** hizmeti.
**Yankı** (günlük duygu kontrol aracı) marka olmaktan çıktı; `dist/work/yanki/`
(TR: `dist/calismalar/yanki/`) sayfasında **yayında bir vaka çalışması** olarak duruyor —
yani üretimde Claude kullanıldığının görülebilir kanıtı.

## Bu depoda ne var

| Yol | İçerik |
|---|---|
| `scripts/icerik.py` | Tüm sayfa metinlerinin tek kaynağı (EN + TR, iki dilli slug'larla) |
| `scripts/build.py` | Statik site üreticisi: `dist/` içine sayfalar, 404, sitemap, robots, llms.txt |
| `scripts/denet.py` | Uç için kural tabanlı kriz/salınım denetimi (Yankı vakası) |
| `dist/assets/` | Tek stil dosyası (`site.css`), mobil menü, demo kutusu + form betiği |
| `cloudflare/worker.mjs` | `POST /api/reflect`, `POST /api/waitlist`, `GET /api/health` + eski URL'ler için 301 yönlendirmeler |
| `data/ornekler.json` | Uçtan **kaydedilmiş** cevaplar; sayfadaki örnekler elle yazılmadı |
| `wrangler.toml` | Workers yapılandırması (Assets + KV + Durable Object + özel alan adları) |

## Sayfa yapısı

| EN | TR |
|---|---|
| `/` Danışmanlık (pozisyon + masaya ne konur + paketler + vakalar) | `/tr/` |
| `/services/` Üç paket: kapsam, süre, fiyat çapası | `/tr/hizmetler/` |
| `/process/` Beş adımlı işleyiş | `/tr/surec/` |
| `/work/` Denetimin yöntemi ve bulguları | `/tr/calismalar/` |
| `/work/yanki/` Vaka: canlı ürün, demo kutusu, API sözleşmesi | `/tr/calismalar/yanki/` |
| `/company/` Kimlik, bağımsız doğrulama bağlantıları, ilk sorulacak sorular | `/tr/kurumsal/` |
| `/privacy/` Site ve müşteri verisi gizliliği, alt işlemciler, KVKK | `/tr/gizlilik/` |

## Dağıtım

```bash
python3 scripts/build.py                                  # dist/ uretir
npx --yes wrangler@latest deploy                          # Workers + Assets
npx --yes wrangler@latest secret put ANTHROPIC_API_KEY    # tek sir (Yanki ucu icin)
```

Ortam değişkeni gerekmez; sır `ANTHROPIC_API_KEY` olarak worker'a bağlıdır.
`wrangler.toml` içindeki `[assets]` bölümü `dist/`'i sunar; worker önce kendi
yollarını (`/api/*`, eski URL yönlendirmeleri) görür, sonra asset'lere düşer.

## Eski URL'ler (301)

Ürün sayfası döneminden kalan yollar kırılmadı, worker üzerinden 301 ile yeni
yapıya bağlandı: `/how-it-works/ → /process/`, `/safety/ → /work/yanki/`,
`/api/ → /work/yanki/#api`, `/tr/nasil/ → /tr/surec/`, `/tr/guvenlik/ →
/tr/calismalar/yanki/`, `/tr/api/ → /tr/calismalar/yanki/#api`.

## Yankı vakasının sıkı kuralları (değişmedi)

- Çıkarım: Anthropic Messages API, `claude-haiku-4-5-20251001`, JSON dönmek zorunda olan istem.
- **Kriz sözcükleri modele sorulmaz**: sabit liste model çağrısından *önce* çalışır; eşleşmede
  cevap `provider: "rule"`, `model: "crisis-list-v1"` ile döner.
- **Alıntı uydurulamaz**: dönen alıntı kullanıcının metninde birebir geçmiyorsa sunucu siler.
- Bozuk/eksik JSON **gösterilmez**: uç `malformed_answer` döner; kural tabanlı sahte yedek yoktur.
- Beta boyunca günlükler saklanmaz; bekleme listesi tek KV satırıdır, istenince aynı gün silinir.
- Hız sınırı IP başına 6 istek / 60 sn; günlük bütçe koruması bitince 503.

## Durum

Yayında: bu site, `POST /api/reflect`, `GET /api/health`, görüşme talebi formu (KV).
Danışmanlık tarafında: aynı anda tek iş; tüzel kişilik henüz yok — ilk ücretli işle
şahıs şirketi kurulur ve bu teklifte baştan yazılır.
İletişim: merhaba@mevlanayalcin.com.tr
