# Yankı

Duygusal günlük kontrol için bir yansıtan yapay zekâ eşlikçisi. Kullanıcı ne yaşadığını
yazar; Yankı duyduğu duyguyu adlandırır, **kullanıcının kendi cümlesini birebir alıntılayarak**
yansıtır ve önündeki bir saat için tek bir somut adım önerir.

**Yankı terapi değildir, teşhis koymaz, tıbbi tavsiye vermez.** Bu üçü arayüzde de,
`safety` sayfasında da bu metinle yazar.

## Bu depoda ne var

| Yol | İçerik |
|---|---|
| `scripts/build.py` | Tüm sayfa metinlerinin tek kaynağı ve statik site üreticisi (`dist/`) |
| `dist/assets/` | Tek stil dosyası, mobil menü, deneme kutusu |
| `cloudflare/worker.mjs` | `POST /api/reflect`, `POST /api/waitlist`, `GET /api/health` |
| `data/ornekler.json` | Uçtan **kaydedilmiş** cevaplar; sayfada basılan örnekler elle yazılmadı |
| `wrangler.toml` | Workers yapılandırması (Assets + KV + Durable Object) |

## Mimari ve bilinçli kısıtlar

- Çıkarım: Anthropic Messages API, `claude-haiku-4-5-20251001`, JSON dönmek zorunda olan
  kısıtlı bir sistem istemi.
- **Kriz sözcükleri modele sorulmaz.** Sabit bir kelime listesi (TR + EN, normalize edilmiş)
  model çağrısından *önce* çalışır; eşleşirse cevap kural tarafından üretilir ve yanıtta
  `provider: "rule"`, `model: "crisis-list-v1"` yazar.
- **Alıntı uydurulamaz.** Dönen `alinti` alanı kullanıcının metninde birebir geçmiyorsa
  sunucu tarafında silinir. Modelin kendi kendine alıntı üretmesi sözleşmeye aykırıdır.
- Bozuk veya eksik JSON **gösterilmez**: uç `malformed_answer` döner, arayüz "ulaşılamadı"
  der. Kural tabanlı sahte bir yedek cevap yoktur.
- Beta boyunca günlükler tarafımızda saklanmaz; bekleme listesi tek bir KV satırıdır.
- Günlük bütçe koruması: ödemenin eşdeğeri birim sayacı tavana dayanırsa uç 503 döner.
- Hız sınırı: IP başına 6 istek / 60 saniye (Durable Object).

## Dağıtım

```bash
python3 scripts/build.py                                  # dist/ uretir
npx --yes wrangler@latest deploy                          # Workers + Assets
npx --yes wrangler@latest secret put ANTHROPIC_API_KEY    # tek sir
```

Ortam değişkeni gerekmez; sır `ANTHROPIC_API_KEY` olarak worker'a bağlıdır.

## Durum

Yayında: bu site, `/api/reflect`, bekleme listesi.
Geliştiriliyor: hesap, günlük geçmişi, hatırlatmalar.
Planlanan: bir klinik uzman tarafından değerlendirilmiş yansıtma protokolü, ikinci dil seti, mobil uygulamalar (tarih yok).

Tek kişi, Ankara. Tescilli tüzel kişilik yok, dışarıdan finansman alınmadı, ücretli müşteri yok.
İletişim: merhaba@mevlanayalcin.com.tr
