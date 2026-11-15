
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Konfigurasi tampilan Django Admin
admin.site.site_header = "ADMIN PCM GATAK"
admin.site.site_title = "Admin PCM Gatak"
admin.site.index_title = "Dashboard Pengelolaan Website PCM Gatak"

urlpatterns = [
    # Halaman Admin
    path('admin/', admin.site.urls),

    # Halaman utama website
    path('', include('web.urls')),
]

# Konfigurasi media saat development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
