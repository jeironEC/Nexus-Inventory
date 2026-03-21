# Internal
import pytest

# DRF
from rest_framework.test import APIClient

# Django
from django.urls import reverse
from django.test import Client
from django.utils import timezone

# Models
from nexus_inventory_backend.db.models import (
    User,
    Role,
    Category,
    Product,
    Inventory,
    InventoryMovement,
    Customer,
    Promotion,
    CustomerPromotion,
    Sale,
    Invoice,
    Supplier,
    Purchase,
)

# Datetime
from datetime import timedelta


# ======================================================================================================================================================================
# GLOBAL
# ======================================================================================================================================================================
@pytest.fixture(autouse=True)
def disable_throttling(settings, request):
    rf = getattr(settings, "REST_FRAMEWORK", {})
    rf.update({"DEFAULT_THROTTLE_CLASSES": []})
    settings.REST_FRAMEWORK = rf


# ======================================================================================================================================================================
# CLIENTS
# ======================================================================================================================================================================
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def api_client_auth(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


# ======================================================================================================================================================================
# OBJECTS DATABASE
# ======================================================================================================================================================================
@pytest.fixture
def admin_role(db):
    return Role.objects.create(name="ADMIN", description="Administrador de usuarios")


@pytest.fixture
def cashier_role(db):
    return Role.objects.create(name="CAJERO", description="Realiza ventas a clientes")


@pytest.fixture
def sales_manager_role(db):
    return Role.objects.create(
        name="encargado de ventas", description="Controla las ventas"
    )


@pytest.fixture
def purchasing_manager_role(db):
    return Role.objects.create(
        name="encargado de ventas", description="Controla las compras"
    )


@pytest.fixture
def admin_user(db, admin_role):
    return User.objects.create_user(
        email="admin@test.com", password="StrongPass123!", role=admin_role
    )


@pytest.fixture
def normal_user(db, cashier_role):
    return User.objects.create_user(
        email="user@test.com", password="StrongPass123!", role=cashier_role
    )


@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Electronics", description="An electronics products"
    )


@pytest.fixture
def another_category(db):
    return Category.objects.create(name="Shoes", description="A shoes products")


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        category_id=category.pk,
        name="Laptop",
        description="Huawei D16",
        unique_code="1234abcd",
        sale_price=400.00,
        purchase_price=440.00,
    )


@pytest.fixture
def another_product(db, another_category):
    return Product.objects.create(
        category_id=another_category.pk,
        name="Movil",
        description="Samsung Galaxy S25 FE",
        unique_code="4321abcd",
        sale_price=650.00,
        purchase_price=740.00,
    )


@pytest.fixture
def inventory(db, product):
    return Inventory.objects.create(product=product, quantity=10)


@pytest.fixture
def another_inventory(db, another_product):
    return Inventory.objects.create(product=another_product, quantity=10)


@pytest.fixture
def low_inventory(db, another_product):
    return Inventory.objects.create(product=another_product, quantity=4)


@pytest.fixture
def inventory_movements(db, product, admin_user):
    return InventoryMovement.objects.create(
        product=product,
        user=admin_user,
        quantity=10,
    )


@pytest.fixture
def another_inventory_movements(db, another_product):
    return InventoryMovement.objects.create(
        product=another_product,
        user=None,
        quantity=20,
    )


@pytest.fixture
def customer(db):
    return Customer.objects.create(
        first_name="Eduardo",
        last_name="Bonilla",
        email="eduardobonilla@gmail.com",
        number_phone="640664411",
        address="Av. Espaillat 123, Bj 2",
    )


@pytest.fixture
def another_customer(db):
    return Customer.objects.create(
        first_name="Rafael",
        last_name="Estrella",
        email="rafaelestrella@gmail.com",
        number_phone="640443322",
        address="Av. Argentina 12, Piso 4A",
    )


@pytest.fixture
def promotion(db):
    return Promotion.objects.create(
        name="promotion 2027",
        description="promotion description 2027",
        discount_percentage=20,
        start_date=timezone.now().date().isoformat(),
        end_date=(timezone.now() + timedelta(days=30)).date().isoformat(),
    )


@pytest.fixture
def another_promotion(db):
    return Promotion.objects.create(
        name="promotion 2028",
        description="promotion description 2028",
        discount_percentage=30,
        start_date=timezone.now().date().isoformat(),
        end_date=(timezone.now() + timedelta(days=30)).date().isoformat(),
    )


@pytest.fixture
def customer_promotion(db, customer, promotion):
    return CustomerPromotion.objects.create(
        customer=customer,
        promotion=promotion,
        applied=True,
    )


