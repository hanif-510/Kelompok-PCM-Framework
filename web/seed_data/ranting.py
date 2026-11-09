from web.models import Ranting

# Nama ranting yang disebut di sumber. Daftar lengkap 14 ranting belum ada.
# TODO (Valen): verifikasi ke pengurus lalu lengkapi. Ketua dan alamat
# dikosongkan, jangan isi nomor HP atau alamat rumah pribadi.
DATA = [
    {'nama': 'Sraten'},
    {'nama': 'Wironanggan'},
    {'nama': 'Trangsan'},
    {'nama': 'Blimbing'},
    {'nama': 'Tempel'},
    {'nama': 'Luwang'},
]


def seed():
    dibuat = 0
    for data in DATA:
        _, baru = Ranting.objects.get_or_create(nama=data['nama'])
        dibuat += baru
    return dibuat
