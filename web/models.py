from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Profil(models.Model):
    """Profil organisasi. Hanya boleh ada satu baris (dijaga di admin)."""
    nama = models.CharField(max_length=200)
    nama_singkat = models.CharField(max_length=50)
    tagline = models.CharField(max_length=200, blank=True)
    tentang = models.TextField(blank=True)
    sejarah = models.TextField(blank=True)
    visi = models.TextField(blank=True)
    misi = models.TextField(blank=True, help_text='Tulis satu misi per baris.')
    alamat = models.TextField(blank=True, help_text='Alamat sekretariat.')
    telepon = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    jumlah_anggota_ktam = models.PositiveIntegerField(default=0)
    gambar_utama = models.ImageField(upload_to='profil/', blank=True)

    class Meta:
        verbose_name = 'Profil organisasi'
        verbose_name_plural = 'Profil organisasi'

    def daftar_misi(self):
        return [baris.strip() for baris in self.misi.splitlines() if baris.strip()]

    def __str__(self):
        return self.nama


class Pimpinan(models.Model):
    nama = models.CharField(max_length=150)
    jabatan = models.CharField(max_length=100)
    periode = models.CharField(max_length=20, help_text='Contoh: 2022-2027')
    foto = models.ImageField(upload_to='pimpinan/', blank=True)
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['urutan', 'nama']
        verbose_name_plural = 'Pimpinan'

    def __str__(self):
        return f'{self.nama} - {self.jabatan}'


class Ranting(models.Model):
    nama = models.CharField(max_length=150)
    ketua = models.CharField(max_length=150, blank=True)
    alamat = models.TextField(blank=True)
    telepon = models.CharField(max_length=50, blank=True, help_text='Isi hanya kontak resmi.')

    class Meta:
        ordering = ['nama']
        verbose_name_plural = 'Ranting'

    def __str__(self):
        return self.nama


class AmalUsaha(models.Model):
    BIDANG = [
        ('pendidikan', 'Pendidikan'),
        ('kesehatan', 'Kesehatan'),
        ('sosial', 'Sosial'),
        ('ekonomi', 'Ekonomi'),
    ]
    nama = models.CharField(max_length=200)
    bidang = models.CharField(max_length=20, choices=BIDANG)
    deskripsi = models.TextField(blank=True)
    alamat = models.TextField(blank=True)
    gambar = models.ImageField(upload_to='amal_usaha/', blank=True)

    class Meta:
        ordering = ['nama']
        verbose_name = 'Amal usaha'
        verbose_name_plural = 'Amal usaha'

    def __str__(self):
        return self.nama


class BeritaQuerySet(models.QuerySet):
    def terbit(self):
        """Hanya berita berstatus terbit dan tanggalnya sudah tiba."""
        return self.filter(status='terbit', tanggal_terbit__lte=timezone.now())


class Berita(models.Model):
    STATUS = [('draf', 'Draf'), ('terbit', 'Terbit')]

    judul = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    ringkasan = models.CharField(max_length=300)
    isi = models.TextField()
    gambar = models.ImageField(upload_to='berita/', blank=True)
    tanggal_terbit = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS, default='draf')

    objects = BeritaQuerySet.as_manager()

    class Meta:
        ordering = ['-tanggal_terbit']
        verbose_name_plural = 'Berita'

    def save(self, *args, **kwargs):
        if not self.slug:
            dasar = slugify(self.judul) or 'berita'
            slug, n = dasar, 2
            while Berita.objects.filter(slug=slug).exists():
                slug = f'{dasar}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul


class Agenda(models.Model):
    nama = models.CharField(max_length=200)
    waktu_mulai = models.DateTimeField()
    tempat = models.CharField(max_length=200, blank=True)
    keterangan = models.TextField(blank=True)

    class Meta:
        ordering = ['waktu_mulai']
        verbose_name_plural = 'Agenda'

    def __str__(self):
        return self.nama


class Dokumen(models.Model):
    judul = models.CharField(max_length=200)
    keterangan = models.TextField(blank=True)
    berkas = models.FileField(upload_to='dokumen/')
    tanggal_unggah = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-tanggal_unggah']
        verbose_name_plural = 'Dokumen'

    def __str__(self):
        return self.judul


class PesanMasuk(models.Model):
    nama = models.CharField(max_length=150)
    email = models.EmailField()
    subjek = models.CharField(max_length=200)
    pesan = models.TextField()
    waktu_kirim = models.DateTimeField(auto_now_add=True)
    sudah_dibaca = models.BooleanField(default=False)

    class Meta:
        ordering = ['-waktu_kirim']
        verbose_name = 'Pesan masuk'
        verbose_name_plural = 'Pesan masuk'

    def __str__(self):
        return f'{self.subjek} ({self.nama})'


class TautanTerkait(models.Model):
    nama = models.CharField(max_length=150)
    url = models.URLField()
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['urutan', 'nama']
        verbose_name = 'Tautan terkait'
        verbose_name_plural = 'Tautan terkait'

    def __str__(self):
        return self.nama