@pytest.fixture
def another_customer_promotion(db, another_customer, another_promotion):
    return CustomerPromotion.objects.create(
        customer=another_customer,
        promotion=another_promotion,
        applied=False,
    )


@pytest.fixture
def sale(db, customer, admin_user):
    return Sale.objects.create(
        customer=customer,
        user=admin_user,
        subtotal=100.00,
        tax_amount=21.00,
        total_amount=121.00,
        payment_method="CASH",
        state="COMPLETED",
    )


@pytest.fixture
def another_sale(db, another_customer, normal_user):
    return Sale.objects.create(
        customer=another_customer,
        user=normal_user,
        subtotal=200.00,
        tax_amount=42.00,
        total_amount=242.00,
        payment_method="CARD",
        state="COMPLETED",
    )


@pytest.fixture
def sale_detail(db, sale, product, inventory_movements):
    from nexus_inventory_backend.db.models import SaleDetail

    return SaleDetail.objects.create(
        sale=sale,
        product=product,
        inventory_movement=inventory_movements,
        quantity=2,
        unit_price=50.00,
        subtotal=100.00,
    )


@pytest.fixture
def another_sale_detail(db, another_sale, another_product, another_inventory_movements):
    from nexus_inventory_backend.db.models import SaleDetail

    return SaleDetail.objects.create(
        sale=another_sale,
        product=another_product,
        inventory_movement=another_inventory_movements,
        quantity=4,
        unit_price=50.00,
        subtotal=200.00,
    )


@pytest.fixture
def invoice(db, sale, admin_user):
    from nexus_inventory_backend.db.enums import InvoiceState

    return Invoice.objects.create(
        sale=sale,
        number_invoice=f"INV-{sale.pk:08d}",
        state=InvoiceState.ISSUED,
        created_by=admin_user,
    )


@pytest.fixture
def another_invoice(db, another_sale, normal_user):
    from nexus_inventory_backend.db.enums import InvoiceState

    return Invoice.objects.create(
        sale=another_sale,
        number_invoice=f"INV-{another_sale.pk:08d}",
        state=InvoiceState.ISSUED,
        created_by=normal_user,
    )


@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        name="Tech Supplies Inc",
        email="contact@techsupplies.com",
        number_phone="5551234567",
        address="123 Tech Lane, Silicon Valley",
    )


@pytest.fixture
def another_supplier(db):
    return Supplier.objects.create(
        name="Global Gadgets",
        email="sales@globalgadgets.net",
        number_phone="5559876543",
        address="456 Gadget Blvd, New York",
    )


# ======================================================================================================================================================================
# PAYLOADS
# ======================================================================================================================================================================
@pytest.fixture
def payload_user(cashier_role):
    return {
        "email": "new@test.com",
        "password": "StrongPass123!",
        "role": cashier_role.id,
    }


@pytest.fixture
def payload_role_cashier():
    return {"name": "Cajero", "description": "Realiza ventas a clientes"}


@pytest.fixture
def payload_role_no_name():
    return {"description": "Realiza ventas a clientes"}


@pytest.fixture
def payload_role_no_description():
    return {
        "name": "Cajero",
    }


@pytest.fixture
def payload_category():
    return {
        "name": "Electronics",
        "description": "An electronics products",
    }


@pytest.fixture
def payload_another_category():
    return {
        "name": "Shoes",
        "description": "A shoes products",
    }


@pytest.fixture
def payload_category_no_name():
    return {"description": "An electronics products"}


@pytest.fixture
def payload_product(category):
    return {
        "category_id": category.pk,
        "name": "Product",
        "description": "Test product",
        "unique_code": "1234abcd",
        "sale_price": 260.00,
        "purchase_price": 200.00,
    }


@pytest.fixture
def payload_another_product(another_category):
    return {
        "category_id": another_category.pk,
        "name": "Product 2",
        "description": "Test product 2",
        "unique_code": "4321dcba",
        "sale_price": 330.00,
        "purchase_price": 250.00,
    }


@pytest.fixture
def payload_product_no_unique_code(category):
    return {
        "category": category.pk,
        "name": "Product",
        "description": "Test product",
        "sale_price": 160.00,
        "purchase_price": 200.00,
    }


@pytest.fixture
def payload_customer():
    return {
        "first_name": "Abel",
        "last_name": "Torres",
        "email": "abeltorres@gmail.com",
        "number_phone": "666313110",
        "address": "Carrer De Albacete 54, Atico A",
    }


@pytest.fixture
def payload_promotion():
    return {
        "name": "promotion 2026",
        "description": "promotion description",
        "discount_percentage": 20,
        "start_date": timezone.now().date().isoformat(),
        "end_date": (timezone.now() + timedelta(days=30)).date().isoformat(),
    }


