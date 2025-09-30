#!/usr/bin/env bash
set -euo pipefail

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

exec gunicorn taskmanager.wsgi:application --bind 0.0.0.0:8080 --workers ${WEB_CONCURRENCY:-2} --timeout 60

