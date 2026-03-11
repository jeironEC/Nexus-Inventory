# Django
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

# Enums
from .enums import State

"""
auto_now_add=True -> Se asigna la fecha y hora solo al crear el registro (equivale a DEFAULT CURRENT_TIMESTAMP).

auto_now=True -> Se actualiza la fecha y hora cada vez que se guarda el registro (equivale a ON UPDATE CURRENT_TIMESTAMP).
"""


# Base model
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and saves a User with the given email and password.
        """

        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """

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


class Role(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")

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


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    state = models.CharField(max_length=20, choices=State.choices, default=State.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="products", null=True
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    unique_code = models.CharField(max_length=50, unique=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=20, choices=State.choices, default=State.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.PROTECT, related_name="inventories"
    )
    quantity = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - Stock: {self.quantity}"


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=120, unique=True)
    number_phone = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    state = models.CharField(max_length=20, choices=State.choices, default=State.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name}: {self.email}"


class Promotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    state = models.CharField(max_length=20, choices=State.choices, default=State.ACTIVE)

    def __str__(self):
        return f"{self.name} - Discount: {self.discount_percentage}%"


class CustomerPromotion(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer_promotions"
    )
    promotion = models.ForeignKey(
        Promotion, on_delete=models.CASCADE, related_name="customer_promotions"
    )
    applied = models.BooleanField(default=False)
    assignment_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "promotion"], name="unique_customer_promotion"
            )
        ]

    def __str__(self):
        return f"{self.customer} - {self.promotion} - Applied: {self.applied}"


class Invoice(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Cash"
        CARD = "CARD", "Card"
        TRANSFER = "TRANSFER", "Transfer"

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        related_name="invoices",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="created_invoices", null=True
    )
    number_invoice = models.CharField(max_length=50, unique=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )
    state = models.CharField(max_length=20, choices=State.choices, default=State.ACTIVE)
    issue_date = models.DateTimeField(auto_now_add=True)
    pdf_generated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.number_invoice} - {self.issue_date}"


class InventoryMovement(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="inventory_movements"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="inventory_movements", null=True
    )
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="details"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="invoice_details"
    )
    inventory_movement = models.OneToOneField(
        InventoryMovement, on_delete=models.PROTECT, related_name="invoice_detail"
    )
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.invoice.number_invoice} - {self.product.name}"


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=120)
    number_phone = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    state = models.CharField(max_length=20, choices=State.choices, default=State.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Purchase(models.Model):
    class StatePurchase(models.TextChoices):
        COMPLETED = "COMPLETED", "Completed"
        CANCELED = "CANCELED", "Canceled"

    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name="purchases"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="purchases", null=True
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(
        max_length=20, choices=StatePurchase.choices, default=StatePurchase.COMPLETED
    )

    def __str__(self):
        return f"{self.supplier.name} - {self.total_amount} - {self.purchase_date}"


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

    def __str__(self):
        return f"{self.purchase.supplier.name} - {self.product.name} - {self.quantity}"
