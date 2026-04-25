# Filtros por Entidad - Backend API

Este documento define los filtros disponibles para cada entidad en el sistema.
Los filtros se implementan en dos niveles:
- **Filter**: Disponible para todos los usuarios (incluye roles estándar)
- **AdminFilter**: Disponible solo para administradores (hereda de Filter + AuditFilter)

---

## Usuarios
**Filtro Estándar**: `UserFilter`

**Campos filtrables:**
- `role_id` - ID del rol (NumberFilter)
- `is_active` - Estado del usuario (Valor booleano)
- `full_name` - Nombre completo (CharFilter con búsqueda icontains)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `UserAdminFilter` (requiere permisos de admin)

---

## Roles
**Filtro Estándar**: `RoleFilter`

**Campos filtrables:**
- `is_active` - Estado del rol (Valor booleano)
- `name` - Nombre del rol (CharFilter con búsqueda icontains)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `RoleAdminFilter` (requiere permisos de admin)

---

## Category (Categorías)
**Filtro Estándar**: `CategoryFilter`

**Campos filtrables:**
- `is_active` - Estado de la categoría (Valor booleano)
- `name` - Nombre de la categoría (CharFilter con búsqueda icontains)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `CategoryAdminFilter` (requiere permisos de admin)

---

## Company (Empresas)
**Filtro Estándar**: `CompanyFilter`

**Campos filtrables:**
- `is_active` - Estado de la empresa (Valor booleano)
- `name` - Nombre de la empresa (CharFilter con búsqueda icontains)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `CompanyAdminFilter` (requiere permisos de admin)

---

## Customer (Clientes)
**Filtro Estándar**: `CustomerFilter`

**Campos filtrables:**
- `is_active` - Estado del usuario (Valor booleano)
- `full_name` - Nombre completo (CharFilter con búsqueda icontains)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `CustomerAdminFilter` (requiere permisos de admin)

---

## Supplier (Proveedores)
**Filtro Estándar**: `SupplierFilter`

**Campos filtrables:**
- `is_active` - Estado del proveedor (Valor booleano)
- `name` - Nombre del proveedor (CharFilter con búsqueda icontains)
- `email` - Email del proveedor (CharFilter con búsqueda icontains)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `SupplierAdminFilter` (requiere permisos de admin)

---

## Product (Productos)
**Filtro Estándar**: `ProductFilter`

**Campos filtrables:**
- `category_id` - ID de categoría (NumberFilter)
- `is_active` - Estado del producto (Valor booleano)
- `name` - Nombre del producto (CharFilter con búsqueda icontains)
- `unique_code` - Código único (CharFilter con búsqueda icontains)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)
- `sale_price_min` - Precio de venta mínimo (NumberFilter)
- `sale_price_max` - Precio de venta máximo (NumberFilter)

**Filtro Administrador**: `ProductAdminFilter` (requiere permisos de admin)

---

## Inventory (Existencias)
**Filtro Estándar**: `InventoryFilter`

**Campos filtrables:**
- `product_id` - ID del producto (NumberFilter)
- `product_name` - Nombre del producto (CharFilter con búsqueda icontains)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)
- `quantity_min` - Cantidad mínima (NumberFilter)
- `quantity_max` - Cantidad máxima (NumberFilter)

**Filtro Administrador**: `InventoryAdminFilter` (requiere permisos de admin)

---

## InventoryMovement (Movimientos de Inventario)
**Filtro Estándar**: `InventoryMovementFilter`

**Campos filtrables:**
- `product_id` - ID del producto (NumberFilter)
- `user_id` - ID del usuario (NumberFilter)
- `movement_type` - Tipo de movimiento (ChoiceFilter - MovementType choices)
- `product_name` - Nombre del producto (CharFilter con búsqueda icontains)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)
- `quantity_min` - Cantidad mínima (NumberFilter)
- `quantity_max` - Cantidad máxima (NumberFilter)

**Filtro Administrador**: `InventoryMovementAdminFilter` (requiere permisos de admin)

---

## Sale (Ventas)
**Filtro Estándar**: `SaleFilter`

**Campos filtrables:**
- `state` - Estado de la venta (ChoiceFilter - OperationState choices)
- `payment_method` - Método de pago (ChoiceFilter - PaymentMethod choices)
- `customer_id` - ID del cliente (NumberFilter)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `SaleAdminFilter` (requiere permisos de admin)

---

