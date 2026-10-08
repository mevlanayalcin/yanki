/**
 * Yanki Worker'i: statik siteyi servis eder, iki de uc verir.
 *   POST /api/reflect  -> kullanicinin kendi metninden yansitma uretir (Claude, JSON-zorunlu)
 *   POST /api/waitlist -> e-postayi Cloudflare KV'ye tek satir olarak yazar
 *
 * Bilincli tercihler:
 *  - Kriz sozcukleri modele sorulmadan ONCE kural listesiyle yakalanir; model bu karari vermez.
 *  - Model bozuk/eksik JSON donerse cevap GOSTERILMEZ; uctan kural taballi sahte bir cevap cikmaz.
 *  - alinti alani kullanicinin metninde birebir gecmiyorsa silinir; model uyduramaz.
 */

const API = "https://api.anthropic.com/v1/messages";
const MODEL = "claude-haiku-4-5-20251001";
const LANGS = ["tr", "en"];
const EN_KISA = 8;
const EN_UZUN = 600;
const SINIR = 6; // IP basina pencere
const PENCERE = 60; // saniye
const BUTCE_BIRIM = Number(globalThis.__YANKI_BUTCE__ || 400_000); // gunluk odeme-esdegeri tavan
const BIRIM = { taze: 1_000_000, yazma: 1_250_000, okuma: 100_000, cikti: 5_000_000 };

// Kriz sozcukleri: muhafazakar liste. Yanlis-pozitif güvenlidir; model devreye girmez.
const KRIZ = [
  "intihar", "kendimi öldür", "kendimi oldur", "öldürmek istiyorum", "oldurmek istiyorum",
  "yaşamak istemiyorum", "yashamak istemiyorum", "hayatı bırak", "hayati birak",
  "kendime zarar", "kendime ziyan", "kendimi parçala",
  "kill myself", "suicide", "end my life", "want to die", "harm myself", "not worth living",
];
const KRIZ_YANIT = {
  tr: "Yazdıkların günlük bir yansıtmanın dışında duruyor. Şu anda güvende değilsen ya da kendini yaralamayı düşünüyorsan Türkiye'de 112'yi ara. Bir uzmana ya da güvendiğin birine ulaşmak için yazman yeterli — bu kutu sana cevap vermesin, sen bir insana ulaş.",
  en: "What you wrote sits outside a daily reflection. If you are not safe right now, or you are thinking of harming yourself, call 112 in Türkiye or your local emergency number. Reach a person — this box is not the one that should answer.",
};

const SYSTEM = `You are Yankı, an emotional check-in companion. You are not a therapist, you do not diagnose, and you never advise on medication.

Read the user's passage and answer with ONE JSON object and nothing else:
{"duygu": "one feeling word in the user's language", "siddet": 1-5, "alternatif": "the feeling you considered and rejected, or null", "yansitma": "one or two sentences in the user's language reflecting what you hear, addressed to 'you'", "alinti": "an exact contiguous substring copied from the user's passage that carries the feeling, or null", "adim": "one concrete action doable within the next hour, in the user's language"}

Rules:
- "alinti" must be copied character-for-character from the user's passage. If you cannot find such a sentence, use null. Never paraphrase inside "alinti".
- Name at most one feeling. Do not add advice about diagnosis, medication or therapy.
- Do not use clinical language, do not ask questions, do not add disclaimers: the app adds them.
- Keep "yansitma" under 45 words and "adim" under 22 words.
- If the passage is empty of feeling, say so plainly in the user's language in "yansitma" and set "duygu" to null.`;

const json = (gövde, durum = 200) =>
  new Response(JSON.stringify(gövde), {
    status: durum,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "access-control-allow-origin": "*",
      "cache-control": "no-store",
    },
  });

const normalizle = (s) =>
  (s || "")
    .toLowerCase()
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/ğ/g, "g").replace(/ü/g, "u").replace(/ş/g, "s")
    .replace(/ı/g, "i").replace(/ö/g, "o").replace(/ç/g, "c")
    .replace(/\s+/g, " ")
    .trim();

// Liste de kullanicinin metniyle ayni normalize etmeden gecirilir; yoksa Turkce
// karakterli desen hicbir zaman eslesmez (ilk yakalama tam da bunu kaciriyordu).
function krizMi(metin) {
  const d = " " + normalizle(metin) + " ";
  return KRIZ.some((k) => {
    const duz = normalizle(k);
    return d.includes(" " + duz + " ") || d.includes(" " + duz);
  });
}

