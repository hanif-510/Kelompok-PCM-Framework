"""
Pengaturan Django untuk website PCM Gatak.

Nilai yang berbeda antara laptop dan server dibaca dari environment variable.
Daftar variabelnya ada di .env.example.
"""

import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Muat .env jika ada. Variabel yang sudah diset di sistem (Docker, Render, dst) tidak ditimpa.
load_dotenv(BASE_DIR / '.env')


def env_bool(nama, default=False):
    """Baca variabel bertipe true/false, mis. DEBUG=True."""
    nilai = os.environ.get(nama)
    if nilai is None:
        return default
    return nilai.strip().lower() in {'1', 'true', 'yes', 'on'}


def env_list(nama):
    """Baca daftar yang dipisah koma, mis. ALLOWED_HOSTS=a.com,b.com."""
    return [item.strip() for item in os.environ.get(nama, '').split(',') if item.strip()]

def env_wajib(nama):
    """Baca variabel yang tidak boleh kosong."""
    nilai = os.environ.get(nama)
    if not nilai:
        raise ImproperlyConfigured(f'{nama} wajib diisi jika STORAGE_BUCKET dipakai.')
    return nilai

# Keamanan
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured(
        'SECRET_KEY belum diisi. Salin .env.example menjadi .env lalu isi nilainya.'
    )

# Bawaan False supaya lupa mengisi di server tidak membuka mode debug.
DEBUG = env_bool('DEBUG', default=False)

ALLOWED_HOSTS = env_list('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS')
# Aktifkan hanya di server HTTPS (Render/Railway). Di Docker lokal biarkan False,
# kalau tidak, localhost:8000 akan dialihkan ke HTTPS dan login admin gagal.
if env_bool('HTTPS_ONLY'):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Mulai dari 1 jam, naikkan setelah HTTPS terbukti stabil.
    SECURE_HSTS_SECONDS = int(os.environ.get('HSTS_SECONDS', '3600'))
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'web.context_processors.profil_dan_tautan',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database: SQLite jika DATABASE_URL kosong, selain itu PostgreSQL (Neon/Supabase).

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=0)}
    # Transaction pooler (port 6543) tidak mendukung server-side cursor.
    if str(DATABASES['default'].get('PORT')) == '6543':
        DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'id'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_TZ = True


# Static dan media

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Media: folder lokal jika STORAGE_BUCKET kosong, object storage S3 jika terisi.
# Disk server tidak permanen, jadi produksi wajib memakai object storage.
STORAGE_BUCKET = os.environ.get('STORAGE_BUCKET')

if STORAGE_BUCKET:
    MEDIA_STORAGE = {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {
            'bucket_name': STORAGE_BUCKET,
            'endpoint_url': env_wajib('STORAGE_ENDPOINT'),
            'region_name': env_wajib('STORAGE_REGION'),
            'access_key': env_wajib('STORAGE_ACCESS_KEY'),
            'secret_key': env_wajib('STORAGE_SECRET_KEY'),
            'custom_domain': env_wajib('STORAGE_PUBLIC_DOMAIN'),
            'signature_version': 's3v4',
            'addressing_style': 'path',
            'querystring_auth': False,
            'file_overwrite': False,
        },
    }
else:
    MEDIA_STORAGE = {'BACKEND': 'django.core.files.storage.FileSystemStorage'}

STORAGES = {
    'default': MEDIA_STORAGE,
    # WhiteNoise menyajikan file statis saat DEBUG=False.
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration
# Situs ini tidak mengirim email (formulir kontak hanya menyimpan ke database),
# jadi backend console aman. Pengecekan ini dibungkam agar check --deploy bersih.
SILENCED_SYSTEM_CHECKS = ['mail.E001']
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}