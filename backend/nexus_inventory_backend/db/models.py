# Django
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# DRF
from rest_framework.exceptions import ValidationError

# Base Models
from .base import TimestampModel, BaseModel, AuditModel, DisplayModel

# Enums
from .enums import (
    OperationState,
    PaymentMethod,
    InvoiceState,
    MovementType,
    InvoiceType,
)


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
class Role(DisplayModel, TimestampModel):
    name = models.CharField(max_length=30)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def get_display_fields(self):
        return ["name"]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL USER
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class User(DisplayModel, BaseModel, AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    nif = models.CharField(max_length=15, unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.deleted_at and self.is_active:
            raise ValueError("Deleted user cannot be active")
        super().save(*args, **kwargs)

    def get_display_fields(self):
        return ["email", lambda obj: obj.role.name]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL PASSWORD RESET OTP
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class PasswordResetOTP(DisplayModel, TimestampModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="password_otps"
    )
    email = models.EmailField()
    otp_hash = models.CharField(max_length=128)
    is_used = models.BooleanField(default=False)
    reset_token = models.UUIDField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def get_display_fields(self):
        return ["email", "created_at"]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL COMPANY
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Company(DisplayModel, BaseModel):
    nif = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    number_phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="company/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def get_display_fields(self):
        return ["name", lambda obj: f"NIF: {obj.nif}"]

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["nif"]),
        ]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL CATEGORY
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Category(DisplayModel, BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def get_display_fields(self):
        return ["name"]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL PRODUCT
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Product(DisplayModel, BaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name="products"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    unique_code = models.CharField(max_length=50, unique=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def get_display_fields(self):
        return ["name"]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL INVENTORY
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Inventory(DisplayModel, BaseModel):
    product = models.OneToOneField(
        Product, on_delete=models.PROTECT, related_name="inventory"
    )
    quantity = models.IntegerField(default=0)

    def get_display_fields(self):
        return [lambda obj: obj.product.name, lambda obj: f"Stock: {obj.quantity}"]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL CUSTOMER
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Customer(DisplayModel, BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=120, unique=True)
    nif = models.CharField(max_length=20, unique=True)
    number_phone = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def get_display_fields(self):
        return ["first_name", "email"]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL SALE
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Sale(DisplayModel, AuditModel):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="sales")
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        related_name="sales",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="created_sales"
    )
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=21.00)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )
    state = models.CharField(
        max_length=20, choices=OperationState.choices, default=OperationState.COMPLETED
    )

    def get_display_fields(self):
        return ["total_amount", "payment_method"]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL INVENTORY MOVEMENT
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class InventoryMovement(DisplayModel, models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="inventory_movements"
    )
    user = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="inventory_movements"
    )
    movement_type = models.CharField(
        max_length=10, choices=MovementType.choices, default=MovementType.IN
    )
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_display_fields(self):
        return [lambda obj: obj.product.name, lambda obj: f"Quantity: {obj.quantity}"]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL SALE DETAIL
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class SaleDetail(DisplayModel, models.Model):
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

    def get_display_fields(self):
        return [lambda obj: obj.sale.total_amount, lambda obj: obj.product.name]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL SUPPLIER
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Supplier(DisplayModel, BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=120, unique=True)
    nif = models.CharField(max_length=20, unique=True)
    number_phone = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def get_display_fields(self):
        return ["name", "email"]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL PURCHASE
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Purchase(DisplayModel, AuditModel):
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, related_name="purchases"
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name="purchases"
    )
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="purchases")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    state = models.CharField(
        max_length=20, choices=OperationState.choices, default=OperationState.COMPLETED
    )

    def get_display_fields(self):
        return [lambda obj: obj.supplier.name, "total_amount", "created_at"]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL PURCHASE DETAIL
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class PurchaseDetail(DisplayModel, models.Model):
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

    def get_display_fields(self):
        return [
            lambda obj: obj.purchase.supplier.name,
            lambda obj: obj.product.name,
            "quantity",
        ]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# MODEL INVOICE
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Invoice(DisplayModel, BaseModel):
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, related_name="invoices"
    )
    sale = models.OneToOneField(
        Sale, on_delete=models.PROTECT, related_name="invoice", null=True, blank=True
    )
    purchase = models.OneToOneField(
        Purchase,
        on_delete=models.PROTECT,
        related_name="invoice",
        null=True,
        blank=True,
    )
    number_invoice = models.CharField(max_length=50, unique=True)
    pdf_generated = models.BooleanField(default=False)
    invoice_type = models.CharField(
        max_length=10, choices=InvoiceType.choices, blank=False
    )
    state = models.CharField(
        max_length=20, choices=InvoiceState.choices, default=InvoiceState.ISSUED
    )

    def clean(self):
        errors = {}

        if self.invoice_type.lower() == "sale":
            if not self.sale:
                errors["sale"] = "A sale-type invoice must be linked to a sale."
            if self.purchase:
                errors["purchase"] = (
                    "A sale-type invoice cannot be linked to a purchase."
                )

        elif self.invoice_type.lower() == "purchase":
            if not self.purchase:
                errors["purchase"] = (
                    "A purchase-type invoice must be linked to a purchase."
                )
            if self.sale:
                errors["sale"] = "A purchase-type invoice cannot be linked to a sale."

        else:
            errors["invoice_type"] = "Invoice type must be either 'sale' or 'purchase'."

        if errors:
            raise ValidationError(errors)

    def get_display_fields(self):
        return ["number_invoice", "state"]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


