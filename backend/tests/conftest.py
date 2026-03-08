# Internal
import pytest

# DRF
from rest_framework.test import APIClient

# Django
from django.urls import reverse
from django.test import Client

# Models
from nexus_inventory_backend.db.models import User, Role, Category, Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def client():
    return Client()


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
def api_client_auth(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def normal_user(db, cashier_role):
    return User.objects.create_user(
        email="user@test.com", password="StrongPass123!", role=cashier_role
    )


@pytest.fixture
def payload_user(cashier_role):
    return {
        "email": "new@test.com",
        "password": "StrongPass123!",
        "role": cashier_role.id,
    }


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
def category(db):
    return Category.objects.create(
        name="Electronics", description="An electronics products"
    )


@pytest.fixture
def another_category(db):
    return Category.objects.create(name="Shoes", description="A shoes products")


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
def product(db, category):
    return Product.objects.create(
        category=category,
        name="Laptop",
        description="Huawei D16",
        unique_code="1234abcd",
        sale_price=400.00,
        purchase_price=440.00,
    )


@pytest.fixture
def another_product(db, another_category):
    return Product.objects.create(
        category=another_category,
        name="Movil",
        description="Samsung Galaxy S25 FE",
        unique_code="4321abcd",
        sale_price=650.00,
        purchase_price=740.00,
    )


@pytest.fixture
def payload_product(category):
    return {
        "category": category.pk,
        "name": "Product",
        "description": "Test product",
        "unique_code": "1234abcd",
        "sale_price": 160.00,
        "purchase_price": 200.00,
    }


@pytest.fixture
def payload_another_product(another_category):
    return {
        "category": another_category.pk,
        "name": "Product 2",
        "description": "Test product 2",
        "unique_code": "4321dcba",
        "sale_price": 230.00,
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
