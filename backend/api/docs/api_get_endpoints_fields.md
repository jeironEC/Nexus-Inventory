# Nexus Inventory API - Endpoints GET (con Campos Retornados)

Listado de todos los endpoints `GET` con los campos que retorna cada uno.
Los campos marcados como **objeto** contienen a su vez los campos del serializer anidado.

---

## Sistema

### `GET /v1/health/`
Retorna estado del sistema (texto plano o JSON simple).

---

## Usuarios

### `GET /v1/users/` y `GET /v1/users/me/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID del usuario |
| `first_name` | string | Nombre |
| `last_name` | string | Apellido |
| `email` | string | Correo electrónico |
| `nif` | string | NIF/DNI |
| `avatar` | string (URL) | Foto de perfil |
| `is_active` | boolean | Estado activo |
| `role` | objeto | `{id, name, description, is_active, created_at, updated_at, deleted_at}` |
| `created_at` | datetime | Fecha de creación |
| `updated_at` | datetime | Fecha de actualización |
| `deleted_at` | datetime | Fecha de eliminación (null si activo) |
| `created_by` | objeto (User) | Usuario que creó el registro |
| `updated_by` | objeto (User) | Usuario que actualizó |
| `deleted_by` | objeto (User) | Usuario que eliminó |

---

## Roles

### `GET /v1/roles/` y `GET /v1/roles/{id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID del rol |
| `name` | string | Nombre del rol |
| `description` | string | Descripción |
| `is_active` | boolean | Estado activo |
| `created_at` | datetime | Fecha de creación |
| `updated_at` | datetime | Fecha de actualización |
| `deleted_at` | datetime | Fecha de eliminación |

---

## Empresa

### `GET /v1/companies/` y `GET /v1/companies/{id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `nif` | string | NIF |
| `name` | string | Nombre |
| `address` | string | Dirección |
| `number_phone` | string | Teléfono |
| `email` | string | Correo |
| `website` | string | Sitio web |
| `logo` | string (URL) | Logo |
| `is_active` | boolean | Activo |
| `created_at` / `updated_at` / `deleted_at` | datetime | Auditoría de fechas |
| `created_by` / `updated_by` / `deleted_by` | objeto (User) | Auditoría de usuarios |

---

## Categorías

### `GET /v1/categories/` y `GET /v1/categories/{id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `name` | string | Nombre |
| `description` | string | Descripción |
| `is_active` | boolean | Activo |
| `created_at` / `updated_at` / `deleted_at` | datetime | Auditoría de fechas |
| `created_by` / `updated_by` / `deleted_by` | objeto (User) | Auditoría de usuarios |

---

## Productos

### `GET /v1/products/` y `GET /v1/products/{id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `category` | objeto (Category) | `{id, name, description, is_active, ...}` |
| `name` | string | Nombre |
| `description` | string | Descripción |
| `unique_code` | string | Código único |
| `sale_price` | decimal | Precio de venta |
| `purchase_price` | decimal | Precio de compra |
| `discount_percentage` | decimal | Descuento |
| `is_active` | boolean | Activo |
| `created_at` / `updated_at` / `deleted_at` | datetime | Auditoría de fechas |
| `created_by` / `updated_by` / `deleted_by` | objeto (User) | Auditoría de usuarios |

---

## Inventario

### `GET /v1/inventories/`, `/product/{id}/`, `/low-stock/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `product` | objeto (Product) | Producto completo |
| `quantity` | integer | Cantidad en stock |
| `created_at` / `updated_at` / `deleted_at` | datetime | Auditoría de fechas |
| `created_by` / `updated_by` / `deleted_by` | objeto (User) | Auditoría de usuarios |

> `/low-stock/` incluye además el campo `threshold` (umbral de stock bajo) en la respuesta del reporte.

---

## Movimientos de Inventario

