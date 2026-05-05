# Nexus Inventory API - Endpoints PATCH (con Campos)

Listado de todos los endpoints `PATCH` con los campos que pueden actualizarse.
En los `partial_update` **todos los campos son opcionales** — solo se envían los que se quieren modificar.
Los endpoints de acción (`/activate/`, `/deactivate/`, `/cancel/`) **no requieren body**.

---

## Usuarios

### `PATCH /v1/users/me/`
Actualizar el perfil del usuario autenticado. Usa `UserUpdateSerializer`.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `first_name` | string | Nombre del usuario |
| `last_name` | string | Apellido del usuario |
| `email` | string (email) | Correo electrónico (único) |
| `avatar` | file (image) | Foto de perfil |
| `nif` | string | NIF/DNI del usuario |
| `role` | integer (FK) | ID del rol (solo admin puede asignar rol admin) |

### `PATCH /v1/users/{id}/activate/`
> Sin body. Activa el usuario indicado.

### `PATCH /v1/users/{id}/deactivate/`
> Sin body. Desactiva el usuario indicado.

---

## Roles

### `PATCH /v1/roles/{id}/`
Actualizar un rol existente.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | string | Nombre del rol (único, case-insensitive) |
| `description` | string | Descripción del rol |

### `PATCH /v1/roles/{id}/activate/`
> Sin body. Activa el rol indicado.

### `PATCH /v1/roles/{id}/deactivate/`
> Sin body. Desactiva el rol indicado.

---

## Empresa

### `PATCH /v1/companies/{id}/`
Actualizar una empresa existente.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `nif` | string | NIF de la empresa (único) |
| `name` | string | Nombre de la empresa |
| `address` | string | Dirección |
| `number_phone` | string | Teléfono |
| `email` | string (email) | Correo electrónico |
| `website` | string (URL) | Sitio web |
| `logo` | file (image) | Logo de la empresa |

### `PATCH /v1/companies/{id}/activate/`
> Sin body. Activa la empresa indicada.

### `PATCH /v1/companies/{id}/deactivate/`
> Sin body. Desactiva la empresa indicada.

---

## Categorías

### `PATCH /v1/categories/{id}/`
Actualizar una categoría existente.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | string | Nombre de la categoría (único, case-insensitive) |
| `description` | string | Descripción de la categoría |

### `PATCH /v1/categories/{id}/activate/`
> Sin body. Activa la categoría indicada.

### `PATCH /v1/categories/{id}/deactivate/`
> Sin body. Desactiva la categoría indicada.

---

## Productos

### `PATCH /v1/products/{id}/`
Actualizar un producto existente.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `category_id` | integer (FK) | ID de la categoría (write_only) |
| `name` | string | Nombre del producto (único) |
| `description` | string | Descripción del producto |
| `unique_code` | string | Código único del producto |
| `sale_price` | decimal | Precio de venta (≥ 0) |
| `purchase_price` | decimal | Precio de compra (≥ 0, no puede superar `sale_price`) |
| `discount_percentage` | decimal | Porcentaje de descuento |

### `PATCH /v1/products/{id}/activate/`
> Sin body. Activa el producto indicado.

### `PATCH /v1/products/{id}/deactivate/`
> Sin body. Desactiva el producto indicado.

---

## Clientes

### `PATCH /v1/customers/{id}/`
Actualizar un cliente existente.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `first_name` | string | Nombre del cliente |
| `last_name` | string | Apellido del cliente |
| `email` | string (email) | Correo electrónico (único, case-insensitive) |
| `nif` | string | NIF/DNI del cliente (único si se proporciona) |
| `number_phone` | string | Teléfono |
| `address` | string | Dirección |

### `PATCH /v1/customers/{id}/activate/`
> Sin body. Activa el cliente indicado.

### `PATCH /v1/customers/{id}/deactivate/`
> Sin body. Desactiva el cliente indicado.

---

## Ventas

### `PATCH /v1/sales/{id}/`
Actualizar una venta existente. Usa `SaleCreateSerializer` en modo parcial.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `company_id` | integer (FK) | ID de la empresa (nullable) |
| `customer_id` | integer (FK) | ID del cliente (nullable) |
| `payment_method` | string | Método de pago |
| `details` | array | Lista de productos |

**Estructura de cada objeto en `details`:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `product_id` | integer (FK) | ID del producto |
| `quantity` | integer | Cantidad (min 1) |
| `unit_price` | decimal | Precio unitario (min 0.01) |

### `PATCH /v1/sales/{id}/cancel/`
> Sin body. Cancela la venta indicada (no reversible).

---

## Facturas

### `PATCH /v1/invoices/{id}/cancel/`
> Sin body. Cancela la factura indicada (no reversible).

---

## Proveedores

### `PATCH /v1/suppliers/{id}/`
Actualizar un proveedor existente.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | string | Nombre del proveedor (único, case-insensitive) |
| `email` | string (email) | Correo electrónico |
| `nif` | string | NIF del proveedor (único si se proporciona) |
| `number_phone` | string | Teléfono |
| `address` | string | Dirección |

### `PATCH /v1/suppliers/{id}/activate/`
> Sin body. Activa el proveedor indicado.

