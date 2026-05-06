# Internal
import pytest
import uuid

# DRF
from rest_framework.test import APIClient

# Django
from django.urls import reverse
from django.test import Client

# Models
from nexus_inventory_backend.db.models import (
    User,
    Role,
    Company,
    Category,
    Product,
    Inventory,
    InventoryMovement,
    Customer,
    Sale,
    SaleDetail,
    Invoice,
    Supplier,
    Purchase,
    SaleReturn,
    SaleReturnDetail,
    PurchaseReturn,
    PurchaseReturnDetail,
)

# Enums
from nexus_inventory_backend.db.enums import InvoiceState, InvoiceType

# Datetime


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
        first_name="admin",
        last_name="test",
        email="admin@test.com",
        nif=str(uuid.uuid4())[:10],
        password="StrongPass123!",
        role=admin_role,
    )


@pytest.fixture
def normal_user(db, cashier_role):
    return User.objects.create_user(
        first_name="user",
        last_name="test",
        email="user@test.com",
        nif=str(uuid.uuid4())[:10],
        password="StrongPass123!",
        role=cashier_role,
    )


@pytest.fixture
def company(db, admin_user):
    return Company.objects.create(
        nif=str(uuid.uuid4())[:10],
        name="Company",
        address="Address",
        number_phone="600000000",
        email="company@company.cat",
        website="https://company.cat",
        is_active=False,
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
def another_inventory_movements(db, another_product, admin_user):
    return InventoryMovement.objects.create(
        product=another_product,
        user=admin_user,
        quantity=20,
    )


@pytest.fixture
def customer(db):
    return Customer.objects.create(
        first_name="Eduardo",
        last_name="Bonilla",
        nif=str(uuid.uuid4())[:10],
        email="eduardobonilla@gmail.com",
        number_phone="640664411",
        address="Av. Espaillat 123, Bj 2",
    )


@pytest.fixture
def customer_inactive(db):
    return Customer.objects.create(
        first_name="Cliente",
        last_name="Inactivo",
        nif=str(uuid.uuid4())[:10],
        email="inactivo@test.com",
        number_phone="640000000",
        address="Dirección inactiva",
        is_active=False,
    )


@pytest.fixture
def another_customer(db):
    return Customer.objects.create(
        first_name="Rafael",
        last_name="Estrella",
        nif=str(uuid.uuid4())[:10],
        email="rafaelestrella@gmail.com",
        number_phone="640443322",
        address="Av. Argentina 12, Piso 4A",
    )


@pytest.fixture
def sale(db, company, customer, admin_user):
    return Sale.objects.create(
        company=company,
        customer=customer,
        user=admin_user,
        discount_amount=0,
        subtotal=100.00,
        tax_percentage=21.00,
        tax_amount=21.00,
        total_amount=121.00,
        payment_method="CASH",
        state="COMPLETED",
    )


@pytest.fixture
def another_sale(db, company, another_customer, normal_user):
    return Sale.objects.create(
        company=company,
        customer=another_customer,
        user=normal_user,
        discount_amount=0,
        subtotal=200.00,
        tax_percentage=21.00,
        tax_amount=42.00,
        total_amount=242.00,
        payment_method="CARD",
        state="COMPLETED",
    )


@pytest.fixture
def sale_detail(db, sale, product, inventory_movements):
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
    return SaleDetail.objects.create(
        sale=another_sale,
        product=another_product,
        inventory_movement=another_inventory_movements,
        quantity=4,
        unit_price=50.00,
        subtotal=200.00,
    )


@pytest.fixture
def purchase(db, company, supplier, admin_user, product):
    return Purchase.objects.create(
        company=company,
        supplier=supplier,
        user=admin_user,
        total_amount=200.00,
        state="COMPLETED",
    )


@pytest.fixture
def another_purchase(db, company, another_supplier, normal_user, another_product):
    return Purchase.objects.create(
        company=company,
        supplier=another_supplier,
        user=normal_user,
        total_amount=500.00,
        state="COMPLETED",
    )


@pytest.fixture
def invoice_sale(db, sale, admin_user):
    return Invoice.objects.create(
        company_id=sale.company.pk,
        sale=sale,
        number_invoice=f"SINV-{sale.pk:08d}-{uuid.uuid4().hex[:6].upper()}",
        invoice_type=InvoiceType.SALE,
        state=InvoiceState.ISSUED,
        created_by=admin_user,
    )


@pytest.fixture
def invoice_purchase(db, purchase, admin_user):
    return Invoice.objects.create(
        company_id=purchase.company.pk,
        purchase=purchase,
        number_invoice=f"PINV-{purchase.pk:08d}-{uuid.uuid4().hex[:6].upper()}",
        invoice_type=InvoiceType.PURCHASE,
        state=InvoiceState.ISSUED,
        created_by=admin_user,
    )


@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        name="Tech Supplies Inc",
        email="contact@techsupplies.com",
        nif=str(uuid.uuid4())[:10],
        number_phone="5551234567",
        address="123 Tech Lane, Silicon Valley",
    )


