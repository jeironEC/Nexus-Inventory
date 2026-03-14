# Django
from django.contrib import admin

# Models
from .models import (
    Role,
    User,
    Category,
    Product,
    Inventory,
    Customer,
    Promotion,
    CustomerPromotion,
    Sale,
    Invoice,
    InventoryMovement,
    SaleDetail,
    Supplier,
    Purchase,
    PurchaseDetail,
)

# Admin Registers
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Customer)
admin.site.register(Promotion)
admin.site.register(CustomerPromotion)
admin.site.register(Sale)
admin.site.register(Invoice)
admin.site.register(InventoryMovement)
admin.site.register(SaleDetail)
admin.site.register(Supplier)
admin.site.register(Purchase)
admin.site.register(PurchaseDetail)
