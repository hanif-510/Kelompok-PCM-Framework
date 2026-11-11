FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_CACHE_DIR=/tmp/uv-cache

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY . .

ENV DEBUG=False \
    ALLOWED_HOSTS=localhost,127.0.0.1 \
    PORT=8000

RUN groupadd --system django && \
    useradd --system --create-home --home-dir /home/django --gid django django && \
    mkdir -p /app/staticfiles /app/media /home/django /tmp/uv-cache && \
    chown -R django:django /home/django /app/media /tmp/uv-cache

RUN SECRET_KEY=build-only-secret-key uv run --no-sync python manage.py collectstatic --noinput

USER django

EXPOSE 8000

CMD ["sh", "-c", "uv run --no-sync gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]