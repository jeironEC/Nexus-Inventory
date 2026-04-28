# Nexus Inventory API - Endpoints PATCH

Listado de todos los endpoints que aceptan el método `PATCH` en la API (`/v1/`).

---

## Usuarios

| Endpoint | Descripción |
|---|---|
| `PATCH /v1/users/me/` | Actualizar perfil del usuario autenticado |
| `PATCH /v1/users/{id}/activate/` | Activar un usuario (StateMixin) |
| `PATCH /v1/users/{id}/deactivate/` | Desactivar un usuario (StateMixin) |

---

## Roles

| Endpoint | Descripción |
|---|---|
| `PATCH /v1/roles/{id}/` | Actualizar un rol (partial_update) |
| `PATCH /v1/roles/{id}/activate/` | Activar un rol |
| `PATCH /v1/roles/{id}/deactivate/` | Desactivar un rol |

---

## Empresa

| Endpoint | Descripción |
|---|---|
| `PATCH /v1/companies/{id}/` | Actualizar una empresa (partial_update) |
| `PATCH /v1/companies/{id}/activate/` | Activar una empresa |
| `PATCH /v1/companies/{id}/deactivate/` | Desactivar una empresa |

---

## Categorías

| Endpoint | Descripción |
|---|---|
| `PATCH /v1/categories/{id}/` | Actualizar una categoría (partial_update) |
| `PATCH /v1/categories/{id}/activate/` | Activar una categoría |
| `PATCH /v1/categories/{id}/deactivate/` | Desactivar una categoría |

---

## Productos

| Endpoint | Descripción |
|---|---|
| `PATCH /v1/products/{id}/` | Actualizar un producto (partial_update) |
| `PATCH /v1/products/{id}/activate/` | Activar un producto |
| `PATCH /v1/products/{id}/deactivate/` | Desactivar un producto |

---

## Clientes

| Endpoint | Descripción |
|---|---|
| `PATCH /v1/customers/{id}/` | Actualizar un cliente (partial_update) |
| `PATCH /v1/customers/{id}/activate/` | Activar un cliente |
| `PATCH /v1/customers/{id}/deactivate/` | Desactivar un cliente |

---

## Ventas

| Endpoint | Descripción |
|---|---|
| `PATCH /v1/sales/{id}/` | Actualizar una venta (partial_update) |
| `PATCH /v1/sales/{id}/cancel/` | Cancelar una venta |

---

## Facturas

| Endpoint | Descripción |
|---|---|
| `PATCH /v1/invoices/{id}/cancel/` | Cancelar una factura |

---

## Proveedores

| Endpoint | Descripción |
|---|---|
| `PATCH /v1/suppliers/{id}/` | Actualizar un proveedor (partial_update) |
| `PATCH /v1/suppliers/{id}/activate/` | Activar un proveedor |
| `PATCH /v1/suppliers/{id}/deactivate/` | Desactivar un proveedor |

---

## Compras

| Endpoint | Descripción |
|---|---|
| `PATCH /v1/purchases/{id}/` | Actualizar una compra (partial_update) |
| `PATCH /v1/purchases/{id}/cancel/` | Cancelar una compra |

---

## Devoluciones de Ventas

| Endpoint | Descripción |
|---|---|
| `PATCH /v1/sale-returns/{id}/` | Actualizar una devolución de venta (partial_update) |
| `PATCH /v1/sale-returns/{id}/cancel/` | Cancelar una devolución de venta |

---

## Devoluciones de Compras

| Endpoint | Descripción |
|---|---|
| `PATCH /v1/purchase-returns/{id}/` | Actualizar una devolución de compra (partial_update) |
| `PATCH /v1/purchase-returns/{id}/cancel/` | Cancelar una devolución de compra |

---

## Resumen Total

| # | Endpoint | Tipo |
|---|---|---|
| 1 | `/v1/users/me/` | partial_update |
| 2 | `/v1/users/{id}/activate/` | action |
| 3 | `/v1/users/{id}/deactivate/` | action |
| 4 | `/v1/roles/{id}/` | partial_update |
| 5 | `/v1/roles/{id}/activate/` | action |
| 6 | `/v1/roles/{id}/deactivate/` | action |
| 7 | `/v1/companies/{id}/` | partial_update |
| 8 | `/v1/companies/{id}/activate/` | action |
| 9 | `/v1/companies/{id}/deactivate/` | action |
| 10 | `/v1/categories/{id}/` | partial_update |
| 11 | `/v1/categories/{id}/activate/` | action |
| 12 | `/v1/categories/{id}/deactivate/` | action |
| 13 | `/v1/products/{id}/` | partial_update |
| 14 | `/v1/products/{id}/activate/` | action |
| 15 | `/v1/products/{id}/deactivate/` | action |
| 16 | `/v1/customers/{id}/` | partial_update |
| 17 | `/v1/customers/{id}/activate/` | action |
| 18 | `/v1/customers/{id}/deactivate/` | action |
| 19 | `/v1/sales/{id}/` | partial_update |
| 20 | `/v1/sales/{id}/cancel/` | action |
| 21 | `/v1/invoices/{id}/cancel/` | action |
| 22 | `/v1/suppliers/{id}/` | partial_update |
| 23 | `/v1/suppliers/{id}/activate/` | action |
| 24 | `/v1/suppliers/{id}/deactivate/` | action |
| 25 | `/v1/purchases/{id}/` | partial_update |
| 26 | `/v1/purchases/{id}/cancel/` | action |
| 27 | `/v1/sale-returns/{id}/` | partial_update |
| 28 | `/v1/sale-returns/{id}/cancel/` | action |
| 29 | `/v1/purchase-returns/{id}/` | partial_update |
| 30 | `/v1/purchase-returns/{id}/cancel/` | action |

**Total: 30 endpoints PATCH**
