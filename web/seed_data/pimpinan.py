from web.models import Pimpinan

PERIODE = '2022-2027'
PERIODE_BELUM_ADA = 'belum tersedia'

# Sumber: SK Pimpinan Cabang Muhammadiyah Kecamatan Gatak Nomor 005/KEP/IV.0/2023
# (ditetapkan di Sukoharjo, 16 Oktober 2023) tentang Penetapan Ketua, Sekretaris,
# Bendahara, dan Anggota Majelis Periode Muktamar ke-48 (2022-2027).
# Yang ditampilkan: Ketua dan Sekretaris PCM (dari tanda tangan SK) serta
# Ketua, Sekretaris, dan Bendahara tiap majelis. Anggota majelis tidak
# dimasukkan supaya halaman tetap ringkas. Foto dikosongkan sampai ada izin.
# NBM tidak ditampilkan karena termasuk data identitas anggota.
JABATAN_PIMPINAN = [
    ('Drs. H. Rombe Mustajab, M.Hum.', 'Ketua PCM Gatak'),
    ('Drs. Shodiq Purnomo, M.M.', 'Sekretaris PCM Gatak'),
]

# (nama majelis, ketua, [sekretaris...], bendahara)
# Ketua Dikdasmen memakai jabatan lama supaya tidak menggandakan data yang
# sudah ada di database.
MAJELIS = [
    ('Majelis Tabligh & Tarjih', 'Agus M. Sholeh, S.Ag.',
     ['Fauzi Nugroho, S.Pd.I.', 'Ahmad Balya'], 'Matrukin, S.Pd.'),
    ('Majelis Dikdasmen & Pendidikan Non Formal', 'Drs. H. Sriyadi',
     ['Drs. H. Mahfud, M.Pd.', 'Amin Bambang P, S.Pd.'], 'Salim, S.Pd.'),
    ('Majelis Ekonomi, Bisnis & Pariwisata', 'Hengki Pranowo Wibowo, S.E.',
     ['Chamzi Rahmad, S.Ag., S.Pd.', 'Nur Wahid, S.Ag.'],
     "Hasim Asy'ari, S.T., M.T."),
    ('Majelis Pendayagunaan Wakaf dan Kehartabendaan', 'H. Muchsinun',
     ['Wahyudi, S.Sos.'], 'Sapta Marjanta, S.Sos.'),
    ('Majelis Pengembangan Kader dan Ranting', 'Ali Faizal Al Halimi, S.E.',
     ['Suhardiman, S.Pd.I.'], 'Taufik Hidayat, S.E.'),
    ('Majelis Pembinaan, Pemberdayaan Masyarakat, dan Kesejahteraan Sosial',
     'Edy Nuryanto, S.Ag.', ['Haryanto, S.Pd.'], 'Bambang Sigit NC, M.Pd.'),
    ('Majelis PKU, Lingkungan Hidup & Penanggulangan Bencana',
     'dr. Nur Hidayat, S.PD', ['Joko Santoso, S.Pd.'], 'Surahman'),
    ('Majelis Hukum & HAM', 'Mustamil, S.Hi., M.M.',
     ['Djayendra Dewa, S.E., M.M.'], 'Heri Abidin Kurniawan'),
    ('Majelis Pustaka dan Informasi', 'Agus Widodo, S.Pd., M.Pd.',
     ['Lutfi Darmawan, S.Sos.', 'Antok Budi Wiratmojo, S.Pd.'],
     'Wasis Suharto, S.Si., M.Pd.'),
]


def _susun_data():
    data = []
    urutan = 1
    for nama, jabatan in JABATAN_PIMPINAN:
        data.append({'nama': nama, 'jabatan': jabatan, 'urutan': urutan})
        urutan += 1
    for i, (majelis, ketua, sekretaris, bendahara) in enumerate(MAJELIS, 1):
        # 'Majelis Dikdasmen ...' dipertahankan dengan jabatan lama.
        label = 'Majelis Dikdasmen' if 'Dikdasmen' in majelis else majelis
        akhiran = ' PCM Gatak'
        urutan = i * 10
        data.append({'nama': ketua, 'jabatan': f'Ketua {label}{akhiran}',
                     'urutan': urutan})
        for n, nama in enumerate(sekretaris, 1):
            tanda = f' {n}' if len(sekretaris) > 1 else ''
            data.append({'nama': nama,
                         'jabatan': f'Sekretaris{tanda} {label}{akhiran}',
                         'urutan': urutan + n})
        data.append({'nama': bendahara,
                     'jabatan': f'Bendahara {label}{akhiran}',
                     'urutan': urutan + len(sekretaris) + 1})
    return data


DATA = _susun_data()


def seed():
    dibuat = 0
    for data in DATA:
        objek, baru = Pimpinan.objects.get_or_create(
            nama=data['nama'],
            jabatan=data['jabatan'],
            defaults={'periode': PERIODE, 'urutan': data['urutan']},
        )
        # Baris lama berperiode placeholder dilengkapi; hasil edit admin aman.
        if not baru and objek.periode == PERIODE_BELUM_ADA:
            objek.periode = PERIODE
            objek.save(update_fields=['periode'])
        dibuat += baru
    return dibuat