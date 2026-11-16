from web.models import Ranting

# Sumber: "Daftar Ketua/Perwakilan PRM se-Kec. Gatak, Kab. Sukoharjo" (PCM Gatak).
# Nomor WA ketua sengaja tidak dimasukkan karena itu nomor pribadi dan halaman
# ranting bersifat publik. Isi kolom telepon hanya dengan kontak resmi.
# Ranting Sanggung: menurut catatan di dokumen sumber belum ada kepengurusan,
# jadi ketua dikosongkan.
DATA = [
    {'nama': 'Tempel', 'ketua': 'Wahyudi, S.Sos'},
    {'nama': 'Sraten', 'ketua': 'Drs. Mahfud, M.Pd.'},
    {'nama': 'Wironanggan', 'ketua': 'Drs. Supardi, M.Pd.'},
    {'nama': 'Trangsan', 'ketua': 'Muchsinun'},
    {'nama': 'Mayang', 'ketua': 'Wasis Suharto, M.Pd.'},
    {'nama': 'Klaseman', 'ketua': 'Meizhar, S.Ag.'},
    {'nama': 'Luwang', 'ketua': 'Saibani, S.Pd.'},
    {'nama': 'Sanggung'},
    {'nama': 'Kagokan', 'ketua': 'Markaban, S.Ag.'},
    {'nama': 'Blimbing', 'ketua': 'Heri Abidin Kurniawan'},
    {'nama': 'Trosemi', 'ketua': 'Drs. Wiyono'},
    {'nama': 'Jati', 'ketua': 'Wanto, A.Md.'},
    {'nama': 'Geneng', 'ketua': 'Subur Aribowo, ST'},
    {'nama': 'Krajan', 'ketua': 'Ir. Kardoyo'},
]


def seed():
    """Buat ranting yang belum ada, dan isi ketua yang masih kosong.

    Ketua yang sudah terisi (misalnya hasil edit pengurus lewat admin)
    tidak ditimpa.
    """
    berubah = 0
    for data in DATA:
        ranting, baru = Ranting.objects.get_or_create(
            nama=data['nama'], defaults={'ketua': data.get('ketua', '')}
        )
        if baru:
            berubah += 1
        elif data.get('ketua') and not ranting.ketua:
            ranting.ketua = data['ketua']
            ranting.save(update_fields=['ketua'])
            berubah += 1
    return berubah