@pytest.fixture
def another_payload_promotion():
    return {
        "name": "promotion 2028",
        "description": "promotion description",
        "discount_percentage": 20,
        "start_date": timezone.now().date().isoformat(),
        "end_date": (timezone.now() + timedelta(days=30)).date().isoformat(),
    }


@pytest.fixture
def payload_customer_promotion(db, customer, promotion):
    return {
        "customer_id": customer.pk,
        "promotion_id": promotion.pk,
        "applied": True,
    }


@pytest.fixture
def payload_another_customer_promotion(db, another_customer, another_promotion):
    return {
        "customer_id": another_customer.pk,
        "promotion_id": another_promotion.pk,
        "applied": False,
    }


@pytest.fixture
def payload_sale(customer, product):
    return {
        "customer_id": customer.pk,
        "payment_method": "CASH",
        "details": [{"product_id": product.pk, "quantity": 2, "unit_price": "100.00"}],
    }


@pytest.fixture
def payload_another_sale(another_customer, another_product):
    return {
        "customer_id": another_customer.pk,
        "payment_method": "CARD",
        "details": [
            {"product_id": another_product.pk, "quantity": 1, "unit_price": "50.00"}
        ],
    }


@pytest.fixture
def payload_supplier():
    return {
        "name": "New Tech Supplier",
        "email": "new@techsupplies.com",
        "number_phone": "5551112233",
        "address": "789 Tech Road",
    }


@pytest.fixture
def payload_supplier_no_email():
    return {
        "name": "New Tech Supplier 2",
        "number_phone": "5551112233",
        "address": "789 Tech Road",
    }


@pytest.fixture
def purchase(db, supplier, admin_user, product):
    return Purchase.objects.create(
        supplier=supplier,
        user=admin_user,
        total_amount="200.00",
        state="COMPLETED",
    )


@pytest.fixture
def another_purchase(db, another_supplier, normal_user, another_product):
    return Purchase.objects.create(
        supplier=another_supplier,
        user=normal_user,
        total_amount="500.00",
        state="COMPLETED",
    )


@pytest.fixture
def payload_purchase(supplier, product):
    return {
        "supplier_id": supplier.pk,
        "details": [{"product_id": product.pk, "quantity": 2, "unit_cost": "100.00"}],
    }


@pytest.fixture
def payload_another_purchase(another_supplier, another_product):
    return {
        "supplier_id": another_supplier.pk,
        "details": [
            {"product_id": another_product.pk, "quantity": 1, "unit_cost": "250.00"}
        ],
    }


# ======================================================================================================================================================================
# URLS
# ======================================================================================================================================================================
@pytest.fixture
def url_users_list():
    return reverse("users-list")


@pytest.fixture
def url_user_me():
    return reverse("user-me")


@pytest.fixture
def url_token():
    return reverse("token_obtain_pair")


@pytest.fixture
def url_token_refresh():
    return reverse("token_refresh")


@pytest.fixture
def url_token_verify():
    return reverse("token_verify")


@pytest.fixture
def roles_url():
    return reverse("roles-list")