@pytest.fixture
def another_supplier(db):
    return Supplier.objects.create(
        name="Global Gadgets",
        email="sales@globalgadgets.net",
        nif=str(uuid.uuid4())[:10],
        number_phone="5559876543",
        address="456 Gadget Blvd, New York",
    )


@pytest.fixture
def sale_return(db, sale, admin_user):
    return SaleReturn.objects.create(
        sale=sale,
        user=admin_user,
        reason="Product defective",
        total_amount="100.00",
        state="COMPLETED",
    )


@pytest.fixture
def sale_return_detail(db, sale_return, product, admin_user):
    from nexus_inventory_backend.db.enums import MovementType

    inventory_movement = InventoryMovement.objects.create(
        product=product,
        user=admin_user,
        movement_type=MovementType.IN,
        quantity=2,
    )
    return SaleReturnDetail.objects.create(
        sale_return=sale_return,
        product=product,
        inventory_movement=inventory_movement,
        quantity=2,
        unit_price=50.00,
        subtotal=100.00,
    )


@pytest.fixture
def purchase_return(db, purchase, admin_user):
    return PurchaseReturn.objects.create(
        purchase=purchase,
        user=admin_user,
        reason="Product defective",
        total_amount="200.00",
        state="COMPLETED",
    )


@pytest.fixture
def purchase_return_detail(db, purchase_return, product, admin_user):
    from nexus_inventory_backend.db.enums import MovementType

    inventory_movement = InventoryMovement.objects.create(
        product=product,
        user=admin_user,
        movement_type=MovementType.OUT,
        quantity=2,
    )
    return PurchaseReturnDetail.objects.create(
        purchase_return=purchase_return,
        product=product,
        inventory_movement=inventory_movement,
        quantity=2,
        unit_cost=100.00,
        subtotal=200.00,
    )