function jsonBul(govde) {
  if (!govde) return null;
  const temiz = govde.replace(/^\s*```(?:json)?/i, "").replace(/```\s*$/, "").trim();
  const adaylar = [temiz];
  const bas = temiz.indexOf("{"), bit = temiz.lastIndexOf("}");
  if (bas >= 0 && bit > bas) adaylar.push(temiz.slice(bas, bit + 1));
  for (const a of adaylar) {
    try {
      const p = JSON.parse(a);
      if (p && typeof p === "object" && !Array.isArray(p)) return p;
    } catch { /* siradaki aday */ }
  }
  return null;
}

function dogrula(k, metin) {
  if (!k) return null;
  const y = typeof k.yansitma === "string" ? k.yansitma.trim() : "";
  if (y.length < 12 || y.length > 900) return null;
  const adim = typeof k.adim === "string" ? k.adim.trim() : "";
  let alinti = typeof k.alinti === "string" ? k.alinti.trim() : "";
  // Alinti kullanicinin metninde birebir gecmiyorsa uydurulmustur: atilir.
  if (alinti && !normalizle(metin).includes(normalizle(alinti))) alinti = "";
  let siddet = Number(k.siddet);
  siddet = Number.isFinite(siddet) ? Math.min(5, Math.max(1, Math.round(siddet))) : null;
  const duygu = typeof k.duygu === "string" && k.duygu.trim().length <= 40 ? k.duygu.trim() : null;
  return {
    duygu, siddet,
    alternatif: typeof k.alternatif === "string" && k.alternatif.length <= 40 ? k.alternatif.trim() : null,
    yansitma: y.slice(0, 600),
    alinti: alinti ? alinti.slice(0, 240) : null,
    adim: adim ? adim.slice(0, 220) : null,
  };
}

async function modelCagrisi(env, metin, dil) {
  const govde = {
    model: MODEL,
    max_tokens: 620,
    temperature: 0.5,
    system: SYSTEM,
    messages: [{ role: "user", content: `${dil === "tr" ? "Kullanıcının günlüğü (Türkçe):" : "The user's journal entry (English):"}\n"""${metin}"""\nAnswer with the JSON object only.` }],
  };
  const r = await fetch(API, {
    method: "POST",
    headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify(govde),
  });
  const veri = await r.json().catch(() => null);
  if (!r.ok) return { hata: (veri && veri.error && veri.error.type) || "upstream", durum: r.status };
  const yazi = ((veri.content || []).filter((b) => b.type === "text").map((b) => b.text).join(" ") || "");
  const u = veri.usage || {};
  const birim = Math.round(
    ((u.input_tokens || 0) * BIRIM.taze + (u.cache_creation_input_tokens || 0) * BIRIM.yazma +
      (u.cache_read_input_tokens || 0) * BIRIM.okuma + (u.output_tokens || 0) * BIRIM.cikti) / BIRIM.taze
  );
  return { veri, yazi, kullanim: u, birim };
}

async function gunlukBirim(env) {
  const anahtar = "yanki:birim:" + new Date().toISOString().slice(0, 10);
  return Number((await env.WAITLIST.get(anahtar)) || 0);
}

async function birimEkle(env, miktar) {
  const anahtar = "yanki:birim:" + new Date().toISOString().slice(0, 10);
  const mevcut = Number((await env.WAITLIST.get(anahtar)) || 0);
  await env.WAITLIST.put(anahtar, String(mevcut + miktar), { expirationTtl: 60 * 60 * 24 * 3 });
}

async function izinli(env, ip) {
  if (!env.SINIRLAYICI) return true;
  const nesne = env.SINIRLAYICI.idFromName(ip);
  const y = await env.SINIRLAYICI.get(nesne).fetch(new Request("https://yanki.sinir/izin", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ id: "istek:" + ip, limit: SINIR, pencere: PENCERE }),
  }));
  const veri = await y.json().catch(() => ({ izin: false }));
  return !!veri.izin;
}

