# Mevlana Yalçın — AI danışmanlığı ve ürünler

İngilizce ve Türkçe danışmanlık sitesi; hizmetler, çalışma biçimi, kurumsal bilgiler
ve Claude kullanan Yankı ürünü. Yankı burada çalışan bir beta üründür.
Anlatım AI danışmanlığı, doğrudan Claude entegrasyonu ve doğrulanabilir ürün
üzerine kuruludur.

## Kaynaklar

| Yol | İçerik |
|---|---|
| `scripts/site_copy.py` | Her iki dilin içerikleri |
| `scripts/build.py` | Sayfa iskeletleri, tek URL haritası, sitemap ve metadata |
| `site/assets/` | CSS, istemci kodu, özgün SVG grafik ve yerel fontlar |
| `dist/` | Üretilen yayın dosyaları; elle düzenlenmez |
| `cloudflare/worker.mjs` | Yankı API, eski URL yönlendirmeleri ve tercih edilen domain |
| `wrangler.toml` | Workers + Assets + KV + Durable Object yapılandırması |
| `scripts/denet.py` | Mevcut canlı sayfa, metadata ve bağlantı denetimi |

## Geliştirme ve yayın

```bash
python3 scripts/build.py
npx --yes wrangler@4.148.0 dev --local --port 4173 --host localhost --local-upstream localhost
```

Yerel preview için host belirtilir; aksi halde Wrangler üretim alan adını taklit
ederken canonical yönlendirmesi localhost'a geri dönüp döngü oluşturabilir.
Yerel geliştirmede üretim API sırrı kullanılmaz; Yankı'nın başarı yanıtı üretim
üzerinde ayrıca doğrulanır. Anahtar dosyaya veya komut argümanına yazılmaz.

```bash
python3 scripts/build.py
npx --yes wrangler@4.148.0 deploy --dry-run --keep-vars
npx --yes wrangler@4.148.0 deploy --keep-vars
python3 scripts/denet.py https://mevlanayalcin.com.tr
```

Üretim ortamında mevcut `ANTHROPIC_API_KEY` secret korunur. `ASSETS`, `WAITLIST`
ve `SINIRLAYICI` bindingleri gerekir. Statik font/CSS/JS/grafikler Worker'ı
çalıştırmadan servis edilir; HTML ve API istekleri Worker üzerinden geçer.
Eski yollar, özellikle `/tr/company/`, çalışan yeni sayfalara yönlendirilir.

## Yankı sınırları

- Anthropic Messages API, `claude-haiku-4-5-20251001` modeli.
- Yanıtın temel biçimi ve alıntının normalize edilmiş metin içinde bulunması
  kontrol edilir. Bu kontroller tüm model hatalarını önleyemez.
- Sabit kriz sözcükleri modeli çağırmadan yardım metni döndürebilir; tüm acil
  durumları tespit eden bir sistem değildir. Yankı terapi veya tıbbi hizmet değildir.
- Başarısız model çağrısında sahte yedek cevap gösterilmez.
- Uygulama günlük metinlerini ve yanıtları bir günlük veritabanına yazmaz.
  Sağlayıcıların veri işleme koşulları ve operasyonel kayıtları ayrıca geçerlidir.
- KV üzerinde kullanım sayacı ve isteğe bağlı bekleme listesi bilgileri tutulur.
  Bekleme kaydı adresle birlikte kayıt zamanı, dil ve kaynak metadatası içerir.
- Günlük bütçe sayacı yaklaşık korumadır; atomik finansal tavan veya bakiye
  doğrulaması değildir. Hız sınırı Durable Object ile uygulanır.
- `/api/health` servis metadatasıdır; gerçek Anthropic bağlantı testi değildir.

## Kimlik

Kurucu: Mevlana Yalçın, Ankara. Ayrı tescilli tüzel kişilik henüz yok.
Domain başlangıcı Eylül 2023, sitedeki danışmanlık ve Yankı başlangıcı Ekim 2026;
bu tarihler şirket tescil tarihi olarak sunulmaz. Site müşteri, yatırım, gelir,
partnerlik veya startup programı kabulü hakkında doğrulanmamış iddia içermez.

İletişim: info@mevlanayalcin.com.tr

Manrope fontu SIL Open Font License ile yerel olarak servis edilir;
lisans `site/assets/OFL-Manrope.txt` içindedir.
