"""Data seed per modul. Tiap modul punya fungsi seed() yang mengembalikan
jumlah data baru, dan hanya membuat data yang belum ada (idempotent).

Pembagian pengisian data:
- profil, pimpinan, ranting, amal_usaha, tautan, dokumen : Valen
- berita, agenda                                         : Hanif
"""

from . import agenda, amal_usaha, berita, dokumen, pimpinan, profil, ranting, tautan

MODUL_SEED = [
    ('Profil', profil.seed),
    ('Pimpinan', pimpinan.seed),
    ('Ranting', ranting.seed),
    ('Amal usaha', amal_usaha.seed),
    ('Tautan terkait', tautan.seed),
    ('Dokumen', dokumen.seed),
    ('Berita', berita.seed),
    ('Agenda', agenda.seed),
]
