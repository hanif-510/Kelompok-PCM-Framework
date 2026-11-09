from web.models import Agenda

# TODO (Hanif): isi agenda riil. Contoh entri:
# {
#     'nama': '...',
#     'waktu_mulai': datetime(2026, 11, 15, 8, 0, tzinfo=timezone.utc),
#     'tempat': '...',
#     'keterangan': '...',
# }
DATA = []


def seed():
    dibuat = 0
    for data in DATA:
        _, baru = Agenda.objects.get_or_create(
            nama=data['nama'],
            waktu_mulai=data['waktu_mulai'],
            defaults={
                'tempat': data.get('tempat', ''),
                'keterangan': data.get('keterangan', ''),
            },
        )
        dibuat += baru
    return dibuat
