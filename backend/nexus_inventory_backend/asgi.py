"""
ASGI config for nexus_inventory_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from configurations.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nexus_inventory_backend.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

application = get_asgi_application()
