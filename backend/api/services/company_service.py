# Models
from nexus_inventory_backend.db.models import Company

# Enums
from nexus_inventory_backend.db.enums import State


class CompanyService:

    @staticmethod
    def get_active_company():
        return Company.objects.filter(state=State.ACTIVE).first()
