#!/bin/sh

set -e

echo "Ejecutando migraciones..."

python manage.py migrate --noinput

echo "Arrancando Gunicorn"

exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers $(nproc) \
    "nexus_inventory_backend.wsgi:application"
