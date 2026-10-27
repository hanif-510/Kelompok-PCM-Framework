from .models import Profil, TautanTerkait


def profil_dan_tautan(request):
    """Menyediakan profil organisasi dan tautan terkait ke semua template."""
    return {
        'profil': Profil.objects.first(),
        'tautan_terkait': TautanTerkait.objects.all(),
    }
