# Nexus Inventory API - Endpoints POST (con Campos)

Listado de todos los endpoints que aceptan el método `POST` en la API (`/v1/`) con los campos esperados en el body de la petición.

---

## Autenticación

### `POST /v1/auth/token/`
Obtener par de tokens JWT (login).

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `email` | string (email) | ✅ | Correo electrónico del usuario |
| `password` | string | ✅ | Contraseña del usuario |

### `POST /v1/auth/token/refresh/`
Refrescar el access token.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `refresh` | string | ✅ | El refresh token JWT vigente |

### `POST /v1/auth/token/verify/`
Verificar si un token es válido.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `token` | string | ✅ | Token JWT a verificar |

---

## Recuperación de Contraseña

### `POST /v1/password-reset/request/`
Solicitar código OTP por correo.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `email` | string (email) | ✅ | Correo electrónico registrado |

### `POST /v1/password-reset/verify/`
Verificar el código OTP.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `email` | string (email) | ✅ | Correo electrónico registrado |
| `otp` | string (6 chars) | ✅ | Código OTP de 6 dígitos |

### `POST /v1/password-reset/confirm/`
Confirmar nueva contraseña.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `reset_token` | UUID | ✅ | Token de recuperación recibido en verify |
| `new_password` | string (min 8) | ✅ | Nueva contraseña (write_only) |

---

## Usuarios

### `POST /v1/users/`
Crear un nuevo usuario.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `first_name` | string | ❌ | Nombre del usuario |
| `last_name` | string | ❌ | Apellido del usuario |
| `email` | string (email) | ✅ | Correo electrónico (único) |
| `password` | string | ✅ | Contraseña (write_only, validada por Django) |
| `nif` | string | ❌ | NIF/DNI del usuario (único) |
| `role` | integer (FK) | ✅ | ID del rol a asignar |

---

## Roles

### `POST /v1/roles/`
Crear un nuevo rol.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `name` | string | ✅ | Nombre del rol (único, case-insensitive) |
| `description` | string | ❌ | Descripción del rol |

---

## Empresa

### `POST /v1/companies/`
Crear una nueva empresa.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `nif` | string | ✅ | NIF de la empresa (único) |
| `name` | string | ✅ | Nombre de la empresa |
| `address` | string | ❌ | Dirección |
| `number_phone` | string | ❌ | Teléfono |
| `email` | string (email) | ❌ | Correo electrónico |
| `website` | string (URL) | ❌ | Sitio web |
| `logo` | file (image) | ❌ | Logo de la empresa |

---

## Categorías

### `POST /v1/categories/`
Crear una nueva categoría.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `name` | string | ✅ | Nombre de la categoría (único, case-insensitive) |
| `description` | string | ❌ | Descripción de la categoría |

---

## Productos

### `POST /v1/products/`
Crear un nuevo producto. Al crearse, se genera automáticamente un registro de inventario con cantidad 0.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `category_id` | integer (FK) | ✅ | ID de la categoría (write_only) |
| `name` | string | ✅ | Nombre del producto (único) |
| `description` | string | ❌ | Descripción del producto |
| `unique_code` | string | ❌ | Código único del producto |
| `sale_price` | decimal | ✅ | Precio de venta (≥ 0) |
| `purchase_price` | decimal | ✅ | Precio de compra (≥ 0, no puede superar `sale_price`) |
| `discount_percentage` | decimal | ❌ | Porcentaje de descuento |

---

## Clientes

### `POST /v1/customers/`
Crear un nuevo cliente.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `first_name` | string | ❌ | Nombre del cliente |
| `last_name` | string | ❌ | Apellido del cliente |
| `email` | string (email) | ✅ | Correo electrónico (único, case-insensitive) |
| `nif` | string | ❌ | NIF/DNI del cliente (único si se proporciona) |
| `number_phone` | string | ❌ | Teléfono |
| `address` | string | ❌ | Dirección |

---

## Ventas

### `POST /v1/sales/`
Crear una nueva venta. Se crea automáticamente una factura y los movimientos de inventario (OUT).

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `company_id` | integer (FK) | ❌ | ID de la empresa (nullable) |
| `customer_id` | integer (FK) | ❌ | ID del cliente (nullable) |
| `payment_method` | string | ✅ | Método de pago |
| `details` | array | ✅ | Lista de productos (mínimo 1) |

