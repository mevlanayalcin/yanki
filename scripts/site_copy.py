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


# Public contact details and service process. Commercial terms are agreed per engagement.
COPY["en"]["contact_page"] = {
    "eyebrow": "Contact", "title": "A direct conversation about your next step.",
    "body": "For a consulting project, product feedback or a question about Yankı, get in touch with Mevlana Yalçın directly.",
    "email_label": "Business enquiries", "founder_label": "Your point of contact",
    "timezone_label": "Based in", "timezone": "Ankara, Türkiye · UTC+3",
    "write_title": "What to include", "write_body": "Tell us about your workflow, the problem you want to solve and your intended timeline. For product feedback, describe what happened without sharing private journal text.",
    "next_title": "What happens next", "next_body": "The founder handles enquiries personally. We discuss the scope and next steps before deciding on an engagement.",
    "cta": "Email Mevlana", "profile": "GitHub profile", "linkedin": "Professional background",
    "source": "Yankı source code", "terms_link": "How an engagement starts"
}
COPY["tr"]["contact_page"] = {
    "eyebrow": "İletişim", "title": "Bir sonraki adımınızı konuşalım.",
    "body": "Bir danışmanlık projesi, ürün geri bildirimi veya Yankı hakkında sorularınız için doğrudan Mevlana Yalçın'a ulaşın.",
    "email_label": "İş görüşmeleri", "founder_label": "İletişim kişiniz",
    "timezone_label": "Merkez", "timezone": "Ankara, Türkiye · UTC+3",
    "write_title": "Nelerden söz edebilirsiniz?", "write_body": "İş akışınızı, çözmek istediğiniz sorunu ve düşündüğünüz takvimi anlatın. Ürün geri bildirimi için özel günlük metninizi paylaşmadan karşılaştığınız durumu açıklayın.",
    "next_title": "Sonraki adım", "next_body": "Görüşmeleri kurucu yürütür. Çalışmaya karar vermeden önce kapsam ve sonraki adımlar birlikte netleştirilir.",
    "cta": "Mevlana'ya yazın", "profile": "GitHub profili", "linkedin": "Profesyonel geçmiş",
    "source": "Yankı kaynak kodu", "terms_link": "Çalışmaya nasıl başlanır?"
}
COPY["en"]["terms"] = {
    "eyebrow": "Working together", "title": "How an engagement starts.",
    "body": "The website describes the services we offer. The details of a specific project are agreed directly with the founder.",
    "sections": [
        {"title": "Define the work", "body": "We discuss the problem, the available inputs and the intended outcome. A written scope identifies the work and deliverables before an engagement begins."},
        {"title": "Agree the commercial details", "body": "The quote and agreement set out the price, payment arrangements, timeline, responsibilities, cancellation and ownership provisions for that engagement. The site does not collect payment or create a subscription."},
        {"title": "Using the Yankı beta", "body": "Yankı is available to try without an account. It is a reflection tool, not therapy, diagnosis, medical advice or an emergency service. Responses can be wrong and the beta can be unavailable. Read the product and privacy pages before entering text."},
        {"title": "Questions", "body": "Contact info@mevlanayalcin.com.tr to discuss the scope or ask about the service before agreeing to any work."},
    ], "cta": "Discuss a project"
}
COPY["tr"]["terms"] = {
    "eyebrow": "Birlikte çalışmak", "title": "Çalışmaya nasıl başlanır?",
    "body": "Site, sunduğumuz hizmetleri tanıtır. Belirli bir projenin ayrıntıları doğrudan kurucuyla görüşülerek kararlaştırılır.",
    "sections": [
        {"title": "Kapsamın belirlenmesi", "body": "Sorunu, kullanılabilecek girdileri ve beklenen sonucu konuşuruz. Çalışma başlamadan önce yapılacak iş ve teslimatlar yazılı kapsamda belirlenir."},
        {"title": "Ticari ayrıntıların kararlaştırılması", "body": "Ücret, ödeme düzeni, takvim, sorumluluklar, iptal ve fikri haklara ilişkin koşullar ilgili işin teklifinde ve sözleşmesinde belirlenir. Site üzerinden ödeme alınmaz veya abonelik başlatılmaz."},
        {"title": "Yankı betasının kullanımı", "body": "Yankı, hesap açmadan denenebilir. Bir düşünme aracıdır; terapi, teşhis, tıbbi tavsiye veya acil yardım hizmeti değildir. Yanıtlar hatalı olabilir ve beta hizmeti zaman zaman kullanılamayabilir. Metin girmeden önce ürün ve gizlilik sayfalarını inceleyin."},
        {"title": "Sorular", "body": "Çalışmaya karar vermeden önce kapsamı görüşmek veya hizmet hakkında soru sormak için info@mevlanayalcin.com.tr adresine ulaşabilirsiniz."},
    ], "cta": "Projenizi konuşalım"
}
COPY["en"]["nav"].update({"contact": "Contact", "terms": "Working together"})
COPY["tr"]["nav"].update({"contact": "İletişim", "terms": "Çalışma koşulları"})