# ======================================================================================================================================================================
# PAYLOADS
# ======================================================================================================================================================================
@pytest.fixture
def payload_user(cashier_role):
    return {
        "first_name": "new",
        "last_name": "test",
        "email": "new@test.com",
        "password": "StrongPass123!",
        "nif": str(uuid.uuid4())[:10],
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
def payload_company():
    return {
        "nif": "A09876543",
        "name": "Company Payload",
        "address": "Address",
        "number_phone": "600000000",
        "email": "company_payload@company.cat",
        "website": "https://company.cat",
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
        "unique_code": str(uuid.uuid4())[:10],
        "sale_price": 260.00,
        "purchase_price": 200.00,
        "discount_percentage": 20,
    }


@pytest.fixture
def payload_another_product(another_category):
    return {
        "category_id": another_category.pk,
        "name": "Product 2",
        "description": "Test product 2",
        "unique_code": str(uuid.uuid4())[:10],
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
def payload_product_with_same_name(category):
    return {
        "category_id": category.pk,
        "name": "LAPTOP",
        "description": "Laptop Product",
        "unique_code": str(uuid.uuid4())[:10],
        "sale_price": 300.00,
        "purchase_price": 200.00,
        "discount_percentage": 10,
    }


@pytest.fixture
def payload_customer():
    return {
        "first_name": "Abel",
        "last_name": "Torres",
        "nif": str(uuid.uuid4())[:10],
        "email": "abeltorres@gmail.com",
        "number_phone": "666313110",
        "address": "Carrer De Albacete 54, Atico A",
    }


@pytest.fixture
def payload_sale(company, customer, product, inventory):
    return {
        "company": company.pk,
        "customer": customer.pk,
        "payment_method": "CASH",
        "details": [{"product_id": product.pk, "quantity": 2, "unit_price": "100.00"}],
    }


@pytest.fixture
def payload_another_sale(company, another_customer, another_product, inventory):
    return {
        "company": company.pk,
        "customer": another_customer.pk,
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
        "nif": str(uuid.uuid4())[:10],
        "number_phone": "5551112233",
        "address": "789 Tech Road",
    }


@pytest.fixture
def payload_supplier_no_email():
    return {
        "name": "New Tech Supplier 2",
        "nif": str(uuid.uuid4())[:10],
        "number_phone": "5551112233",
        "address": "789 Tech Road",
    }


@pytest.fixture
def payload_purchase(company, supplier, product, inventory):
    return {
        "company": company.pk,
        "supplier": supplier.pk,
        "details": [{"product_id": product.pk, "quantity": 2, "unit_cost": "100.00"}],
    }


@pytest.fixture
def payload_another_purchase(
    company, another_supplier, another_product, another_inventory
):
    return {
        "company": company.pk,
        "supplier": another_supplier.pk,
        "details": [
            {"product_id": another_product.pk, "quantity": 1, "unit_cost": "250.00"}
        ],
    }


@pytest.fixture
def payload_sale_return(sale, product, sale_detail):
    return {
        "sale": sale.pk,
        "reason": "Product not as described",
        "details": [{"product_id": product.pk, "quantity": 1, "unit_price": "50.00"}],
    }


@pytest.fixture
def sale_return_payload_no_details(sale):
    return {
        "sale": sale.pk,
        "reason": "Product not as described",
    }


@pytest.fixture
def payload_sale_return_exceeds_quantity(sale, product, sale_detail):
    return {
        "sale": sale.pk,
        "reason": "Product not as described",
        "details": [{"product_id": product.pk, "quantity": 100, "unit_price": "50.00"}],
    }


@pytest.fixture
def payload_purchase_return(purchase, product, purchase_detail):
    return {
        "purchase": purchase.pk,
        "reason": "Product not as described",
        "details": [{"product_id": product.pk, "quantity": 1, "unit_cost": "100.00"}],
    }


@pytest.fixture
def purchase_return_payload_no_details(purchase):
    return {
        "purchase": purchase.pk,
        "reason": "Product not as described",
    }


@pytest.fixture
def payload_purchase_return_exceeds_quantity(purchase, product, purchase_detail):
    return {
        "purchase": purchase.pk,
        "reason": "Product not as described",
        "details": [{"product_id": product.pk, "quantity": 100, "unit_cost": "100.00"}],
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
def url_password_reset_request():
    return reverse("password-reset-request")


@pytest.fixture
def url_password_reset_confirm():
    return reverse("password-reset-confirm")


@pytest.fixture
def companies_url():
    return reverse("companies-list")


@pytest.fixture
def company_detail_url():
    def _url(pk):
        return reverse("companies-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def company_activate_url():
    def _url(pk):
        return reverse("companies-activate", kwargs={"pk": pk})

    return _url


@pytest.fixture
def company_deactivate_url():
    def _url(pk):
        return reverse("companies-deactivate", kwargs={"pk": pk})

    return _url


@pytest.fixture
def categories_url():
    return reverse("categories-list")


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
    return reverse("inventory-movements-list")


@pytest.fixture
def inventory_movements_detail_url():
    def _url(pk):
        return reverse("inventory-movements-detail", kwargs={"pk": pk})

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
def sales_url():
    return reverse("sales-list")


@pytest.fixture
def sale_detail_url():
    def _url(pk):
        return reverse("sales-detail", kwargs={"pk": pk})

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
def sale_returns_url():
    return reverse("sale-returns-list")


@pytest.fixture
def sale_return_detail_url():
    def _url(pk):
        return reverse("sale-returns-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def sale_return_details_url():
    def _url(sale_return_pk):
        return reverse(
            "sale-return-detail-list", kwargs={"sale_returns_pk": sale_return_pk}
        )

    return _url


@pytest.fixture
def sale_return_detail_item_url():
    def _url(sale_return_pk, pk):
        return reverse(
            "sale-return-detail-detail",
            kwargs={"sale_returns_pk": sale_return_pk, "pk": pk},
        )

    return _url


@pytest.fixture
def purchase_returns_url():
    return reverse("purchase-returns-list")


@pytest.fixture
def purchase_return_detail_url():
    def _url(pk):
        return reverse("purchase-returns-detail", kwargs={"pk": pk})

    return _url


@pytest.fixture
def purchase_return_details_url():
    def _url(purchase_return_pk):
        return reverse(
            "purchase-return-detail-list",
            kwargs={"purchase_returns_pk": purchase_return_pk},
        )

    return _url


@pytest.fixture
def purchase_return_detail_item_url():
    def _url(purchase_return_pk, pk):
        return reverse(
            "purchase-return-detail-detail",
            kwargs={"purchase_returns_pk": purchase_return_pk, "pk": pk},
        )

    return _url


@pytest.fixture
def url_reports_sales():
    return reverse("sale-reports-list")


@pytest.fixture
def url_reports_sales_by_customer():
    return f"{reverse('sale-reports-list')}?group_by=customer"


@pytest.fixture
def url_reports_sales_by_payment_method():
    return f"{reverse('sale-reports-list')}?group_by=payment_method"


@pytest.fixture
def url_reports_sales_by_period():
    return f"{reverse('sale-reports-list')}?group_by=period"


@pytest.fixture
def url_reports_purchases():
    return reverse("purchase-reports-list")


@pytest.fixture
def url_reports_purchases_by_supplier():
    return f"{reverse('purchase-reports-list')}?group_by=supplier"


@pytest.fixture
def url_reports_purchases_by_period():
    return f"{reverse('purchase-reports-list')}?group_by=period"


@pytest.fixture
def url_reports_inventory():
    return reverse("inventory-reports-list")


@pytest.fixture
def url_reports_inventory_low_stock():
    return f"{reverse('inventory-reports-list')}?view=low_stock"


@pytest.fixture
def url_reports_inventory_movements():
    return f"{reverse('inventory-reports-list')}?view=movements"


@pytest.fixture
def url_reports_products_top_selling():
    return f"{reverse('product-reports-list')}?view=top_selling"


@pytest.fixture
def url_reports_products_low_selling():
    return f"{reverse('product-reports-list')}?view=low_selling"


@pytest.fixture
def url_reports_products_most_purchased():
    return f"{reverse('product-reports-list')}?view=most_purchased"


@pytest.fixture
def url_reports_products_by_category():
    return f"{reverse('product-reports-list')}?view=by_category"


@pytest.fixture
def url_reports_customers_top():
    return f"{reverse('customer-reports-list')}?view=top_customers"


@pytest.fixture
def url_reports_invoices():
    return reverse("invoice-reports-list")


@pytest.fixture
def url_reports_invoices_sales():
    return f"{reverse('invoice-reports-list')}?invoice_type=SALE"


@pytest.fixture
def url_reports_invoices_purchases():
    return f"{reverse('invoice-reports-list')}?invoice_type=PURCHASE"


@pytest.fixture
def url_reports_sale_returns():
    return f"{reverse('return-reports-list')}?type=sale"


@pytest.fixture
def url_reports_purchase_returns():
    return f"{reverse('return-reports-list')}?type=purchase"


@pytest.fixture
def url_reports_sales_pdf():
    return reverse("sale-reports-sales-pdf")


@pytest.fixture
def url_reports_sales_by_customer_pdf():
    return f"{reverse('sale-reports-sales-pdf')}?group_by=customer"


@pytest.fixture
def url_reports_sales_by_payment_method_pdf():
    return f"{reverse('sale-reports-sales-pdf')}?group_by=payment_method"


@pytest.fixture
def url_reports_sales_by_period_pdf():
    return f"{reverse('sale-reports-sales-pdf')}?group_by=period"


@pytest.fixture
def url_reports_purchases_pdf():
    return reverse("purchase-reports-purchases-pdf")


@pytest.fixture
def url_reports_purchases_by_supplier_pdf():
    return f"{reverse('purchase-reports-purchases-pdf')}?group_by=supplier"


@pytest.fixture
def url_reports_purchases_by_period_pdf():
    return f"{reverse('purchase-reports-purchases-pdf')}?group_by=period"


@pytest.fixture
def url_reports_inventory_pdf():
    return reverse("inventory-reports-inventory-pdf")


@pytest.fixture
def url_reports_inventory_low_stock_pdf():
    return f"{reverse('inventory-reports-inventory-pdf')}?view=low_stock"


@pytest.fixture
def url_reports_inventory_movements_pdf():
    return f"{reverse('inventory-reports-inventory-pdf')}?view=movements"


@pytest.fixture
def url_reports_products_pdf():
    return reverse("product-reports-products-pdf")


@pytest.fixture
def url_reports_products_top_selling_pdf():
    return f"{reverse('product-reports-products-pdf')}?view=top_selling"


@pytest.fixture
def url_reports_products_low_selling_pdf():
    return f"{reverse('product-reports-products-pdf')}?view=low_selling"


@pytest.fixture
def url_reports_products_most_purchased_pdf():
    return f"{reverse('product-reports-products-pdf')}?view=most_purchased"


@pytest.fixture
def url_reports_products_by_category_pdf():
    return f"{reverse('product-reports-products-pdf')}?view=by_category"


@pytest.fixture
def url_reports_customers_pdf():
    return reverse("customer-reports-customers-pdf")


@pytest.fixture
def url_reports_customers_top_pdf():
    return f"{reverse('customer-reports-customers-pdf')}?view=top_customers"


@pytest.fixture
def url_reports_invoices_pdf():
    return reverse("invoice-reports-invoices-pdf")


@pytest.fixture
def url_reports_invoices_sales_pdf():
    return f"{reverse('invoice-reports-invoices-pdf')}?invoice_type=SALE"


@pytest.fixture
def url_reports_invoices_purchases_pdf():
    return f"{reverse('invoice-reports-invoices-pdf')}?invoice_type=PURCHASE"


@pytest.fixture
def url_reports_sale_returns_pdf():
    return f"{reverse('return-reports-returns-pdf')}?type=sale"


@pytest.fixture
def url_reports_purchase_returns_pdf():
    return f"{reverse('return-reports-returns-pdf')}?type=purchase"
