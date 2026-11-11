# Website PCM Gatak

Website resmi Pimpinan Cabang Muhammadiyah (PCM) Gatak, Kabupaten Sukoharjo, Jawa Tengah.

## Kelompok

| No | Nama | NIM |
|----|------|-----|
| 1 | Raden Bagus Indra Wijaya Nugraha | L200240003 |
| 2 | Muhammad Valentino Khansa | L200240016 |
| 3 | Muhammad Afif Haravi | L200240018 |
| 4 | Hanif | L200240048 |
| 5 | Sandy Matin Falah | L200240052 |

## PCM yang Dipilih

- **Nama:** PCM Gatak
- **Wilayah:** Kecamatan Gatak, Kabupaten Sukoharjo, Jawa Tengah
- **Tujuan website:** Website ini dibuat untuk memperkenalkan PCM Gatak kepada masyarakat sekaligus menjadi sarana publikasi berita, agenda, dan dokumen, serta menerima pesan dari masyarakat melalui formulir kontak. Seluruh isinya dapat dikelola pengurus lewat panel admin tanpa mengubah kode.

### Sumber Data

| Data | Sumber | Tanggal diambil | Pemberi izin |
|------|--------|-----------------|--------------|
| Logo Muhammadiyah | Wikimedia Commons | TODO | - |
| Profil, struktur pimpinan, ranting, amal usaha | TODO | TODO | TODO |
| Berita dan agenda | TODO | TODO | TODO |
| Foto | TODO | TODO | TODO |

## Kontribusi Anggota

| Nama | Kontribusi |
|------|------------|
| Raden Bagus Indra Wijaya Nugraha | Backend, database, dan deployment: konfigurasi settings berbasis environment variable, WhiteNoise untuk file statis, database PostgreSQL di Supabase, migrasi dan seeding data produksi, penyimpanan media ke object storage S3, serta HSTS dan pengecekan `check --deploy`. |
| Muhammad Valentino Khansa | TODO |
| Muhammad Afif Haravi | TODO |
| Hanif | struktur awal website PCM Gatak, UI dan navigasi menu, penyesuaian tampilan/CSS. Implementasi Docker melalui Dockerfile, .dockerignore, dan Docker Compose untuk menjalankan Django dan PostgreSQL. Pengujian build image dan container, konfigurasi permission & startup, migrasi database, memastikan website berjalan melalui localhost:8000 menggunakan Gunicorn. |
| Sandy Matin Falah | TODO |

## Produksi

| Item | Pilihan | Alasan |
|------|---------|--------|
| URL produksi | TODO | Harus tetap menyala sampai penilaian selesai |
| Platform | TODO | TODO |
| Database | PostgreSQL di Supabase (Session pooler, port 5432) | Database terkelola dan gratis. Session pooler mendukung IPv4 dan cocok dengan koneksi Django biasa |
| Penyimpanan gambar | Supabase Storage lewat endpoint S3 dan `django-storages` | Disk server platform deploy tidak permanen, sehingga gambar upload akan hilang setelah redeploy jika disimpan lokal |

## Cara Menjalankan

### Dengan uv (di laptop)

Prasyarat: Python 3.14 atau lebih baru dan [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/hanif-510/Kelompok-PCM-Framework.git
cd Kelompok-PCM-Framework
cp .env.example .env      # lalu isi nilainya, minimal SECRET_KEY
uv sync
uv run python manage.py migrate
uv run python manage.py seed_pcm
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Buka `http://localhost:8000`. Panel admin ada di `http://localhost:8000/admin/`.

Jika `DATABASE_URL` dan `STORAGE_BUCKET` dikosongkan, proyek memakai SQLite dan folder `media/` lokal.

### Dengan Docker

Docker telah dikonfigurasi menggunakan Dockerfile dan compose.yaml untuk menjalankan aplikasi Django dan PostgreSQL dalam container.

Prasyarat: Docker Desktop sudah terpasang dan berjalan.

```bash
cp .env.example .env      # lalu isi nilainya
docker compose up --build
```

Buka `http://localhost:8000`.

Panel admin tersedia di `http://localhost:8000/admin/`.

Untuk mengisi data awal PCM Gatak:

```bash
docker compose exec web uv run --no-sync python manage.py seed_pcm
```

Untuk membuat akun administrator:

```bash
docker compose exec web uv run --no-sync python manage.py createsuperuser
```

Untuk menghentikan container:

```bash
docker compose down
```

Untuk menghentikan container sekaligus menghapus volume database dan media:

```bash
docker compose down -v
```

**Catatan:** Perintah `docker compose down -v` akan menghapus volume database dan media yang tersimpan di Docker.

## Environment Variable

Daftar lengkap ada di [`.env.example`](.env.example). Jangan commit file `.env` yang berisi nilai asli.

| Variabel | Fungsi |
|----------|--------|
| `SECRET_KEY` | Kunci rahasia Django. Wajib diisi |
| `DEBUG` | Mode debug. Bawaannya `False` |
| `ALLOWED_HOSTS` | Daftar host yang diizinkan, dipisah koma |
| `CSRF_TRUSTED_ORIGINS` | Daftar origin tepercaya untuk CSRF, dipisah koma |
| `HTTPS_ONLY` | `True` hanya di server HTTPS. Mengaktifkan redirect SSL, cookie aman, dan HSTS |
| `HSTS_SECONDS` | Durasi HSTS dalam detik. Mulai dari 3600, naikkan setelah HTTPS terbukti stabil |
| `DATABASE_URL` | URL PostgreSQL. Kosong berarti SQLite lokal |
| `STORAGE_BUCKET` | Nama bucket. Kosong berarti media disimpan di folder lokal |
| `STORAGE_ENDPOINT` | Endpoint S3 dari Supabase Storage |
| `STORAGE_REGION` | Region bucket |
| `STORAGE_ACCESS_KEY` | Access key S3 |
| `STORAGE_SECRET_KEY` | Secret key S3 |
| `STORAGE_PUBLIC_DOMAIN` | Domain publik bucket tanpa `https://`, dipakai untuk membentuk URL gambar |

Semua variabel `STORAGE_*` selain `STORAGE_BUCKET` wajib terisi jika `STORAGE_BUCKET` dipakai. Aplikasi akan berhenti dengan pesan error jika ada yang kosong.

## Fitur

**Halaman publik:** Profil, struktur pimpinan, ranting, amal usaha, berita, agenda, dokumen, tautan terkait, dan formulir kontak.

**Panel admin:** Login admin Django di `/admin/` untuk mengelola semua konten di atas dan membaca pesan masuk dari formulir kontak.

## Akun Admin Demo

Tidak ditulis di repo. Kredensial dikirim terpisah ke dosen melalui Google Classroom.

## Video Demo

TODO

## Slide Presentasi

File PDF ada di [`docs/slides/`](docs/slides/).

## Struktur Repo

```text
.
├── README.md
├── .env.example
├── .gitignore
├── .dockerignore
├── manage.py
├── pyproject.toml
├── uv.lock
├── Dockerfile              
├── compose.yaml            
├── config/                 # settings, urls, wsgi
├── web/
│   ├── management/commands/seed_pcm.py
│   ├── static/web/img/
│   └── ...                 # models, views, admin
├── templates/
└── docs/
    ├── slides/
    └── screenshots/
```
