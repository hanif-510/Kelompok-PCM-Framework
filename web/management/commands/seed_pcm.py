from django.core.management.base import BaseCommand
from django.db import transaction

from web.seed_data import MODUL_SEED


class Command(BaseCommand):
    help = (
        'Mengisi database dengan data riil PCM Gatak. Aman dijalankan berulang '
        'kali: data yang sudah ada tidak ditimpa, jadi hasil edit lewat admin '
        'tetap terjaga.'
    )

    def handle(self, *args, **options):
        with transaction.atomic():
            for label, seed in MODUL_SEED:
                dibuat = seed()
                self.stdout.write(f'{label}: {dibuat} data baru')
        self.stdout.write(self.style.SUCCESS('seed_pcm selesai.'))
