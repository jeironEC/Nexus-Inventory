# Esquema base de datos (Nexus Inventory)
Este esquema está diseñado utilizando tablas y campos en inglés para garantizar una mayor compatibilidad y escalabilidad.

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
* El nombre del rol debe ser único (UNIQUE).
* Un rol no puede existir sin nombre (NOT NULL).
* Un usuario debe tener siempre un rol asignado (relación obligatoria desde user).
* La fecha de creación del rol se registra automáticamente mediante created_at.

---

### Tabla User
La tabla **User** almacena la información de los usuarios del sistema, permitiendo identificar a las personas que interactúan con la aplicación y registrar su rol dentro del sistema.

Los usuarios pueden realizar diferentes operaciones como gestionar productos, registrar ventas, registrar compras y generar movimientos de inventario, dependiendo del rol asignado.

Relaciones:
```bash
role (1) ─── (N) user

user (1) ─── (N) invoice
user (1) ─── (N) purchase
user (1) ─── (N) inventory_movement
```
* Un rol puede tener muchos usuarios.
* Un usuario puede crear muchas facturas.
* Un usuario puede registrar muchas compras.
* Un usuario puede generar muchos movimientos de inventario.

Reglas de negocio:
* Cada usuario debe tener un rol asignado (role_id NOT NULL).
* El correo electrónico debe ser único (UNIQUE).
* El correo y la contraseña son obligatorios para la autenticación.
* La contraseña se almacena únicamente como hash (password_hash).
* El estado del usuario puede ser activo o inactivo.
* La fecha de creación del usuario se registra automáticamente.
* El campo updated_at permite registrar modificaciones del usuario.

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
* Una categoría debe tener un nombre obligatorio (NOT NULL).
* El estado de la categoría puede ser activa o inactiva
* Una categoría inactiva no debería asignarse a nuevos productos (regla de negocio a nivel de aplicación).
* La fecha de creación se registra automáticamente mediante created_at.
* Un producto siempre debe estar asociado a una categoría existente mediante la clave foránea en product.

---

### Tabla Product
La tabla **Product** almacena la información de los productos gestionados en el inventario del sistema **Nexus Inventory**.

Cada registro representa un producto que puede venderse, comprarse y cuyo stock se controla dentro del inventario.

Relaciones:
```bash
category (1) ─── (N) product
product (1) ─── (1) inventory
product (1) ─── (N) invoice_detail
product (1) ─── (N) purchase_detail
product (1) ─── (N) inventory_movement
```
* Cada producto pertenece a una única categoría.
* Cada producto tiene un único registro de inventario.
* Un producto puede aparecer en múltiples detalles de factura.
* Un producto puede aparecer en múltiples detalles de compra.
* Un producto puede generar múltiples movimientos de inventario.

Reglas de negocio:
* Un producto debe pertenecer obligatoriamente a una categoría (category_id NOT NULL).
* El código único del producto debe ser único en el sistema (unique_code UNIQUE).
* El precio de venta y el precio de compra son obligatorios.
* El estado del producto puede ser active o inactive.
* La fecha de creación del producto se registra automáticamente.
* El campo updated_at permite registrar modificaciones del producto.
* Cada producto debe tener un registro correspondiente en la tabla inventory para controlar su stock.

---

### Tabla Inventory
La tabla **Inventory** almacena el stock actual de cada producto dentro del sistema.

Su función es mantener el conteo actualizado de unidades disponibles de cada producto en el inventario. Este valor se modifica automaticamente cuando se registran ventas o compras, a través de los movimientos de inventario.

Relaciones:
```bash
product (1) ─── (1) inventory
```
* Cada producto tiene un único registro en inventario.
* Cada registro de inventario pertenece a un solo producto.

Reglas de negocio:
* Cada producto debe tener un único registro en inventario (product_id UNIQUE).
* El producto es obligatorio para crear un registro de inventario (product_id NOT NULL).
* La cantidad de inventario no puede ser nula (amount NOT NULL).
* El stock inicial de un producto es 0 por defecto.
* La fecha de última actualización se modifica automáticamente cuando cambia el stock (last_update).

---

### Tabla Customer
La tabla **Customer** almacena la información de los clientes del sistema.

Permite registrar a las personas o empresas que realizan compras, facilitando la gestión de facturación, historial de ventas y control de clientes frecuentes.

