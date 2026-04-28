# Nexus Inventory API - Endpoints DELETE

Listado de todos los endpoints que aceptan el método `DELETE` en la API (`/v1/`).

> **Importante:** Todos los `DELETE` son **soft deletes** — no eliminan el registro de la base de datos.
> En su lugar asignan `deleted_at` (timestamp) y `deleted_by` (usuario que eliminó).
> Los registros eliminados quedan ocultos en todos los listados gracias al `SoftDeleteQuerysetMixin`.

---

## Usuarios

| Endpoint | Descripción | Tipo |
|---|---|---|
| `DELETE /v1/users/me/` | Soft delete de la propia cuenta del usuario autenticado | Soft Delete |

> **Nota:** No existe `DELETE /v1/users/{id}/` — solo cada usuario puede eliminar su propia cuenta.

---

## Roles

| Endpoint | Descripción | Tipo |
|---|---|---|
| `DELETE /v1/roles/{id}/` | Soft delete de un rol | Soft Delete |

---

## Empresa

| Endpoint | Descripción | Tipo |
|---|---|---|
| `DELETE /v1/companies/{id}/` | Soft delete de una empresa | Soft Delete |

---

## Categorías

| Endpoint | Descripción | Tipo |
|---|---|---|
| `DELETE /v1/categories/{id}/` | Soft delete de una categoría | Soft Delete |

---

## Productos

| Endpoint | Descripción | Tipo |
|---|---|---|
| `DELETE /v1/products/{id}/` | Soft delete de un producto | Soft Delete |

---

## Clientes

| Endpoint | Descripción | Tipo |
|---|---|---|
| `DELETE /v1/customers/{id}/` | Soft delete de un cliente | Soft Delete |

---

## Ventas

| Endpoint | Descripción | Tipo |
|---|---|---|
| `DELETE /v1/sales/{id}/` | Soft delete de una venta | Soft Delete |

---

## Proveedores

| Endpoint | Descripción | Tipo |
|---|---|---|
| `DELETE /v1/suppliers/{id}/` | Soft delete de un proveedor | Soft Delete |

---

## Compras

| Endpoint | Descripción | Tipo |
|---|---|---|
| `DELETE /v1/purchases/{id}/` | Soft delete de una compra | Soft Delete |

---

## Devoluciones de Ventas

| Endpoint | Descripción | Tipo |
|---|---|---|
| `DELETE /v1/sale-returns/{id}/` | Soft delete de una devolución de venta | Soft Delete |

---

## Devoluciones de Compras

| Endpoint | Descripción | Tipo |
|---|---|---|
| `DELETE /v1/purchase-returns/{id}/` | Soft delete de una devolución de compra | Soft Delete |

---

## Sin DELETE (solo lectura)

Los siguientes recursos **no admiten DELETE**:

| Recurso | Razón |
|---|---|
| `Inventario` | `ListModelMixin` únicamente — solo lectura |
| `Movimientos de Inventario` | `List + Retrieve` únicamente — generados por el sistema |
| `Facturas` | `ReadOnlyModelViewSet` — generadas automáticamente |
| `Detalles de Venta` | `http_method_names = ["get"]` — creados dentro del serializador de venta |
| `Detalles de Compra` | `http_method_names = ["get"]` — creados dentro del serializador de compra |
| `Detalles de Devolución de Venta` | `http_method_names = ["get"]` |
| `Detalles de Devolución de Compra` | `http_method_names = ["get"]` |
| `Reportes` | `ViewSet` de solo lectura |

---

## Comportamiento del Soft Delete

Al ejecutar un `DELETE` en cualquier endpoint, el sistema:

1. **Asigna `deleted_at`** con el timestamp actual (`timezone.now()`).
2. **Asigna `deleted_by`** con el usuario autenticado que realizó la petición.
3. **Actualiza `updated_at`** automáticamente.
4. El registro **permanece en la base de datos** pero queda **invisible** en todos los `GET` (filtrado por `deleted_at__isnull=True`).
5. Retorna `HTTP 204 No Content`.

---

## Resumen Total

| # | Endpoint | Módulo |
|---|---|---|
| 1 | `DELETE /v1/users/me/` | Usuarios |
| 2 | `DELETE /v1/roles/{id}/` | Roles |
| 3 | `DELETE /v1/companies/{id}/` | Empresa |
| 4 | `DELETE /v1/categories/{id}/` | Categorías |
| 5 | `DELETE /v1/products/{id}/` | Productos |
| 6 | `DELETE /v1/customers/{id}/` | Clientes |
| 7 | `DELETE /v1/sales/{id}/` | Ventas |
| 8 | `DELETE /v1/suppliers/{id}/` | Proveedores |
| 9 | `DELETE /v1/purchases/{id}/` | Compras |
| 10 | `DELETE /v1/sale-returns/{id}/` | Devoluciones de Ventas |
| 11 | `DELETE /v1/purchase-returns/{id}/` | Devoluciones de Compras |

**Total: 11 endpoints DELETE (todos Soft Delete)**
