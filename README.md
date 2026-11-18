# Website PCM Gatak

Website PCM Gatak, Kabupaten Sukoharjo, Jawa Tengah. Proyek ini dibuat sebagai tugas mata kuliah Pemrograman Web berbasis Framework dan **bukan website resmi** Pimpinan Cabang Muhammadiyah (PCM) Gatak.

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
| Logo Muhammadiyah | Wikimedia Commons | 09-11-2026 | - |
| Profil, struktur pimpinan, ranting, amal | Dokumen Ketua PCM | 12-11-2026 | Drs. Shodiq Purnomo, M.M. |
| Berita dan agenda | Website Berita | 16-11-2026 | - |
| Foto | Website Berita | 15-11-2026 | - |

## Kontribusi Anggota

| Nama | Kontribusi |
|------|------------|
| Raden Bagus Indra Wijaya Nugraha | Backend, database, dan deployment. Penataan proyek uv dan dependensi, konfigurasi ruff, `.gitignore` dan `.env.example`, settings berbasis environment variable, WhiteNoise untuk file statis, kerangka command `seed_pcm` yang idempotent beserta testnya, serta test queryset berita terbit, slug, dan admin (termasuk perbaikan `max_length` slug untuk PostgreSQL). Database PostgreSQL di Supabase (Session pooler), migrasi ke produksi, dan Row Level Security di semua tabel. Penyimpanan media ke Supabase Storage lewat S3 yang sudah diuji unggah dari admin, HSTS, `SECURE_PROXY_SSL_HEADER`, dan pengecekan `check --deploy`. Perbaikan logo dan tampilan kartu anggota ber-KTAM di beranda. Review konfigurasi Docker. |
| Muhammad Valentino Khansa | Mengisi dan mencari data riil PCM Gatak di seed data: susunan pimpinan dari SK PCM Gatak (pimpinan.py), daftar amal usaha (amal_usaha.py), dan data ketua ranting (ranting.py). |
| Muhammad Afif Haravi | Mengembangkan tampilan dan fitur website, termasuk template dasar, header, footer, CSS halaman admin, kartu berita, halaman beranda, serta formulir kontak. Melakukan pengujian aplikasi Django dan Docker Compose, khususnya pengujian persistensi data dan media menggunakan Docker Volume serta pemulihan aplikasi setelah penghapusan volume. |
| Hanif | Struktur awal website PCM Gatak, UI dan navigasi menu, penyesuaian tampilan/CSS website. Implementasi Docker melalui Dockerfile, .dockerignore, dan Docker Compose untuk menjalankan Django dan PostgreSQL. Pengujian build image dan container, konfigurasi permission dan startup, migrasi database, memastikan website berjalan melalui localhost:8000 menggunakan Gunicorn, docker. Pengembangan fitur berita dan detail berita, agenda mendatang/selesai, pencarian berita, pagination 6 berita per halaman, setup GitHub Actions untuk Django tests otomatis, Deployment menggunakan Railway. |
| Sandy Matin Falah | Tidak ada kontribusi pada pengerjaan proyek ini. |

## Produksi

| Item | Pilihan | Alasan |
|------|---------|--------|
| URL Produksi | https://kelompok-pcm-framework-production.up.railway.app | Alamat publik dengan HTTPS dari Railway |
| Platform | Railway (Web Service memakai `Dockerfile`) | Kemudahan penggunaan, integrasi dengan GitHub, dan memakai `Dockerfile` yang sama dengan Docker lokal |
| Database | PostgreSQL di Supabase (Session pooler, port 5432) | Database terkelola dan gratis. Session pooler mendukung IPv4 dan cocok dengan koneksi Django biasa. Row Level Security aktif di semua tabel |
| Penyimpanan gambar | Supabase Storage lewat endpoint S3 dan `django-storages` (bucket publik `media`) | Disk server platform deploy tidak permanen, sehingga gambar upload akan hilang setelah redeploy jika disimpan lokal. Sudah diuji: gambar yang diunggah dari admin tersimpan di bucket |

**Catatan layanan gratis:**

