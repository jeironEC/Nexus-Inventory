# API Endpoints - Nexus Inventory

> Base URL: `URL/v1`

---

## Auth

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| POST | `/auth/token/` | Login (obtener access + refresh token) |
| POST | `/auth/token/refresh/` | Refrescar token de acceso |
| POST | `/auth/token/verify/` | Verificar token válido |
| **Total:** | | **3 Endpoints** |

---

## Categories

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/categories/` | Listar todas las categorías |
| POST | `/categories/` | Crear categoría |
| GET | `/categories/{id}/` | Obtener categoría por ID |
| PATCH | `/categories/{id}/` | Actualizar categoría |
| DELETE | `/categories/{id}/` | Eliminar categoría |
| PATCH | `/categories/{id}/activate/` | Activar categoría |
| PATCH | `/categories/{id}/deactivate/` | Desactivar categoría |
| GET | `/categories/active/` | Listar categorías activas |
| GET | `/categories/inactive/` | Listar categorías inactivas |
| **Total:** | | **9 Endpoints** |

---

## Companies

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/companies/` | Listar todas las compañias |
| POST | `/companies/` | Crear compañia |
| GET | `/companies/{id}/` | Obtener compañia por ID |
| PATCH | `/companies/{id}/` | Actualizar compañia |
| DELETE | `/companies/{id}/` | Eliminar compañia |
| PATCH | `/companies/{id}/activate/` | Activar compañia |
| PATCH | `/companies/{id}/deactivate/` | Desactivar compañia |
| GET | `/companies/active/` | Listar compañias activas |
| GET | `/companies/inactive/` | Listar compañias inactivas |
| **Total:** | | **9 Endpoints** |

---

## Customer Promotions

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/customer-promotions/` | Listar todas las promociones de clientes |
| POST | `/customer-promotions/` | Asignar promoción a cliente |
| GET | `/customer-promotions/{id}/` | Obtener promoción de cliente por ID |
| PATCH | `/customer-promotions/{id}/` | Actualizar promoción de cliente |
| DELETE | `/customer-promotions/{id}/` | Eliminar promoción de cliente |
| PATCH | `/customer-promotions/{id}/apply/` | Aplicar promoción a cliente |
| **Total:** | | **6 Endpoints** |

---

## Customers

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/customers/` | Listar todos los clientes |
| POST | `/customers/` | Crear cliente |
| GET | `/customers/{id}/` | Obtener cliente por ID |
| PATCH | `/customers/{id}/` | Actualizar cliente |
| DELETE | `/customers/{id}/` | Eliminar cliente |
| PATCH | `/customers/{id}/activate/` | Activar cliente |
| PATCH | `/customers/{id}/deactivate/` | Desactivar cliente |
| GET | `/customers/{id}/list-promotions/` | Listar promociones del cliente |
| GET | `/customers/active/` | Listar clientes activos |
| GET | `/customers/inactive/` | Listar clientes inactivos |
| **Total:** | | **10 Endpoints** |

---

## Inventory

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/inventories/` | Listar todos los inventarios |
| GET | `/inventories/low-stock/` | Listar productos con bajo stock |
| GET | `/inventories/product/{product_id}/` | Obtener inventario por producto |
| **Total:** | | **3 Endpoints** |

---

## Inventory Movements

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/inventory-movements/` | Listar todos los movimientos |
| GET | `/inventory-movements/{id}/` | Obtener movimiento por ID |
| **Total:** | | **2 Endpoints** |

---

## Invoices

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/invoices/` | Listar todas las facturas |
| GET | `/invoices/{id}/` | Obtener factura por ID |
| PATCH | `/invoices/{id}/cancel/` | Cancelar factura |
| **Total:** | | **3 Endpoints** |

---

## Products

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/products/` | Listar todos los productos |
| POST | `/products/` | Crear producto |
| GET | `/products/{id}/` | Obtener producto por ID |
| PATCH | `/products/{id}/` | Actualizar producto |
| DELETE | `/products/{id}/` | Eliminar producto |
| PATCH | `/products/{id}/activate/` | Activar producto |
| PATCH | `/products/{id}/deactivate/` | Desactivar producto |
| GET | `/products/active/` | Listar productos activos |
| GET | `/products/inactive/` | Listar productos inactivos |
| **Total:** | | **9 Endpoints** |

---

