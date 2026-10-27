from django.contrib import admin

from .models import (
    Agenda, AmalUsaha, Berita, Dokumen, PesanMasuk,
    Pimpinan, Profil, Ranting, TautanTerkait,
)

admin.site.site_header = 'Admin Website PCM Gatak'
admin.site.site_title = 'Admin PCM Gatak'
admin.site.index_title = 'Kelola isi website'


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nama_singkat', 'telepon', 'email', 'jumlah_anggota_ktam')

    def has_add_permission(self, request):
        # Hanya boleh ada satu baris profil.
        return not Profil.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Pimpinan)
class PimpinanAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jabatan', 'periode', 'urutan')
    list_filter = ('periode',)
    search_fields = ('nama', 'jabatan')


@admin.register(Ranting)
class RantingAdmin(admin.ModelAdmin):
    list_display = ('nama', 'ketua', 'telepon')
    search_fields = ('nama', 'ketua')


@admin.register(AmalUsaha)
class AmalUsahaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'bidang', 'alamat')
    list_filter = ('bidang',)
    search_fields = ('nama',)


@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'status', 'tanggal_terbit')
    list_filter = ('status',)
    search_fields = ('judul', 'ringkasan')
    prepopulated_fields = {'slug': ('judul',)}
    date_hierarchy = 'tanggal_terbit'


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'waktu_mulai', 'tempat')
    list_filter = ('waktu_mulai',)
    search_fields = ('nama', 'tempat')


@admin.register(Dokumen)
class DokumenAdmin(admin.ModelAdmin):
    list_display = ('judul', 'tanggal_unggah')
    search_fields = ('judul',)


@admin.register(PesanMasuk)
class PesanMasukAdmin(admin.ModelAdmin):
    list_display = ('subjek', 'nama', 'email', 'waktu_kirim', 'sudah_dibaca')
    list_filter = ('sudah_dibaca', 'waktu_kirim')
    search_fields = ('nama', 'email', 'subjek')
    # Isi pesan tidak boleh diubah; hanya status "sudah dibaca" yang boleh.
    readonly_fields = ('nama', 'email', 'subjek', 'pesan', 'waktu_kirim')

    def has_add_permission(self, request):
        return False


@admin.register(TautanTerkait)
class TautanTerkaitAdmin(admin.ModelAdmin):
    list_display = ('nama', 'url', 'urutan')