- Proyek Supabase paket gratis dijeda jika aktivitas database rendah selama 7 hari dan bisa dipulihkan lewat Resume project di dashboard. Lihat [dokumentasi Supabase](https://supabase.com/docs/guides/platform/free-plan-pausing).

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

### Persistensi Data dan Volume Docker

Docker Compose menggunakan **named volume** untuk mempertahankan data meskipun container dihentikan, dihapus, atau dibuat ulang.

Pada proyek ini terdapat dua named volume utama, yaitu `postgres_data` dan `media_data`.

**Konfigurasi volume:**

| Volume | Lokasi di Container | Fungsi |
|---|---|---|
| `postgres_data` | `/var/lib/postgresql/data` | Menyimpan data database PostgreSQL, termasuk tabel, berita, agenda, akun administrator, dan data lainnya. |
| `media_data` | `/app/media` | Menyimpan file media yang diunggah melalui aplikasi Django, seperti gambar berita. |

Kedua volume tersebut didefinisikan dalam `compose.yaml` dan digunakan oleh service PostgreSQL dan Django.

#### 1. Mempertahankan Data Setelah Container Dihentikan

Untuk menghentikan container tanpa menghapus data yang tersimpan, gunakan:

```bash
docker compose down
```

Kemudian jalankan kembali aplikasi:

```bash
docker compose up -d
```

Perintah `docker compose down` akan menghentikan dan menghapus container serta network yang dibuat oleh Docker Compose. Namun, named volume tidak ikut dihapus.

Ketika aplikasi dijalankan kembali, Docker akan menggunakan volume yang sama sehingga data database dan file media tetap tersedia.

Dengan demikian:

- Data PostgreSQL tetap tersimpan.
- Berita, agenda, akun administrator, dan data lainnya tidak hilang.
- Gambar yang telah diunggah tetap tersedia selama disimpan dalam volume `media_data`.

#### 2. Cara Memeriksa Volume Docker

Untuk melihat volume yang didefinisikan dalam konfigurasi Docker Compose, jalankan:

```bash
docker compose config --volumes
```

Untuk melihat seluruh volume Docker yang tersedia:

```bash
docker volume ls
```

Untuk memeriksa konfigurasi volume yang digunakan oleh container:

```bash
docker compose config
```

Periksa bagian `volumes` pada service `web` dan `db`.

Konfigurasi media pada service Django seharusnya mengarah ke:

```yaml
volumes:
  - media_data:/app/media
```

Sedangkan konfigurasi database PostgreSQL seharusnya mengarah ke:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

#### 3. Pengujian Persistensi Data dan Gambar

Persistensi data dapat diuji dengan langkah berikut:

**Langkah 1: Jalankan aplikasi**

```bash
docker compose up -d
```

**Langkah 2: Periksa status container**

```bash
docker compose ps
```

Pastikan container Django dan PostgreSQL berjalan dengan baik.

**Langkah 3: Periksa file media yang tersimpan**

```bash
docker compose exec web sh -c "find /app/media -type f -print"
```

Perintah tersebut menampilkan daftar seluruh file yang tersimpan di direktori media Django.

**Langkah 4: Hentikan container**

```bash
docker compose down
```

**Langkah 5: Jalankan kembali container**

```bash
docker compose up -d
```

**Langkah 6: Periksa kembali file media**

```bash
docker compose exec web sh -c "find /app/media -type f -print"
```

Jika file gambar yang sebelumnya diunggah masih muncul, berarti persistensi media berhasil bekerja.

Pengujian juga dapat dilakukan dengan membuka kembali website dan memastikan data berita, agenda, akun administrator, serta gambar tetap tersedia.

#### 4. Menghapus Seluruh Data Menggunakan `docker compose down -v`

Jika ingin menghentikan container sekaligus menghapus seluruh named volume yang digunakan oleh proyek, jalankan:

```bash
docker compose down -v
```

Berbeda dengan `docker compose down` biasa, penambahan opsi `-v` (`--volumes`) akan menghapus named volume yang didefinisikan dalam konfigurasi Docker Compose serta volume anonim yang terkait.

Dampaknya pada proyek ini:

| Komponen | Dampak |
|---|---|
| Container Django | Dihapus |
| Container PostgreSQL | Dihapus |
| Network Docker | Dihapus |
| `postgres_data` | Dihapus beserta seluruh data database |
| `media_data` | Dihapus beserta seluruh file media lokal |

Setelah perintah tersebut dijalankan, data database dan file media yang tersimpan dalam kedua volume tidak dapat digunakan kembali melalui container berikutnya.

Untuk menjalankan aplikasi kembali dengan penyimpanan baru, gunakan:

```bash
docker compose up -d
```

Docker akan membuat named volume baru yang masih kosong. Database perlu diinisialisasi kembali melalui migrasi Django:

```bash
docker compose exec web uv run --no-sync python manage.py migrate
```

Jika diperlukan, data awal PCM Gatak dapat dimasukkan kembali menggunakan:

```bash
docker compose exec web uv run --no-sync python manage.py seed_pcm
```

Akun administrator juga perlu dibuat kembali menggunakan:

```bash
docker compose exec web uv run --no-sync python manage.py createsuperuser
```

**Catatan penting:**

- Gunakan `docker compose down` jika hanya ingin menghentikan aplikasi tanpa kehilangan data.
- Gunakan `docker compose down -v` hanya jika memang ingin menghapus data database dan media lokal secara permanen.
- Sebelum menjalankan `docker compose down -v`, pastikan data penting sudah dicadangkan.
- Penghapusan volume Docker tidak menghapus file yang tersimpan di luar volume tersebut.
- Jika aplikasi menggunakan Supabase Storage sebagai penyimpanan media eksternal, file yang tersimpan di Supabase tidak ikut terhapus oleh perintah `docker compose down -v`.

#### 5. Hasil Pengujian Persistensi pada Proyek

Pengujian persistensi media telah dilakukan secara langsung menggunakan Docker Compose.

**Pengujian pertama: `docker compose down` dan `docker compose up -d`**

File gambar yang digunakan sebagai objek pengujian:

```text
/app/media/berita/Fishbone_VPN_MITM_Judul_Dalam_Kotak_1.png
```

Sebelum container dihentikan, file tersebut ditemukan pada direktori media Django.

Kemudian dilakukan pengujian dengan menjalankan:

```bash
docker compose down
docker compose up -d
```

Setelah container berjalan kembali, dilakukan pemeriksaan menggunakan:

```bash
docker compose exec web sh -c "find /app/media -type f -print"
```

Hasil pemeriksaan menunjukkan bahwa file gambar yang sama masih tersedia:

```text
/app/media/berita/Fishbone_VPN_MITM_Judul_Dalam_Kotak_1.png
```

**Kesimpulan pengujian pertama:**

Hasil tersebut membuktikan bahwa konfigurasi named volume `media_data` berhasil mempertahankan file gambar meskipun container dihentikan dan dibuat ulang.

**Pengujian kedua: `docker compose down -v`**

Pengujian berikutnya dilakukan untuk membuktikan bahwa opsi `-v` menghapus named volume yang digunakan oleh proyek.

Perintah yang dijalankan:

```bash
docker compose down -v
```

Setelah itu, volume diperiksa dan aplikasi dijalankan kembali:

```bash
docker volume ls
docker compose up -d
```

Pemeriksaan folder media dilakukan menggunakan:

```bash
docker compose exec web sh -c "find /app/media -type f -print"
```

Hasil pengujian menunjukkan bahwa file gambar yang sebelumnya tersimpan dalam volume `media_data` sudah tidak tersedia setelah volume dihapus dan dibuat ulang.

Database juga dibuat kembali dalam kondisi baru sehingga migrasi database perlu dijalankan kembali dan akun administrator perlu dibuat ulang.

Setelah proses tersebut selesai, panel admin Django berhasil diakses kembali menggunakan akun administrator yang baru dibuat.

**Kesimpulan pengujian kedua:**

Perintah `docker compose down -v` berhasil menghapus named volume yang digunakan oleh proyek, termasuk data PostgreSQL dan media lokal. Ketika aplikasi dijalankan kembali, Docker membuat volume baru sehingga penyimpanan dimulai dari kondisi kosong.

#### 6. Kesimpulan Pengujian Docker Volume

Berdasarkan kedua pengujian yang telah dilakukan, dapat disimpulkan bahwa konfigurasi Docker Compose pada proyek Website PCM Gatak telah menerapkan mekanisme persistensi data menggunakan named volume.

Perintah `docker compose down` digunakan untuk menghentikan dan menghapus container tanpa menghapus data yang tersimpan dalam named volume. Ketika aplikasi dijalankan kembali menggunakan `docker compose up -d`, data database dan file media tetap tersedia.

Sebaliknya, perintah `docker compose down -v` digunakan untuk menghentikan container sekaligus menghapus named volume. Akibatnya, data database dan file media lokal ikut terhapus. Setelah aplikasi dijalankan kembali, database perlu dimigrasikan dan akun administrator perlu dibuat ulang.

Dengan demikian, kedua perintah tersebut memiliki fungsi yang berbeda dalam pengelolaan container dan penyimpanan data Docker.

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
| `POSTGRES_PASSWORD` | Password database PostgreSQL untuk Docker Compose. Wajib diisi di `.env` saat memakai `docker compose` |
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
