from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    path('', views.beranda, name='beranda'),
    path('profil/', views.profil_halaman, name='profil'),
    path('pimpinan/', views.pimpinan, name='pimpinan'),
    path('ranting/', views.ranting, name='ranting'),
    path('amal-usaha/', views.amal_usaha, name='amal_usaha'),
    path('berita/', views.daftar_berita, name='daftar_berita'),
    path('berita/<slug:slug>/', views.detail_berita, name='detail_berita'),
    path('agenda/', views.agenda, name='agenda'),
    path('unduhan/', views.unduhan, name='unduhan'),
    path('kontak/', views.kontak, name='kontak'),
]
