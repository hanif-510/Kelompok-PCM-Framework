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
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
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

STORAGES = {
    # Penyimpanan media. Akan diganti ke object storage saat deployment.
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    # WhiteNoise menyajikan file statis saat DEBUG=False.
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}