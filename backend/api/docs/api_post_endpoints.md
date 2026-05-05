# Nexus Inventory API - Endpoints POST

Listado de todos los endpoints que aceptan el método `POST` en la API (`/v1/`).

---

## Autenticación

| Endpoint | Descripción |
|---|---|
| `POST /v1/auth/token/` | Obtener par de tokens JWT (login con email y contraseña) |
| `POST /v1/auth/token/refresh/` | Refrescar el access token usando el refresh token |
| `POST /v1/auth/token/verify/` | Verificar si un token JWT es válido |

---

## Recuperación de Contraseña

| Endpoint | Descripción |
|---|---|
| `POST /v1/password-reset/request/` | Solicitar código OTP por correo electrónico |
| `POST /v1/password-reset/verify/` | Verificar el código OTP y obtener un reset token |
| `POST /v1/password-reset/confirm/` | Confirmar nueva contraseña usando el reset token |

---

## Usuarios

| Endpoint | Descripción |
|---|---|
| `POST /v1/users/` | Crear un nuevo usuario (`CreateModelMixin`) |

---

## Roles

| Endpoint | Descripción |
|---|---|
| `POST /v1/roles/` | Crear un nuevo rol (`ModelViewSet`) |

---

## Empresa

| Endpoint | Descripción |
|---|---|
| `POST /v1/companies/` | Crear una nueva empresa (`ModelViewSet`) |

---

## Categorías

| Endpoint | Descripción |
|---|---|
| `POST /v1/categories/` | Crear una nueva categoría (`ModelViewSet`) |

---

## Productos

| Endpoint | Descripción |
|---|---|
| `POST /v1/products/` | Crear un nuevo producto (`ModelViewSet`) |

---

## Clientes

| Endpoint | Descripción |
|---|---|
| `POST /v1/customers/` | Crear un nuevo cliente (`ModelViewSet`) |

---

## Ventas

| Endpoint | Descripción |
|---|---|
| `POST /v1/sales/` | Crear una nueva venta con sus detalles (`ModelViewSet`) |

---

## Proveedores

| Endpoint | Descripción |
|---|---|
| `POST /v1/suppliers/` | Crear un nuevo proveedor (`ModelViewSet`) |

---

## Compras

| Endpoint | Descripción |
|---|---|
| `POST /v1/purchases/` | Crear una nueva compra con sus detalles (`ModelViewSet`) |

---

## Devoluciones de Ventas

| Endpoint | Descripción |
|---|---|
| `POST /v1/sale-returns/` | Crear una devolución de venta (`ModelViewSet`) |

> **Nota:** `SaleReturnDetailViewSet` tiene `http_method_names = ["get"]`, los detalles se crean dentro del serializador.

---

## Devoluciones de Compras

| Endpoint | Descripción |
|---|---|
| `POST /v1/purchase-returns/` | Crear una devolución de compra (`ModelViewSet`) |

---

## Resumen Total

| # | Endpoint | Método |
|---|---|---|
| 1 | `/v1/auth/token/` | POST |
| 2 | `/v1/auth/token/refresh/` | POST |
| 3 | `/v1/auth/token/verify/` | POST |
| 4 | `/v1/password-reset/request/` | POST |
| 5 | `/v1/password-reset/verify/` | POST |
| 6 | `/v1/password-reset/confirm/` | POST |
| 7 | `/v1/users/` | POST |
| 8 | `/v1/roles/` | POST |
| 9 | `/v1/companies/` | POST |
| 10 | `/v1/categories/` | POST |
| 11 | `/v1/products/` | POST |
| 12 | `/v1/customers/` | POST |
| 13 | `/v1/sales/` | POST |
| 14 | `/v1/suppliers/` | POST |
| 15 | `/v1/purchases/` | POST |
| 16 | `/v1/sale-returns/` | POST |
| 17 | `/v1/purchase-returns/` | POST |

**Total: 17 endpoints POST**