Relaciones:
```bash
customer (1) ─── (N) invoice
customer (1) ─── (N) customer_promotion
```
* Un cliente puede tener muchas facturas.
* Un cliente puede estar asociado a múltiples promociones.

Reglas de negocio:
* El nombre del cliente es obligatorio (NOT NULL).
* El correo electrónico es opcional, ya que algunos clientes pueden no proporcionarlo.
* El número de teléfono y dirección son opcionales.
* El estado del cliente puede ser active o inactive.
* La fecha de registro del cliente se guarda automáticamente mediante created_at.
* Un cliente puede existir en el sistema incluso si nunca ha realizado una compra.
* Un cliente inactivo no debería poder registrarse en nuevas facturas (regla de negocio a nivel de aplicación).

---

### Tabla Promotion
La tabla **Promotion** almacena las promociones o descuentos disponibles en el sistema.

Permite definir campañas de descuento que pueden aplicarse a determinados clientes, facilitando estrategias comerciales como ofertas temporales, promociones especiales o fidelización de clientes.

Relaciones:
```bash
promotion (1) ─── (N) customer_promotion
```
* Una promoción puede asignarse a múltiples clientes.
* La relación entre clientes y promociones se gestiona mediante la tabla customer_promotion.

Reglas de negocio:
* El nombre de la promoción es obligatorio (NOT NULL).
* El porcentaje de descuento se almacena en discount_percentage.
* El descuento por defecto es 0 si no se especifica.
* Una promoción puede tener fechas de inicio y fin para controlar su periodo de validez.
* El estado de la promoción puede ser active o inactive.
* Solo las promociones activas y dentro del rango de fechas deberían aplicarse a ventas (regla de negocio a nivel de aplicación).

---

### Tabla Customer Promotion
La tabla **Customer Promotion** gestiona la asignación de promociones a clientes específicos dentro del sistema.

Permite controlar qué promociones están disponibles para cada cliente y si dichas promociones ya han sido utilizadas o aplicadas en una venta.

Relaciones:
```bash
customer (1) ─── (N) customer_promotion
promotion (1) ─── (N) customer_promotion
```
* Un cliente puede tener múltiples promociones asignadas.
* Una promoción puede asignarse a múltiples clientes.
* Esta tabla funciona como una tabla intermedia (relación muchos a muchos) entre customer y promotion.

Reglas de negocio:
* Cada registro debe estar asociado a un cliente existente (customer_id NOT NULL).
* Cada registro debe estar asociado a una promoción existente (promotion_id NOT NULL).
* El campo applied indica si la promoción ya fue utilizada en una compra.
* La fecha de asignación se registra automáticamente mediante assignment_date.
* Un cliente puede tener varias promociones asignadas simultáneamente.
* Una promoción solo debería aplicarse una vez si applied = TRUE (regla de negocio controlada a nivel de aplicación).

---

### Tabla Invoice
La tabla **Invoice** almacena las facturas generadas en el sistema cuando se realiza una venta.

Cada factura representa una transacción de venta completa, incluyendo el cliente asociado, el usuario que realizó la operación, los montos calculados y el método de pago utilizado.

Relaciones:
```bash
customer (1) ─── (N) invoice
user (1) ─── (N) invoice
invoice (1) ─── (N) invoice_detail
```
* Un cliente puede tener múltiples facturas.
* Un usuario puede emitir múltiples facturas.
* Una factura contiene múltiples líneas de productos en la tabla invoice_detail.

Reglas de negocio:
* Cada factura debe estar asociada a un usuario que realizó la venta (user_id NOT NULL).
* El cliente es opcional, permitiendo ventas sin cliente registrado (customer_id NULL).
* El número de factura debe ser único en el sistema (number_invoice UNIQUE).
* Los campos de subtotal, impuestos y total son obligatorios.
* El método de pago puede ser efectivo, tarjeta o transferencia.
* El estado de la factura puede ser emitida o cancelada.
* La fecha de emisión se registra automáticamente (issue_date).
* El campo pdf_generated indica si la factura ya fue exportada o generada en PDF.
* Una factura cancelada no debería generar movimientos de inventario nuevos (regla de negocio a nivel de aplicación).

---

### Tabla Inventory Movement
La tabla **Inventory Movement** registra los movimientos de stock de los productos dentro del sistema.

