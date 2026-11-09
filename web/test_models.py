from datetime import timedelta

from django.contrib import admin
from django.test import RequestFactory, TestCase
from django.utils import timezone

from .admin import PesanMasukAdmin, ProfilAdmin
from .models import Berita, Profil


def buat_berita(judul='Berita', status='terbit', selisih_hari=-1):
    return Berita.objects.create(
        judul=judul,
        ringkasan='Ringkasan',
        isi='Isi berita',
        status=status,
        tanggal_terbit=timezone.now() + timedelta(days=selisih_hari),
    )


class BeritaQuerySetTest(TestCase):
    def test_terbit_hanya_berita_terbit_yang_tanggalnya_sudah_tiba(self):
        tayang = buat_berita('Tayang')
        buat_berita('Masih draf', status='draf')
        buat_berita('Terjadwal', selisih_hari=3)

        self.assertEqual(list(Berita.objects.terbit()), [tayang])

    def test_terbit_diurutkan_dari_yang_terbaru(self):
        lama = buat_berita('Lama', selisih_hari=-5)
        baru = buat_berita('Baru', selisih_hari=-1)

        self.assertEqual(list(Berita.objects.terbit()), [baru, lama])


class BeritaSlugTest(TestCase):
    def test_judul_sama_menghasilkan_slug_berurutan(self):
        slugs = [buat_berita('Judul Sama').slug for _ in range(3)]
        self.assertEqual(slugs, ['judul-sama', 'judul-sama-2', 'judul-sama-3'])

    def test_slug_tidak_berubah_saat_judul_diedit(self):
        berita = buat_berita('Judul Awal')
        berita.judul = 'Judul Baru'
        berita.save()
        berita.refresh_from_db()

        self.assertEqual(berita.slug, 'judul-awal')

    def test_judul_tanpa_huruf_memakai_slug_cadangan(self):
        self.assertEqual(buat_berita('!!!').slug, 'berita')

    def test_slug_muat_di_kolom_untuk_judul_terpanjang(self):
        # Regresi: SlugField bawaan hanya 50 karakter dan ditolak PostgreSQL.
        batas_slug = Berita._meta.get_field('slug').max_length
        batas_judul = Berita._meta.get_field('judul').max_length
        judul_panjang = 'a' * batas_judul

        pertama = buat_berita(judul_panjang)
        kedua = buat_berita(judul_panjang)

        self.assertGreaterEqual(batas_slug, batas_judul)
        self.assertLessEqual(len(kedua.slug), batas_slug)
        self.assertTrue(kedua.slug.endswith('-2'))
        self.assertNotEqual(pertama.slug, kedua.slug)


class AdminTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')

    def test_profil_tidak_bisa_ditambah_jika_sudah_ada(self):
        model_admin = ProfilAdmin(Profil, admin.site)
        self.assertTrue(model_admin.has_add_permission(self.request))

        Profil.objects.create(nama='PCM Gatak', nama_singkat='PCM Gatak')

        self.assertFalse(model_admin.has_add_permission(self.request))

    def test_profil_tidak_bisa_dihapus(self):
        model_admin = ProfilAdmin(Profil, admin.site)
        self.assertFalse(model_admin.has_delete_permission(self.request))

    def test_pesan_masuk_tidak_bisa_ditambah_dari_admin(self):
        from .models import PesanMasuk

        model_admin = PesanMasukAdmin(PesanMasuk, admin.site)
        self.assertFalse(model_admin.has_add_permission(self.request))
