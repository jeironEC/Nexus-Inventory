# Esquema base de datos (Nexus Inventory)
Este esquema está diseñado utilizando nombres para tablas y campos en inglés para garantizar una mayor compatibilidad y escalabilidad.

---

## Campos de auditoría

La mayoría de tablas del sistema incluyen los siguientes campos de auditoría para mantener trazabilidad completa de los registros:

| Campo | Tipo | Descripción |
|---|---|---|
| `created_at` | `TIMESTAMP` | Fecha y hora de creación del registro |
| `updated_at` | `TIMESTAMP NULL` | Fecha y hora de la última modificación |
| `created_by` | `BIGINT NULL FK → user(id)` | Usuario que creó el registro |
| `updated_by` | `BIGINT NULL FK → user(id)` | Usuario que realizó la última modificación |

> **Nota:** El valor `NULL` en `created_by` indica que el registro fue creado por el sistema (seed inicial), no por un usuario humano.

---

## Proposito de cada tabla

### Tabla Role
La tabla **Role** almacena los distintos roles de usuario del sistema, permitiendo clasificar a los usuarios según su nivel de acceso y responsabilidades dentro de la aplicación.

Cada registro de esta tabla representa un tipo de usuario con un conjunto específico de responsabilidades dentro del sistema.

Relaciones:
```bash
role (1) ─── (N) user
```
* Un rol puede estar asociado a muchos usuarios, pero cada usuario tiene un único rol.

Reglas de negocio:
* El nombre del rol debe ser único (`UNIQUE`).
* El estado del rol puede ser `active` o `inactive`.
* Un rol no puede existir sin nombre (`NOT NULL`).
* Un usuario debe tener siempre un rol asignado (relación obligatoria desde `user`).
* La fecha de creación del rol se registra automáticamente mediante `created_at`.
* Las FK de auditoría (`created_by`, `updated_by`) se agregan mediante `ALTER TABLE` después de crear la tabla `user`, debido a la dependencia circular entre `role` y `user`.

---

### Tabla User
La tabla **User** almacena la información de los usuarios del sistema, permitiendo identificar a las personas que interactúan con la aplicación y registrar su rol dentro del sistema.

Los usuarios pueden realizar diferentes operaciones como gestionar productos, registrar ventas, registrar compras y generar movimientos de inventario, dependiendo del rol asignado.

Relaciones:
```bash
role (1) ─── (N) user

user (1) ─── (N) sale
user (1) ─── (N) invoice
user (1) ─── (N) purchase
user (1) ─── (N) inventory_movement
```
* Un rol puede tener muchos usuarios.
* Un usuario puede procesar muchas ventas.
* Un usuario puede emitir muchas facturas.
* Un usuario puede registrar muchas compras.
* Un usuario puede generar muchos movimientos de inventario.

Reglas de negocio:
* Cada usuario debe tener un rol asignado (`role_id NOT NULL`).
* El nombre del usuario se almacena en dos campos separados: `first_name` y `last_name`, ambos obligatorios (`NOT NULL`).
* El correo electrónico debe ser único (`UNIQUE`).
* El correo y la contraseña son obligatorios para la autenticación.
* La contraseña se almacena únicamente como hash (`password_hash`).
* El estado del usuario puede ser `active` o `inactive`.
* La fecha de creación del usuario se registra automáticamente.
* El campo `updated_at` permite registrar modificaciones del usuario.
* Los campos `created_by` y `updated_by` implementan una **auto-referencia**, ya que un usuario puede crear o modificar a otro usuario. El primer usuario del sistema tendrá `NULL` en ambos campos.

---

### Tabla Category
La tabla **Category** almacena las categorías de productos dentro del sistema.

Permite organizar y clasificar los productos del inventario para facilitar su gestión, búsqueda y control dentro del sistema.

Relaciones:
```bash
category (1) ─── (N) product
```
* Una categoría puede tener muchos productos, pero cada producto pertenece a una única categoría.

Reglas de negocio:
* Una categoría debe tener un nombre obligatorio (`NOT NULL`).
* El estado de la categoría puede ser `active` o `inactive`.
* Una categoría inactiva no debería asignarse a nuevos productos (regla de negocio a nivel de aplicación).
* La fecha de creación se registra automáticamente mediante `created_at`.
* Un producto siempre debe estar asociado a una categoría existente mediante la clave foránea en `product`.

