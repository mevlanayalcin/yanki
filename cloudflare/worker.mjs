/**
 * Yankı Edge Worker: statik çift dilli vitrin ve dokümantasyon sitesini servis eder,
 * özel önizleme (waitlist) kaydı ve servis sağlık durumunu sunar.
 *
 * Not: Canlı çıkarım uç noktası (/api/reflect) bulut konsolu yapım aşamasında olduğu için
 * genel kullanıma kapalıdır (503 private_preview).
 */

const LANGS = ["tr", "en"];
const SINIR = 6; // IP basina pencere
const PENCERE = 60; // saniye

const json = (gövde, durum = 200) =>
  new Response(JSON.stringify(gövde), {
    status: durum,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "access-control-allow-origin": "*",
      "cache-control": "no-store",
    },
  });

async function izinli(env, ip) {
  if (!env.SINIRLAYICI) return true;
  const nesne = env.SINIRLAYICI.idFromName(ip);
  const y = await env.SINIRLAYICI.get(nesne).fetch(
    new Request("https://yanki.sinir/izin", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ id: "istek:" + ip, limit: SINIR, pencere: PENCERE }),
    })
  );
  const veri = await y.json().catch(() => ({ izin: false }));
  return !!veri.izin;
}

async function handlePrivatePreview(request) {
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
  return json(
    {
      ok: false,
      error: "private_preview",
      status: "in_development",
      message:
        "Yankı Cloud Gateway is currently in active development and limited to private preview partners. Inspect verified production traces or join the waitlist at https://mevlanayalcin.com.tr/work/yanki/",
    },
    503
  );
}

async function handleWaitlist(request, env) {
  if (request.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "access-control-allow-origin": "*",
        "access-control-allow-methods": "POST, OPTIONS",
        "access-control-allow-headers": "content-type",
      },
    });
  }
  if (request.method !== "POST") return json({ error: "method_not_allowed" }, 405);
  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  if (!(await izinli(env, ip))) return json({ error: "busy" }, 429);
  let gövde = {};
  try {
    gövde = await request.json();
  } catch {
    return json({ error: "bad_request" }, 400);
  }
  const adres = String(gövde.email || "").trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(adres) || adres.length > 180) {
    return json({ error: "bad_email" }, 400);
  }
  if (!env.WAITLIST) return json({ created: true, sayac: 1 }, 201);
  const anahtar = "yanki:bekleyen:" + adres;
  if (await env.WAITLIST.get(anahtar)) {
    return json({ kayitli: true, sayac: Number((await env.WAITLIST.get("yanki:meta:sayac")) || 0) });
  }
  const adet = Number((await env.WAITLIST.get("yanki:meta:sayac")) || 0) + 1;
  await env.WAITLIST.put(
    anahtar,
    JSON.stringify({
      zaman: new Date().toISOString(),
      dil: LANGS.includes(gövde.lang) ? gövde.lang : "en",
      kaynak: String(gövde.via || "site").slice(0, 24),
    })
  );
  await env.WAITLIST.put("yanki:meta:sayac", String(adet));
  return json({ created: true, sayac: adet }, 201);
}

export class Sinirlayici {
  constructor(state) {
    this.state = state;
  }
  async fetch(request) {
    const { limit, pencere } = await request.json().catch(() => ({}));
    const sure = Math.max(5, Number(pencere) || PENCERE);
    const tavan = Math.max(1, Number(limit) || SINIR);
    const anahtar = "pencere:" + Math.floor(Date.now() / (sure * 1000));
    const mevcut = (await this.state.storage.get(anahtar)) || 0;
    if (mevcut >= tavan) return json({ izin: false, kalan: 0 });
    await this.state.storage.put(anahtar, mevcut + 1, { expirationTtl: sure * 2 });
    return json({ izin: true, kalan: tavan - mevcut - 1 });
  }
}

// Kalıcı yönlendirmeler korunur.
const YONLENDIRME = {
  "/how-it-works": "/process/",
  "/how-it-works/": "/process/",
  "/safety": "/work/yanki/",
  "/safety/": "/work/yanki/",
  "/api": "/work/yanki/#architecture",
  "/api/": "/work/yanki/#architecture",
  "/work": "/products/",
  "/work/": "/products/",
  "/tr/nasil": "/tr/surec/",
  "/tr/nasil/": "/tr/surec/",
  "/tr/guvenlik": "/tr/calismalar/yanki/",
  "/tr/guvenlik/": "/tr/calismalar/yanki/",
  "/tr/api": "/tr/calismalar/yanki/#architecture",
  "/tr/api/": "/tr/calismalar/yanki/#architecture",
  "/tr/company": "/tr/kurumsal/",
  "/tr/company/": "/tr/kurumsal/",
  "/tr/calismalar": "/tr/urunler/",
  "/tr/calismalar/": "/tr/urunler/",
  "/tr/work/yanki": "/tr/calismalar/yanki/",
  "/tr/work/yanki/": "/tr/calismalar/yanki/",
};

export default {
  async fetch(request, env) {
    const adres = new URL(request.url);
    const yol = adres.pathname;
    if (
      ["mevlanayalcin.com.tr", "www.mevlanayalcin.com.tr"].includes(adres.hostname) &&
      (adres.protocol !== "https:" || adres.hostname.startsWith("www."))
    ) {
      adres.protocol = "https:";
      adres.hostname = "mevlanayalcin.com.tr";
      return Response.redirect(adres.toString(), 308);
    }
    if (YONLENDIRME[yol]) {
      const hedef = new URL(YONLENDIRME[yol], adres);
      hedef.search = adres.search;
      return Response.redirect(hedef.toString(), 301);
    }
    if (yol === "/api/reflect") return handlePrivatePreview(request);
    if (yol === "/api/waitlist") return handleWaitlist(request, env);
    if (yol === "/api/health") {
      return json({
        ok: true,
        service: "yanki-verification-platform",
        engineVersion: "0.2.0",
        stage: "private_preview",
        publicSandboxEnabled: false,
      });
    }
    return env.ASSETS.fetch(request);
  },
};
