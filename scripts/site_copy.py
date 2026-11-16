"""Public-facing copy for the consulting site, in English and Turkish.

All values are plain text. Business registration, domain ownership and product
development dates are kept separate.
"""

COPY = {
    "en": {
        "meta": {
            "title": "Mevlana Yalçın — Yankı Grounding Engine & AI Engineering",
            "description": "AI product studio and consultancy in Ankara. Creators of Yankı (MIT): deterministic multilingual LLM quote-grounding, RAG citation verification, and live Claude reflection.",
        },
        "nav": {
            "services": "Expertise", "products": "Yankı", "approach": "Approach",
            "company": "About", "contact": "Let's talk", "language": "TR",
        },
        "hero": {
            "eyebrow": "AI product engineering, verification & consulting",
            "title": "Grounded AI.",
            "title_accent": "Verified in code.",
            "body": "We build Yankı: an open-source (MIT) multilingual quote-grounding, pre-inference safety gating and multi-source RAG citation verification engine, paired with a live zero-retention reflection sandbox on Claude.",
            "primary": "Explore Yankı & live demo", "secondary": "Verification architecture",
            "note": "Founded and led by Mevlana Yalçın · Open-source Python engine (v0.2.0) & AI consultancy · Ankara, Türkiye.",
        },
        "intro": {
            "eyebrow": "Engineering informed by production",
            "title": "Deterministic checks around probabilistic models.",
            "body": "Language models paraphrase, hallucinate citations and mishandle Unicode offsets in morphologically rich languages like Turkish. Yankı solves this in deterministic code—verifying exact character spans, stripping fabricated quotes and gating crisis inputs before inference—and shapes how we engineer AI systems for clients.",
        },
        "services": {
            "eyebrow": "Expertise",
            "title": "From a clear question to a verified system.",
            "body": "A focused engagement, with measurable evaluation harnesses and direct access to the engineer doing the work.",
            "items": [
                {"number": "01", "title": "LLM & Claude architecture", "body": "Define where frontier or open-weight models belong in your stack, establish latency and token budgets, and design deterministic verification boundaries around model outputs.", "tags": ["System architecture", "Claude & vLLM", "Delivery planning"]},
                {"number": "02", "title": "Grounded RAG & product integration", "body": "Connect models to retrieval pipelines and user-facing products with character-level citation provenance, strict JSON schema contracts and resilient fallback handling.", "tags": ["Quote grounding", "Multi-source RAG", "Product engineering"]},
                {"number": "03", "title": "Evaluation, safety & GPU benchmarking", "body": "Audit live inference behaviour across providers, measure hallucination and citation drift on golden test suites, and benchmark throughput versus cost before scaling.", "tags": ["Golden eval suites", "Safety guardrails", "Throughput & cost"]},
            ],
        },
        "products": {
            "eyebrow": "Product & open-source engine",
            "title": "Meet Yankı.",
            "body": "One architecture, two surfaces: a zero-retention daily reflection sandbox running at the edge with Claude, and an open-source Python verification package (MIT) for deterministic quote-grounding and multi-source RAG citation audits.",
            "items": [
                {"slug": "yanki", "name": "Yankı Sandbox", "category": "Live edge application · Claude API", "status": "Live beta", "title": "Zero-retention reflection with verified quotes.", "body": "Write a few sentences in English or Turkish. Yankı runs a pre-inference crisis rule gate, requests structured JSON from Claude, and verifies every quoted span character-for-character before rendering.", "cta": "Try live sandbox", "href": "/work/yanki/", "detail": "A reflective companion, not therapy or medical advice."},
                {"slug": "yanki-engine", "name": "yanki 0.2.0", "category": "Open-source Python package · MIT", "status": "24/24 eval passing", "title": "Multilingual quote-grounding & RAG citation engine.", "body": "Index-preserving Turkish İ/ı & Unicode offset mapping, multi-document RAG span verification, <think>-aware strict JSON contracts, and Slurm/Apptainer multi-GPU vLLM evaluation recipes.", "cta": "Inspect architecture & source", "href": "/work/yanki/#engine", "detail": "pip install -e . · Python 3.11+ · Zero heavy runtime dependencies."},
            ],
        },
        "claude": {
            "eyebrow": "Verification in practice",
            "title": "Every model claim checked before it reaches the user.",
            "body": "Whether calling Anthropic's API at the edge or evaluating open-weight models on vLLM and SGLang clusters, Yankı enforces three deterministic boundaries in application code.",
            "items": [
                {"title": "Index-preserving span provenance", "body": "Standard Unicode case-folding expands characters like Turkish 'İ' (U+0130) and corrupts character offsets. Yankı maps every folded codepoint 1-to-1 back to its exact [start_char, end_char) slice in the source document."},
                {"title": "Pre-inference safety & schema contracts", "body": "High-risk crisis phrases short-circuit deterministically in sub-millisecond rule code without calling an LLM. Model responses strip reasoning <think> blocks and must satisfy strict typed JSON bounds or fail closed."},
                {"title": "Multi-source RAG & CI benchmarks", "body": "verify_multi_source_citations audits retrieved chunks against cited document IDs, stripping fabricated or cross-contaminated quotes. Shipped with a 24-case TR/EN adversarial benchmark suite and GitHub Actions CI."},
            ],
            "cta": "Open Yankı & benchmarks", "source_label": "View GitHub repository (MIT)",
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
            "body": "Mevlana Yalçın is a founder-led AI product engineering studio and consultancy based in Ankara, Türkiye. We build Yankı—an open-source (MIT) multilingual quote-grounding and RAG citation verification engine paired with a live edge reflection sandbox—and help engineering teams integrate, verify and benchmark LLM systems.",
            "facts": [
                {"label": "Based in", "value": "Ankara, Türkiye"},
                {"label": "Led by", "value": "Mevlana Yalçın"},
                {"label": "Focus", "value": "AI verification, RAG grounding & engineering"},
                {"label": "Open source & live", "value": "Yankı v0.2.0 (MIT) · live beta"},
            ],
            "legal": "Mevlana Yalçın operates this AI consulting and product development business. Enquiries and engagement terms are handled directly by the founder.",
            "dates": "The business was registered in November 2023. The founder has held mevlanayalcin.com.tr since September 2023. Product and verification engine work on Yankı began in October 2026.",
            "model_use": "Yankı calls Anthropic's Messages API at the edge and supports vLLM, SGLang and OpenAI-compatible runtimes in its open-source Python evaluation harness, enforcing deterministic pre-inference crisis gates, strict JSON contracts and character-level quote provenance.",
        },
        "contact": {
            "eyebrow": "Have something in mind?",
            "title": "Let's give your next idea a clear direction.",
            "body": "Tell us what you are working on, what is getting in the way and what a useful outcome would look like. We'll take it from there.",
            "cta": "Start a conversation", "email": "info@mevlanayalcin.com.tr",
        },
        "footer": {
            "description": "AI verification engineering & consultancy. Creators of Yankı (MIT).",
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
            "eyebrow": "Open-source engine (MIT) & live edge sandbox",
            "title": "Deterministic quote-grounding and live reflection.",
            "body": "Yankı combines a zero-retention bilingual reflection companion at the edge with an open-source Python verification engine (yanki 0.2.0) that enforces index-preserving Turkish/English quote provenance, pre-inference crisis gating, and multi-source RAG citation audits.",
            "status": "v0.2.0 · Live beta", "cta": "Live zero-retention sandbox",
            "safety": "Yankı is a reflective companion and verification showcase. It is not therapy, diagnosis or medical advice, and is not an emergency service. High-risk crisis wording short-circuits deterministically before any LLM call; if you are in immediate danger, contact local emergency services (112 in Türkiye).",
            "features": [
                {"title": "01 · Pre-inference deterministic safety gate", "body": "Before any network call to an LLM, normalized Turkish and English crisis rules execute locally in sub-millisecond code and short-circuit high-risk inputs safely."},
                {"title": "02 · Strict JSON & reasoning-tag parser", "body": "Claude (edge) or vLLM/SGLang (cluster) generates a bounded JSON reflection; reasoning <think> blocks and malformed schemas fail closed instead of leaking raw model output."},
                {"title": "03 · Character-exact quote provenance", "body": "The quoted phrase ('alinti') must match a contiguous character span in your original passage under index-preserving Unicode folding—paraphrased or fabricated quotes are stripped."},
            ],
            "input_label": "Try the live verification pipeline (English or Turkish)",
            "input_placeholder": "Write a few sentences about your day and how it felt—watch Yankı extract an exact grounded quote…",
            "input_button": "Run grounded reflection", "loading": "Checking guardrails & verifying quote span…",
            "error": "Yankı couldn't complete this reflection. Please try again later.",
            "privacy_note": "Processed transiently via Cloudflare Workers + Anthropic API; no journal database is stored. Avoid sharing identifying or sensitive personal records.",
        },
        "labels": {
            "back": "Back to home", "learn_more": "Learn more", "external": "External site",
            "available": "Open to project enquiries", "not_found_title": "This page could not be found.",
            "not_found_body": "The address may have changed. Head back to the home page to find what you need.",
        },
    },
    "tr": {
        "meta": {
            "title": "Mevlana Yalçın — Yankı Doğrulama Motoru ve AI Mühendisliği",
            "description": "Ankara merkezli AI ürün geliştirme ve mühendislik stüdyosu. Açık kaynaklı (MIT) çok dilli LLM alıntı doğrulama, RAG kaynak denetimi ve canlı yansıtma motoru Yankı'yı geliştiriyoruz.",
        },
        "nav": {
            "services": "Uzmanlık", "products": "Yankı", "approach": "Yaklaşım",
            "company": "Hakkımızda", "contact": "Konuşalım", "language": "EN",
        },
        "hero": {
            "eyebrow": "AI ürün mühendisliği, doğrulama ve danışmanlık",
            "title": "Denetlenebilir AI.",
            "title_accent": "Kodla doğrulanan.",
            "body": "Açık kaynaklı (MIT) çok dilli alıntı doğrulama (quote-grounding), çıkarım öncesi güvenlik kapısı ve çok kaynaklı RAG atıf denetimi motoru Yankı'yı ve Claude tabanlı sıfır-kayıtlı canlı deneme ortamını geliştiriyoruz.",
            "primary": "Yankı’yı ve canlı demoyu açın", "secondary": "Doğrulama mimarisi",
            "note": "Mevlana Yalçın tarafından kuruldu · Açık kaynak Python motoru (v0.2.0) ve AI danışmanlığı · Ankara.",
        },
        "intro": {
            "eyebrow": "Üretimden beslenen mühendislik",
            "title": "Olasılıksal modellerin etrafında deterministik sınırlar.",
            "body": "Dil modelleri alıntıları yeniden yazar, olmayan kaynaklara atıf üretir ve Türkçe İ/ı gibi Unicode dönüşümlerinde karakter indislerini kaydırır. Yankı bu sorunları deterministik kod katmanında çözer; danışmanlık projelerimizde de aynı doğrulanabilir mimariyi kurarız.",
        },
        "services": {
            "eyebrow": "Uzmanlık",
            "title": "Doğru sorudan doğrulanmış bir sisteme.",
            "body": "Ölçülebilir değerlendirme testleri ve işi doğrudan geliştiren mühendisle birebir çalışma.",
            "items": [
                {"number": "01", "title": "LLM ve Claude sistem mimarisi", "body": "Sınır (frontier) veya açık ağırlıklı modellerin iş akışınızdaki yerini, gecikme/bütçe sınırlarını ve model çıktısını denetleyen deterministik doğrulama katmanlarını tasarlayalım.", "tags": ["Sistem mimarisi", "Claude ve vLLM", "Uygulama planı"]},
                {"number": "02", "title": "Doğrulanmış RAG ve ürün entegrasyonu", "body": "Modelleri karakter düzeyinde kaynak kanıtı (citation provenance), katı JSON şema sözleşmeleri ve güvenli hata yakalama katmanlarıyla ürününüze bağlayalım.", "tags": ["Alıntı doğrulama", "Çok kaynaklı RAG", "Ürün mühendisliği"]},
                {"number": "03", "title": "Değerlendirme, güvenlik ve GPU kıyaslama", "body": "Canlı çıkarım davranışını sağlayıcılar genelinde denetleyelim; altın test kümeleriyle halüsinasyon oranını, yanıt süresini ve GPU/API maliyetini ölçelim.", "tags": ["Altın test kümeleri", "Güvenlik kapıları", "Performans ve maliyet"]},
            ],
        },
        "products": {
            "eyebrow": "Ürün ve açık kaynak motoru",
            "title": "Yankı ile tanışın.",
            "body": "Tek mimari, iki yüzey: uçta (edge) Claude ile çalışan sıfır-kayıtlı canlı yansıtma deneme alanı ve deterministik alıntı/RAG kaynak doğrulaması için açık kaynaklı (MIT) Python paketi.",
            "items": [
                {"slug": "yanki", "name": "Yankı Canlı Ortam", "category": "Uç uygulama · Claude API", "status": "Beta yayında", "title": "Doğrulanmış alıntılarla sıfır-kayıtlı yansıtma.", "body": "Türkçe veya İngilizce birkaç cümle yazın. Yankı çıkarım öncesi kriz kuralını çalıştırır, Claude'dan yapılandırılmış JSON alır ve alıntıyı metninizle karakter karakter doğrulayarak gösterir.", "cta": "Canlı ortamı deneyin", "href": "/tr/calismalar/yanki/", "detail": "Bir düşünme eşlikçisidir; terapi veya tıbbi tavsiye değildir."},
                {"slug": "yanki-engine", "name": "yanki 0.2.0", "category": "Açık kaynak Python paketi · MIT", "status": "24/24 test geçti", "title": "Çok dilli alıntı doğrulama ve RAG atıf motoru.", "body": "İndis koruyan Türkçe İ/ı ve Unicode normalizasyonu, çok belgeli RAG karakter aralığı doğrulaması, <think> ayıklayan katı JSON şeması ve Slurm/Apptainer vLLM kıyaslama betikleri.", "cta": "Mimariyi ve kodu inceleyin", "href": "/tr/calismalar/yanki/#engine", "detail": "pip install -e . · Python 3.11+ · Ek çalışma zamanı bağımlılığı yok."},
            ],
        },
        "claude": {
            "eyebrow": "Uygulamada doğrulama",
            "title": "Modelin her iddiası kullanıcıya ulaşmadan denetlenir.",
            "body": "İster uçta Anthropic API çağrılsın ister vLLM ve SGLang kümelerinde açık ağırlıklı modeller çalıştırılsın, Yankı uygulama kodunda üç deterministik sınır uygular.",
            "items": [
                {"title": "İndis koruyan karakter aralığı kanıtı", "body": "Standart Unicode küçük harfe çevirme işlemi Türkçe 'İ' (U+0130) karakterini genişleterek karakter ofsetlerini bozar. Yankı her karakteri kaynak metindeki [start_char, end_char) aralığına birebir eşler."},
                {"title": "Çıkarım öncesi güvenlik ve katı şema", "body": "Yüksek riskli kriz ifadeleri modele hiç gitmeden milisaniye altı kural koduyla yakalanır. Model yanıtlarındaki <think> blokları ayıklanır ve katı JSON şemasına uymayan yanıtlar reddedilir."},
                {"title": "Çok kaynaklı RAG ve CI kıyaslama", "body": "verify_multi_source_citations, getirilen belge parçalarını kaynak kimlikleriyle denetler; uydurma alıntıları temizler. 24 vakalık TR/EN test paketi ve GitHub Actions CI ile doğrulanır."},
            ],
            "cta": "Yankı’yı ve testleri açın", "source_label": "GitHub deposunu inceleyin (MIT)",
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
            "body": "Mevlana Yalçın, Ankara merkezli kurucu liderliğinde bir AI ürün mühendisliği stüdyosu ve danışmanlık girişimidir. Açık kaynaklı (MIT) çok dilli alıntı doğrulama ve RAG atıf denetim motoru Yankı'yı geliştirir; mühendislik ekiplerine LLM entegrasyonu, doğrulama ve kıyaslama danışmanlığı sunar.",
            "facts": [
                {"label": "Merkez", "value": "Ankara, Türkiye"},
                {"label": "Kurucu", "value": "Mevlana Yalçın"},
                {"label": "Odak", "value": "AI doğrulama, RAG grounding ve mühendislik"},
                {"label": "Açık kaynak ve canlı", "value": "Yankı v0.2.0 (MIT) · beta yayında"},
            ],
            "legal": "Mevlana Yalçın, bu AI danışmanlığı ve ürün geliştirme işletmesini yürütür. Görüşmeler ve çalışma koşulları doğrudan kurucu tarafından belirlenir.",
            "dates": "İşletme Kasım 2023'te tescil edilmiştir. mevlanayalcin.com.tr alan adı Eylül 2023'ten beri kurucuya aittir. Yankı ürün ve doğrulama motoru çalışmaları Ekim 2026'da başlamıştır.",
            "model_use": "Yankı uçta Anthropic Messages API üzerinden Claude kullanır; açık kaynak Python değerlendirme paketinde ise vLLM, SGLang ve OpenAI uyumlu çalışma zamanlarını destekleyerek çıkarım öncesi kriz kapısı, katı JSON şeması ve karakter düzeyinde alıntı doğrulaması uygular.",
        },
        "contact": {
            "eyebrow": "Aklınızda bir fikir mi var?",
            "title": "Bir sonraki adımı birlikte netleştirelim.",
            "body": "Ne üzerinde çalıştığınızı, nerede zorlandığınızı ve nasıl bir sonuç beklediğinizi anlatın. Gerisini birlikte şekillendirelim.",
            "cta": "İletişime geçin", "email": "info@mevlanayalcin.com.tr",
        },
        "footer": {
            "description": "AI doğrulama mühendisliği ve danışmanlık. Yankı (MIT) geliştiricisi.",
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
            "eyebrow": "Açık kaynak motor (MIT) ve canlı uç ortamı",
            "title": "Deterministik alıntı doğrulama ve canlı yansıtma.",
            "body": "Yankı, uçta çalışan sıfır-kayıtlı iki dilli yansıtma deneyimini; indis koruyan Türkçe/İngilizce alıntı kanıtı, çıkarım öncesi kriz kapısı ve çok kaynaklı RAG atıf denetimi sağlayan açık kaynaklı Python doğrulama motoruyla (yanki 0.2.0) birleştirir.",
            "status": "v0.2.0 · Beta yayında", "cta": "Canlı sıfır-kayıtlı deneme alanı",
            "safety": "Yankı bir düşünme eşlikçisi ve doğrulama vitrinidir; terapi, teşhis veya tıbbi tavsiye sunmaz. Yüksek riskli kriz ifadeleri model çağrılmadan önce deterministik kuralla durdurulur; acil tehlike durumunda 112'yi arayın.",
            "features": [
                {"title": "01 · Çıkarım öncesi deterministik güvenlik kapısı", "body": "Modele herhangi bir ağ çağrısı yapılmadan önce normalize edilmiş Türkçe ve İngilizce kriz kuralları milisaniye altında çalışır ve riskli girdileri güvenle durdurur."},
                {"title": "02 · Katı JSON şeması ve <think> ayıklayıcı", "body": "Claude (uçta) veya vLLM/SGLang (kümede) sınırlandırılmış JSON üretir; akıl yürütme blokları ayıklanır, bozuk şemalar ham metin sızdırmadan reddedilir."},
                {"title": "03 · Karakter düzeyinde alıntı kanıtı", "body": "Alıntılanan ifade ('alinti'), indis koruyan Unicode katlama altında kaynak metninizdeki kesintisiz bir karakter aralığıyla birebir eşleşmiyorsa otomatik olarak silinir."},
            ],
            "input_label": "Canlı doğrulama boru hattını deneyin (Türkçe veya İngilizce)",
            "input_placeholder": "Gününüzü ve nasıl hissettirdiğini birkaç cümleyle yazın—Yankı'nın birebir doğrulanmış alıntıyı nasıl çıkardığını görün…",
            "input_button": "Doğrulanmış yansıtma üret", "loading": "Güvenlik kapısı ve alıntı aralığı doğrulanıyor…",
            "error": "Yankı bu yansıtmayı tamamlayamadı. Lütfen daha sonra yeniden deneyin.",
            "privacy_note": "Cloudflare Workers + Anthropic API üzerinden geçici olarak işlenir; günlük veritabanı tutulmaz. Kimlik belirten veya hassas kişisel kayıt paylaşmayın.",
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

# ---------------------------------------------------------------------------
# Fiyat cifpasi ve denetim vaka calismasi (codex surumune geri eklendi)
# ---------------------------------------------------------------------------
COPY["en"].update({
    "prices": {
        "label": "Starting point",
        "retainer": "Advisory retainer: from $1,200 / month, about two working days.",
        "note": ("Prices are starting points for a fixed-scope engagement and exclude taxes. You get a "
                 "written quote before work starts; it does not change without an agreed change of scope."),
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
            "Opened twenty accounts programmatically, one residential exit IP each, and instrumented the "
            "service from the API keys those accounts issued.",
            "Measured behaviour rather than documentation: request bodies, receipts, timing, cache headers "
            "and the endpoints the web console itself calls.",
            "Sent controlled inputs, including out-of-band canaries in URL-fetching fields, to see what the "
            "service touches on a customer's behalf.",
            "Where a request failed, we read the API's own validation errors to recover the real field names.",
        ],
        "findings_title": "Nine findings worth paying for",
        "findings": [
            {"title": "Blind server-side request forgery", "body":
                "A URL field fetched our canary from two unrelated cloud networks, with a generic Go HTTP "
                "client and no sign of an allow-list. Internal endpoints are reachable in principle."},
            {"title": "A timing oracle on the same field", "body":
                "Refused, answered and filtered inputs returned in about 2.5, 3.9 and 12.5 seconds. Three "
                "reproducible timings tell an observer which path a URL took."},
            {"title": "Deterministic failure on image responses", "body":
                "One response shape produced the same 502 with an undecodable body every time, so the fault "
                "sits in the platform's handling rather than in model randomness."},
            {"title": "Cache hits are free and shared across keys", "body":
                "A cached answer served to a different account's key, and the hit drew down no credit. Good "
                "for repeated prompts; worth knowing if you expect isolation between keys."},
            {"title": "Failures cost nothing; SLA credit was unreachable", "body":
                "Failed jobs were never billed. Across 600+ observed jobs, every one was recorded as meeting "
                "its service promise, so the advertised service credit never triggered."},
            {"title": "One supplier holds the market", "body":
                "A single seller held roughly 98% of offers (773 of 786) and 1,882 lifetime jobs, against "
                "379, 267, 54, 49 and 1 for everyone else. Price competition is nominal today."},
            {"title": "Referral reward is on fees, not spend", "body":
                "The referral pays 20% of the platform's fee, near 1% of what your referee spends. "
                "Materially different from how these programmes are usually read."},
            {"title": "Frontier availability follows supply, not naming", "body":
                "On the first pass, dated model snapshots served while alias and 'latest' names failed "
                "identically across nineteen request shapes and three surfaces. Re-measured two weeks later "
                "the pattern inverted: undated names served and the dated snapshots returned 404. Automatic "
                "selection only runs at all once a price bound (`x-liquid-cap-usd`) is supplied."},
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
})

COPY["tr"].update({
    "prices": {
        "label": "Başlangıç",
        "retainer": "Danışmanlık aboneliği: ayda 1.200 $'dan, yaklaşık iki iş günü.",
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
        "body": ("Herkese açık bir çıkarım pazarı her istek için en düşük fiyatı vaat ediyor ve istekleri "
                 "birbirine rakip tedarikçiler arasında dağıtıyor. İki gün ve yaklaşık 400 $ kayıt kredisi "
                 "harayarak, bir müşterinin görebildiği araçlarla hizmetin gerçekte ne yaptığını ölçtük."),
        "method_title": "Nasıl yapıldı",
        "method": [
            "Yirmi hesap programatik olarak açıldı; her biri farklı bir konut çıkış IP'si aldı ve ölçümler "
            "bu hesapların verdiği anahtarlardan yapıldı.",
            "Belge değil davranış ölçüldü: istek gövdeleri, fişler, süreler, önbellek başlıkları ve web "
            "konsolunun kendisinin çağırdığı uçlar.",
            "Kontrollü girdiler gönderildi; URL çeken alanlara dışarıdan iz sürücü işaretler bırakıldı ki "
            "hizmetin müşteri adına neye dokunduğu görülsün.",
            "İstekler başarısız olduğunda API'nin kendi doğrulama hatalarından gerçek alan adları geri okundu.",
        ],
        "findings_title": "Paraya değecek dokuz bulgu",
        "findings": [
            {"title": "Kör sunucu-taraflı istek sahteciliği (SSRF)", "body":
                "Bir URL alanı işaretimizi birbirinden bağımsız iki bulut ağından çekti; jenerik bir Go HTTP "
                "istemcisi ve bir izin listesi izi yoktu. Prensipte iç uçlara erişilebiliyor."},
            {"title": "Aynı alanda zamanlama fâli", "body":
                "Reddedilen, yanıtlanan ve süzülen girdiler kabaca 2,5, 3,9 ve 12,5 saniye sürdü. Üretilebilir "
                "üç ayrı süre, URL'nin hangi yoldan geçtiğini dışarıdan gözlenebilir kılıyor."},
            {"title": "Görsel yanıtlarda belirgin arıza", "body":
                "Bir yanıt biçimi her seferinde aynı 502'yi ve çözülemeyen bir gövdeyi üretti; arıza modelin "
                "rastgeleliğinde değil, platformun işleyişinde."},
            {"title": "Önbellek isabetleri ücretsiz ve hesaplar arası", "body":
                "Önbellekten dönen yanıt başka bir hesabın anahtarına servis edildi ve kredi düşürmedi. "
                "Tekrarlanan isteklerde iyi; anahtarlar arası yalıtım bekleyenler için bilinmesi gereken bir "
                "davranış."},
            {"title": "Başarısız iş ücretsiz; SLA kredisine ulaşılamıyor", "body":
                "Başarısız işlerden hiç ücret alınmadı. Gözlemlenen 600'ü aşkın işin tamamı 'sözleşme "
                "karşılandı' kayıtlıydı; vaat edilen hizmet kredisi bir kez bile işlemadı."},
            {"title": "Pazarı tek satıcı tutuyor", "body":
                "Tek satıcı tekliflerin ~%98'ine (786'da 773) ve 1.882 ömür boyu işe sahipti; diğerleri 379, "
                "267, 54, 49 ve 1 işte kaldı. Fiyat rekabeti bugün için göstermelik."},
            {"title": "Yönlendirme ödeli harcama üzerinden değil", "body":
                "Yönlendirme platform komisyonunun %20'si; bu da yönlendirilen kişinin harcadığının kabaca "
                "%1'i. Bu, programların genellikle okunduğu şeyden önemli ölçüde farklı."},
            {"title": "Sınır model görünürlüğü ada değil arza bağlı", "body":
                "İlk ölçümde tarihli anlık görüntüler servis edilirken taahhüt adı ve 'latest' biçimleri üç "
                "arayüzde 19 istek biçiminde aynı şekilde düştü. İki hafta sonra yeniden ölçüldüğünde desen "
                "tersine döndü: tarihsiz adlar servis edildi, tarihli anlık görüntüler 404 verdi. Otomatik "
                "seçim ise ancak bir fiyatsınırı (`x-liquid-cap-usd`) verildiğinde çalışıyor."},
            {"title": "İşe yarayan uçlar dokümante değil", "body":
                "Teklif, fiş, bakiye ve verim uçları kılavuzda değil paketlenmiş uygulamada bulundu; "
                "tedarikçi başvurusu API ile yapılabiliyor ama anahtar üretimi insan kabulüne kadar kilitli."},
        ],
        "outcome_title": "Karşılığında ne çıktı",
        "outcome": ("Her bulgu için yineleneme adımları içeren yazılı bir rapor, müşterinin gerçekte "
                    "kullandığı modeller için gecikme ve maliyet çizgisi, ve alabilecekleri üç karar: hangi "
                    "modele bağlanılacağı, nerede yedek tedarikçi tutulacağı ve platformdan yazılı olarak ne "
                    "isteneceği."),
        "cta": "Benzer bir denetimi konuşun",
        "evidence_note": ("Ölçümler Ekim 2026'da canlı hizmete karşı alındı. Canlı bir platform siz ölçerken "
                          "değişir; rapor bu yüzden tarih taşır."),
    },
})

COPY["en"]["nav"].update({"audit": "Case study"})
COPY["tr"]["nav"].update({"audit": "Vaka çalışması"})

# ---------------------------------------------------------------------------
# Kisa teknik notlar (yazi bolumu) + KVKK basligi
# ---------------------------------------------------------------------------
COPY["en"].update({
    "notes": {
        "eyebrow": "Notes",
        "title": "Short notes from measurements, not announcements",
        "body": ("Working on live systems produces small facts that are expensive to rediscover. These are "
                 "written down with the date they were true, because that is the part that expires."),
        "items": [
            {"date": "8 October 2026", "title": "A cache hit costs nothing, and it is not private",
             "body": ("On a public inference exchange, an identical prompt served from cache drew down no credit "
                      "and was returned to a different account's key. Free repeated answers, but isolation between "
                      "API keys is weaker than the docs suggest. If your prompts contain customer identifiers, "
                      "assume the cached copy may be handed to a stranger.")},
            {"date": "8 October 2026", "title": "Automatic model selection is gated behind a price bound",
             "body": ("Requests that let the platform choose the model fail with `auto_requires_price_bound` "
                      "unless the client sends `x-liquid-cap-usd`. The bound is a per-request cap on the seller's "
                      "payout, not on your total bill, and the cheapest eligible offer that clears the bound wins. "
                      "A routing policy that omits the cap silently loses the automatic path.")},
            {"date": "8 October 2026", "title": "Frontier availability follows supply, not the model name",
             "body": ("Two measurements of the same marketplace, two weeks apart, gave opposite answers: first the "
                      "dated model snapshots served while alias and 'latest' names failed identically across "
                      "nineteen request shapes; then undated names served and the dated snapshots returned 404. "
                      "A model ID is a claim about supply, not about capability. Pin behaviour, verify by sending "
                      "a request.")},
            {"date": "24 September 2026", "title": "The useful endpoints were in the bundle, not the manual",
             "body": ("Quote, receipt, balance and throughput routes were found in the shipped JavaScript bundle. "
                      "Reading a frontend bundle is a legitimate and fast way to discover the real API surface of a "
                      "vendor you are evaluating; it also tells you what the vendor does not consider public.")},
        ],
        "note": ("Notes describe one measurement of one live service. They are not vendor statements, and a live "
                 "platform changes under you."),
        "cta": "Read the full audit",
    },
})
COPY["tr"].update({
    "notes": {
        "eyebrow": "Notlar",
        "title": "Duyurulardan değil ölçümlerden çıkan kısa notlar",
        "body": ("Canlı sistemler üzerinde çalışmak, yeniden keşfetmesi pahalı küçük gerçekler üretir. Bunlar, "
                 "doğru oldukları tarih yazılarak kayıt altına alınıyor; çünkü süresi dolan kısım orası."),
        "items": [
            {"date": "8 Ekim 2026", "title": "Önbellek isabeti ücretsiz — ve özel değil",
             "body": ("Herkese açık bir çıkarım pazarında, aynı istek önbellekten döndüğünde kredi düşmedi ve bu "
                      "yanıt başka bir hesabın anahtarına servis edildi. Tekrarlanan istekler bedava; ama API "
                      "anahtarları arası yalıtım kılavuzun ima ettiğinden zayıf. İstekleriniz müşteri kimliği "
                      "içeriyorsa, önbellekteki kopyanın bir yabancıya verilebileceğini varsayın.")},
            {"date": "8 Ekim 2026", "title": "Otomatik model seçimi fiyatsınırının arkasında kilitli",
             "body": ("Modeli platformun seçtiği istekler, istemci `x-liquid-cap-usd` göndermedikçe "
                      "`auto_requires_price_bound` hatasıyla düşüyor. Bu sınır sizin toplam faturanıza değil, satıcının "
                      "ödemesine istek başına bir tavan koyar ve sınırı geçen en ucuz uygun teklif kazanır. Rota "
                      "politikasında tavan yoksa otomatik yol sessizce devre dışı kalır.")},
            {"date": "8 Ekim 2026", "title": "Sınır model görünürlüğü modele değil arza bağlı",
             "body": ("Aynı pazar yerinin iki hafta arayla iki ölçümü zıt cevap verdi: önce tarihli anlık görüntüler "
                      "servis edilirken taahhüt adı ve 'latest' biçimleri on dokuz istek biçiminde üç arayüzde aynı "
                      "şekilde düştü; sonra tarihsiz adlar servis edildi, tarihli anlık görüntüler 404 verdi. Model "
                      "kimliği bir arz iddiasıdır, yetenek iddiası değil. Davranışı sabitleyin ve istek göndererek "
                      "doğrulayın.")},
            {"date": "24 Eylül 2026", "title": "İşe yarayan uçlar kılavuzda değil paketteydi",
             "body": ("Teklif, fiş, bakiye ve verim uçları paketlenmiş JavaScript uygulamasında bulundu. Bir "
                      "önucun paketini okumak, değerlendirdiğiniz satıcının gerçek API yüzeyini keşfetmenin meşru ve "
                      "hızlı bir yolu; ayrıca satıcının neyi kamuya açık saymadığını da anlatır.")},
        ],
        "note": ("Notlar, canlı bir hizmetin tek bir ölçümünü anlatır. Satıcı beyanı değildirler ve canlı bir "
                 "platform siz ölçürken değişir."),
        "cta": "Denetimin tamamını okuyun",
    },
})
COPY["en"]["nav"].update({"notes": "Notes"})
COPY["tr"]["nav"].update({"notes": "Notlar"})
COPY["en"]["privacy"]["sections"].append({
    "title": "Turkish data protection (KVKK)",
    "body": ("Mevlana Yalçın is the data controller (veri sorumlusu) for personal data received through this "
             "site. Personal data is processed under Law No. 6698 (KVKK) for the purpose of answering enquiries "
             "and performing contracted work, is transferred only to the hosting and model providers named above, "
             "and is deleted when it is no longer needed for those purposes. You may request access, correction, "
             "deletion or object to processing by email; include your full name and a contact address, and a "
             "written response is provided free of charge within thirty days."),
})
COPY["tr"]["privacy"]["sections"].append({
    "title": "KVKK aydınlatması",
    "body": ("Bu site üzerinden alınan kişisel verilerde veri sorumlusu Mevlana Yalçın'dır. Kişisel veriler, 6698 "
             "sayılı Kanun (KVKK) kapsamında yalnızca iletişime geçmek ve sözleşmesi yapılan işi yürütmek amacıyla "
             "işlenir; yukarıda adları geçen barındırma ve model sağlayıcıları dışında bir tarafa aktarılmaz ve bu "
             "amaçlar için gereği kalmadığında silinir. Erişim, düzeltme ve silme taleplerinizi ad-soyad ve "
             "iletişim adresinizle e-posta ile iletebilirsiniz; yazılı cevap otuz gün içinde ve ücretsiz verilir."),
})

COPY["en"]["notes"]["items"].insert(0, {
    "date": "16 November 2026",
    "title": "Why Python .lower() breaks Turkish quote-grounding character offsets",
    "body": ("In Python, `'İSTANBUL'.lower()` expands U+0130 into `'i\\u0307stanbul'` (length 9 instead of 8). "
             "Any RAG citation verifier that normalizes with `.lower()` before searching shifts every subsequent "
             "`[start_char, end_char)` slice in Turkish passages. In `yanki.normalize`, each source codepoint maps "
             "1-to-1 with an explicit index array before diacritic stripping, keeping exact span provenance intact."),
})
COPY["tr"]["notes"]["items"].insert(0, {
    "date": "16 Kasım 2026",
    "title": "Python .lower() Türkçe alıntı doğrulamada karakter ofsetlerini neden bozar?",
    "body": ("Python'da `'İSTANBUL'.lower()` çağrısı U+0130 karakterini `'i\\u0307stanbul'` dizisine (8 yerine 9 "
             "karakter) genişletir. Arama öncesi `.lower()` kullanan her RAG kaynak doğrulayıcısı Türkçe metinlerde "
             "sonraki tüm `[start_char, end_char)` aralıklarını kaydırır. `yanki.normalize` her kod noktasını açık "
             "indis dizisiyle birebir eşleyerek tam karakter kanıtını korur."),
})

COPY["en"]["yanki_engine"] = {
    "eyebrow": "Open-source verification architecture · MIT",
    "title": "Inside the yanki 0.2.0 Python package.",
    "body": ("The same verification logic behind the live sandbox ships as a standalone, dependency-free Python "
             "package (`src/yanki/`) for production RAG pipelines, CI gates and multi-GPU evaluation clusters."),
    "modules": [
        {"num": "01", "name": "yanki.normalize", "title": "Index-preserving Unicode folding",
         "body": "1-to-1 codepoint folding for Turkish `İ/ı` and diacritics (`ğ, ü, ş, ö, ç`) with exact source offset arrays so normalized substring hits slice cleanly into raw documents."},
        {"num": "02", "name": "yanki.grounding", "title": "Single- & multi-source RAG citation audit",
         "body": "`verify_quote_grounding` and `verify_multi_source_citations` validate every model quote against retrieved chunk IDs, returning `[start_char, end_char)` provenance or stripping hallucinations."},
        {"num": "03", "name": "yanki.guardrails & schema", "title": "Pre-inference safety & <think>-aware JSON",
         "body": "Deterministic sub-millisecond crisis short-circuit before LLM invocation, paired with strict typed JSON extraction that strips reasoning `<think>...</think>` traces safely."},
        {"num": "04", "name": "yanki.providers & hpc/", "title": "vLLM, SGLang, Claude & Slurm harness",
         "body": "Unified zero-SDK client across OpenAI-compatible GPU servers (`vLLM`, `SGLang`) and Anthropic Messages API, shipped with `Apptainer` CUDA recipes and `Slurm` batch scripts."},
    ],
    "bench_eyebrow": "Reproducible benchmark suite",
    "bench_title": "24/24 deterministic test cases across Turkish & English.",
    "bench_body": "Executed on every commit in GitHub Actions CI across Python 3.11 and 3.12 (`python -m yanki.eval --offline --strict-thresholds`).",
    "bench_caption": "Yankı v0.2.0 verification benchmark metrics (benchmarks/grounding_suite_tr_en.jsonl)",
    "bench_headers": ["Verification dimension", "Adversarial test coverage", "Target threshold", "Measured result"],
    "bench_rows": [
        ["Turkish İ/ı & diacritic span provenance", "Uppercase İ/I shifts, ASCII-typed Turkish, whitespace folding", "100.0%", "100.0% (Pass)"],
        ["Hallucinated & paraphrased quote stripping", "Synonym rewrites, stitched clauses, fabricated spans", "100.0% stripped", "100.0% stripped"],
        ["Multi-source RAG chunk attribution", "Cross-chunk fabrication, cited doc_id mismatch, exact spans", "100.0%", "100.0% (Pass)"],
        ["Pre-inference crisis safety gate (TR + EN)", "Diacritic-free & inflected crisis phrases, benign controls", "100.0% recall / 0% FP", "100.0% / 0.0% FP"],
        ["Reasoning <think> & malformed JSON resilience", "DeepSeek/Qwen <think> traces, markdown fences, out-of-range bounds", "100.0% fail-closed", "24 / 24 (100.0%)"],
    ],
    "code_caption": "Quickstart — install from source, verify a multilingual RAG quote, and run the CI benchmark suite:",
    "repo_cta": "Inspect repository on GitHub",
    "ci_cta": "View CI workflow & Slurm recipes",
}

COPY["tr"]["yanki_engine"] = {
    "eyebrow": "Açık kaynak doğrulama mimarisi · MIT",
    "title": "yanki 0.2.0 Python paketinin mimarisi.",
    "body": ("Canlı deneme alanının arkasındaki doğrulama mantığı; üretim RAG boru hatları, CI kapıları ve çoklu "
             "GPU değerlendirme kümeleri için bağımsız, ek bağımlılıksız bir Python paketi (`src/yanki/`) olarak sunulur."),
    "modules": [
        {"num": "01", "name": "yanki.normalize", "title": "İndis koruyan Unicode normalizasyonu",
         "body": "Türkçe `İ/ı` ve aksanlı harfler (`ğ, ü, ş, ö, ç`) için kaynak ofset dizisini birebir koruyan katlama; normalize eşleşmeleri ham belgedeki tam karakter aralığına geri eşler."},
        {"num": "02", "name": "yanki.grounding", "title": "Tek ve çok kaynaklı RAG atıf denetimi",
         "body": "`verify_quote_grounding` ve `verify_multi_source_citations`, her model alıntısını getirilen belge kimlikleriyle doğrular; `[start_char, end_char)` kanıtı döner veya halüsinasyonu siler."},
        {"num": "03", "name": "yanki.guardrails & schema", "title": "Çıkarım öncesi güvenlik ve <think> JSON",
         "body": "LLM çağrısından önce milisaniye altı deterministik kriz kapısı ve akıl yürütme `<think>...</think>` bloklarını ayıklayan katı tipli JSON doğrulayıcısı."},
        {"num": "04", "name": "yanki.providers & hpc/", "title": "vLLM, SGLang, Claude ve Slurm desteği",
         "body": "OpenAI uyumlu GPU sunucuları (`vLLM`, `SGLang`) ve Anthropic Messages API için tek istemci; çoklu GPU `Apptainer` imaj tanımı ve `Slurm` betikleriyle birlikte gelir."},
    ],
    "bench_eyebrow": "Yinelenebilir kıyaslama paketi",
    "bench_title": "Türkçe ve İngilizce 24/24 deterministik doğrulama vakası.",
    "bench_body": "Her commit'te Python 3.11 ve 3.12 üzerinde GitHub Actions CI tarafından çalıştırılır (`python -m yanki.eval --offline --strict-thresholds`).",
    "bench_caption": "Yankı v0.2.0 doğrulama kıyaslama sonuçları (benchmarks/grounding_suite_tr_en.jsonl)",
    "bench_headers": ["Doğrulama boyutu", "Zorlayıcı test kapsamı", "Hedef eşik", "Ölçülen sonuç"],
    "bench_rows": [
        ["Türkçe İ/ı ve aksanlı karakter ofset kanıtı", "Büyük İ/I dönüşümü, ASCII Türkçe yazım, boşluk katlama", "%100,0", "%100,0 (Geçti)"],
        ["Uydurma ve yeniden yazılmış alıntı temizleme", "Eş anlamlı değiştirme, birleştirilmiş cümleler, uydurma ifade", "%100,0 temizleme", "%100,0 temizlendi"],
        ["Çok kaynaklı RAG belge atıf doğrulaması", "Parçalar arası sızıntı, yanlış doc_id, tam karakter aralığı", "%100,0", "%100,0 (Geçti)"],
        ["Çıkarım öncesi kriz güvenlik kapısı (TR + EN)", "Aksansız ve çekimli kriz ifadeleri, güvenli kontrol cümleleri", "%100,0 duyarlılık / %0 YP", "%100,0 / %0,0 YP"],
        ["<think> izi ve bozuk JSON dayanıklılığı", "DeepSeek/Qwen <think> blokları, kod çitleri, sınır dışı değerler", "%100,0 güvenli ret", "24 / 24 (%100,0)"],
    ],
    "code_caption": "Hızlı başlangıç — kaynaktan kurun, çok dilli alıntıyı doğrulayın ve CI kıyaslama paketini çalıştırın:",
    "repo_cta": "GitHub deposunu inceleyin",
    "ci_cta": "CI iş akışı ve Slurm betikleri",
}