Cada registro representa un cambio en la cantidad disponible de un producto, ya sea por ventas o compras, permitiendo mantener un historial completo de modificaciones del inventario.

Relaciones:
```bash
product (1) ─── (N) inventory_movement
user (1) ─── (N) inventory_movement
inventory_movement (1) ─── (1) invoice_detail
inventory_movement (1) ─── (1) purchase_detail
```
* Un producto puede tener múltiples movimientos de inventario.
* Un usuario puede generar múltiples movimientos de inventario.
* Cada movimiento puede estar asociado a un detalle de factura (salida de stock).
* Cada movimiento puede estar asociado a un detalle de compra (entrada de stock).

Reglas de negocio:
* Cada movimiento debe estar asociado a un producto existente (product_id NOT NULL).
* Cada movimiento debe registrar el usuario que realizó la operación (user_id NOT NULL).
* El campo amount representa la cantidad de unidades movidas.
* La fecha del movimiento se registra automáticamente mediante created_at.
* Los movimientos no se crean manualmente, sino como resultado de:
* una venta (factura) → salida de inventario
* una compra → entrada de inventario
* El historial de movimientos no debe eliminarse, ya que forma parte del registro histórico del inventario.

---

### Tabla Invoice Detail
La tabla **Invoice Detail** almacena las líneas o ítems individuales de cada factura dentro del sistema.

Cada registro representa un producto incluido en una factura, indicando cantidad vendida, precio unitario y subtotal, además de vincular el movimiento correspodiente en el inventario.

Relaciones:
```bash
invoice (1) ─── (N) invoice_detail
product (1) ─── (N) invoice_detail
invoice_detail (1) ─── (1) inventory_movement
```
* Una factura puede contener múltiples productos.
* Un producto puede aparecer en múltiples facturas.
* Cada línea de factura genera un único movimiento de inventario.

Reglas de negocio:
* Cada detalle debe estar asociado a una factura existente (invoice_id NOT NULL).
* Si una factura se elimina, todos sus detalles se eliminan automáticamente (ON DELETE CASCADE).
* Cada detalle debe referenciar un producto existente (product_id NOT NULL).
* Cada detalle está vinculado a un único movimiento de inventario (inventory_movement_id UNIQUE).
* La cantidad vendida se almacena en amount.
* El precio unitario corresponde al precio del producto en el momento de la venta, no necesariamente al precio actual del producto.
* El subtotal se calcula como amount × unit_price.
* Cada línea de factura debe generar un movimiento de inventario de salida (regla de negocio a nivel de aplicación).

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
* Cada proveedor debe tener un nombre (name NOT NULL).
* Los campos email, teléfono y dirección son opcionales.
* El campo state indica si el proveedor está activo o inactivo en el sistema.
* Solo proveedores activos deberían poder ser utilizados para registrar nuevas compras (regla de negocio a nivel de aplicación).
* La fecha created_at registra automáticamente cuándo se creó el proveedor.
* El historial de proveedores no debería eliminarse si existen compras asociadas, para mantener la trazabilidad del inventario.

---

### Tabla Purchase
La tabla **Purchase** almacena las compras realizadas a proveedores dentro del sistema.

Representa el documento principal de compra, donde se registra que proveedor suministró los productos, qué usuario registró la compra y el monto total de la operación.

Las líneas de productos comprados se almacenan en la tabla **Purchase Detail**.

Relaciones:
```bash
supplier (1) ─── (N) purchase
user (1) ─── (N) purchase
purchase (1) ─── (N) purchase_detail
```
* Un proveedor puede tener múltiples compras.
* Un usuario puede registrar múltiples compras.
* Cada compra puede tener múltiples líneas de detalle en **Purchase Detail**.

Reglas de negocio:
* Cada compra debe estar asociada a un proveedor (supplier_id NOT NULL).
* Cada compra debe estar registrada por un usuario del sistema (user_id NOT NULL).
* El monto total de la compra es obligatorio (total_amount NOT NULL).
* La fecha de compra se registra automáticamente mediante purchase_date.
* El campo state indica si la compra:
* completada → la compra fue válida y afecta al inventario.
* cancelada → la compra fue anulada.
* Una compra debe tener al menos un registro en purchase_detail para representar los productos comprados.
* Las compras generan movimientos de inventario positivos a través de los registros en inventory_movement asociados a los detalles de compra.

