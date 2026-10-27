from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PesanForm
from .models import (
    Agenda, AmalUsaha, Berita, Dokumen, Pimpinan, Profil, Ranting,
)


def beranda(request):
    sekarang = timezone.now()
    konteks = {
        'berita': Berita.objects.terbit()[:3],
        'agenda': Agenda.objects.filter(waktu_mulai__gte=sekarang)[:3],
        'jumlah_ranting': Ranting.objects.count(),
        'jumlah_amal_usaha': AmalUsaha.objects.count(),
    }
    return render(request, 'web/beranda.html', konteks)


def profil_halaman(request):
    return render(request, 'web/profil.html')


def pimpinan(request):
    return render(request, 'web/pimpinan.html', {'daftar': Pimpinan.objects.all()})


def ranting(request):
    return render(request, 'web/ranting.html', {'daftar': Ranting.objects.all()})


def amal_usaha(request):
    kelompok = []
    for kode, label in AmalUsaha.BIDANG:
        isi = AmalUsaha.objects.filter(bidang=kode)
        if isi.exists():
            kelompok.append((label, isi))
    return render(request, 'web/amal_usaha.html', {'kelompok': kelompok})


def daftar_berita(request):
    paginator = Paginator(Berita.objects.terbit(), 6)
    halaman = paginator.get_page(request.GET.get('page'))
    return render(request, 'web/daftar_berita.html', {'page_obj': halaman})


def detail_berita(request, slug):
    berita = get_object_or_404(Berita.objects.terbit(), slug=slug)
    lainnya = Berita.objects.terbit().exclude(pk=berita.pk)[:3]
    return render(request, 'web/detail_berita.html', {'berita': berita, 'lainnya': lainnya})


def agenda(request):
    sekarang = timezone.now()
    return render(request, 'web/agenda.html', {
        'mendatang': Agenda.objects.filter(waktu_mulai__gte=sekarang),
        'selesai': Agenda.objects.filter(waktu_mulai__lt=sekarang).order_by('-waktu_mulai'),
    })


def unduhan(request):
    return render(request, 'web/unduhan.html', {'daftar': Dokumen.objects.all()})


def kontak(request):
    if request.method == 'POST':
        form = PesanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Terima kasih, pesan Anda sudah terkirim.')
            return redirect('web:kontak')
    else:
        form = PesanForm()
    return render(request, 'web/kontak.html', {'form': form})
