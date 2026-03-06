from django.contrib import admin
from .models import (
    Role,
    User,
    Category,
    Product,
    Inventory,
    Customer,
    Promotion,
    CustomerPromotion,
    Invoice,
    InventoryMovement,
    InvoiceDetail,
)

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Customer)
admin.site.register(Promotion)
admin.site.register(CustomerPromotion)
admin.site.register(Invoice)
admin.site.register(InventoryMovement)
admin.site.register(InvoiceDetail)
