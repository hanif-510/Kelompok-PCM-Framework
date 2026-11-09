from web.models import TautanTerkait

# TODO (Valen): tambahkan website resmi PDM Sukoharjo dan PWM Jawa Tengah
# setelah domain resminya dibuka dan dipastikan bisa diakses.
DATA = [
    {'nama': 'Muhammadiyah', 'url': 'https://muhammadiyah.or.id', 'urutan': 1},
]


def seed():
    dibuat = 0
    for data in DATA:
        _, baru = TautanTerkait.objects.get_or_create(
            nama=data['nama'],
            defaults={'url': data['url'], 'urutan': data['urutan']},
        )
        dibuat += baru
    return dibuat
