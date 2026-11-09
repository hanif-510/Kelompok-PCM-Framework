from web.models import Dokumen

from .utils import FOLDER_BERKAS, pasang_berkas

# TODO (Valen): isi dengan dokumen yang boleh dipublikasikan. Taruh berkasnya
# di web/seed_data/berkas/. Contoh entri:
# {'judul': 'Judul dokumen', 'keterangan': '...', 'berkas': 'nama-berkas.pdf'}
DATA = []


def seed():
    dibuat = 0
    for data in DATA:
        sumber = FOLDER_BERKAS / data['berkas']
        if not sumber.exists():
            continue  # berkas wajib ada, jadi entri tanpa berkas dilewati
        objek, baru = Dokumen.objects.get_or_create(
            judul=data['judul'],
            defaults={'keterangan': data.get('keterangan', '')},
        )
        pasang_berkas(objek, 'berkas', data['berkas'], folder=FOLDER_BERKAS)
        dibuat += baru
    return dibuat
