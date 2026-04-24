# Models
from nexus_inventory_backend.db.models import Company


class CompanyService:

    @staticmethod
    def get_active_company():
        return Company.objects.filter(is_active=True).first()
