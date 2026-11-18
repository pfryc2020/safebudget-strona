/* Safe Budget — zachowanie strony: menu ☰, lista języków, powiększanie zrzutów. */
(function () {
  "use strict";
  var naglowek = document.getElementById("naglowek");
  var przycisk = document.getElementById("menu-przycisk");
  var menu = document.getElementById("menu");
  var jezyk = document.getElementById("jezyk");

  // ---------------------------------------------------------------- menu ☰
  function ustawMenu(otwarte) {
    naglowek.classList.toggle("otwarte", otwarte);
    przycisk.setAttribute("aria-expanded", otwarte ? "true" : "false");
    przycisk.setAttribute("aria-label", otwarte ? przycisk.getAttribute("data-zamknij") : przycisk.getAttribute("data-otworz"));
  }
  var zamknijMenu = function () { ustawMenu(false); };

  // Odnośniki zwijają się do przycisku ☰, gdy nie mieszczą się w nagłówku — szerokość zależy od języka.
  function dopasuj() {
    if (window.sbDopasuj) window.sbDopasuj();
    if (!naglowek.classList.contains("zwiniete")) zamknijMenu();
  }

  przycisk.addEventListener("click", function () {
    ustawMenu(!naglowek.classList.contains("otwarte"));
    if (jezyk) jezyk.open = false;
  });
  menu.addEventListener("click", function (e) {
    if (e.target.closest("a")) zamknijMenu();
  });
  if (jezyk) {
    jezyk.addEventListener("toggle", function () { if (jezyk.open) zamknijMenu(); });
  }
  document.addEventListener("click", function (e) {
    if (!naglowek.contains(e.target)) zamknijMenu();
    if (jezyk && jezyk.open && !jezyk.contains(e.target)) jezyk.open = false;
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (naglowek.classList.contains("otwarte")) { zamknijMenu(); przycisk.focus(); }
    if (jezyk && jezyk.open) { jezyk.open = false; jezyk.querySelector("summary").focus(); }
  });
  window.addEventListener("resize", dopasuj);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(dopasuj);
  dopasuj();

  // ---------------------------------------------------------------- wybór języka
  // Wybór z listy zapamiętuje się: strona polska nie przekieruje już do języka przeglądarki.
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[data-jezyk]");
    if (!a) return;
    try { localStorage.setItem("jezyk", a.getAttribute("data-jezyk")); } catch (blad) { /* tryb prywatny */ }
  });

  // ---------------------------------------------------------------- powiększanie zrzutów
  var okno = document.getElementById("podglad");
  if (okno && okno.showModal) {
    var obraz = document.getElementById("podglad-img");
    var podpis = document.getElementById("podglad-podpis");
    document.querySelectorAll(".zrzut-btn").forEach(function (b) {
      b.addEventListener("click", function () {
        obraz.src = b.getAttribute("data-src");
        obraz.alt = b.getAttribute("data-podpis");
        podpis.textContent = b.getAttribute("data-podpis");
        okno.showModal();
      });
    });
    okno.addEventListener("click", function (e) { if (e.target === okno) okno.close(); });
  }
})();
