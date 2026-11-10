/* Pengalih tema terang/gelap untuk Website PCM Gatak.
   Dimuat di <head> tanpa defer, supaya tema terpasang sebelum halaman
   digambar dan layar tidak berkedip saat dibuka.
   Tema bawaan adalah gelap. Pilihan pengunjung disimpan di localStorage
   dengan kunci "tema-pcm", jadi tetap sama saat pindah halaman atau
   membuka situs lagi. */
(function () {
  var KUNCI = 'tema-pcm';
  var akar = document.documentElement;

  function bacaPilihan() {
    try {
      return localStorage.getItem(KUNCI);
    } catch (galat) {
      return null; // penyimpanan diblokir: pakai tema bawaan
    }
  }

  function simpanPilihan(tema) {
    try {
      localStorage.setItem(KUNCI, tema);
    } catch (galat) {
      /* abaikan: tema tetap berganti, hanya tidak diingat */
    }
  }

  function temaSekarang() {
    return akar.getAttribute('data-tema') === 'terang' ? 'terang' : 'gelap';
  }

  function terapkan(tema) {
    if (tema === 'terang') {
      akar.setAttribute('data-tema', 'terang');
    } else {
      akar.removeAttribute('data-tema'); // gelap = bawaan CSS
    }
    var tombol = document.querySelector('.tombol-tema');
    if (tombol) {
      var label = tema === 'terang' ? 'Ganti ke tema gelap' : 'Ganti ke tema terang';
      tombol.setAttribute('aria-label', label);
      tombol.setAttribute('title', label);
    }
  }

  // 1. Pasang tema yang tersimpan secepat mungkin.
  terapkan(bacaPilihan() === 'terang' ? 'terang' : 'gelap');

  // 2. Setelah halaman siap, sambungkan tombol di header.
  document.addEventListener('DOMContentLoaded', function () {
    var tombol = document.querySelector('.tombol-tema');
    if (!tombol) return;

    terapkan(temaSekarang()); // perbarui label tombol
    tombol.addEventListener('click', function () {
      var berikutnya = temaSekarang() === 'terang' ? 'gelap' : 'terang';
      terapkan(berikutnya);
      simpanPilihan(berikutnya);
    });
  });
})();