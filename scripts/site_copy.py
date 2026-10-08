"""Public-facing copy for the consulting site, in English and Turkish.

All values are plain text. Product status and legal identity are intentionally
separate: a working product does not imply an incorporated company.
"""

COPY = {
    "en": {
        "meta": {
            "title": "Mevlana Yalçın — AI Consulting & Yankı",
            "description": "AI consulting and product engineering from Ankara. We build with Claude and develop Yankı, a live reflection companion with public source code.",
        },
        "nav": {
            "services": "Expertise", "products": "Yankı", "approach": "Approach",
            "company": "About", "contact": "Let's talk", "language": "TR",
        },
        "hero": {
            "eyebrow": "AI consulting & product engineering",
            "title": "Practical AI.",
            "title_accent": "Built with Claude.",
            "body": "We are an AI consultancy building Yankı, a reflection companion powered by Claude. Our product work informs how we help teams choose, integrate and evaluate AI.",
            "primary": "Try Yankı", "secondary": "How we use Claude",
            "note": "Founded and led by Mevlana Yalçın. Based in Ankara.",
        },
        "intro": {
            "eyebrow": "Consulting informed by building",
            "title": "A working product behind the advice.",
            "body": "Yankı gives us a concrete place to work through the decisions behind an AI application: a clear purpose, careful handling of user text and responses that can be checked. We bring that approach to our consulting offer.",
        },
        "services": {
            "eyebrow": "Expertise",
            "title": "From a clear question to a working system.",
            "body": "A focused engagement, with a defined outcome and direct access to the person doing the work.",
            "items": [
                {"number": "01", "title": "Claude adoption", "body": "Identify where Claude can help in your workflow. Define the use case, the data it needs and the result that would make the work worthwhile.", "tags": ["Use-case discovery", "Technical direction", "Delivery planning"]},
                {"number": "02", "title": "AI integration", "body": "Connect Claude to a useful experience. Build the interface, application logic and API integration around a focused product or workflow.", "tags": ["Claude API", "Application design", "Product engineering"]},
                {"number": "03", "title": "Evaluation & reliability", "body": "Review how the system responds in real use cases. Assess answer quality, failure cases, response times and cost before deciding what to improve.", "tags": ["Output evaluation", "Failure handling", "Performance & cost"]},
            ],
        },
        "products": {
            "eyebrow": "Our product",
            "title": "Meet Yankı.",
            "body": "A simple daily check-in for people who want to put a moment into words and reflect on it. Claude provides the reflection; our application shapes the experience around it.",
            "items": [
                {"slug": "yanki", "name": "Yankı", "category": "Personal reflection", "status": "Live beta", "title": "A little space to hear yourself think.", "body": "Write about your day. Yankı offers a short reflection, draws on your own words and suggests one small next step.", "cta": "Try Yankı", "href": "/work/yanki/", "detail": "A reflective companion, not therapy or medical advice."},
            ],
        },
        "claude": {
            "eyebrow": "Claude in practice",
            "title": "A real integration. Open to inspection.",
            "body": "Claude is central to Yankı: it reads the user's passage and produces the reflection. The live experience and public source show how we put the model to work.",
            "items": [
                {"title": "Try the live product", "body": "Write your own text in Yankı and receive a new response. The beta calls the live service and shows an error when a reflection is unavailable."},
                {"title": "See how Claude is used", "body": "Yankı calls Anthropic's API directly. The application checks response structure and quoted text, with a separate rule check for crisis wording. These checks reduce risk; they do not make every response correct."},
                {"title": "Inspect the source", "body": "The public repository contains the prompt, API integration and response checks. You can see what the application asks of Claude and how it handles the result."},
            ],
            "cta": "Try Yankı", "source_label": "View source on GitHub",
        },
        "process": {
            "eyebrow": "How we work",
            "title": "Small steps. Clear decisions.",
            "steps": [
                {"number": "01", "title": "Understand the problem", "body": "We start with the people, the workflow and the outcome you need. Together, we decide what is worth building and how we will judge it."},
                {"number": "02", "title": "Make it tangible", "body": "We build a focused first version and review it with you. Working software gives us something concrete to learn from."},
                {"number": "03", "title": "Refine and deliver", "body": "We test the important cases, improve the weak points and agree on what comes next, including documentation and ongoing care."},
            ],
        },
        "company": {
            "eyebrow": "The practice",
            "title": "Independent by design. Involved in the details.",
            "body": "Mevlana Yalçın is a founder-led AI consultancy and product studio based in Ankara, Türkiye. The founder develops Yankı and offers consulting on Claude adoption, integration and evaluation. Enquiries go directly to the person responsible for the work.",
            "facts": [
                {"label": "Based in", "value": "Ankara, Türkiye"},
                {"label": "Led by", "value": "Mevlana Yalçın"},
                {"label": "Focus", "value": "AI consulting & product engineering"},
                {"label": "Our product", "value": "Yankı · live beta"},
            ],
            "legal": "Mevlana Yalçın is the name of this independent practice. It is not currently a separately incorporated legal entity. Enquiries and engagement terms are handled directly by the founder.",
            "dates": "The founder has held mevlanayalcin.com.tr since September 2023. The consulting offer on this site and product work on Yankı began in October 2026. The domain date is not an incorporation date.",
            "model_use": "Yankı uses Claude through Anthropic's API to produce reflections. Our own application checks the response format and quoted text, and applies a separate crisis-word check.",
        },
        "contact": {
            "eyebrow": "Have something in mind?",
            "title": "Let's give your next idea a clear direction.",
            "body": "Tell us what you are working on, what is getting in the way and what a useful outcome would look like. We'll take it from there.",
            "cta": "Start a conversation", "email": "info@mevlanayalcin.com.tr",
        },
        "footer": {
            "description": "AI consulting and engineering. Makers of Yankı.",
            "location": "Ankara, Türkiye", "legal": "About the practice",
            "privacy": "Privacy", "source": "Yankı source code",
        },
        "privacy": {
            "eyebrow": "Privacy",
            "title": "A clear account of what you share.",
            "intro": "This page describes the consulting site and the Yankı experience hosted here.",
            "sections": [
                {"title": "Getting in touch", "body": "When you contact us by email, we receive the information you choose to send. We use it to respond to your enquiry and discuss the work. Please do not include passwords, private keys or sensitive personal records."},
                {"title": "Using Yankı", "body": "To produce a reflection, your text is processed by this site's service and sent to Anthropic's API. The application does not save the text or reflection in a journal database. Anthropic and the hosting provider handle data under their own service terms; this is not a promise of zero retention by every provider."},
                {"title": "Service protection", "body": "The service uses your network address to limit repeated requests and keeps usage counters to control the daily budget. These operational records are separate from the text you submit."},
                {"title": "Product updates", "body": "If you join the Yankı waitlist, we store your email address with the signup time, language and source in Cloudflare. Contact us if you would like that entry removed."},
                {"title": "Website infrastructure", "body": "Cloudflare hosts and protects the site. Its infrastructure may process network and request information. We do not include advertising pixels or session-replay tools in the site's application code."},
                {"title": "Questions or deletion requests", "body": "Write to info@mevlanayalcin.com.tr with your request. The contact responsible for this site is Mevlana Yalçın, Ankara, Türkiye."},
            ],
        },
        "yanki": {
            "eyebrow": "A product by Mevlana Yalçın",
            "title": "Make a little room for reflection.",
            "body": "Some days become easier to understand when you put them into words. Yankı reads what you share and offers a brief reflection, a phrase from your own text and one small next step.",
            "status": "Live beta", "cta": "Try a reflection",
            "safety": "Yankı is a reflective companion. It is not therapy, diagnosis or medical advice, and is not an emergency service. If you are in immediate danger, contact local emergency services: 112 in Türkiye.",
            "features": [
                {"title": "Begin in your own words", "body": "Describe a moment from your day and how it felt. There is no right way to write it."},
                {"title": "See what comes through", "body": "Yankı suggests a feeling and reflects what it hears. It can get things wrong; you decide what fits."},
                {"title": "Choose a small next step", "body": "Consider one manageable action, such as a short pause, a note to yourself or a conversation."},
            ],
            "input_label": "What's on your mind?",
            "input_placeholder": "Write a few sentences about your day and how it felt…",
            "input_button": "Reflect", "loading": "Reading your words…",
            "error": "Yankı couldn't complete this reflection. Please try again later.",
            "privacy_note": "Your text is sent to Anthropic to generate a response. This application does not save a journal history. Avoid sharing identifying or sensitive details.",
        },
        "labels": {
            "back": "Back to home", "learn_more": "Learn more", "external": "External site",
            "available": "Open to project enquiries", "not_found_title": "This page could not be found.",
            "not_found_body": "The address may have changed. Head back to the home page to find what you need.",
        },
    },
    "tr": {
        "meta": {
            "title": "Mevlana Yalçın — AI Danışmanlığı ve Ürün Geliştirme",
            "description": "Ankara merkezli AI danışmanlığı ve ürün geliştirme. Claude ile çalışan, kaynak kodu açık düşünme eşlikçisi Yankı'yı geliştiriyoruz.",
        },
        "nav": {
            "services": "Uzmanlık", "products": "Yankı", "approach": "Yaklaşım",
            "company": "Hakkımızda", "contact": "Konuşalım", "language": "EN",
        },
        "hero": {
            "eyebrow": "Claude ile AI danışmanlığı ve ürün geliştirme",
            "title": "Fikirden ürüne.",
            "title_accent": "Claude ile.",
            "body": "Claude ile çalışan düşünme eşlikçisi Yankı'yı geliştiren bir AI danışmanlığı girişimiyiz. Ürün deneyimimizi yapay zekâ seçimi, entegrasyonu ve değerlendirmesi için sunuyoruz.",
            "primary": "Yankı’yı deneyin", "secondary": "Claude’u nasıl kullanıyoruz",
            "note": "Mevlana Yalçın tarafından kuruldu ve yürütülüyor. Ankara merkezli.",
        },
        "intro": {
            "eyebrow": "Ürün geliştirerek öğreniyoruz",
            "title": "Danışmanlığımızın arkasında çalışan bir ürün var.",
            "body": "Yankı ile bir AI uygulamasının temel kararlarını somut bir ürün üzerinde ele alıyoruz: açık bir amaç, kullanıcı metninin dikkatli işlenmesi ve denetlenebilir yanıtlar. Danışmanlık hizmetimize de aynı yaklaşımı taşıyoruz.",
        },
        "services": {
            "eyebrow": "Uzmanlık",
            "title": "Doğru sorudan çalışan bir sisteme.",
            "body": "Kapsamı ve beklenen sonucu belli bir çalışma. İşi yapan kişiyle doğrudan iletişim.",
            "items": [
                {"number": "01", "title": "Claude kullanım danışmanlığı", "body": "Claude'un iş akışınızda nerede yarar sağlayacağını belirleyelim. Kullanım amacını, gereken veriyi ve çalışmadan beklenen sonucu netleştirelim.", "tags": ["İhtiyaç analizi", "Teknik yönlendirme", "Uygulama planı"]},
                {"number": "02", "title": "AI entegrasyonu", "body": "Claude'u kullanışlı bir deneyime bağlayalım. Belirli bir ürün veya iş akışı için arayüzü, uygulama mantığını ve API bağlantısını geliştirelim.", "tags": ["Claude API", "Uygulama tasarımı", "Ürün mühendisliği"]},
                {"number": "03", "title": "Değerlendirme ve güvenilirlik", "body": "Sistemin gerçek kullanım durumlarındaki yanıtlarını inceleyelim. Yanıt kalitesini, hata durumlarını, süreyi ve maliyeti değerlendirerek neyi iyileştireceğimizi belirleyelim.", "tags": ["Yanıt kalitesi", "Hata yönetimi", "Performans ve maliyet"]},
            ],
        },
        "products": {
            "eyebrow": "Ürünümüz",
            "title": "Yankı ile tanışın.",
            "body": "Yaşadığı bir anı kelimelere döküp üzerine düşünmek isteyenler için sade bir günlük deneyimi. Yansıtmayı Claude üretir; uygulamamız bu yanıtın etrafındaki deneyimi kurar.",
            "items": [
                {"slug": "yanki", "name": "Yankı", "category": "Kişisel yansıtma", "status": "Beta yayında", "title": "Kendinizi duymak için küçük bir alan.", "body": "Gününüzden söz edin. Yankı, kendi cümlelerinizden yola çıkan kısa bir yansıtma ve atabileceğiniz küçük bir adım sunsun.", "cta": "Yankı'yı deneyin", "href": "/tr/calismalar/yanki/", "detail": "Bir düşünme eşlikçisidir; terapi veya tıbbi tavsiye değildir."},
            ],
        },
        "claude": {
            "eyebrow": "Claude'u nasıl kullanıyoruz",
            "title": "Çalışan entegrasyon. İncelenebilir kaynak kodu.",
            "body": "Claude, Yankı'nın temel işlevini yerine getirir: kullanıcının metnini okur ve yansıtmayı üretir. Canlı ürün ve açık kaynak kodu, modeli nasıl kullandığımızı gösterir.",
            "items": [
                {"title": "Canlı ürünü deneyin", "body": "Yankı'ya kendi metninizi yazın ve yeni bir yanıt alın. Beta gerçek hizmeti çağırır; yansıtma üretilemediğinde hata gösterir."},
                {"title": "Claude'un rolünü görün", "body": "Yankı doğrudan Anthropic API'yi çağırır. Uygulama yanıt yapısını ve alıntıları denetler; kriz sözcüklerini ayrı bir kuralla kontrol eder. Bu kontroller riski azaltır, her yanıtın doğru olacağını garanti etmez."},
                {"title": "Kaynak kodunu inceleyin", "body": "Herkese açık depoda modele verilen talimatlar, API entegrasyonu ve yanıt kontrolleri bulunur. Uygulamanın Claude'dan ne istediğini ve sonucu nasıl işlediğini görebilirsiniz."},
            ],
            "cta": "Yankı’yı deneyin", "source_label": "GitHub'da kaynak kodunu inceleyin",
        },
        "process": {
            "eyebrow": "Çalışma biçimimiz",
            "title": "Küçük adımlar. Net kararlar.",
            "steps": [
                {"number": "01", "title": "İhtiyacı anlayalım", "body": "Kullanıcıları, iş akışını ve ulaşmak istediğiniz sonucu konuşarak başlıyoruz. Neyi geliştireceğimize ve nasıl değerlendireceğimize birlikte karar veriyoruz."},
                {"number": "02", "title": "Somutlaştıralım", "body": "Odaklı bir ilk sürüm geliştirip sizinle gözden geçiriyoruz. Çalışan yazılım, bir sonraki karar için ortak bir zemin oluşturuyor."},
                {"number": "03", "title": "İyileştirip teslim edelim", "body": "Önemli kullanım durumlarını deneyip eksikleri gideriyoruz. Dokümantasyon, bakım ve sonraki adımların kapsamını birlikte belirliyoruz."},
            ],
        },
        "company": {
            "eyebrow": "Hakkımızda",
            "title": "Bağımsız çalışıyoruz. Ayrıntılarla ilgileniyoruz.",
            "body": "Mevlana Yalçın, Ankara merkezli bir AI danışmanlığı ve ürün geliştirme girişimidir. Kurucu, Yankı'yı geliştirir; Claude kullanımı, entegrasyonu ve değerlendirmesi üzerine danışmanlık sunar. Görüşmeler doğrudan işin sorumluluğunu alan kişiyle yürütülür.",
            "facts": [
                {"label": "Merkez", "value": "Ankara, Türkiye"},
                {"label": "Kurucu", "value": "Mevlana Yalçın"},
                {"label": "Odak", "value": "AI danışmanlığı ve ürün geliştirme"},
                {"label": "Ürünümüz", "value": "Yankı · beta yayında"},
            ],
            "legal": "Mevlana Yalçın, bu bağımsız faaliyetin adıdır. Henüz ayrı bir tescilli tüzel kişilik bulunmamaktadır. Görüşmeler ve çalışma koşulları doğrudan kurucu tarafından yürütülür.",
            "dates": "mevlanayalcin.com.tr alan adı Eylül 2023'ten beri kurucuya aittir. Bu sitedeki danışmanlık hizmetleri ve Yankı'nın ürün geliştirme çalışmaları Ekim 2026'da başlamıştır. Alan adının tarihi, şirket tescil tarihi değildir.",
            "model_use": "Yankı, yansıtmaları üretmek için Anthropic API üzerinden Claude kullanır. Uygulama yanıt biçimini ve alıntıları denetler; kriz sözcükleri için ayrıca bir kural kontrolü uygular.",
        },
        "contact": {
            "eyebrow": "Aklınızda bir fikir mi var?",
            "title": "Bir sonraki adımı birlikte netleştirelim.",
            "body": "Ne üzerinde çalıştığınızı, nerede zorlandığınızı ve nasıl bir sonuç beklediğinizi anlatın. Gerisini birlikte şekillendirelim.",
            "cta": "İletişime geçin", "email": "info@mevlanayalcin.com.tr",
        },
        "footer": {
            "description": "AI danışmanlığı ve mühendislik. Yankı'nın geliştiricisi.",
            "location": "Ankara, Türkiye", "legal": "Kurumsal bilgiler",
            "privacy": "Gizlilik", "source": "Yankı kaynak kodu",
        },
        "privacy": {
            "eyebrow": "Gizlilik",
            "title": "Paylaştıklarınıza ne olduğunu bilin.",
            "intro": "Bu sayfa danışmanlık sitesini ve burada sunulan Yankı deneyimini kapsar.",
            "sections": [
                {"title": "İletişime geçtiğinizde", "body": "E-posta ile gönderdiğiniz bilgileri talebinize yanıt vermek ve olası çalışmayı görüşmek için kullanırız. Lütfen parola, özel anahtar veya hassas kişisel kayıt göndermeyin."},
                {"title": "Yankı'yı kullandığınızda", "body": "Yansıtma üretmek için yazdığınız metin bu sitenin hizmetinde işlenir ve Anthropic API'ye gönderilir. Uygulama, metni veya yanıtı bir günlük veritabanına kaydetmez. Anthropic ve barındırma sağlayıcısı verileri kendi hizmet koşulları kapsamında işler; bu, tüm sağlayıcıların hiçbir veri saklamadığı anlamına gelmez."},
                {"title": "Hizmetin korunması", "body": "Tekrarlanan istekleri sınırlamak için ağ adresiniz kullanılır. Günlük bütçeyi denetlemek için kullanım sayaçları tutulur. Bu işletim kayıtları, gönderdiğiniz metinden ayrıdır."},
                {"title": "Ürün güncellemeleri", "body": "Yankı bekleme listesine katılırsanız e-posta adresiniz, kayıt zamanı, dil ve kayıt kaynağı Cloudflare üzerinde saklanır. Kaydınızın silinmesi için bize ulaşabilirsiniz."},
                {"title": "Site altyapısı", "body": "Site Cloudflare üzerinde barındırılır ve korunur. Bu altyapı ağ ve istek bilgilerini işleyebilir. Sitenin uygulama kodunda reklam pikseli veya oturum kaydı aracı kullanmıyoruz."},
                {"title": "Sorular ve silme talepleri", "body": "Talebinizi info@mevlanayalcin.com.tr adresine gönderebilirsiniz. Bu siteden sorumlu iletişim kişisi Mevlana Yalçın'dır; Ankara, Türkiye."},
            ],
        },
        "yanki": {
            "eyebrow": "Mevlana Yalçın tarafından geliştirildi",
            "title": "Kendinize küçük bir düşünme alanı açın.",
            "body": "Bazı günleri anlamak, onları kelimelere dökünce kolaylaşır. Yankı yazdıklarınızı okuyarak kısa bir yansıtma, kendi metninizden bir cümle ve atabileceğiniz küçük bir adım sunar.",
            "status": "Beta yayında", "cta": "Bir yansıtma deneyin",
            "safety": "Yankı bir düşünme eşlikçisidir. Terapi, teşhis veya tıbbi tavsiye sunmaz; acil yardım hizmeti değildir. Acil tehlike durumunda bulunduğunuz yerin acil yardım hattını arayın: Türkiye'de 112.",
            "features": [
                {"title": "Kendi kelimelerinizle başlayın", "body": "Gününüzden bir anı ve size nasıl hissettirdiğini anlatın. Bunu yazmanın tek bir doğru yolu yok."},
                {"title": "Duyduklarına bir bakın", "body": "Yankı bir duygu önerir ve duyduğunu yansıtır. Yanılabilir; size neyin uyduğuna siz karar verirsiniz."},
                {"title": "Küçük bir adım seçin", "body": "Kısa bir mola, kendinize bir not veya bir sohbet gibi uygulanabilir bir adımı değerlendirin."},
            ],
            "input_label": "Aklınızdan neler geçiyor?",
            "input_placeholder": "Gününüzü ve size nasıl hissettirdiğini birkaç cümleyle yazın…",
            "input_button": "Yansıt", "loading": "Yazdıklarınız okunuyor…",
            "error": "Yankı bu yansıtmayı tamamlayamadı. Lütfen daha sonra yeniden deneyin.",
            "privacy_note": "Yanıt üretmek için metniniz Anthropic'e gönderilir. Uygulama günlük geçmişi kaydetmez. Kimliğinizi belirten veya hassas bilgiler paylaşmamaya özen gösterin.",
        },
        "labels": {
            "back": "Ana sayfaya dön", "learn_more": "Ayrıntıları incele", "external": "Harici site",
            "available": "Proje görüşmelerine açığız", "not_found_title": "Bu sayfa taşınmış olabilir.",
            "not_found_body": "Aradığınız sayfanın adresi değişmiş olabilir. Ana sayfadan devam edebilirsiniz.",
        },
    },
}

