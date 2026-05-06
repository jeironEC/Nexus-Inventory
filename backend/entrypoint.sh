#!/bin/sh

set -e

echo "Ejecutando migraciones..."

python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Inicializando administrador y datos base..."
python manage.py bootstrap_admin --noinput || true

echo "Arrancando Gunicorn"

exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers $(nproc) \
    "nexus_inventory_backend.wsgi:application"