async function handleReflect(request, env) {
  if (request.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "access-control-allow-origin": "*",
        "access-control-allow-methods": "POST, OPTIONS",
        "access-control-allow-headers": "content-type",
        "access-control-max-age": "86400",
      },
    });
  }
  if (request.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  let gövde;
  try { gövde = await request.json(); } catch { return json({ error: "bad_request" }, 400); }
  const metin = typeof gövde.text === "string" ? gövde.text.replace(/\s+/g, " ").trim() : "";
  const dil = LANGS.includes(gövde.lang) ? gövde.lang : "en";
  if (!metin) return json({ error: "bad_request", reason: "empty" }, 400);
  if (metin.length < EN_KISA) return json({ error: "bad_request", reason: "too_short" }, 400);
  if (metin.length > EN_UZUN) return json({ error: "too_long" }, 413);

  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  if (!(await izinli(env, ip))) return json({ error: "busy" }, 429);

  // Kriz karari modele birakilmaz: kural listesi once calisir ve model hic cagrilmez.
  if (krizMi(metin)) {
    return json({
      kriz: true, yansitma: KRIZ_YANIT[dil], duygu: null, siddet: null, alinti: null, adim: null,
      disclaimer: dil === "tr" ? "Yankı terapi değildir. Kriz sözcükleri kural listesiyle yakalanır; bu yanıtta model çağrılmadı." : "Yankı is not therapy. Crisis wording is caught by a rule list; no model was called for this answer.",
      provider: "rule", model: "crisis-list-v1",
    });
  }

  if (!env.ANTHROPIC_API_KEY) return json({ error: "not_configured" }, 500);
  if ((await gunlukBirim(env)) >= BUTCE_BIRIM) return json({ error: "daily_budget" }, 503);

  const sonuc = await modelCagrisi(env, metin, dil);
  if (sonuc.hata) return json({ error: sonuc.hata }, sonuc.durum === 429 ? 429 : 502);
  await birimEkle(env, sonuc.birim || 0);

  const cevap = dogrula(jsonBul(sonuc.yazi), metin);
  if (!cevap) return json({ error: "malformed_answer" }, 502);

  return json({
    ...cevap,
    disclaimer: dil === "tr" ? "Yankı bir eşlikçidir; terapi, teşhis veya tıbbi tavsiye değildir." : "Yankı is a companion, not therapy, a diagnosis or medical advice.",
    provider: "anthropic", model: MODEL,
    usage: { girdi: sonuc.kullanim.input_tokens || 0, çıktı: sonuc.kullanim.output_tokens || 0 },
    cache: { yazma: sonuc.kullanim.cache_creation_input_tokens || 0, okuma: sonuc.kullanim.cache_read_input_tokens || 0 },
    birim: sonuc.birim || 0,
  });
}

async function handleWaitlist(request, env) {
  if (request.method === "OPTIONS") {
    return new Response(null, { headers: { "access-control-allow-origin": "*", "access-control-allow-methods": "POST, OPTIONS", "access-control-allow-headers": "content-type" } });
  }
  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  if (!(await izinli(env, ip))) return json({ error: "busy" }, 429);
  let gövde = {};
  try { gövde = await request.json(); } catch { return json({ error: "bad_request" }, 400); }
  const adres = String(gövde.email || "").trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(adres) || adres.length > 180) return json({ error: "bad_email" }, 400);
  const anahtar = "yanki:bekleyen:" + adres;
  if (await env.WAITLIST.get(anahtar)) return json({ kayitli: true, sayac: Number((await env.WAITLIST.get("yanki:meta:sayac")) || 0) });
  const adet = Number((await env.WAITLIST.get("yanki:meta:sayac")) || 0) + 1;
  await env.WAITLIST.put(anahtar, JSON.stringify({ zaman: new Date().toISOString(), dil: LANGS.includes(gövde.lang) ? gövde.lang : "en", kaynak: String(gövde.via || "site").slice(0, 24) }));
  await env.WAITLIST.put("yanki:meta:sayac", String(adet));
  return json({ created: true, sayac: adet }, 201);
}

export class Sinirlayici {
  constructor(state) { this.state = state; }
  async fetch(request) {
    const { id, limit, pencere } = await request.json().catch(() => ({}));
    const sure = Math.max(5, Number(pencere) || PENCERE);
    const tavan = Math.max(1, Number(limit) || SINIR);
    const anahtar = "pencere:" + Math.floor(Date.now() / (sure * 1000));
    const mevcut = (await this.state.storage.get(anahtar)) || 0;
    if (mevcut >= tavan) return json({ izin: false, kalan: 0 });
    await this.state.storage.put(anahtar, mevcut + 1, { expirationTtl: sure * 2 });
    return json({ izin: true, kalan: tavan - mevcut - 1 });
  }
}

export default {
  async fetch(request, env) {
    const yol = new URL(request.url).pathname;
    if (yol === "/api/reflect") return handleReflect(request, env);
    if (yol === "/api/waitlist") return handleWaitlist(request, env);
    if (yol === "/api/health") return json({ ok: true, model: MODEL, butce: BUTCE_BIRIM, krizSozcuk: KRIZ.length });
    return env.ASSETS.fetch(request);
  },
};