## Promotions

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/promotions/` | Listar todas las promociones |
| POST | `/promotions/` | Crear promoción |
| GET | `/promotions/{id}/` | Obtener promoción por ID |
| PATCH | `/promotions/{id}/` | Actualizar promoción |
| DELETE | `/promotions/{id}/` | Eliminar promoción |
| PATCH | `/promotions/{id}/activate/` | Activar promoción |
| PATCH | `/promotions/{id}/deactivate/` | Desactivar promoción |
| GET | `/promotions/active/` | Listar promociones activas |
| GET | `/promotions/inactive/` | Listar promociones inactivas |
| **Total:** | | **9 Endpoints** |

---

## Purchase Returns

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/purchase-returns/` | Listar todas las devoluciones de compras |
| POST | `/purchase-returns/` | Crear devolución de compra |
| GET | `/purchase-returns/{id}/` | Obtener devolución por ID |
| PATCH | `/purchase-returns/{id}/` | Actualizar devolución |
| DELETE | `/purchase-returns/{id}/` | Eliminar devolución |
| PATCH | `/purchase-returns/{id}/cancel/` | Cancelar devolución |
| GET | `/purchase-returns/{purchase_returns_pk}/details/` | Listar detalles de devolución |
| GET | `/purchase-returns/{purchase_returns_pk}/details/{id}/` | Obtener detalle de devolución |
| GET | `/purchase-returns/completed/` | Listar devoluciones completadas |
| GET | `/purchase-returns/canceled/` | Listar devoluciones canceladas |
| **Total:** | | **10 Endpoints** |

---

## Purchases

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/purchases/` | Listar todas las compras |
| POST | `/purchases/` | Crear compra |
| GET | `/purchases/{id}/` | Obtener compra por ID |
| PATCH | `/purchases/{id}/` | Actualizar compra |
| DELETE | `/purchases/{id}/` | Eliminar compra |
| PATCH | `/purchases/{id}/cancel/` | Cancelar compra |
| GET | `/purchases/{purchases_pk}/details/` | Listar detalles de compra |
| GET | `/purchases/{purchases_pk}/details/{id}/` | Obtener detalle de compra |
| GET | `/purchases/completed/` | Listar compras completadas |
| GET | `/purchases/canceled/` | Listar compras canceladas |
| **Total:** | | **10 Endpoints** |

---

## Reports

### Customers
| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/reports/customers/` | Reporte de clientes |
| GET | `/reports/customers/promotions/` | Promociones por cliente |
| GET | `/reports/customers/top/` | Mejores clientes |
| **Total:** | | **3 Endpoints** |

### Inventory
| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/reports/inventory/` | Reporte de inventario |
| GET | `/reports/inventory/low-stock/` | Inventario con bajo stock |
| GET | `/reports/inventory/movements/` | Movimientos de inventario |
| **Total:** | | **3 Endpoints** |

### Invoices
| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/reports/invoices/` | Reporte de facturas |
| GET | `/reports/invoices/purchases/` | Facturas de compras |
| GET | `/reports/invoices/sales/` | Facturas de ventas |
| **Total:** | | **3 Endpoints** |

### Products
| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/reports/products/` | Reporte de productos |
| GET | `/reports/products/by-category/` | Productos por categoría |
| GET | `/reports/products/low-selling/` | Productos menos vendidos |
| GET | `/reports/products/most-purchased/` | Productos más comprados |
| GET | `/reports/products/top-selling/` | Productos más vendidos |
| **Total:** | | **5 Endpoints** |

### Purchase Returns
| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/reports/purchase-returns/` | Devoluciones de compras |
| **Total:** | | **1 Endpoints** |

### Purchases
| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/reports/purchases/` | Reporte de compras |
| GET | `/reports/purchases/by-period/` | Compras por período |
| GET | `/reports/purchases/by-supplier/` | Compras por proveedor |
| **Total:** | | **3 Endpoints** |

### Sale Returns
| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/reports/sale-returns/` | Devoluciones de ventas |
| **Total:** | | **1 Endpoints** |

### Sales
| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/reports/sales/` | Reporte de ventas |
| GET | `/reports/sales/by-customer/` | Ventas por cliente |
| GET | `/reports/sales/by-payment-method/` | Ventas por método de pago |
| GET | `/reports/sales/by-period/` | Ventas por período |
| **Total:** | | **4 Endpoints** |

---

### PDFs
| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/v1/invoices/{id}/pdf/` | PDF factura compra o venta |
| GET | `/reports/sales/pdf/` | PDF reporte de ventas |
| GET | `/reports/sales/by-customer/pdf/` | PDF ventas por cliente |
| GET | `/reports/sales/by-payment-method/pdf/` | PDF ventas por método de pago |
| GET | `/reports/sales/by-period/pdf/` | PDF ventas por período |
| GET | `/reports/purchases/pdf/` | PDF reporte de compras |
| GET | `/reports/purchases/by-supplier/pdf/` | PDF compras por proveedor |
| GET | `/reports/purchases/by-period/pdf/` | PDF compras por período |
| GET | `/reports/inventory/pdf/` | PDF reporte de inventario |
| GET | `/reports/inventory/low-stock/pdf/` | PDF inventario bajo stock |
| GET | `/reports/inventory/movements/pdf/` | PDF movimientos de inventario |
| GET | `/reports/products/pdf/` | PDF reporte de productos |
| GET | `/reports/products/top-selling/pdf/` | PDF productos más vendidos |
| GET | `/reports/products/low-selling/pdf/` | PDF productos menos vendidos |
| GET | `/reports/products/most-purchased/pdf/` | PDF productos más comprados |
| GET | `/reports/products/by-category/pdf/` | PDF productos por categoría |
| GET | `/reports/customers/pdf/` | PDF reporte de clientes |
| GET | `/reports/customers/top/pdf/` | PDF mejores clientes |
| GET | `/reports/customers/promotions/pdf/` | PDF promociones por cliente |
| GET | `/reports/invoices/pdf/` | PDF reporte de facturas |
| GET | `/reports/invoices/sales/pdf/` | PDF facturas de ventas |
| GET | `/reports/invoices/purchases/pdf/` | PDF facturas de compras |
| GET | `/reports/sale-returns/pdf/` | PDF devoluciones de ventas |
| GET | `/reports/purchase-returns/pdf/` | PDF devoluciones de compras |
| **Total:** | | **24 Endpoints** |