# ---------------------------------------------------------------------------
# Sonradan eklenen bolumler: fiyat cifpasi, denetim vaka calismasi, hizmet
# sartlari ve kimlik baglari. build.py bu anahtarlari varsa kullanir.
# ---------------------------------------------------------------------------
KIMLIK = {
    "github_profil": "https://github.com/mevlanayalcin",
    "linkedin": "https://www.linkedin.com/in/mevlanayalcin",
    "saat_dilimi": "Europe/Istanbul (UTC+3)",
    "yanit_suresi": {"en": "Replies within one business day", "tr": "Bir is gunu icinde yanit verilir"},
}

COPY["en"].update({
    "prices": {
        "label": "Starting point",
        "retainer": "Advisory retainer: from $1,200 / month (about two working days).",
        "note": ("Prices are starting points for a fixed-scope engagement and exclude taxes. You get a written "
                 "quote before any work starts; it does not change without an agreed change of scope."),
        "items": {
            "01": "1–2 weeks · from $2,500",
            "02": "2–6 weeks · from $6,000",
            "03": "5–10 working days · from $4,500",
        },
    },
    "audit": {
        "eyebrow": "Case study",
        "title": "Auditing a live LLM marketplace from the buyer's seat",
        "body": ("A public inference exchange promises the lowest price for every prompt and routes requests "
                 "between competing suppliers. We spent two days and about $400 of signup credit testing what "
                 "the service actually does for a buyer, using only what a customer can see."),
        "method_title": "How it was done",
        "method": [
            "Signed up programmatically for 20 accounts, one residential exit IP each, and instrumented the "
            "service from those keys.",
            "Measured behaviour, not documentation: request bodies, receipts, timing, cache headers and the "
            "endpoints the web console itself calls.",
            "Sent controlled inputs (including URL-fetching fields with out-of-band canaries) to see what the "
            "service touches on our behalf.",
            "Where a request failed, the API's own validation errors were used to recover the real field names.",
        ],
        "findings_title": "Nine findings worth paying for",
        "findings": [
            {"title": "Blind server-side request forgery", "body":
                "A URL field fetched our canary from two unrelated cloud networks, with a generic Go HTTP "
                "client and no sign of an allow-list. Internal endpoints are reachable in principle."},
            {"title": "A timing oracle on the same field", "body":
                "Refused, answered and filtered inputs returned in about 2.5, 3.9 and 12.5 seconds. Three "
                "distinct timings, reproducible, tell an observer which path a URL took."},
            {"title": "Deterministic failure on image responses", "body":
                "One response shape produced the same 502 with an undecodable body every time, so the fault "
                "sits in the platform's handling rather than in model randomness."},
            {"title": "Cache hits are free and shared across keys", "body":
                "A cached answer served to a different account's key, and the hit did not draw down credit. "
                "Good for repeated prompts; worth knowing if you expect isolation between keys."},
            {"title": "Failures cost nothing; SLA credit was unreachable", "body":
                "Failed jobs were never billed. Across 600+ observed jobs, every one was recorded as meeting "
                "its service promise, so the advertised service credit never triggered."},
            {"title": "One supplier holds the market", "body":
                "A single seller accounted for roughly 98% of offers (773 of 786) and 1,882 lifetime jobs, "
                "against 379, 267, 54, 49 and 1 for everyone else. Price competition is nominal today."},
            {"title": "Referral reward is on fees, not spend", "body":
                "The referral pays 20% of the platform's fee, which works out near 1% of what your referee "
                "spends. Materially different from how these programmes are usually read."},
            {"title": "Frontier models depend on supplier admission", "body":
                "Dated model snapshots served; alias and 'latest' identifiers returned supplier-side failures. "
                "Nineteen request shapes across three surfaces behaved the same way, which places the limit "
                "with the supplier, not the client. Re-testing on 8 October reversed the pattern "
                "outright: undated names served and the dated snapshots returned 404. Availability "
                "tracks admission, and a price bound (`x-liquid-cap-usd`) is what makes the "
                "automatic selection work at all."},
            {"title": "The useful endpoints are undocumented", "body":
                "Quotes, receipts, balance and throughput routes were found in the shipped bundle, not the "
                "manual; provider applications could be filed by API but key creation stayed gated behind "
                "human admission."},
        ],
        "outcome_title": "What the client got",
        "outcome": ("A written report with reproduction steps for every finding, a latency and cost baseline "
                    "for the models they actually use, and three decisions they could make: which models to "
                    "pin, where to keep a fallback supplier, and what to ask the platform in writing."),
        "cta": "Discuss an audit like this",
        "evidence_note": ("Measurements were taken in October 2026 against the production service. A live "
                          "platform changes under you; the report is dated for that reason."),
    },
    "terms": {
        "eyebrow": "Working together",
        "title": "Terms of engagement",
        "body": ("Short on purpose. These are the points we would otherwise end up discussing twice."),
        "sections": [
            {"title": "Scope and quotes", "body":
                "Every engagement starts from a written scope: what is examined or built, what is delivered, "
                "and what is explicitly not included. Prices shown on this site are starting points and "
                "exclude taxes. A quote is valid for 30 days and does not change unless the scope changes."},
            {"title": "Invoicing and payment", "body":
                "Bank transfer or card, invoices due within 15 days. Work above $5,000 starts after half the "
                "fee. This practice invoices as a sole proprietorship, opened with the first paid engagement; "
                "that is stated here rather than discovered later."},
            {"title": "Cancellation", "body":
                "Either side can stop an engagement at any time. Work completed up to that point is billed, "
                "and any unused part of a retainer is not. A retainer ends on 30 days' notice."},
            {"title": "Ownership", "body":
                "Deliverables belong to the client once paid for. Methods, scripts and checklists written "
                "before or alongside the engagement stay with us and are licensed to you for use."},
            {"title": "Confidentiality and data", "body":
                "Client material stays with us; we sign an NDA on request. Personal data is processed only to "
                "answer you and to invoice you, as described in the privacy notice, under Türkiye's KVKK."},
            {"title": "What we do not claim", "body":
                "We do not give legal or tax advice, and an audit does not certify a vendor. Findings come "
                "with the measurements and the date they were taken, so you can check them."},
            {"title": "Governing law", "body":
                "Engagements are governed by the law of Türkiye, with Istanbul courts for disputes."},
        ],
        "cta": "Ask about terms before you commit",
    },
})

