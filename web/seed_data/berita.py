from web.models import Berita

from .utils import pasang_berkas

# TODO (Hanif): isi berita riil beserta gambarnya. Contoh entri:
# {
#     'judul': '...',
#     'ringkasan': '...',
#     'isi': '...',
#     'tanggal_terbit': datetime(2026, 5, 8, 12, 0, tzinfo=timezone.utc),
#     'gambar': 'nama-berkas.jpg',   # taruh di web/seed_data/gambar/
# }
# Status otomatis 'terbit'. Pakai foto hanya jika ada izin dan sebut kreditnya.
DATA = []


def seed():
    dibuat = 0
    for data in DATA:
        data = dict(data)
        nama_gambar = data.pop('gambar', '')
        objek, baru = Berita.objects.get_or_create(
            judul=data.pop('judul'),
            defaults={'status': 'terbit', **data},
        )
        pasang_berkas(objek, 'gambar', nama_gambar)
        dibuat += baru
    return dibuat
