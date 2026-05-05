# Nexus Inventory API - Endpoints GET

Listado de todos los endpoints `GET` en la API (`/v1/`).

---

## Sistema
| Endpoint | Descripción |
|---|---|
| `GET /v1/health/` | Estado del sistema |

## Usuarios
| Endpoint | Descripción |
|---|---|
| `GET /v1/users/` | Listar usuarios |
| `GET /v1/users/me/` | Perfil del usuario autenticado |

## Roles
| Endpoint | Descripción |
|---|---|
| `GET /v1/roles/` | Listar roles |
| `GET /v1/roles/{id}/` | Obtener rol por ID |

## Empresa
| Endpoint | Descripción |
|---|---|
| `GET /v1/companies/` | Listar empresas |
| `GET /v1/companies/{id}/` | Obtener empresa por ID |

## Categorías
| Endpoint | Descripción |
|---|---|
| `GET /v1/categories/` | Listar categorías |
| `GET /v1/categories/{id}/` | Obtener categoría por ID |

## Productos
| Endpoint | Descripción |
|---|---|
| `GET /v1/products/` | Listar productos |
| `GET /v1/products/{id}/` | Obtener producto por ID |
| `GET /v1/products/by-supplier/{supplier_id}/` | Listar productos de un proveedor |

## Inventario
| Endpoint | Descripción |
|---|---|
| `GET /v1/inventories/` | Listar inventario |
| `GET /v1/inventories/product/{product_id}/` | Inventario de un producto |
| `GET /v1/inventories/low-stock/` | Productos con stock bajo |

## Movimientos de Inventario
| Endpoint | Descripción |
|---|---|
| `GET /v1/inventory-movements/` | Listar movimientos |
| `GET /v1/inventory-movements/{id}/` | Obtener movimiento por ID |

## Clientes
| Endpoint | Descripción |
|---|---|
| `GET /v1/customers/` | Listar clientes |
| `GET /v1/customers/{id}/` | Obtener cliente por ID |

## Ventas
| Endpoint | Descripción |
|---|---|
| `GET /v1/sales/` | Listar ventas |
| `GET /v1/sales/{id}/` | Obtener venta por ID |
| `GET /v1/sales/{id}/details/` | Detalles de una venta |
| `GET /v1/sales/{id}/details/{detail_id}/` | Detalle de venta por ID |

## Facturas
| Endpoint | Descripción |
|---|---|
| `GET /v1/invoices/` | Listar facturas |
| `GET /v1/invoices/{id}/` | Obtener factura por ID |
| `GET /v1/invoices/{id}/pdf/` | Descargar factura en PDF |

## Proveedores
| Endpoint | Descripción |
|---|---|
| `GET /v1/suppliers/` | Listar proveedores |
| `GET /v1/suppliers/{id}/` | Obtener proveedor por ID |

## Compras
| Endpoint | Descripción |
|---|---|
| `GET /v1/purchases/` | Listar compras |
| `GET /v1/purchases/{id}/` | Obtener compra por ID |
| `GET /v1/purchases/{id}/details/` | Detalles de una compra |
| `GET /v1/purchases/{id}/details/{detail_id}/` | Detalle de compra por ID |

## Devoluciones de Ventas
| Endpoint | Descripción |
|---|---|
| `GET /v1/sale-returns/` | Listar devoluciones de ventas |
| `GET /v1/sale-returns/{id}/` | Obtener devolución por ID |
| `GET /v1/sale-returns/{id}/details/` | Detalles de una devolución |
| `GET /v1/sale-returns/{id}/details/{detail_id}/` | Detalle por ID |

## Devoluciones de Compras
| Endpoint | Descripción |
|---|---|
| `GET /v1/purchase-returns/` | Listar devoluciones de compras |
| `GET /v1/purchase-returns/{id}/` | Obtener devolución por ID |
| `GET /v1/purchase-returns/{id}/details/` | Detalles de una devolución |
| `GET /v1/purchase-returns/{id}/details/{detail_id}/` | Detalle por ID |

## Reportes de Ventas
| Endpoint | Query Params | Descripción |
|---|---|---|
| `GET /v1/reports/sales/` | `group_by` (customer/payment_method/period), `period` (day/week/month/year) | Resumen y agrupación de ventas |
| `GET /v1/reports/sales/pdf/` | `group_by`, `period` | PDF del reporte de ventas |

## Reportes de Compras
| Endpoint | Query Params | Descripción |
|---|---|---|
| `GET /v1/reports/purchases/` | `group_by` (supplier/period), `period` (day/week/month/year) | Resumen y agrupación de compras |
| `GET /v1/reports/purchases/pdf/` | `group_by`, `period` | PDF del reporte de compras |

## Reportes de Inventario
| Endpoint | Descripción |
|---|---|
| `GET /v1/reports/inventory/` | Estado del inventario |
| `GET /v1/reports/inventory/pdf/` | PDF del reporte de inventario |

## Reportes de Productos
| Endpoint | Query Params | Descripción |
|---|---|---|
| `GET /v1/reports/products/` | `group_by` (category/performance) | Rendimiento de productos |
| `GET /v1/reports/products/pdf/` | `group_by` | PDF del reporte de productos |

## Reportes de Clientes
| Endpoint | Query Params | Descripción |
|---|---|---|
| `GET /v1/reports/customers/` | `view` (top), `limit` | Ranking y resumen de clientes |
| `GET /v1/reports/customers/pdf/` | `view`, `limit` | PDF del reporte de clientes |

## Reportes de Facturas
| Endpoint | Query Params | Descripción |
|---|---|---|
| `GET /v1/reports/invoices/` | `invoice_type` (SALE/PURCHASE) | Resumen de facturas |
| `GET /v1/reports/invoices/pdf/` | filtros | PDF del reporte de facturas |

## Reportes de Devoluciones
| Endpoint | Query Params | Descripción |
|---|---|---|
| `GET /v1/reports/returns/` | `return_type` (sale/purchase) | Resumen de devoluciones |
| `GET /v1/reports/returns/pdf/` | filtros | PDF del reporte de devoluciones |

---

## Resumen Total

| Categoría | Cantidad |
|---|---|
| Sistema | 1 |
| Usuarios | 2 |
| Roles | 2 |
| Empresa | 2 |
| Categorías | 2 |
| Productos | 2 |
| Inventario | 3 |
| Movimientos | 2 |
| Clientes | 2 |
| Ventas + Detalles | 4 |
| Facturas | 3 |
| Proveedores | 2 |
| Compras + Detalles | 4 |
| Dev. Ventas + Detalles | 4 |
| Dev. Compras + Detalles | 4 |
| Reportes (7 × 2) | 14 |
| **Total** | **~57** |
