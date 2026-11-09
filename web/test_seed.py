from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from .models import AmalUsaha, Pimpinan, Profil, Ranting, TautanTerkait

MODEL_SEED = (Profil, Pimpinan, Ranting, AmalUsaha, TautanTerkait)


def jalankan_seed():
    call_command('seed_pcm', stdout=StringIO())


class SeedPcmTest(TestCase):
    def test_seed_berulang_tidak_menggandakan_data(self):
        jalankan_seed()
        jumlah_awal = {model: model.objects.count() for model in MODEL_SEED}

        jalankan_seed()

        for model, jumlah in jumlah_awal.items():
            with self.subTest(model=model.__name__):
                self.assertEqual(model.objects.count(), jumlah)

    def test_seed_mengisi_profil_satu_baris(self):
        jalankan_seed()
        self.assertEqual(Profil.objects.count(), 1)

    def test_seed_ulang_tidak_menimpa_hasil_edit_admin(self):
        jalankan_seed()
        ranting = Ranting.objects.first()
        ranting.ketua = 'Diedit pengurus'
        ranting.save()

        jalankan_seed()

        ranting.refresh_from_db()
        self.assertEqual(ranting.ketua, 'Diedit pengurus')
