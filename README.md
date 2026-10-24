# Website PCM Gatak

Website resmi Pimpinan Cabang Muhammadiyah (PCM) Gatak, Kabupaten Sukoharjo, Jawa Tengah.

<!-- PETUNJUK: Teks di dalam komentar seperti ini tidak tampil di GitHub. Isi bagian bertanda TODO, lalu hapus komentarnya jika sudah selesai. -->

## Kelompok

**Nama kelompok:** TODO

| No | Nama | NIM |
|----|------|-----|
| 1 | Raden Bagus Indra Wijaya Nugraha | L200240003 |
| 2 | Muhammad Valentino Khansa | L200240016 |
| 3 | Muhammad Afif Haravi | L200240018 |
| 4 | Hanif | L200240048 |
| 5 | Sandy Matin Falah | L200240052 |

## PCM yang Dipilih

- **Nama:** PCM Gatak
- **Wilayah:** Kecamatan Gatak, Kabupaten Sukoharjo, Jawa Tengah <!-- cek ulang kebenaran wilayahnya -->
- **Tujuan website:** TODO <!-- 2-3 kalimat: untuk apa website ini dan siapa penggunanya -->

### Sumber Data

<!-- Catat semua data yang dipakai: profil, berita, foto, struktur pengurus, kontak. Tulis nama pengurus yang memberi izin jika ada. -->

| Data | Sumber | Tanggal diambil | Pemberi izin |
|------|--------|-----------------|--------------|
| TODO | TODO | TODO | TODO |

## Kontribusi Anggota

<!-- Isi dengan pekerjaan nyata masing-masing, contoh: desain UI, halaman publik, panel admin, database, deployment, Docker, video, slide, pengumpulan data. -->

| Nama | Kontribusi |
|------|------------|
| Raden Bagus Indra Wijaya Nugraha | TODO |
| Muhammad Valentino Khansa | TODO |
| Muhammad Afif Haravi | TODO |
| Hanif | TODO |
| Sandy Matin Falah | TODO |

## Produksi

| Item | Pilihan | Alasan |
|------|---------|--------|
| URL produksi | TODO | Harus tetap menyala sampai penilaian selesai |
| Platform | TODO | TODO |
| Database | TODO | TODO |
| Penyimpanan gambar | TODO | TODO |

## Cara Menjalankan

### Dengan uv (di laptop)

Prasyarat: Python TODO dan [uv](https://docs.astral.sh/uv/).

```bash
git clone TODO-URL-REPO
cd TODO-NAMA-FOLDER
cp .env.example .env      # lalu isi nilainya
uv sync
uv run TODO-PERINTAH-RUN  # contoh: fastapi dev, flask run, python manage.py runserver
```

Buka `http://localhost:8000` (sesuaikan port).

### Dengan Docker

```bash
cp .env.example .env      # lalu isi nilainya
docker compose up --build
```

Buka `http://localhost:8000` (sesuaikan port).

## Environment Variable

Daftar lengkap ada di [`.env.example`](.env.example). Jangan commit file `.env` yang berisi nilai asli.

| Variabel | Fungsi |
|----------|--------|
| `APP_ENV` | Mode aplikasi (development atau production) |
| `SECRET_KEY` | Kunci rahasia sesi |
| `DATABASE_URL` | Connection string database |
| `ADMIN_USERNAME` | Username admin awal |
| `ADMIN_PASSWORD` | Password admin awal |
| `UPLOAD_DIR` | Lokasi penyimpanan gambar berita |
| `PORT` | Port aplikasi |

<!-- Sesuaikan tabel ini dengan isi .env.example yang sebenarnya. -->

## Fitur

**Halaman publik:** TODO <!-- contoh: Beranda, Profil, Berita, Detail Berita, Kontak -->

**Panel admin:** TODO <!-- contoh: login, tambah/ubah/hapus berita bergambar, lihat pesan kontak -->

## Akun Admin Demo

Tidak ditulis di repo. Kredensial dikirim terpisah ke dosen melalui Google Classroom.

## Video Demo

TODO <!-- link YouTube unlisted atau Google Drive, durasi 5-10 menit -->

## Slide Presentasi

File PDF ada di [`docs/slides/`](docs/slides/).

## Struktur Repo

```
.
├── README.md
├── .env.example
├── .gitignore
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── app/
│   ├── static/
│   └── templates/
├── data/
├── tests/
└── docs/
    ├── slides/
    └── screenshots/
```