### `GET /v1/inventory-movements/` y `/{id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `product` | objeto (Product) | Producto |
| `user` | objeto (User) | Usuario que generó el movimiento |
| `quantity` | integer | Cantidad movida |
| `created_at` | datetime | Fecha del movimiento |

> `movement_type` (IN/OUT) — campo del modelo, puede venir implícito en la respuesta.

---

## Clientes

### `GET /v1/customers/` y `/{id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `first_name` | string | Nombre |
| `last_name` | string | Apellido |
| `email` | string | Correo |
| `nif` | string | NIF/DNI |
| `number_phone` | string | Teléfono |
| `address` | string | Dirección |
| `is_active` | boolean | Activo |
| `created_at` / `updated_at` / `deleted_at` | datetime | Auditoría de fechas |
| `created_by` / `updated_by` / `deleted_by` | objeto (User) | Auditoría de usuarios |

---

## Ventas

### `GET /v1/sales/` y `/{id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `company` | objeto (Company) | Empresa |
| `customer` | objeto (Customer) | Cliente |
| `user` | objeto (User) | Usuario que creó la venta |
| `discount_amount` | decimal | Monto de descuento |
| `subtotal` | decimal | Subtotal |
| `tax_percentage` | decimal | Porcentaje de impuesto |
| `tax_amount` | decimal | Monto de impuesto |
| `total_amount` | decimal | Total |
| `payment_method` | string | Método de pago |
| `state` | string | Estado (COMPLETED/CANCELED) |
| `created_at` / `updated_at` / `deleted_at` | datetime | Auditoría |
| `updated_by` / `deleted_by` | objeto (User) | Auditoría de usuarios |

### `GET /v1/sales/{id}/details/` y `/{detail_id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `product` | objeto (Product) | Producto |
| `inventory_movement` | objeto | Movimiento generado |
| `quantity` | integer | Cantidad |
| `unit_price` | decimal | Precio unitario (con descuento aplicado) |
| `subtotal` | decimal | Subtotal del detalle |
| `created_at` | datetime | Fecha |

---

## Facturas

### `GET /v1/invoices/` y `/{id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `company` | objeto (Company) | Empresa |
| `sale` | objeto (Sale) | Venta relacionada (null si es de compra) |
| `purchase` | objeto (Purchase) | Compra relacionada (null si es de venta) |
| `number_invoice` | string | Número de factura |
| `invoice_type` | string | SALE o PURCHASE |
| `pdf_generated` | boolean | Si se generó PDF |
| `state` | string | ISSUED o CANCELED |
| `created_at` / `updated_at` / `deleted_at` | datetime | Auditoría |

### `GET /v1/invoices/{id}/pdf/`
> Retorna el archivo PDF directamente (`Content-Type: application/pdf`).

---

## Proveedores

### `GET /v1/suppliers/` y `/{id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `name` | string | Nombre |
| `email` | string | Correo |
| `nif` | string | NIF |
| `number_phone` | string | Teléfono |
| `address` | string | Dirección |
| `is_active` | boolean | Activo |
| `created_at` / `updated_at` / `deleted_at` | datetime | Auditoría de fechas |
| `created_by` / `updated_by` / `deleted_by` | objeto (User) | Auditoría de usuarios |

---

## Compras

### `GET /v1/purchases/` y `/{id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `company` | objeto (Company) | Empresa |
| `supplier` | objeto (Supplier) | Proveedor |
| `user` | objeto (User) | Usuario que creó la compra |
| `total_amount` | decimal | Total |
| `state` | string | Estado (COMPLETED/CANCELED) |
| `created_at` / `updated_at` / `deleted_at` | datetime | Auditoría |
| `updated_by` / `deleted_by` | objeto (User) | Auditoría de usuarios |

### `GET /v1/purchases/{id}/details/` y `/{detail_id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `product` | objeto (Product) | Producto |
| `inventory_movement` | objeto | Movimiento generado |
| `quantity` | integer | Cantidad |
| `unit_cost` | decimal | Costo unitario |
| `subtotal` | decimal | Subtotal |
| `created_at` | datetime | Fecha |

