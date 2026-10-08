// Mobil menuyu acar/kapatir. Etiket dilde kalmali, bu yuzden yola bakilir.
(function () {
  var dugme = document.getElementById("menudugme");
  var menu = document.getElementById("menu");
  if (!dugme || !menu) return;
  var tr = location.pathname.indexOf("/tr/") === 0;
  var etiketler = tr ? ["Menü", "Kapat"] : ["Menu", "Close"];
  dugme.textContent = etiketler[0];
  dugme.addEventListener("click", function () {
    var acik = menu.classList.toggle("acik");
    dugme.setAttribute("aria-expanded", acik ? "true" : "false");
    dugme.textContent = acik ? etiketler[1] : etiketler[0];
  });
  menu.addEventListener("click", function (olay) {
    if (!olay.target.closest("a")) return;
    menu.classList.remove("acik");
    dugme.setAttribute("aria-expanded", "false");
    dugme.textContent = etiketler[0];
  });
  document.addEventListener("keydown", function (olay) {
    if (olay.key !== "Escape" || !menu.classList.contains("acik")) return;
    menu.classList.remove("acik");
    dugme.setAttribute("aria-expanded", "false");
    dugme.textContent = etiketler[0];
    dugme.focus();
  });
})();
