from web.models import AmalUsaha

from .utils import pasang_berkas

# Sumber: dokumen "Amal usaha yang dimiliki" (PCM Gatak).
# Untuk menambahkan gambar pada satu entri, tambahkan 'gambar': 'nama-berkas.jpg'
# lalu taruh berkasnya di web/seed_data/gambar/ (hanya jika ada izin pemakaian).

PAUD = 'Pendidikan Anak Usia Dini (PAUD).'
TK = 'Taman Kanak-Kanak (TK) Bustanul Athfal \u2018Aisyiyah.'
MI = 'Madrasah Ibtidaiyah Muhammadiyah.'
SMP = 'Sekolah Menengah Pertama (SMP) Muhammadiyah.'
SMA = 'Sekolah Menengah Atas (SMA) Muhammadiyah.'


def _pendidikan(deskripsi, daftar_nama):
    return [
        {'nama': nama, 'bidang': 'pendidikan', 'deskripsi': deskripsi}
        for nama in daftar_nama
    ]


DATA = [
    {
        'nama': 'Muhammadiyah Boarding School (MBS) Gatak',
        'bidang': 'pendidikan',
        'deskripsi': (
            'Pondok pesantren modern berbasis Muhammadiyah yang berawal dari '
            'wakaf tanah pada tahun 2003.'
        ),
    },
    *_pendidikan(PAUD, [
        'PAUD Buana Luwang',
        'PAUD Nur Rohman Blimbing',
        'PAUD Roudhotul Jannah Klaseman',
    ]),
    *_pendidikan(TK, [
        'TK Bustanul Athfal \u2018Aisyiyah Sraten',
        'TK Bustanul Athfal \u2018Aisyiyah Wironanggan',
        'TK Bustanul Athfal \u2018Aisyiyah Trangsan 1',
        'TK Bustanul Athfal \u2018Aisyiyah Trangsan 2',
        'TK Bustanul Athfal \u2018Aisyiyah Luwang 1',
        'TK Bustanul Athfal \u2018Aisyiyah Luwang 2',
        'TK Bustanul Athfal \u2018Aisyiyah Klaseman',
        'TK Bustanul Athfal \u2018Aisyiyah Mayang',
        'TK Bustanul Athfal \u2018Aisyiyah Krajan',
    ]),
    *_pendidikan(MI, [
        'MIM Sraten',
        'MIM Trangsan',
        'MIM Klaseman',
        'MIM Luwang',
        'MIM Mayang',
        'MIM PK Blimbing',
    ]),
    *_pendidikan(SMP, ['SMP Muhammadiyah 1', 'SMP Muhammadiyah 2']),
    {
        'nama': 'MBS Putra Trangsan',
        'bidang': 'pendidikan',
        'deskripsi': 'Muhammadiyah Boarding School putra.',
        'alamat': 'Trangsan',
    },
    {
        'nama': 'MBS Putri Jati',
        'bidang': 'pendidikan',
        'deskripsi': 'Muhammadiyah Boarding School putri.',
        'alamat': 'Jati',
    },
    *_pendidikan(SMA, ['SMA Muhammadiyah 5']),
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