---

## Devoluciones de Ventas

### `GET /v1/sale-returns/` y `/{id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `sale` | objeto (Sale) | Venta original |
| `user` | objeto (User) | Usuario que creó la devolución |
| `reason` | string | Motivo |
| `total_amount` | decimal | Total devuelto |
| `state` | string | Estado |
| `created_at` / `updated_at` / `deleted_at` | datetime | Auditoría |
| `updated_by` / `deleted_by` | objeto (User) | Auditoría |

### `GET /v1/sale-returns/{id}/details/` y `/{detail_id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `product` | objeto (Product) | Producto |
| `inventory_movement` | objeto | Movimiento generado |
| `quantity` | integer | Cantidad devuelta |
| `unit_price` | decimal | Precio unitario |
| `subtotal` | decimal | Subtotal |
| `created_at` | datetime | Fecha |

---

## Devoluciones de Compras

### `GET /v1/purchase-returns/` y `/{id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `purchase` | objeto (Purchase) | Compra original |
| `user` | objeto (User) | Usuario |
| `reason` | string | Motivo |
| `total_amount` | decimal | Total devuelto |
| `state` | string | Estado |
| `created_at` / `updated_at` / `deleted_at` | datetime | Auditoría |
| `updated_by` / `deleted_by` | objeto (User) | Auditoría |

### `GET /v1/purchase-returns/{id}/details/` y `/{detail_id}/`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID |
| `product` | objeto (Product) | Producto |
| `inventory_movement` | objeto | Movimiento generado |
| `quantity` | integer | Cantidad devuelta |
| `unit_cost` | decimal | Costo unitario |
| `subtotal` | decimal | Subtotal |
| `created_at` | datetime | Fecha |

---

## Reportes

Los reportes retornan siempre `{ "summary": {...}, "data": [...] }`.

### `GET /v1/reports/sales/`
**summary:** `total_sales`, `total_revenue`, `total_tax`, `average_ticket`, `canceled_sales`
**data (sin group_by):** igual al summary
**data (group_by=customer):** `customer_id`, `customer_name`, `total_sales`, `total_revenue`
**data (group_by=payment_method):** `payment_method`, `payment_method_display`, `total_sales`, `total_revenue`
**data (group_by=period):** `period`, `total_sales`, `total_revenue`

### `GET /v1/reports/purchases/`
**summary:** `total_purchases`, `total_spent`, `total_tax`, `canceled_purchases`
**data (group_by=supplier):** `supplier_id`, `supplier_name`, `total_purchases`, `total_spent`
**data (group_by=period):** `period`, `total_purchases`, `total_spent`

### `GET /v1/reports/inventory/`
**data:** `product_id`, `product_name`, `category`, `quantity`, `sale_price`, `stock_value`
**low-stock añade:** `threshold`

### `GET /v1/reports/inventory/movements/`
**data:** `product_id`, `product_name`, `movement_type`, `quantity`, `user`, `created_at`

### `GET /v1/reports/products/`
**data (group_by=category):** `category_id`, `category_name`, `total_products`, `total_quantity_sold`, `total_revenue`
**data (performance):** `product_id`, `product_name`, `category`, `total_quantity_sold`, `total_revenue`, `total_quantity_purchased`, `total_spent`

### `GET /v1/reports/customers/`
**summary:** `total_customers`, `total_purchases`, `total_spent`
**data:** `customer_id`, `customer_name`, `total_purchases`, `total_spent`

### `GET /v1/reports/invoices/`
**summary:** `total_invoices`, `issued_invoices`, `canceled_invoices`, `pdf_generated`

### `GET /v1/reports/returns/`
**summary:** `total_returns`, `completed_returns`, `canceled_returns`, `total_refund_amount`
**data:** `id`, `created_at`, `customer_name` o `supplier_name`, `reason`, `total_amount`, `state`

> Los endpoints `/pdf/` retornan `Content-Type: application/pdf` directamente.