---

## Roles

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/roles/` | Listar todos los roles |
| POST | `/roles/` | Crear rol |
| GET | `/roles/{id}/` | Obtener rol por ID |
| PATCH | `/roles/{id}/` | Actualizar rol |
| DELETE | `/roles/{id}/` | Eliminar rol |
| PATCH | `/roles/{id}/activate/` | Activar rol |
| PATCH | `/roles/{id}/deactivate/` | Desactivar rol |
| GET | `/roles/active/` | Listar roles activos |
| GET | `/roles/inactive/` | Listar roles inactivos |
| **Total:** | | **9 Endpoints** |

---

## Sale Returns

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/sale-returns/` | Listar todas las devoluciones de ventas |
| POST | `/sale-returns/` | Crear devolución de venta |
| GET | `/sale-returns/{id}/` | Obtener devolución por ID |
| PATCH | `/sale-returns/{id}/` | Actualizar devolución |
| DELETE | `/sale-returns/{id}/` | Eliminar devolución |
| PATCH | `/sale-returns/{id}/cancel/` | Cancelar devolución |
| GET | `/sale-returns/{sale_returns_pk}/details/` | Listar detalles de devolución |
| GET | `/sale-returns/{sale_returns_pk}/details/{id}/` | Obtener detalle de devolución |
| GET | `/sale-returns/completed/` | Listar devoluciones completadas |
| GET | `/sale-returns/canceled/` | Listar devoluciones canceladas |
| **Total:** | | **10 Endpoints** |

---

## Sales

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/sales/` | Listar todas las ventas |
| POST | `/sales/` | Crear venta |
| GET | `/sales/{id}/` | Obtener venta por ID |
| PATCH | `/sales/{id}/` | Actualizar venta |
| DELETE | `/sales/{id}/` | Eliminar venta |
| PATCH | `/sales/{id}/cancel/` | Cancelar venta |
| GET | `/sales/{sales_pk}/details/` | Listar detalles de venta |
| GET | `/sales/{sales_pk}/details/{id}/` | Obtener detalle de venta |
| GET | `/sales/completed/` | Listar ventas completadas |
| GET | `/sales/canceled/` | Listar ventas canceladas |
| **Total:** | | **10 Endpoints** |

---

## Schema

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/schema/` | OpenAPI Schema |
| **Total:** | | **1 Endpoints** |

---

## Suppliers

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/suppliers/` | Listar todos los proveedores |
| POST | `/suppliers/` | Crear proveedor |
| GET | `/suppliers/{id}/` | Obtener proveedor por ID |
| PATCH | `/suppliers/{id}/` | Actualizar proveedor |
| DELETE | `/suppliers/{id}/` | Eliminar proveedor |
| PATCH | `/suppliers/{id}/activate/` | Activar proveedor |
| PATCH | `/suppliers/{id}/deactivate/` | Desactivar proveedor |
| GET | `/suppliers/active/` | Listar proveedores activos |
| GET | `/suppliers/inactive/` | Listar proveedores inactivos |
| **Total:** | | **9 Endpoints** |

---

## Users

| Método | Endpoint | Descripción |
| ------ | -------- | ----------- |
| GET | `/users/` | Listar todos los usuarios |
| POST | `/users/` | Crear usuario |
| PATCH | `/users/{id}/activate/` | Activar usuario |
| PATCH | `/users/{id}/deactivate/` | Desactivar usuario |
| GET | `/users/active/` | Listar usuarios activos |
| GET | `/users/inactive/` | Listar usuarios inactivos |
| GET | `/users/me/` | Obtener perfil del usuario actual |
| PATCH | `/users/me/` | Actualizar perfil del usuario actual |
| DELETE | `/users/me/` | Eliminar cuenta del usuario actual |
| **Total:** | | **9 Endpoints** |

---

## Total de endpoints
**177**

## Autenticación

Para endpoints protegidos, usar el header:

```
Authorization: Bearer <access_token>
```

Para operaciones POST, PUT, PATCH, DELETE, también usar:

```
X-CSRFTOKEN: <csrftoken_cookie>
```
