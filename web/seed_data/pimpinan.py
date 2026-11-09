from web.models import Pimpinan

PERIODE_BELUM_ADA = 'belum tersedia'

# Hanya nama yang punya sumber publik. Foto dikosongkan sampai ada izin.
# Susunan lengkap belum ditemukan, minta SK pengurus ke sekretariat PCM.
DATA = [
    {
        'nama': 'Drs. H. Rombe Mustajab, M.Hum.',
        'jabatan': 'Ketua PCM Gatak',
        'urutan': 1,
        # sumber: dimsa.sch.id (1 Feb 2025) dan sukoharjo.aisyiyah.or.id (Jun 2025)
    },
    {
        'nama': 'Drs. H. Sriyadi',
        'jabatan': 'Ketua Majelis Dikdasmen PCM Gatak',
        'urutan': 2,
        # sumber: dimsa.sch.id (1 Feb 2025) dan sukoharjo.aisyiyah.or.id (4 Feb 2026)
    },
]


def seed():
    dibuat = 0
    for data in DATA:
        _, baru = Pimpinan.objects.get_or_create(
            nama=data['nama'],
            jabatan=data['jabatan'],
            defaults={'periode': PERIODE_BELUM_ADA, 'urutan': data['urutan']},
        )
        dibuat += baru
    return dibuat
