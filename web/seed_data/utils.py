from pathlib import Path

from django.core.files import File

FOLDER_SEED = Path(__file__).resolve().parent
FOLDER_GAMBAR = FOLDER_SEED / 'gambar'
FOLDER_BERKAS = FOLDER_SEED / 'berkas'


def pasang_berkas(objek, nama_field, nama_berkas, folder=FOLDER_GAMBAR):
    """Pasang berkas dari folder seed ke field model.

    Dilewati jika nama berkas kosong, berkas tidak ditemukan, atau field sudah
    berisi (misalnya gambar yang sudah diganti pengurus lewat admin).
    Mengembalikan True jika berkas terpasang.
    """
    if not nama_berkas:
        return False
    field = getattr(objek, nama_field)
    if field:
        return False
    sumber = folder / nama_berkas
    if not sumber.exists():
        return False
    with sumber.open('rb') as berkas:
        field.save(nama_berkas, File(berkas), save=True)
    return True