---

### Tabla Product
La tabla **Product** almacena la información de los productos gestionados en el inventario del sistema **Nexus Inventory**.

Cada registro representa un producto que puede venderse, comprarse y cuyo stock se controla dentro del inventario.

Relaciones:
```bash
category (1) ─── (N) product
product  (1) ─── (1) inventory
product  (1) ─── (N) sale_detail
product  (1) ─── (N) purchase_detail
product  (1) ─── (N) inventory_movement
```
* Cada producto pertenece a una única categoría.
* Cada producto tiene un único registro de inventario.
* Un producto puede aparecer en múltiples detalles de venta.
* Un producto puede aparecer en múltiples detalles de compra.
* Un producto puede generar múltiples movimientos de inventario.

Reglas de negocio:
* Un producto debe pertenecer obligatoriamente a una categoría (`category_id NOT NULL`).
* El código único del producto debe ser único en el sistema (`unique_code UNIQUE`).
* El precio de venta y el precio de compra son obligatorios.
* El estado del producto puede ser `active` o `inactive`.
* La fecha de creación del producto se registra automáticamente.
* El campo `updated_at` permite registrar modificaciones del producto.
* Cada producto debe tener un registro correspondiente en la tabla `inventory` para controlar su stock.

---

### Tabla Inventory
La tabla **Inventory** almacena el stock actual de cada producto dentro del sistema.

Su función es mantener el conteo actualizado de unidades disponibles de cada producto en el inventario. Este valor se modifica automáticamente cuando se registran ventas o compras, a través de los movimientos de inventario.

Relaciones:
```bash
product (1) ─── (1) inventory
```
* Cada producto tiene un único registro en inventario.
* Cada registro de inventario pertenece a un solo producto.

Reglas de negocio:
* Cada producto debe tener un único registro en inventario (`product_id UNIQUE`).
* El producto es obligatorio para crear un registro de inventario (`product_id NOT NULL`).
* La cantidad de inventario no puede ser nula (`quantity NOT NULL`).
* El stock inicial de un producto es `0` por defecto.
* El campo `updated_at` se actualiza automáticamente (`ON UPDATE CURRENT_TIMESTAMP`) cada vez que cambia el stock.
* Si un producto es eliminado, su registro de inventario se elimina automáticamente (`ON DELETE CASCADE`).

---

### Tabla Customer
La tabla **Customer** almacena la información de los clientes del sistema.

Permite registrar a las personas o empresas que realizan compras, facilitando la gestión de facturación, historial de ventas y control de clientes frecuentes.

Relaciones:
```bash
customer (1) ─── (N) sale
customer (1) ─── (N) customer_promotion
```
* Un cliente puede tener muchas ventas asociadas.
* Un cliente puede estar asociado a múltiples promociones.

Reglas de negocio:
* El nombre del cliente se almacena en dos campos separados: `first_name` y `last_name`, ambos obligatorios (`NOT NULL`).
* El correo electrónico es único (`UNIQUE`) y obligatorio.
* El número de teléfono y dirección son opcionales.
* El estado del cliente puede ser `active` o `inactive`.
* La fecha de registro del cliente se guarda automáticamente mediante `created_at`.
* Un cliente puede existir en el sistema incluso si nunca ha realizado una compra.
* Un cliente inactivo no debería poder registrarse en nuevas ventas (regla de negocio a nivel de aplicación).

---

### Tabla Promotion
La tabla **Promotion** almacena las promociones o descuentos disponibles en el sistema.

Permite definir campañas de descuento que pueden aplicarse a determinados clientes, facilitando estrategias comerciales como ofertas temporales, promociones especiales o fidelización de clientes.

Relaciones:
```bash
promotion (1) ─── (N) customer_promotion
```
* Una promoción puede asignarse a múltiples clientes.
* La relación entre clientes y promociones se gestiona mediante la tabla `customer_promotion`.

