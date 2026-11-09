from web.models import AmalUsaha

from .utils import pasang_berkas

# TODO (Valen): tambahkan amal usaha lain (TK ABA, MI, SMP, SMA, PAUD) setelah
# diverifikasi. Contoh entri dengan gambar: tambahkan 'gambar': 'mbs.jpg' lalu
# taruh berkasnya di web/seed_data/gambar/ (hanya jika ada izin pemakaian).
DATA = [
    {
        'nama': 'Muhammadiyah Boarding School (MBS) Gatak',
        'bidang': 'pendidikan',
        'deskripsi': (
            'Pondok pesantren modern berbasis Muhammadiyah yang berawal dari '
            'wakaf tanah pada tahun 2003.'
        ),
    },
]


def seed():
    dibuat = 0
    for data in DATA:
        data = dict(data)
        nama_gambar = data.pop('gambar', '')
        objek, baru = AmalUsaha.objects.get_or_create(
            nama=data.pop('nama'), defaults=data
        )
        pasang_berkas(objek, 'gambar', nama_gambar)
        dibuat += baru
    return dibuat
