from web.models import Profil

# TODO (Valen): lengkapi visi, misi, sejarah, alamat sekretariat, dan kontak
# resmi setelah dapat dari pengurus. Jangan mengarang. Tulis 'belum tersedia'
# untuk data yang belum ada.
DATA = {
    'nama': 'Pimpinan Cabang Muhammadiyah Gatak',
    'nama_singkat': 'PCM Gatak',
    'tagline': '',
    'tentang': (
        'PCM Gatak berada di Kecamatan Gatak, Kabupaten Sukoharjo, Jawa Tengah.'
    ),
    'alamat': 'belum tersedia',
}


def seed():
    # Profil hanya boleh satu baris, jadi jangan buat lagi jika sudah ada.
    if Profil.objects.exists():
        return 0
    Profil.objects.create(**DATA)
    return 1