Reglas de negocio:
* El nombre de la promoción es obligatorio (`NOT NULL`).
* El porcentaje de descuento se almacena en `discount_percentage`.
* El descuento por defecto es `0` si no se especifica.
* Una promoción puede tener fechas de inicio y fin para controlar su periodo de validez.
* El estado de la promoción puede ser `active` o `inactive`.
* Solo las promociones activas y dentro del rango de fechas deberían aplicarse a ventas (regla de negocio a nivel de aplicación).

---

### Tabla Customer Promotion
La tabla **Customer Promotion** gestiona la asignación de promociones a clientes específicos dentro del sistema.

Permite controlar qué promociones están disponibles para cada cliente y si dichas promociones ya han sido utilizadas o aplicadas en una venta.

Relaciones:
```bash
customer  (1) ─── (N) customer_promotion
promotion (1) ─── (N) customer_promotion
```
* Un cliente puede tener múltiples promociones asignadas.
* Una promoción puede asignarse a múltiples clientes.
* Esta tabla funciona como una tabla intermedia (relación muchos a muchos) entre `customer` y `promotion`.

Reglas de negocio:
* Cada registro debe estar asociado a un cliente existente (`customer_id NOT NULL`).
* Cada registro debe estar asociado a una promoción existente (`promotion_id NOT NULL`).
* La combinación `(customer_id, promotion_id)` debe ser única, evitando asignar la misma promoción al mismo cliente más de una vez (`UNIQUE KEY uq_customer_promotion`).
* El campo `applied` indica si la promoción ya fue utilizada en una compra.
* La fecha de asignación se registra automáticamente mediante `assignment_date`.
* El campo `updated_at` se actualiza automáticamente cuando cambia el estado de `applied`.
* Una promoción solo debería aplicarse una vez si `applied = TRUE` (regla de negocio controlada a nivel de aplicación).

---

### Tabla Sale
La tabla **Sale** almacena las transacciones comerciales realizadas en el sistema.

Representa el registro central de cada venta, donde se captura el cliente, el usuario que procesó la operación, los montos calculados y el método de pago. Una venta puede o no generar una factura, dependiendo de si el cliente la solicita.

Relaciones:
```bash
customer (1) ─── (N) sale
user     (1) ─── (N) sale
sale     (1) ─── (1) invoice
sale     (1) ─── (N) sale_detail
```
* Un cliente puede tener múltiples ventas.
* Un usuario puede procesar múltiples ventas.
* Una venta puede generar como máximo una factura.
* Una venta contiene múltiples líneas de productos en `sale_detail`.

Reglas de negocio:
* Cada venta debe estar asociada a un usuario que realizó la operación (`user_id NOT NULL`).
* El cliente es opcional, permitiendo ventas sin cliente registrado (`customer_id NULL`).
* Los campos `subtotal`, `tax_amount` y `total_amount` son obligatorios.
* El método de pago puede ser `cash`, `card` o `transfer`.
* El estado de la venta puede ser `completed` o `canceled`.
* La fecha de la venta se registra automáticamente (`sale_date`).
* Una venta cancelada no debería generar movimientos de inventario nuevos (regla de negocio a nivel de aplicación).

---

### Tabla Invoice
La tabla **Invoice** almacena los documentos fiscales generados a partir de una venta.

Una factura es opcional y se emite únicamente cuando el cliente la solicita. Siempre está vinculada a una venta existente y no puede existir de forma independiente.

Relaciones:
```bash
sale (1) ─── (1) invoice
user (1) ─── (N) invoice
```
* Cada factura está asociada a exactamente una venta (`sale_id UNIQUE`).
* Una venta puede tener como máximo una factura.
* Un usuario puede emitir múltiples facturas.

Reglas de negocio:
* Cada factura debe estar vinculada a una venta existente (`sale_id NOT NULL UNIQUE`).
* El número de factura debe ser único en el sistema (`number_invoice UNIQUE`).
* El estado de la factura puede ser `issued` o `canceled`.
* La fecha de emisión se registra automáticamente (`issue_date`).
* El campo `pdf_generated` indica si la factura ya fue exportada en PDF.
* El campo `created_by` registra el usuario que emitió la factura.
* Si la venta asociada es eliminada, la factura se elimina automáticamente (`ON DELETE CASCADE`).