### `PATCH /v1/suppliers/{id}/deactivate/`
> Sin body. Desactiva el proveedor indicado.

---

## Compras

### `PATCH /v1/purchases/{id}/`
Actualizar una compra existente. Usa `PurchaseCreateSerializer` en modo parcial.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `company_id` | integer (FK) | ID de la empresa (nullable) |
| `supplier_id` | integer (FK) | ID del proveedor |
| `details` | array | Lista de productos |

**Estructura de cada objeto en `details`:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `product_id` | integer (FK) | ID del producto |
| `quantity` | integer | Cantidad (min 1) |
| `unit_cost` | decimal | Costo unitario (min 0.01) |

### `PATCH /v1/purchases/{id}/cancel/`
> Sin body. Cancela la compra indicada (no reversible).

---

## Devoluciones de Ventas

### `PATCH /v1/sale-returns/{id}/`
Actualizar una devolución de venta. Usa `SaleReturnCreateSerializer` en modo parcial.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `sale_id` | integer (FK) | ID de la venta original (no puede estar cancelada) |
| `reason` | string | Motivo de la devolución |
| `details` | array | Lista de productos a devolver |

**Estructura de cada objeto en `details`:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `product_id` | integer (FK) | ID del producto |
| `quantity` | integer | Cantidad a devolver (min 1) |
| `unit_price` | decimal | Precio unitario del reembolso (min 0.01) |

### `PATCH /v1/sale-returns/{id}/cancel/`
> Sin body. Cancela la devolución de venta indicada (no reversible).

---

## Devoluciones de Compras

### `PATCH /v1/purchase-returns/{id}/`
Actualizar una devolución de compra. Usa `PurchaseReturnCreateSerializer` en modo parcial.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `purchase_id` | integer (FK) | ID de la compra original (no puede estar cancelada) |
| `reason` | string | Motivo de la devolución |
| `details` | array | Lista de productos a devolver |

**Estructura de cada objeto en `details`:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `product_id` | integer (FK) | ID del producto |
| `quantity` | integer | Cantidad a devolver (min 1) |
| `unit_cost` | decimal | Costo unitario del reembolso (min 0.01) |

### `PATCH /v1/purchase-returns/{id}/cancel/`
> Sin body. Cancela la devolución de compra indicada (no reversible).

---

## Resumen Total

| # | Endpoint | Campos actualizables |
|---|---|---|
| 1 | `/v1/users/me/` | `first_name`, `last_name`, `email`, `avatar`, `nif`, `role` |
| 2 | `/v1/users/{id}/activate/` | — (sin body) |
| 3 | `/v1/users/{id}/deactivate/` | — (sin body) |
| 4 | `/v1/roles/{id}/` | `name`, `description` |
| 5 | `/v1/roles/{id}/activate/` | — (sin body) |
| 6 | `/v1/roles/{id}/deactivate/` | — (sin body) |
| 7 | `/v1/companies/{id}/` | `nif`, `name`, `address`, `number_phone`, `email`, `website`, `logo` |
| 8 | `/v1/companies/{id}/activate/` | — (sin body) |
| 9 | `/v1/companies/{id}/deactivate/` | — (sin body) |
| 10 | `/v1/categories/{id}/` | `name`, `description` |
| 11 | `/v1/categories/{id}/activate/` | — (sin body) |
| 12 | `/v1/categories/{id}/deactivate/` | — (sin body) |
| 13 | `/v1/products/{id}/` | `category_id`, `name`, `description`, `unique_code`, `sale_price`, `purchase_price`, `discount_percentage` |
| 14 | `/v1/products/{id}/activate/` | — (sin body) |
| 15 | `/v1/products/{id}/deactivate/` | — (sin body) |
| 16 | `/v1/customers/{id}/` | `first_name`, `last_name`, `email`, `nif`, `number_phone`, `address` |
| 17 | `/v1/customers/{id}/activate/` | — (sin body) |
| 18 | `/v1/customers/{id}/deactivate/` | — (sin body) |
| 19 | `/v1/sales/{id}/` | `company_id`, `customer_id`, `payment_method`, `details[]` |
| 20 | `/v1/sales/{id}/cancel/` | — (sin body) |
| 21 | `/v1/invoices/{id}/cancel/` | — (sin body) |
| 22 | `/v1/suppliers/{id}/` | `name`, `email`, `nif`, `number_phone`, `address` |
| 23 | `/v1/suppliers/{id}/activate/` | — (sin body) |
| 24 | `/v1/suppliers/{id}/deactivate/` | — (sin body) |
| 25 | `/v1/purchases/{id}/` | `company_id`, `supplier_id`, `details[]` |
| 26 | `/v1/purchases/{id}/cancel/` | — (sin body) |
| 27 | `/v1/sale-returns/{id}/` | `sale_id`, `reason`, `details[]` |
| 28 | `/v1/sale-returns/{id}/cancel/` | — (sin body) |
| 29 | `/v1/purchase-returns/{id}/` | `purchase_id`, `reason`, `details[]` |
| 30 | `/v1/purchase-returns/{id}/cancel/` | — (sin body) |

**Total: 30 endpoints PATCH**
