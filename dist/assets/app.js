// Deneme kutusu + bekleme listesi. Hepsi ayni ucleri kullanir; yanit ne ise o gosterilir.
(function () {
  var tr = location.pathname.indexOf("/tr/") === 0;
  var ETIKET = tr
    ? { duygu: "Duygu", siddet: "Şiddet", yansitma: "Yansıtma", alinti: "Senin cümlen", adim: "Adım",
        kriz: "Kriz sözcüğü geçti", bekliyoruz: "Listedesin — adres kaydedildi.", hatali: "Geçersiz adres.",
        ulasilamadi: "Uç şu anda ulaşılamadı. Bir şey saklanmadı.",
        beklemetuşucu: "Adres kaydedilemedi, birazdan yine dene." }
    : { duygu: "Feeling", siddet: "Intensity", yansitma: "Reflection", alinti: "Your words", adim: "Next step",
        kriz: "A crisis word appeared", bekliyoruz: "You are on the list — address saved.", hatali: "Invalid address.",
        ulasilamadi: "The endpoint is unavailable right now. Nothing was stored.",
        beklemetuşucu: "Could not save the address, try again shortly." };

  function metin(e, s) { e.textContent = s; }

  function satir(dl, baslik, icerik) {
    var dt = document.createElement("dt"); dt.textContent = baslik;
    var dd = document.createElement("dd"); dd.textContent = icerik;
    dl.appendChild(dt); dl.appendChild(dd);
  }

  var dugme = document.getElementById("yansit");
  var girdi = document.getElementById("girdi");
  var durum = document.getElementById("durum");
  var sonuc = document.getElementById("sonuc");

  if (dugme && girdi && sonuc) {
    var beklenen = 0;
    dugme.addEventListener("click", function () {
      var metin = girdi.value.trim();
      sonuc.hidden = true;
      sonuc.innerHTML = "";
      if (metin.length < 8) { metin(durum, tr ? "En az bir cümle yaz (8 karakter)." : "Write at least a sentence (8 characters)."); return; }
      var kuyruk = ++beklenen;
      dugme.disabled = true;
      metin(durum, tr ? "Düşünüyor…" : "Thinking…");
      fetch("/api/reflect", {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ text: metin, lang: tr ? "tr" : "en" })
      })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (sonuc_) {
          if (kuyruk !== beklenen) return;
          durum.textContent = "";
          sonuc.hidden = false;
          var j = sonuc_.j || {};
          if (!sonuc_.ok || j.error) {
            var h = document.createElement("p"); h.className = "motorNotu";
            h.textContent = ETIKET.ulasilamadi + (j.error ? " (" + j.error + ")" : "");
            sonuc.appendChild(h);
            return;
          }
          if (j.kriz) {
            var k = document.createElement("p"); k.className = "kriz";
            k.textContent = j.yansitma || ETIKET.kriz;
            sonuc.appendChild(k);
          }
          var dl = document.createElement("dl");
          if (j.duygu) { satir(dl, ETIKET.duygu, j.duygu + (j.siddet ? " · " + j.siddet + "/5" : "")); }
          if (j.yansitma && !j.kriz) { satir(dl, ETIKET.yansitma, j.yansitma); }
          if (j.alinti) { satir(dl, ETIKET.alinti, "“" + j.alinti + "”"); }
          if (j.adim) { satir(dl, ETIKET.adim, j.adim); }
          sonuc.appendChild(dl);
          var dip = document.createElement("p"); dip.className = "motor";
          dip.textContent = (j.provider || "") + " · " + (j.model || "") + (j.cache && j.cache.read ? " · cache read" : "");
          sonuc.appendChild(dip);
          if (j.disclaimer) {
            var d = document.createElement("p"); d.className = "motor"; d.textContent = j.disclaimer;
            sonuc.appendChild(d);
          }
        })
        .catch(function () {
          if (kuyruk !== beklenen) return;
          durum.textContent = ETIKET.ulasilamadi;
        })
        .then(function () { dugme.disabled = false; });
    });
  }

  var form = document.getElementById("bekleme");
  if (form) {
    form.addEventListener("submit", function (olay) {
      olay.preventDefault();
      var yazit = document.getElementById("beklemeyanit");
      var adres = (form.querySelector("input[name=email]") || {}).value || "";
      if (adres.indexOf("@") < 1) { metin(yazit, ETIKET.hatali); return; }
      fetch("/api/waitlist", {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ email: adres, lang: tr ? "tr" : "en", via: "site" })
      })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (sonuc_) {
          if (sonuc_.ok) {
            metin(yazit, ETIKET.bekliyoruz);
            form.querySelector("input[name=email]").disabled = true;
            form.querySelector("button").disabled = true;
          } else {
            metin(yazit, ETIKET.beklemetuşucu + (sonuc_.j && sonuc_.j.error ? " (" + sonuc_.j.error + ")" : ""));
          }
        })
        .catch(function () { metin(yazit, ETIKET.beklemetuşucu); });
    });
  }
})();
