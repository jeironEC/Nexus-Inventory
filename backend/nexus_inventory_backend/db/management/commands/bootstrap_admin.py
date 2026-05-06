import os

from django.core.management.base import BaseCommand, CommandError

from nexus_inventory_backend.db.models import Role, User

DEFAULT_ROLES = [
    {"name": "admin", "description": "Administrador del sistema"},
]


class Command(BaseCommand):
    help = "Crea roles por defecto y un usuario administrador"

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str)
        parser.add_argument("--password", type=str)
        parser.add_argument("--first-name", type=str, default="Admin")
        parser.add_argument("--last-name", type=str, default="Sistema")
        parser.add_argument("--nif", type=str, default="00000000A")

    def handle(self, *args, **options):
        self.stdout.write("Creando roles por defecto...")
        for role_data in DEFAULT_ROLES:
            role, created = Role.objects.get_or_create(
                name=role_data["name"],
                defaults={"description": role_data["description"]},
            )
            status = "creado" if created else "ya existe"
            self.stdout.write(f"  - Rol '{role.name}': {status}")

        self._create_admin(options)

    def _create_admin(self, options):
        admin_role = Role.objects.get(name="admin")

        if User.objects.filter(role=admin_role).exists():
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
