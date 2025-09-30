# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# System deps
RUN apt-get update \ 
    && apt-get install -y --no-install-recommends build-essential libpq-dev curl \ 
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt ./
RUN pip install --upgrade pip \ 
    && pip install -r requirements.txt

# App code
COPY . .

# Collect static at build time to leverage layer caching
RUN python manage.py collectstatic --noinput || true

EXPOSE 8080

# Entrypoint will run migrations then launch gunicorn
RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]