---

### Tabla Inventory Movement
La tabla **Inventory Movement** registra los movimientos de stock de los productos dentro del sistema.

Cada registro representa un cambio en la cantidad disponible de un producto, ya sea por ventas o compras, permitiendo mantener un historial completo de modificaciones del inventario.

Relaciones:
```bash
product            (1) ─── (N) inventory_movement
user               (1) ─── (N) inventory_movement
inventory_movement (1) ─── (1) sale_detail
inventory_movement (1) ─── (1) purchase_detail
```
* Un producto puede tener múltiples movimientos de inventario.
* Un usuario puede generar múltiples movimientos de inventario.
* Cada movimiento puede estar asociado a un detalle de venta (salida de stock).
* Cada movimiento puede estar asociado a un detalle de compra (entrada de stock).

Reglas de negocio:
* Cada movimiento debe estar asociado a un producto existente (`product_id NOT NULL`).
* Cada movimiento debe registrar el usuario que realizó la operación (`user_id NOT NULL`).
* El campo `movement_type` indica la dirección del movimiento:
  * `in` → entrada de stock (compra).
  * `out` → salida de stock (venta).
* El campo `quantity` representa la cantidad de unidades movidas.
* La fecha del movimiento se registra automáticamente mediante `created_at`.
* Los movimientos no se crean manualmente, sino como resultado de:
  * una venta → salida de inventario (`out`).
  * una compra → entrada de inventario (`in`).
* El historial de movimientos no debe eliminarse, ya que forma parte del registro histórico del inventario.

---

### Tabla Sale Detail
La tabla **Sale Detail** almacena las líneas o ítems individuales de cada venta dentro del sistema.

Cada registro representa un producto incluido en una venta, indicando cantidad vendida, precio unitario y subtotal, además de vincular el movimiento correspondiente en el inventario.

Relaciones:
```bash
sale               (1) ─── (N) sale_detail
product            (1) ─── (N) sale_detail
sale_detail        (1) ─── (1) inventory_movement
```
* Una venta puede contener múltiples productos.
* Un producto puede aparecer en múltiples ventas.
* Cada línea de venta genera un único movimiento de inventario.

Reglas de negocio:
* Cada detalle debe estar asociado a una venta existente (`sale_id NOT NULL`).
* Si una venta se elimina, todos sus detalles se eliminan automáticamente (`ON DELETE CASCADE`).
* Cada detalle debe referenciar un producto existente (`product_id NOT NULL`).
* Cada detalle está vinculado a un único movimiento de inventario (`inventory_movement_id UNIQUE`).
* La cantidad vendida se almacena en `quantity`.
* El precio unitario corresponde al precio del producto en el momento de la venta, no necesariamente al precio actual del producto.
* El subtotal se calcula como `quantity × unit_price`.
* Cada línea de venta debe generar un movimiento de inventario de salida (regla de negocio a nivel de aplicación).

---

### Tabla Supplier
La tabla **Supplier** almacena la información de los proveedores que suministran productos al negocio dentro del sistema.

Permite registrar los datos de contacto y estado de cada proveedor para poder gestionar compras de productos y mantener trazabilidad del origen del inventario.

Relaciones:
```bash
supplier (1) ─── (N) purchase
```
* Un proveedor puede estar asociado a múltiples compras.
* Cada compra debe estar asociada a un único proveedor.

Reglas de negocio:
* Cada proveedor debe tener un nombre (`name NOT NULL`).
* Los campos `email`, `number_phone` y `address` son opcionales.
* El campo `state` indica si el proveedor está `active` o `inactive` en el sistema.
* Solo proveedores activos deberían poder ser utilizados para registrar nuevas compras (regla de negocio a nivel de aplicación).
* La fecha `created_at` registra automáticamente cuándo se creó el proveedor.
* El historial de proveedores no debería eliminarse si existen compras asociadas, para mantener la trazabilidad del inventario.

---

### Tabla Purchase
La tabla **Purchase** almacena las compras realizadas a proveedores dentro del sistema.

Representa el documento principal de compra, donde se registra qué proveedor suministró los productos, qué usuario registró la compra y el monto total de la operación.

