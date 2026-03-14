# Django
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

# Base Models
from .base import BaseModel, AuditModel

# Enums
from .enums import State, OperationState

"""
NOTA:
    · auto_now_add=True -> Se asigna la fecha y hora solo al crear el registro (equivale a DEFAULT CURRENT_TIMESTAMP).

    · auto_now=True -> Se actualiza la fecha y hora cada vez que se guarda el registro (equivale a ON UPDATE CURRENT_TIMESTAMP).
"""


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL MANAGER
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superiser must hava is_staff on True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superiser must hava is_superuser on True.")

        admin_role, _ = Role.objects.get_or_create(
            name="ADMIN", defaults={"description": "Administrator role"}
        )
        extra_fields.setdefault("role", admin_role)
        return self.create_user(email, password, **extra_fields)


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL ROLE
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Role(BaseModel):
    name = models.CharField(max_length=30)
    description = models.TextField()
    state = models.CharField(max_length=20, choices=State.choices, default=State.ACTIVE)

    def __str__(self):
        return self.name


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL USER
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_active", "deleted_at"])

    def save(self, *args, **kwargs):
        if self.deleted_at and self.is_active:
            raise ValueError("Deleted user cannot be active")
        super().save(*args, **kwargs)


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL CATEGORY
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    state = models.CharField(max_length=20, choices=State.choices, default=State.ACTIVE)

    def __str__(self):
        return self.name


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL PRODUCT
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Product(BaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="products", null=True
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    unique_code = models.CharField(max_length=50, unique=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=20, choices=State.choices, default=State.ACTIVE)

    def __str__(self):
        return self.name


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL INVENTORY
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Inventory(BaseModel):
    product = models.OneToOneField(
        Product, on_delete=models.PROTECT, related_name="inventory"
    )
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - Stock: {self.quantity}"


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL CUSTOMER
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Customer(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=120, unique=True)
    number_phone = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    state = models.CharField(max_length=20, choices=State.choices, default=State.ACTIVE)

    def __str__(self):
        return f"{self.first_name}: {self.email}"


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL PROMOTION
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Promotion(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    state = models.CharField(max_length=20, choices=State.choices, default=State.ACTIVE)

    def __str__(self):
        return f"{self.name} - Discount: {self.discount_percentage}%"


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL CUSTOMER PROMOTION
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class CustomerPromotion(BaseModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer_promotions"
    )
    promotion = models.ForeignKey(
        Promotion, on_delete=models.CASCADE, related_name="customer_promotions"
    )
    applied = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "promotion"], name="unique_customer_promotion"
            )
        ]

    def __str__(self):
        return f"{self.customer} - {self.promotion} - Applied: {self.applied}"


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL SALE
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Sale(AuditModel):
    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Cash"
        CARD = "CARD", "Card"
        TRANSFER = "TRANSFER", "Transfer"

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        related_name="sales",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="created_sales", null=True
    )
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )
    state = models.CharField(
        max_length=20, choices=OperationState.choices, default=OperationState.COMPLETED
    )

    def __str__(self):
        return f"{self.total_amount} - {self.payment_method}"


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL INVOICE
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Invoice(BaseModel):
    class InvoiceState(models.TextChoices):
        ISSUED = "ISSUED", "Issued"
        CANCELED = "CANCELED", "Canceled"

    sale = models.OneToOneField(Sale, on_delete=models.PROTECT, related_name="invoice")
    number_invoice = models.CharField(max_length=50, unique=True)
    pdf_generated = models.BooleanField(default=False)
    state = models.CharField(
        max_length=20, choices=InvoiceState.choices, default=InvoiceState.ISSUED
    )

    def __str__(self):
        return f"{self.number_invoice} - {self.state}"


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL INVENTORY MOVEMENT
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class InventoryMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = "IN", "In"
        OUT = "OUT", "Out"

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="inventory_movements"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="inventory_movements", null=True
    )
    movement_type = models.CharField(
        max_length=10, choices=MovementType.choices, default=MovementType.IN
    )
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL SALE DETAIL
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="details")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="sale_details"
    )
    inventory_movement = models.OneToOneField(
        InventoryMovement, on_delete=models.PROTECT, related_name="sale_detail"
    )
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sale.total_amount} - {self.product.name}"


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL SUPPLIER
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Supplier(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=120)
    number_phone = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    state = models.CharField(max_length=20, choices=State.choices, default=State.ACTIVE)

    def __str__(self):
        return f"{self.name} - {self.email}"


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL PURCHASE
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Purchase(AuditModel):
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name="purchases"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="purchases", null=True
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    state = models.CharField(
        max_length=20, choices=OperationState.choices, default=OperationState.COMPLETED
    )

    def __str__(self):
        return f"{self.supplier.name} - {self.total_amount} - {self.created_at}"


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL PURCHASE DETAIL
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE, related_name="details"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="purchase_details"
    )
    inventory_movement = models.OneToOneField(
        InventoryMovement, on_delete=models.PROTECT, related_name="purchase_detail"
    )
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.purchase.supplier.name} - {self.product.name} - {self.quantity}"
