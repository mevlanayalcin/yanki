// Etkilesimli dogrulama izi (trace) sekmeleri + ozel onizleme (waitlist) formu.
// Canli model cagrisi yapilmaz; tum ornekler gercek deterministik motor ciktilaridir.
(function () {
  var tr = location.pathname.indexOf("/tr/") === 0;
  var MSG = tr
    ? {
        bekliyoruz: "Özel önizleme listesine eklendiniz — erişim açıldığında e-posta ile bilgilendireceğiz.",
        zatenKayitli: "Bu e-posta adresi özel önizleme listesinde zaten kayıtlı.",
        hatali: "Lütfen geçerli bir kurumsal veya kişisel e-posta adresi girin.",
        gonderiliyor: "Kaydediliyor…",
        hata: "Kayıt şu anda tamamlanamadı. Lütfen info@mevlanayalcin.com.tr adresine yazın.",
      }
    : {
        bekliyoruz: "Added to the private preview queue — we will reach out as design-partner slots open.",
        zatenKayitli: "This email address is already registered on the private preview list.",
        hatali: "Please enter a valid work or personal email address.",
        gonderiliyor: "Registering…",
        hata: "Could not register right now. Please write directly to info@mevlanayalcin.com.tr.",
      };

  // 1. Sekmeli dogrulama ornekleri (tabs + hidden="until-found" + beforematch)
  var tabGroups = document.querySelectorAll(".trace-tabs");
  var hasNativeFocusGroup =
    typeof HTMLElement !== "undefined" && Object.prototype.hasOwnProperty.call(HTMLElement.prototype, "focusGroup");

  tabGroups.forEach(function (group) {
    var tablist = group.querySelector('[role="tablist"]');
    if (!tablist) return;
    var tabs = Array.prototype.slice.call(tablist.querySelectorAll('[role="tab"]'));
    var panels = Array.prototype.slice.call(group.querySelectorAll('[role="tabpanel"]'));
    if (!tabs.length || tabs.length !== panels.length) return;

    function selectTab(nextTab, moveFocus) {
      tabs.forEach(function (tab, idx) {
        var active = tab === nextTab;
        tab.setAttribute("aria-selected", active ? "true" : "false");
        if (active) {
          tab.setAttribute("focusgroupstart", "");
          tab.removeAttribute("tabindex");
        } else {
          tab.removeAttribute("focusgroupstart");
          if (!hasNativeFocusGroup) tab.setAttribute("tabindex", "-1");
        }
        var panel = panels[idx];
        if (active) {
          panel.hidden = false;
          panel.removeAttribute("hidden");
          panel.setAttribute("tabindex", "0");
        } else {
          panel.hidden = "until-found";
          panel.removeAttribute("tabindex");
        }
      });
      try {
        nextTab.scrollIntoView({ block: "nearest", inline: "nearest", container: "nearest" });
      } catch (_) {
        nextTab.scrollIntoView({ block: "nearest", inline: "nearest" });
      }
      if (moveFocus) nextTab.focus();
    }

    tabs.forEach(function (tab, idx) {
      if (tab.getAttribute("aria-selected") !== "true" && !hasNativeFocusGroup) {
        tab.setAttribute("tabindex", "-1");
      }
      tab.addEventListener("click", function () {
        selectTab(tab, false);
      });
      tab.addEventListener("focus", function () {
        if (tab.getAttribute("aria-selected") !== "true") {
          selectTab(tab, false);
        }
      });
      if (!hasNativeFocusGroup) {
        tab.addEventListener("keydown", function (e) {
          var targetIdx = -1;
          if (e.key === "ArrowRight") targetIdx = (idx + 1) % tabs.length;
          else if (e.key === "ArrowLeft") targetIdx = (idx - 1 + tabs.length) % tabs.length;
          else if (e.key === "Home") targetIdx = 0;
          else if (e.key === "End") targetIdx = tabs.length - 1;
          if (targetIdx >= 0) {
            e.preventDefault();
            selectTab(tabs[targetIdx], true);
          }
        });
      }
    });

    group.addEventListener("beforematch", function (e) {
      var matchedPanel = e.target.closest ? e.target.closest('[role="tabpanel"]') : null;
      if (!matchedPanel) return;
      var matchedIdx = panels.indexOf(matchedPanel);
      if (matchedIdx >= 0) selectTab(tabs[matchedIdx], false);
    });
  });

  // 2. Ozel onizleme (early access waitlist) formu
  var form = document.getElementById("bekleme");
  if (form) {
    var input = form.querySelector('input[name="email"]');
    var statusEl = document.getElementById("beklemeyanit");
    var submitBtn = form.querySelector('button[type="submit"]');
    var touched = false;

    function validEmail(val) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(val) && val.length <= 180;
    }

    if (input && statusEl) {
      input.addEventListener("input", function () {
        if (input.getAttribute("aria-invalid") === "true" && validEmail(input.value.trim())) {
          input.removeAttribute("aria-invalid");
          statusEl.textContent = "";
          statusEl.className = "form-status";
        }
      });

      input.addEventListener("blur", function () {
        var v = input.value.trim();
        if (!v) return;
        touched = true;
        if (!validEmail(v)) {
          input.setAttribute("aria-invalid", "true");
          statusEl.textContent = MSG.hatali;
          statusEl.className = "form-status error";
        }
      });

      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var adres = input.value.trim().toLowerCase();
        if (!validEmail(adres)) {
          touched = true;
          input.setAttribute("aria-invalid", "true");
          statusEl.textContent = MSG.hatali;
          statusEl.className = "form-status error";
          input.focus();
          return;
        }
        input.removeAttribute("aria-invalid");
        if (submitBtn) submitBtn.disabled = true;
        statusEl.textContent = MSG.gonderiliyor;
        statusEl.className = "form-status";

        fetch("/api/waitlist", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ email: adres, lang: tr ? "tr" : "en", via: "private-preview" }),
        })
          .then(function (r) {
            return r.json().then(function (j) {
              return { ok: r.ok, j: j };
            });
          })
          .then(function (res) {
            if (res.ok && res.j) {
              statusEl.textContent = res.j.kayitli ? MSG.zatenKayitli : MSG.bekliyoruz;
              statusEl.className = "form-status ok";
              input.disabled = true;
            } else {
              if (submitBtn) submitBtn.disabled = false;
              statusEl.textContent = MSG.hata;
              statusEl.className = "form-status error";
            }
          })
          .catch(function () {
            if (submitBtn) submitBtn.disabled = false;
            statusEl.textContent = MSG.hata;
            statusEl.className = "form-status error";
          });
      });
    }
  }
})();
