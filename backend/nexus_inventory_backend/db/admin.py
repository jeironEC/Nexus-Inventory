# Django
from django.contrib import admin

# Models
from .models import (
    Role,
    User,
    Company,
    Category,
    Product,
    Inventory,
    Customer,
    Sale,
    Invoice,
    InventoryMovement,
    SaleDetail,
    Supplier,
    Purchase,
    PurchaseDetail,
    SaleReturn,
    SaleReturnDetail,
    PurchaseReturn,
    PurchaseReturnDetail,
)

# Admin Registers
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Customer)
admin.site.register(Sale)
admin.site.register(Invoice)
admin.site.register(InventoryMovement)
admin.site.register(SaleDetail)
admin.site.register(Supplier)
admin.site.register(Purchase)
admin.site.register(PurchaseDetail)
admin.site.register(SaleReturn)
admin.site.register(SaleReturnDetail)
admin.site.register(PurchaseReturn)
admin.site.register(PurchaseReturnDetail)