Las líneas de productos comprados se almacenan en la tabla **Purchase Detail**.

Relaciones:
```bash
supplier (1) ─── (N) purchase
user     (1) ─── (N) purchase
purchase (1) ─── (N) purchase_detail
```
* Un proveedor puede tener múltiples compras.
* Un usuario puede registrar múltiples compras.
* Cada compra puede tener múltiples líneas de detalle en `purchase_detail`.

Reglas de negocio:
* Cada compra debe estar asociada a un proveedor (`supplier_id NOT NULL`).
* Cada compra debe estar registrada por un usuario del sistema (`user_id NOT NULL`).
* El monto total de la compra es obligatorio (`total_amount NOT NULL`).
* La fecha de compra se registra automáticamente mediante `purchase_date`.
* El campo `state` indica si la compra fue:
  * `completed` → la compra fue válida y afecta al inventario.
  * `canceled` → la compra fue anulada.
* Una compra debe tener al menos un registro en `purchase_detail` para representar los productos comprados.
* Las compras generan movimientos de inventario positivos (`in`) a través de los registros en `inventory_movement` asociados a los detalles de compra.

---

### Tabla Purchase Detail
La tabla **Purchase Detail** almacena las líneas o ítems individuales de cada compra registrada en el sistema.

Cada registro representa un producto adquirido en una compra, indicando la cantidad, el costo unitario y el subtotal de ese ítem, además de vincular el movimiento correspondiente en el inventario.

Relaciones:
```bash
purchase        (1) ─── (N) purchase_detail
product         (1) ─── (N) purchase_detail
purchase_detail (1) ─── (1) inventory_movement
```
* Una compra puede contener múltiples productos.
* Un producto puede aparecer en múltiples compras.
* Cada línea de compra genera un único movimiento de inventario positivo.

Reglas de negocio:
* Cada detalle debe estar asociado a una compra existente (`purchase_id NOT NULL`).
* Si una compra se elimina, todos sus detalles se eliminan automáticamente (`ON DELETE CASCADE`).
* Cada detalle debe referenciar un producto existente (`product_id NOT NULL`).
* Cada detalle está vinculado a un único movimiento de inventario (`inventory_movement_id UNIQUE`).
* La cantidad comprada se almacena en `quantity`.
* El costo unitario corresponde al precio de adquisición del producto en el momento de la compra (`unit_cost`).
* El subtotal se calcula como `quantity × unit_cost`.
* Cada línea de compra debe generar un movimiento de inventario de entrada (`in`) (regla de negocio a nivel de aplicación).
* Una compra cancelada no debería generar movimientos de inventario nuevos ni afectar el stock (regla de negocio a nivel de aplicación).