# ───────────────────────────────────────────────────────────────────────────────
# MODEL SALE RETURN
# ───────────────────────────────────────────────────────────────────────────────
class SaleReturn(DisplayModel, AuditModel):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name="returns")
    user = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="sale_returns"
    )
    reason = models.TextField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    state = models.CharField(
        max_length=20, choices=OperationState.choices, default=OperationState.COMPLETED
    )

    def get_display_fields(self):
        return [lambda obj: f"Return Sale #{obj.sale.id}", "total_amount", "state"]


# ───────────────────────────────────────────────────────────────────────────────
# MODEL SALE RETURN DETAIL
# ───────────────────────────────────────────────────────────────────────────────
class SaleReturnDetail(DisplayModel, models.Model):
    sale_return = models.ForeignKey(
        SaleReturn, on_delete=models.CASCADE, related_name="details"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="sale_return_details"
    )
    inventory_movement = models.OneToOneField(
        InventoryMovement, on_delete=models.PROTECT, related_name="sale_return_detail"
    )
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_display_fields(self):
        return [
            lambda obj: obj.product.name,
            lambda obj: f"Quantity {obj.quantity}",
            lambda obj: f"Return #{obj.sale_return.id}",
        ]


# ───────────────────────────────────────────────────────────────────────────────
# MODEL PURCHASE RETURN
# ───────────────────────────────────────────────────────────────────────────────
class PurchaseReturn(DisplayModel, AuditModel):
    purchase = models.ForeignKey(
        Purchase, on_delete=models.PROTECT, related_name="returns"
    )
    user = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="purchase_returns"
    )
    reason = models.TextField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    state = models.CharField(
        max_length=20, choices=OperationState.choices, default=OperationState.COMPLETED
    )

    def get_display_fields(self):
        return [
            lambda obj: f"Return Purchase #{obj.purchase.id}",
            "total_amount",
            "state",
        ]


# ───────────────────────────────────────────────────────────────────────────────
# MODEL PURCHASE RETURN DETAIL
# ───────────────────────────────────────────────────────────────────────────────
class PurchaseReturnDetail(DisplayModel, models.Model):
    purchase_return = models.ForeignKey(
        PurchaseReturn, on_delete=models.CASCADE, related_name="details"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="purchase_return_details"
    )
    inventory_movement = models.OneToOneField(
        InventoryMovement,
        on_delete=models.PROTECT,
        related_name="purchase_return_detail",
    )
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_display_fields(self):
        return [
            lambda obj: obj.product.name,
            lambda obj: f"Quantity {obj.quantity}",
            lambda obj: f"Return #{obj.purchase_return.id}",
        ]
