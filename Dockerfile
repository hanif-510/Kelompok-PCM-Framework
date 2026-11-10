
# Base image Python
FROM python:3.14-slim

# Mengatur direktori kerja
WORKDIR /app

# Install uv untuk mengelola dependency
RUN pip install --no-cache-dir uv

# Menyalin file dependency terlebih dahulu
COPY pyproject.toml uv.lock ./

# Install dependency dari uv.lock
RUN uv sync --frozen --no-dev --no-install-project

# Menyalin seluruh kode aplikasi
COPY . .

# Konfigurasi sementara untuk proses collectstatic saat build
ENV SECRET_KEY=build-only-secret-key \
    DEBUG=False \
    ALLOWED_HOSTS=localhost,127.0.0.1 \
    PORT=8000

# Membuat folder static dan media
RUN mkdir -p /app/staticfiles /app/media

# Mengumpulkan file static Django
RUN uv run --no-sync python manage.py collectstatic --noinput

# Membuat user non-root
RUN groupadd --system django && \
    useradd --system --gid django django && \
    chown -R django:django /app/media

# Menjalankan aplikasi sebagai user non-root
USER django

# Port aplikasi
EXPOSE 8000

# Menjalankan Django menggunakan Gunicorn
CMD ["sh", "-c", "uv run --no-sync gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