**Estructura de cada objeto en `details`:**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `product_id` | integer (FK) | ✅ | ID del producto |
| `quantity` | integer | ✅ | Cantidad (min 1) |
| `unit_price` | decimal | ✅ | Precio unitario (min 0.01) |

---

## Proveedores

### `POST /v1/suppliers/`
Crear un nuevo proveedor.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `name` | string | ✅ | Nombre del proveedor (único, case-insensitive) |
| `email` | string (email) | ❌ | Correo electrónico |
| `nif` | string | ❌ | NIF del proveedor (único si se proporciona) |
| `number_phone` | string | ❌ | Teléfono |
| `address` | string | ❌ | Dirección |

---

## Compras

### `POST /v1/purchases/`
Crear una nueva compra. Se crea automáticamente una factura y los movimientos de inventario (IN).

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `company_id` | integer (FK) | ❌ | ID de la empresa (nullable) |
| `supplier_id` | integer (FK) | ✅ | ID del proveedor |
| `details` | array | ✅ | Lista de productos (mínimo 1) |

**Estructura de cada objeto en `details`:**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `product_id` | integer (FK) | ✅ | ID del producto |
| `quantity` | integer | ✅ | Cantidad (min 1) |
| `unit_cost` | decimal | ✅ | Costo unitario (min 0.01) |

---

## Devoluciones de Ventas

### `POST /v1/sale-returns/`
Crear una devolución de venta. Se generan movimientos de inventario (IN) para devolver stock.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `sale_id` | integer (FK) | ✅ | ID de la venta original (no puede estar cancelada) |
| `reason` | string | ❌ | Motivo de la devolución |
| `details` | array | ✅ | Lista de productos a devolver (mínimo 1) |

**Estructura de cada objeto en `details`:**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `product_id` | integer (FK) | ✅ | ID del producto |
| `quantity` | integer | ✅ | Cantidad a devolver (min 1, no puede exceder lo vendido menos lo ya devuelto) |
| `unit_price` | decimal | ✅ | Precio unitario del reembolso (min 0.01) |

---

## Devoluciones de Compras

### `POST /v1/purchase-returns/`
Crear una devolución de compra. Se generan movimientos de inventario (OUT) para reducir stock.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `purchase_id` | integer (FK) | ✅ | ID de la compra original (no puede estar cancelada) |
| `reason` | string | ❌ | Motivo de la devolución |
| `details` | array | ✅ | Lista de productos a devolver (mínimo 1) |

**Estructura de cada objeto en `details`:**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `product_id` | integer (FK) | ✅ | ID del producto |
| `quantity` | integer | ✅ | Cantidad a devolver (min 1, no puede exceder lo comprado menos lo ya devuelto) |
| `unit_cost` | decimal | ✅ | Costo unitario del reembolso (min 0.01) |

---

## Resumen Total

| # | Endpoint | Campos requeridos |
|---|---|---|
| 1 | `/v1/auth/token/` | `email`, `password` |
| 2 | `/v1/auth/token/refresh/` | `refresh` |
| 3 | `/v1/auth/token/verify/` | `token` |
| 4 | `/v1/password-reset/request/` | `email` |
| 5 | `/v1/password-reset/verify/` | `email`, `otp` |
| 6 | `/v1/password-reset/confirm/` | `reset_token`, `new_password` |
| 7 | `/v1/users/` | `email`, `password`, `role` |
| 8 | `/v1/roles/` | `name` |
| 9 | `/v1/companies/` | `nif`, `name` |
| 10 | `/v1/categories/` | `name` |
| 11 | `/v1/products/` | `category_id`, `name`, `sale_price`, `purchase_price` |
| 12 | `/v1/customers/` | `email` |
| 13 | `/v1/sales/` | `payment_method`, `details[]` |
| 14 | `/v1/suppliers/` | `name` |
| 15 | `/v1/purchases/` | `supplier_id`, `details[]` |
| 16 | `/v1/sale-returns/` | `sale_id`, `details[]` |
| 17 | `/v1/purchase-returns/` | `purchase_id`, `details[]` |

**Total: 17 endpoints POST**
