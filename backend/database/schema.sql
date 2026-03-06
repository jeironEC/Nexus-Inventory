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
    state ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,

    FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE IF NOT EXISTS category (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    state ENUM('active', 'inactive') DEFAULT 'active',
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
    payment_method ENUM('cash', 'card', 'transfer') DEFAULT 'cash',
    state ENUM('issued', 'canceled') DEFAULT 'issued',
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
    state ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS purchase (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    supplier_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    state ENUM('completed', 'canceled') DEFAULT 'completed',

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
