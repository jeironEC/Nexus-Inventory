#!/bin/sh

set -e

echo "Ejecutando migraciones..."

python manage.py migrate --noinput

echo "Arrancando Gunicorn"

exec gunicorn \
    --bind 127.0.0.1:8000 \
    --workers $(nproc) \
    "nexus_inventory_backend.wsgi:application"
