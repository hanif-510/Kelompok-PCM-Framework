from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Berita, PesanMasuk


def buat_berita(judul='Berita', status='terbit', selisih_hari=-1):
    return Berita.objects.create(
        judul=judul,
        ringkasan='Ringkasan',
        isi='Isi berita',
        status=status,
        tanggal_terbit=timezone.now() + timedelta(days=selisih_hari),
    )


class HalamanPublikTest(TestCase):
    def test_semua_halaman_publik_200(self):
        for nama in ['beranda', 'profil', 'pimpinan', 'ranting', 'amal_usaha',
                     'daftar_berita', 'agenda', 'unduhan', 'kontak']:
            with self.subTest(halaman=nama):
                response = self.client.get(reverse(f'web:{nama}'))
                self.assertEqual(response.status_code, 200)

    def test_detail_berita_terbit_200(self):
        berita = buat_berita()
        response = self.client.get(reverse('web:detail_berita', args=[berita.slug]))
        self.assertEqual(response.status_code, 200)


class BeritaTest(TestCase):
    def test_berita_draf_404(self):
        berita = buat_berita(status='draf')
        response = self.client.get(reverse('web:detail_berita', args=[berita.slug]))
        self.assertEqual(response.status_code, 404)

    def test_berita_tanggal_masa_depan_404(self):
        berita = buat_berita(selisih_hari=5)
        response = self.client.get(reverse('web:detail_berita', args=[berita.slug]))
        self.assertEqual(response.status_code, 404)

    def test_slug_tetap_unik_untuk_judul_sama(self):
        a = buat_berita(judul='Pengajian')
        b = buat_berita(judul='Pengajian')
        self.assertNotEqual(a.slug, b.slug)

    def test_paginasi_6_per_halaman(self):
        for i in range(7):
            buat_berita(judul=f'Berita {i}')
        response = self.client.get(reverse('web:daftar_berita'))
        self.assertEqual(len(response.context['page_obj']), 6)
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 2)


class KontakTest(TestCase):
    def test_formulir_menyimpan_pesan(self):
        response = self.client.post(reverse('web:kontak'), {
            'nama': 'Budi',
            'email': 'budi@contoh.com',
            'subjek': 'Tanya kegiatan',
            'pesan': 'Kapan pengajian berikutnya diadakan?',
        })
        self.assertRedirects(response, reverse('web:kontak'))
        self.assertEqual(PesanMasuk.objects.count(), 1)

    def test_pesan_terlalu_pendek_ditolak(self):
        self.client.post(reverse('web:kontak'), {
            'nama': 'Budi', 'email': 'budi@contoh.com',
            'subjek': 'Hai', 'pesan': 'pendek',
        })
        self.assertEqual(PesanMasuk.objects.count(), 0)