@pytest.fixture
def role_detail_url():
    def _url(pk):
        return reverse("roles-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def categories_url():
    return reverse("categories-list")


@pytest.fixture
def categories_actives_url():
    return reverse("categories-active")


@pytest.fixture
def categories_inactives_url():
    return reverse("categories-inactive")


@pytest.fixture
def category_detail_url():
    def _url(pk):
        return reverse("categories-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def category_activate_url():
    def _url(pk):
        return reverse("categories-activate", kwargs={"pk": pk})

    return _url


@pytest.fixture
def category_deactivate_url():
    def _url(pk):
        return reverse("categories-deactivate", kwargs={"pk": pk})

    return _url


@pytest.fixture
def products_url():
    return reverse("products-list")


@pytest.fixture
def products_actives_url():
    return reverse("products-active")


@pytest.fixture
def products_inactives_url():
    return reverse("products-inactive")


@pytest.fixture
def product_detail_url():
    def _url(pk):
        return reverse("products-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def product_activate_url():
    def _url(pk):
        return reverse("products-activate", kwargs={"pk": pk})

    return _url


@pytest.fixture
def product_deactivate_url():
    def _url(pk):
        return reverse("products-deactivate", kwargs={"pk": pk})

    return _url


@pytest.fixture
def inventories_url():
    return reverse("inventories-list")


@pytest.fixture
def inventory_detail_url():
    def _url(pk):
        return reverse("inventories-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def inventories_product_url():
    def _url(pk):
        return reverse("inventories-get-by-product", kwargs={"product_id": pk})

    return _url


@pytest.fixture
def inventories_low_stock_url():
    return reverse("inventories-low-stock")


@pytest.fixture
def inventory_movements_url():
    return reverse("inventory_movements-list")


@pytest.fixture
def inventory_movements_detail_url():
    def _url(pk):
        return reverse("inventory_movements-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def customers_url():
    return reverse("customers-list")


@pytest.fixture
def customer_detail_url():
    def _url(pk):
        return reverse("customers-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def promotions_url():
    return reverse("promotions-list")


@pytest.fixture
def promotion_detail_url():
    def _url(pk):
        return reverse("promotions-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def customer_promotions_url():
    return reverse("customer_promotions-list")


@pytest.fixture
def customer_promotion_detail_url():
    def _url(pk):
        return reverse("customer_promotions-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def customer_list_promotions_url():
    def _url(pk):
        return reverse("customers-list-promotions", kwargs={"pk": pk})

    return _url


@pytest.fixture
def customer_promotion_assign_url():
    def _url(pk):
        return reverse("customers-add-promotion", kwargs={"pk": pk})

    return _url


@pytest.fixture
def sales_url():
    return reverse("sales-list")


@pytest.fixture
def sale_detail_url():
    def _url(pk):
        return reverse("sales-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def sale_cancel_url():
    def _url(pk):
        return reverse("sales-cancel", kwargs={"pk": pk})

    return _url


@pytest.fixture
def sale_details_url():
    def _url(sale_pk):
        return reverse("sale-detail-list", kwargs={"sales_pk": sale_pk})

    return _url


@pytest.fixture
def sale_detail_item_url():
    def _url(sale_pk, pk):
        return reverse("sale-detail-detail", kwargs={"sales_pk": sale_pk, "pk": pk})

    return _url


@pytest.fixture
def invoices_url():
    return reverse("invoices-list")


@pytest.fixture
def invoice_detail_url():
    def _url(pk):
        return reverse("invoices-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def invoice_cancel_url():
    def _url(pk):
        return reverse("invoices-cancel", kwargs={"pk": pk})

    return _url


@pytest.fixture
def suppliers_url():
    return reverse("suppliers-list")


@pytest.fixture
def supplier_detail_url():
    def _url(pk):
        return reverse("suppliers-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def purchases_url():
    return reverse("purchases-list")


@pytest.fixture
def purchase_detail_url():
    def _url(pk):
        return reverse("purchases-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def purchase_cancel_url():
    def _url(pk):
        return reverse("purchases-cancel", kwargs={"pk": pk})

    return _url


@pytest.fixture
def purchase_details_url():
    def _url(purchase_pk):
        return reverse("purchase-detail-list", kwargs={"purchases_pk": purchase_pk})

    return _url


@pytest.fixture
def purchase_detail_item_url():
    def _url(purchase_pk, pk):
        return reverse(
            "purchase-detail-detail", kwargs={"purchases_pk": purchase_pk, "pk": pk}
        )

    return _url


@pytest.fixture
def url_reports_sales():
    return reverse("sale-reports-sales")


@pytest.fixture
def url_reports_sales_by_customer():
    return reverse("sale-reports-sales-by-customer")


@pytest.fixture
def url_reports_sales_by_payment_method():
    return reverse("sale-reports-sales-by-payment-method")


@pytest.fixture
def url_reports_sales_by_period():
    return reverse("sale-reports-sales-by-period")


@pytest.fixture
def url_reports_purchases():
    return reverse("purchase-reports-purchases")


@pytest.fixture
def url_reports_purchases_by_supplier():
    return reverse("purchase-reports-purchases-by-supplier")


@pytest.fixture
def url_reports_purchases_by_period():
    return reverse("purchase-reports-purchases-by-period")


@pytest.fixture
def url_reports_inventory():
    return reverse("inventory-reports-inventory")


@pytest.fixture
def url_reports_inventory_low_stock():
    return reverse("inventory-reports-low-stock")


@pytest.fixture
def url_reports_inventory_movements():
    return reverse("inventory-reports-movements")


@pytest.fixture
def url_reports_products_top_selling():
    return reverse("product-reports-top-selling")


@pytest.fixture
def url_reports_products_low_selling():
    return reverse("product-reports-low-selling")


@pytest.fixture
def url_reports_products_most_purchased():
    return reverse("product-reports-most-purchased")


@pytest.fixture
def url_reports_products_by_category():
    return reverse("product-reports-by-category")


@pytest.fixture
def url_reports_customers_top():
    return reverse("customer-reports-top-customers")


@pytest.fixture
def url_reports_customers_promotions():
    return reverse("customer-reports-customer-promotions")


@pytest.fixture
def url_reports_invoices():
    return reverse("invoice-reports-invoices")