---

### Tabla Purchase Detail
La tabla **Purchase Detail** almacena las lineas o ítems individuales de cada compra registrada en el sistema.

Cada registro representa un producto adquirido en una compra, indicando la cantidad, el costo unitario y el subtotal de ese ítem, además de vincular el movimiento correspondiente en el inventario.

Relaciones:
```bash
purchase (1) ─── (N) purchase_detail
product (1) ─── (N) purchase_detail
purchase_detail (1) ─── (1) inventory_movement
```
* Una compra puede contener múltiples productos.
* Un producto puede aparecer en múltiples compras.
* Cada línea de compra genera un único movimiento de inventario positivo.

Reglas de negocio:
* Cada detalle debe estar asociado a una compra existente (purchase_id NOT NULL).
* Si una compra se elimina, todos sus detalles se eliminan automáticamente (ON DELETE CASCADE).
* Cada detalle debe referenciar un producto existente (product_id NOT NULL).
* Cada detalle está vinculado a un único movimiento de inventario (inventory_movement_id UNIQUE).
* La cantidad comprada se almacena en amount.
* El costo unitario corresponde al precio de adquisición del producto en el momento de la compra (unit_cost).
* El subtotal se calcula como amount × unit_cost.
* Cada línea de compra debe generar un movimiento de inventario de entrada (regla de negocio a nivel de aplicación).
* Una compra cancelada no debería generar movimientos de inventario nuevos ni afectar el stock (regla de negocio a nivel de aplicación).

## Esquema
```bash
CREATE TABLE IF NOT EXISTS role (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(30) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    role_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    state ENUM('activo', 'inactivo') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,

    FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE IF NOT EXISTS category (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    state ENUM('activa', 'inactiva') DEFAULT 'activa',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    category_id BIGINT NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    unique_code VARCHAR(50) UNIQUE NOT NULL,
    sale_price DECIMAL(10, 2) NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    state ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,

    FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE IF NOT EXISTS inventory (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT UNIQUE NOT NULl,
    amount INT NOT NULL DEFAULT 0,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS customer (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120),
    number_phone VARCHAR(50),
    address TEXT,
    state ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS promotion (
	id BIGINT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(100) NOT NULL,
	description TEXT,
    discount_percentage DECIMAL(5, 2) DEFAULT 0,
	start_date DATE,
	end_date DATE,
	state ENUM('active', 'inactive') DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS customer_promotion(
	id BIGINT PRIMARY KEY AUTO_INCREMENT,
	customer_id BIGINT NOT NULL,
	promotion_id BIGINT NOT NULL,
	applied BOOLEAN DEFAULT FALSE,
	assignment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	FOREIGN KEY (customer_id) REFERENCES customer(id),
	FOREIGN KEY (promotion_id) REFERENCES promotion(id)
);

CREATE TABLE IF NOT EXISTS invoice (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT NULL,
    user_id BIGINT NOT NULL,
    number_invoice VARCHAR(50) UNIQUE NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,
    tax_amount DECIMAL(12, 2) DEFAULT 0,
    total_amount DECIMAL(12, 2) NOT NULL,
    payment_method ENUM('efectivo', 'tarjeta', 'transferencia') DEFAULT 'efectivo',
    state ENUM('emitida', 'cancelada') DEFAULT 'emitida',
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pdf_generated BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS inventory_movement (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    amount INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS invoice_detail (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    invoice_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    inventory_movement_id BIGINT UNIQUE NOT NULL,
    amount INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,

    FOREIGN KEY (invoice_id) REFERENCES invoice(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (inventory_movement_id) REFERENCES inventory_movement(id)
);

CREATE TABLE IF NOT EXISTS supplier (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120),
    number_phone VARCHAR(50),
    address TEXT,
    state ENUM('activo', 'inactivo') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS purchase (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    supplier_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    state ENUM('completada', 'cancelada') DEFAULT 'completada',

    FOREIGN KEY (supplier_id) REFERENCES supplier(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS purchase_detail (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    purchase_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    inventory_movement_id BIGINT UNIQUE NOT NULL,
    amount INT NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,

    FOREIGN KEY (purchase_id) REFERENCES purchase(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (inventory_movement_id) REFERENCES inventory_movement(id)
);
```