COPY["tr"].update({
    "prices": {
        "label": "Başlangıç",
        "retainer": "Danışmanlık aboneliği: ayda 1.200 $'dan (yaklaşık iki iş günü).",
        "note": ("Fiyatlar, kapsamı belli bir iş için başlangıç noktalarıdır ve vergiler hariçtir. İş "
                 "başlamadan yazılı teklif verilir; kapsam değişmedikçe teklif değişmez."),
        "items": {
            "01": "1–2 hafta · 2.500 $'dan",
            "02": "2–6 hafta · 6.000 $'dan",
            "03": "5–10 iş günü · 4.500 $'dan",
        },
    },
    "audit": {
        "eyebrow": "Vaka çalışması",
        "title": "Canlı bir LLM pazar yerini alıcı tarafında denetlemek",
        "body": ("Herkese açık bir çıkarım pazarı, her istek için en düşük fiyatı vaat ediyor ve istekleri "
                 "birbirine rakip tedarikçiler arasında dağıtıyor. İki gün ve yaklaşık 400 $ kayıt kredisi "
                 "harayarak, müşterinin görebildiği araçlarla hizmetin gerçekte ne yaptığını ölçtük."),
        "method_title": "Nasıl yapıldı",
        "method": [
            "Programatik olarak 20 hesap açıldı; her biri farklı bir ev çıkış IP'si aldı ve ölçümler bu "
            "anahtarlardan yapıldı.",
            "Belge değil davranış ölçüldü: istek gövdeleri, fişler, süreler, önbellek başlıkları ve web "
            "konsolunun kendisinin çağırdığı uçlar.",
            "Kontrollü girdiler gönderildi (URL çeken alanlara dışarıdan iz sürücü işaretler bırakıldı) ki "
            "hizmetin bizim adımıza neye dokunduğu görülsün.",
            "İstekler başarısız olduğunda, API'nin kendi doğrulama hatalarından gerçek alan adları geri "
            "okundu.",
        ],
        "findings_title": "Paraya değecek dokuz bulgu",
        "findings": [
            {"title": "Kör sunucu-taraflı istek sahteciliği (SSRF)", "body":
                "Bir URL alanı, işaretimizi birbirinden bağımsız iki bulut ağından çekti; jenerik bir Go HTTP "
                "istemcisi ve bir izin listesi izi yoktu. Prensipte iç uçlara erişilebiliyor."},
            {"title": "Aynı alanda zamanlama fâli", "body":
                "Reddedilen, yanıtlanan ve süzülen girdiler sırasıyla ~2,5, ~3,9 ve ~12,5 saniye sürdü. "
                "Üretilabilir üç ayrı süre, URL'nin hangi yoldan geçtiğini söylüyor."},
            {"title": "Görsel yanıtlarda belirgin arıza", "body":
                "Bir yanıt biçimi her seferinde aynı 502'yi ve çözülemeyen bir gövdeyi üretti; arıza modelin "
                "rastgeleliğinde değil, platformun işleyişinde."},
            {"title": "Önbellek isabetleri ücretsiz ve hesaplar arası", "body":
                "Önbellekten dönen yanıt başka bir hesabın anahtarına servis edildi ve kredi düşürmedi. "
                "Tekrarlanan isteklerde iyi; anahtarlar arası yalıtım bekliyorsanız bilinmesi gereken bir şey."},
            {"title": "Başarısız iş ücretsiz; SLA kredisine ulaşılamıyor", "body":
                "Başarısız işlerden hiç ücret alınmadı. Gözlemlenen 600+ işin tamamı 'sözleşme karşılandı' "
                "kayıtlıydı; vaat edilen hizmet kredisi bir kez bile işlemadı."},
            {"title": "Pazarı tek satıcı tutuyor", "body":
                "Tek satıcı tekliflerin ~%98'ine (786'da 773) ve 1.882 ömür boyu işe sahipti; diğerleri "
                "379, 267, 54, 49 ve 1 işte kaldı. Fiyat rekabeti bugün için göstermelik."},
            {"title": "Yönlendirme ödeli harcama üzerinden değil", "body":
                "Yönlendirme, platform komisyonunun %20'si; bu da yönlendirilen kişinin harcadığının kabaca "
                "%1'i. Bu, programların genellikle okunduğu şeyden önemli ölçüde farklı."},
            {"title": "Sınır modelleri tedarikçi kabulüne bağlı", "body":
                "Tarihli model anlık görüntüleri servis edildi; taahhüt adı ve 'latest' biçimleri tedarikçi "
                "tarafı hataları döndü. Üç arayüzde 19 istek biçimi aynı sonucu verdi: sınır müşteride değil. 8 Ekim'deki yeniden testte desen tümüyle tersine döndü: tarihli anlık görüntüler 404 verir, tarihsiz adlar servis edilir. Yani sınır kabul ve arz meselesi; otomatik seçimin çalışması ayrıca bir fiyatsınırına (`x-liquid-cap-usd`) bağlı."},
            {"title": "İşe yarayan uçlar dokümante değil", "body":
                "Teklif, fiş, bakiye ve verim uçları kılavuzda değil paketlenmiş uygulamada bulundu; tedarikçi "
                "başvurusu API ile yapılabiliyor ama anahtar üretimi insan kabulüne kadar kilitli."},
        ],
        "outcome_title": "Karşılığında ne çıktı",
        "outcome": ("Her bulgu için yineleneme adımları içeren yazılı bir rapor, müşterinin gerçekte kullandığı "
                    "modeller için gecikme ve maliyet çizgisi, ve alabilecekleri üç karar: hangi modellere "
                    "bağlanılacağı, nerede yedek tedarikçi tutulacağı ve platformdan yazılı olarak ne "
                    "isteneceği."),
        "cta": "Benzer bir denetimi konuşun",
        "evidence_note": ("Ölçümler Ekim 2026'da canlı hizmete karşı alındı. Canlı bir platform siz ölçerken "
                          "değişir; rapor bu yüzden tarih taşır."),
    },
    "terms": {
        "eyebrow": "Çalışma biçimi",
        "title": "Hizmet şartları",
        "body": "Kasıtlı olarak kısa. Aksi hâlde iki kez konuşacağımız maddeler.",
        "sections": [
            {"title": "Kapsam ve teklif", "body":
                "Her iş yazılı kapsamla başlar: neyin inceleneceği veya üretileceği, neyin teslim edileceği "
                "ve neyin açıkça dışarıda kaldığı. Sitedeki fiyatlar başlangıç noktalarıdır, vergiler "
                "hariçtir. Teklif 30 gün geçerlidir; kapsam değişmedikçe teklif değişmez."},
            {"title": "Faturalama ve ödeme", "body":
                "Havale/EFT veya kart; faturalar 15 gün içinde ödenir. 5.000 $ üzeri işler ücretin yarısı "
                "alındıktan sonra başlar. Bu pratik, ilk ücretli işle birlikte kurulacak bir şahıs şirketi "
                "olarak fatura keser; bu burada yazılır, sonra sürpriz olmaz."},
            {"title": "Fesih", "body":
                "İş, her iki tarafça herhangi bir zamanda durdurulabilir. O ana kadar yapılan iş faturalanır; "
                "aboneliğin kullanılmayan kısmı faturalanmaz. Abonelik 30 gün önceki bildirimle biter."},
            {"title": "Fikri haklar", "body":
                "Ödeme yapıldığında teslim edilen iş müşteriye aittir. Önceden yazılmış yöntemler, betikler "
                "ve kontrol listeleri bizde kalır ve kullanım için size lisanslanır."},
            {"title": "Gizlilik ve veri", "body":
                "Müşteri materyali bizde kalır; istenirse gizlilik sözleşmesi imzalanır. Kişisel veri yalnızca "
                "yanıt vermek ve faturalandırmak için işlenir; Türkiye'nin KVKK kapsamındadır."},
            {"title": "Ne vaad etmiyoruz", "body":
                "Hukuk veya vergi tavsiyesi vermeyiz; bir denetim tedarikçiyi sertifikalandırmaz. Bulgular "
                "ölçümleri ve tarihiyle birlikte gelir, böylece siz de kontrol edebilirsiniz."},
            {"title": "Uygulanacak hukuk", "body":
                "İşler Türkiye hukukuna tabidir; uyuşmazlıklarda İstanbul mahkemeleri yetkilidir."},
        ],
        "cta": "Karar vermeden önce şartları sorun",
    },
})

# Yeni sayfalarin menü/etiket adlari (title ve footer bunlari kullanir)
COPY["en"]["nav"].update({"audit": "Audit case study", "terms": "Terms of engagement"})
COPY["tr"]["nav"].update({"audit": "Denetim vakası", "terms": "Hizmet şartları"})
