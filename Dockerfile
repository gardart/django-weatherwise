FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=weatherwise.settings \
    DJANGO_DB_PATH=/data/weather.db

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

RUN chmod +x scripts/entrypoint.sh scripts/fetch_observations.sh scripts/hourly_observations.sh

# Pre-build static assets into the image.
RUN python weatherwise/manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["scripts/entrypoint.sh"]
CMD ["gunicorn", "weatherwise.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "30"]