## SaleDetail (Detalles de Venta)
**Filtro Estándar**: `SaleDetailFilter`

**Campos filtrables:**
- `product_id` - ID del producto (NumberFilter)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `SaleDetailAdminFilter` (requiere permisos de admin)

---

## SaleReturn (Devoluciones de Venta)
**Filtro Estándar**: `SaleReturnFilter`

**Campos filtrables:**
- `state` - Estado de la devolución (ChoiceFilter - OperationState choices)
- `sale_id` - ID de la venta (NumberFilter)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `SaleReturnAdminFilter` (requiere permisos de admin)

---

## SaleReturnDetail (Detalles de Devolución)
**Filtro Estándar**: `SaleReturnDetailFilter`

**Campos filtrables:**
- `product_id` - ID del producto (NumberFilter)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `SaleReturnDetailAdminFilter` (requiere permisos de admin)

---

## Purchase (Compras)
**Filtro Estándar**: `PurchaseFilter`

**Campos filtrables:**
- `state` - Estado de la compra (ChoiceFilter - OperationState choices)
- `supplier_id` - ID del proveedor (NumberFilter)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `PurchaseAdminFilter` (requiere permisos de admin)

---

## PurchaseDetail (Detalles de Compra)
**Filtro Estándar**: `PurchaseDetailFilter`

**Campos filtrables:**
- `product_id` - ID del producto (NumberFilter)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `PurchaseDetailAdminFilter` (requiere permisos de admin)

---

## PurchaseReturn (Devoluciones de Compra)
**Filtro Estándar**: `PurchaseReturnFilter`

**Campos filtrables:**
- `state` - Estado de la devolución (ChoiceFilter - OperationState choices)
- `purchase_id` - ID de la compra (NumberFilter)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `PurchaseReturnAdminFilter` (requiere permisos de admin)

---

## PurchaseReturnDetail (Detalles de Devolución)
**Filtro Estándar**: `PurchaseReturnDetailFilter`

**Campos filtrables:**
- `product_id` - ID del producto (NumberFilter)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `PurchaseReturnDetailAdminFilter` (requiere permisos de admin)

---

## Invoice (Facturas)
**Filtro Estándar**: `InvoiceFilter`

**Campos filtrables:**
- `state` - Estado de la factura (ChoiceFilter - InvoiceState choices)
- `invoice_type` - Tipo de factura (ChoiceFilter - InvoiceType choices)
- `pdf_generated` - PDF generado (BooleanFilter)
- `sale_id` - ID de la venta (NumberFilter)
- `purchase_id` - ID de la compra (NumberFilter)
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Administrador**: `InvoiceAdminFilter` (requiere permisos de admin)

---

## Report (Reportes Generales)
**Filtro Estándar**: `SaleReportFilter`

**Campos filtrables:**
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)
- `payment_method` - Método de pago (CharFilter con búsqueda iexact)
- `customer_id` - ID del cliente (NumberFilter)
- `period` - Período (ChoiceFilter: day, week, month)

**Filtro Estándar**: `PurchaseReportFilter`

**Campos filtrables:**
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)
- `supplier_id` - ID del proveedor (NumberFilter)
- `period` - Período (ChoiceFilter: day, week, month)

**Filtro Estándar**: `InventoryReportFilter`

**Campos filtrables:**
- `category_id` - ID de categoría (NumberFilter)

**Filtro Estándar**: `ProductReportFilter`

**Campos filtrables:**
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)
- `category_id` - ID de categoría (NumberFilter)

**Filtro Estándar**: `CustomerReportFilter`

**Campos filtrables:**
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)

**Filtro Estándar**: `InvoiceReportFilter`

**Campos filtrables:**
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)
- `state` - Estado de la factura (CharFilter con búsqueda iexact)
- `invoice_type` - Tipo de factura (CharFilter con búsqueda iexact)
- `sale_id` - ID de la venta (NumberFilter)
- `purchase_id` - ID de la compra (NumberFilter)

**Filtro Estándar**: `SaleReturnReportFilter`

**Campos filtrables:**
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)
- `state` - Estado de la devolución (CharFilter con búsqueda iexact)

**Filtro Estándar**: `PurchaseReturnReportFilter`

**Campos filtrables:**
- `date_from` - Fecha desde (DateFilter)
- `date_to` - Fecha hasta (DateFilter)
- `state` - Estado de la devolución (CharFilter con búsqueda iexact)
