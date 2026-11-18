/* Język strony dla tego gościa: wybrany wcześniej z listy (zapamiętany), a jeśli go nie ma — pierwszy
   z języków przeglądarki, który strona obsługuje. A = {kod: adres}. Zwraca kod albo null. */
function sbJezyk(A, pomijajRoboty) {
  var j = null;
  try { j = localStorage.getItem("jezyk"); } catch (e) {}
  if (j && A[j]) return j;
  if (pomijajRoboty && /bot|crawl|spider|slurp|lighthouse|preview/i.test(navigator.userAgent)) return null;
  var l = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ""];
  for (var i = 0; i < l.length; i++) {
    var k = String(l[i]).toLowerCase().slice(0, 2);
    if (k === "in") k = "id";                     // dawny kod indonezyjskiego w Androidzie
    if (A[k]) return k;
  }
  return null;
}
