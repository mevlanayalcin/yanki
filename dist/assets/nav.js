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
})();
