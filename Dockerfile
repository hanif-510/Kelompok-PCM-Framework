
FROM python:3.14-slim

# Konfigurasi Python dan cache uv
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_CACHE_DIR=/tmp/uv-cache

# Folder kerja aplikasi
WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Salin file dependency
COPY pyproject.toml uv.lock ./

# Install dependency berdasarkan uv.lock
RUN uv sync --frozen --no-dev --no-install-project

# Salin seluruh source code Django
COPY . .

# Konfigurasi sementara untuk build
ENV SECRET_KEY=build-only-secret-key \
    DEBUG=False \
    ALLOWED_HOSTS=localhost,127.0.0.1 \
    PORT=8000

# Buat user non-root dan folder yang dibutuhkan
RUN groupadd --system django && \
    useradd --system --create-home --home-dir /home/django --gid django django && \
    mkdir -p /app/staticfiles /app/media /home/django /tmp/uv-cache && \
    chown -R django:django /home/django /app/media /tmp/uv-cache

# Mengumpulkan static files
RUN uv run --no-sync python manage.py collectstatic --noinput

# Jalankan aplikasi sebagai user non-root
USER django

# Port aplikasi
EXPOSE 8000

# Jalankan Django menggunakan Gunicorn
CMD ["sh", "-c", "uv run --no-sync gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
