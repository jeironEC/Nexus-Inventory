import os

from django.core.management.base import BaseCommand, CommandError

from nexus_inventory_backend.db.models import User


class Command(BaseCommand):
    help = "Crea un usuario administrador si no existe"

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str)
        parser.add_argument("--password", type=str)
        parser.add_argument("--first-name", type=str, default="Admin")
        parser.add_argument("--last-name", type=str, default="Sistema")
        parser.add_argument("--nif", type=str, default="00000000A")

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS("Administrador ya existe. Omitiendo."))
            return

        email = options.get("email") or os.environ.get("NEXUS_ADMIN_EMAIL")
        password = options.get("password") or os.environ.get("NEXUS_ADMIN_PASSWORD")

        if not email:
            email = input("Email del administrador: ").strip()
        if not password:
            import getpass

            password = getpass.getpass("Contraseña del administrador: ")

        if not email or not password:
            raise CommandError("Email y contraseña son obligatorios")

        User.objects.create_superuser(
            email=email,
            password=password,
            first_name=options["first_name"],
            last_name=options["last_name"],
            nif=options["nif"],
        )
        self.stdout.write(self.style.SUCCESS(f"Administrador '{email}' creado"))
