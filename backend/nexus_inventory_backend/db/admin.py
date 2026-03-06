from django.contrib import admin
from .models import Role, User, Category, Product, Inventory

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Inventory)