## Esquema
```bash
-- ─────────────────────────────────────────
-- ROLE
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS role (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(30) UNIQUE NOT NULL,
    description TEXT,
    state       ENUM('active', 'inactive') DEFAULT 'active',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NULL,
    deleted_at  TIMESTAMP NULL,
    created_by  BIGINT NULL,
    updated_by  BIGINT NULL,
    delete_by   BIGINT NULL
);

-- ─────────────────────────────────────────
-- USER
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user (
    id            BIGINT PRIMARY KEY AUTO_INCREMENT,
    role_id       BIGINT NOT NULL,
    avatar        VARCHAR(500) NULL,
    first_name    VARCHAR(100) NOT NULL,
    last_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(120) UNIQUE NOT NULL,
    password      VARCHAR(255) NOT NULL,
    state         ENUM('active', 'inactive') DEFAULT 'active',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP NULL,
    deleted_at    TIMESTAMP NULL,
    created_by    BIGINT NULL,
    updated_by    BIGINT NULL,
    deleted_by    BIGINT NULL,

    FOREIGN KEY (role_id)    REFERENCES role(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    FOREIGN KEY (deleted_by) REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- FK ROLE
-- ─────────────────────────────────────────
ALTER TABLE role
    ADD CONSTRAINT fk_role_created_by FOREIGN KEY (created_by) REFERENCES user(id),
    ADD CONSTRAINT fk_role_updated_by FOREIGN KEY (updated_by) REFERENCES user(id),
    ADD CONSTRAINT fk_role_deleted_by FOREIGN KEY (deleted_by) REFERENCES user(id);

-- ─────────────────────────────────────────
-- CATEGORY
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS category (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    description TEXT,
    state       ENUM('active', 'inactive') DEFAULT 'active',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NULL,
    deleted_at  TIMESTAMP NULL,
    created_by  BIGINT NULL,
    updated_by  BIGINT NULL,
    deleted_by  BIGINT NULL,

    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    FOREIGN KEY (deleted_by) REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- PRODUCT
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS product (
    id             BIGINT PRIMARY KEY AUTO_INCREMENT,
    category_id    BIGINT NOT NULL,
    name           VARCHAR(150) NOT NULL,
    description    TEXT,
    unique_code    VARCHAR(50) UNIQUE NOT NULL,
    sale_price     DECIMAL(10, 2) NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    state          ENUM('active', 'inactive') DEFAULT 'active',
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP NULL,
    deleted_at     TIMESTAMP NULL,
    created_by     BIGINT NULL,
    updated_by     BIGINT NULL,
    deleted_by     BIGINT NULL,

    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (created_by)  REFERENCES user(id),
    FOREIGN KEY (updated_by)  REFERENCES user(id),
    FOREIGN KEY (deleted_by)  REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- INVENTORY
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS inventory (
    id         BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT UNIQUE NOT NULl,
    quantity   INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    deleted_at TIMESTAMP NULL,
    created_by BIGINT NULL,
    updated_by BIGINT NULL,
    deleted_by BIGINT NULL,

    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    FOREIGN KEY (deleted_by) REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- CUSTOMER
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS customer (
    id           BIGINT PRIMARY KEY AUTO_INCREMENT,
    first_name   VARCHAR(100) NOT NULL,
    last_name    VARCHAR(100) NOT NULL,
    email        VARCHAR(120) UNIQUE NOT NULL,
    number_phone VARCHAR(50),
    address      TEXT,
    state        ENUM('active', 'inactive') DEFAULT 'active',
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP NULL,
    deleted_at   TIMESTAMP NULL,
    created_by   BIGINT NULL,
    updated_by   BIGINT NULL,
    deleted_by   BIGINT NULL,

    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    FOREIGN KEY (deleted_by) REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- PROMOTION
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS promotion (
	id                  BIGINT PRIMARY KEY AUTO_INCREMENT,
	name                VARCHAR(100) NOT NULL,
	description         TEXT,
    discount_percentage DECIMAL(5, 2) DEFAULT 0,
	start_date          DATE,
	end_date            DATE,
	state               ENUM('active', 'inactive') DEFAULT 'active',
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NULL,
    deleted_at          TIMESTAMP NULL,
    created_by          BIGINT NULL,
    updated_by          BIGINT NULL,
    deleted_by          BIGINT NULL,

    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    FOREIGN KEY (deleted_by) REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- CUSTOMER_PROMOTION
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS customer_promotion(
	id              BIGINT PRIMARY KEY AUTO_INCREMENT,
	customer_id     BIGINT NOT NULL,
	promotion_id    BIGINT NOT NULL,
	applied         BOOLEAN DEFAULT FALSE,
	created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NULL,
    deleted_at      TIMESTAMP NULL,
    created_by      BIGINT NULL,
    updated_by      BIGINT NULL,
    deleted_by      BIGINT NULL,

    UNIQUE KEY uq_customer_promotion (customer_id, promotion_id),

	FOREIGN KEY (customer_id)  REFERENCES customer(id),
	FOREIGN KEY (promotion_id) REFERENCES promotion(id),
    FOREIGN KEY (created_by)   REFERENCES user(id),
    FOREIGN KEY (updated_by)   REFERENCES user(id),
    FOREIGN KEY (deleted_by)   REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- SALE
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sale (
    id             BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id    BIGINT NULL,
    user_id        BIGINT NOT NULL,
    subtotal       DECIMAL(12, 2) NOT NULL,
    tax_amount     DECIMAL(12, 2) DEFAULT 0,
    total_amount   DECIMAL(12, 2) NOT NULL,
    payment_method ENUM('cash', 'card', 'transfer') DEFAULT 'cash',
    state          ENUM('completed', 'canceled') DEFAULT 'completed',
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP NULL,
    deleted_at     TIMESTAMP NULL,
    updated_by     BIGINT NULL,
    deleted_by     BIGINT NULL,

    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (user_id)     REFERENCES user(id),
    FOREIGN KEY (updated_by)  REFERENCES user(id),
    FOREIGN KEY (deleted_by)  REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- INVOICE
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS invoice (
    id             BIGINT PRIMARY KEY AUTO_INCREMENT,
    sale_id        BIGINT UNIQUE NOT NULL,
    number_invoice VARCHAR(50) UNIQUE NOT NULL,
    state          ENUM('issued', 'canceled') DEFAULT 'issued',
    pdf_generated  BOOLEAN DEFAULT FALSE,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP NULL,
    deleted_at     TIMESTAMP NULL,
    created_by     BIGINT NULL,
    updated_by     BIGINT NULL,
    deleted_by     BIGINT NULL,

    FOREIGN KEY (sale_id)    REFERENCES sale(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    FOREIGN KEY (deleted_by) REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- INVENTORY_MOVEMENT
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS inventory_movement (
    id            BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id    BIGINT NOT NULL,
    user_id       BIGINT NOT NULL,
    movement_type ENUM('in', 'out') NOT NULL,
    quantity      INT NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (user_id)    REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- SALE_DETAIL
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sale_detail (
    id                    BIGINT PRIMARY KEY AUTO_INCREMENT,
    sale_id               BIGINT NOT NULL,
    product_id            BIGINT NOT NULL,
    inventory_movement_id BIGINT UNIQUE NOT NULL,
    quantity              INT NOT NULL,
    unit_price            DECIMAL(10, 2) NOT NULL,
    subtotal              DECIMAL(12, 2) NOT NULL,
    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (sale_id)               REFERENCES sale(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id)            REFERENCES product(id),
    FOREIGN KEY (inventory_movement_id) REFERENCES inventory_movement(id)
);

-- ─────────────────────────────────────────
-- SUPPLIER
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS supplier (
    id           BIGINT PRIMARY KEY AUTO_INCREMENT,
    name         VARCHAR(100) NOT NULL,
    email        VARCHAR(120),
    number_phone VARCHAR(50),
    address      TEXT,
    state        ENUM('active', 'inactive') DEFAULT 'active',
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP NULL,
    deleted_at   TIMESTAMP NULL,
    created_by   BIGINT NULL,
    updated_by   BIGINT NULL,
    deleted_by   BIGINT NULL,

    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    FOREIGN KEY (deleted_by) REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- PURCHASE
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS purchase (
    id            BIGINT PRIMARY KEY AUTO_INCREMENT,
    supplier_id   BIGINT NOT NULL,
    user_id       BIGINT NOT NULL,
    total_amount  DECIMAL(12, 2) NOT NULL,
    state         ENUM('completed', 'canceled') DEFAULT 'completed',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP NULL,
    deleted_at    TIMESTAMP NULL,
    updated_by    BIGINT NULL,
    deleted_by    BIGINT NULL,

    FOREIGN KEY (supplier_id) REFERENCES supplier(id),
    FOREIGN KEY (user_id)     REFERENCES user(id),
    FOREIGN KEY (updated_by)  REFERENCES user(id),
    FOREIGN KEY (deleted_by)  REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- PURCHASE_DETAIL
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS purchase_detail (
    id                    BIGINT PRIMARY KEY AUTO_INCREMENT,
    purchase_id           BIGINT NOT NULL,
    product_id            BIGINT NOT NULL,
    inventory_movement_id BIGINT UNIQUE NOT NULL,
    quantity              INT NOT NULL,
    unit_cost             DECIMAL(10, 2) NOT NULL,
    subtotal              DECIMAL(12, 2) NOT NULL,
    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (purchase_id)           REFERENCES purchase(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id)            REFERENCES product(id),
    FOREIGN KEY (inventory_movement_id) REFERENCES inventory_movement(id)
);
```
