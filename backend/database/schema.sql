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
-- COMPANY
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS company (
    id           BIGINT PRIMARY KEY AUTO_INCREMENT,
    tax_id       VARCHAR(20) UNIQUE NOT NULL,
    name         VARCHAR(255) NOT NULL,
    address      TEXT,
    number_phone VARCHAR(50),
    email        VARCHAR(120) UNIQUE NOT NULL,
    website      TEXT,
    logo         VARCHAR(255),
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
    company_id     BIGINT NOT NULL,
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

    FOREIGN KEY (company_id)  REFERENCES company(id),
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (user_id)     REFERENCES user(id),
    FOREIGN KEY (updated_by)  REFERENCES user(id),
    FOREIGN KEY (deleted_by)  REFERENCES user(id)
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
    company_id    BIGINT NOT NULL,
    supplier_id   BIGINT NOT NULL,
    user_id       BIGINT NOT NULL,
    total_amount  DECIMAL(12, 2) NOT NULL,
    state         ENUM('completed', 'canceled') DEFAULT 'completed',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP NULL,
    deleted_at    TIMESTAMP NULL,
    updated_by    BIGINT NULL,
    deleted_by    BIGINT NULL,

    FOREIGN KEY (company_id)  REFERENCES company(id),
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

-- ─────────────────────────────────────────
-- INVOICE
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS invoice (
    id             BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_id     BIGINT NOT NULL,
    sale_id        BIGINT UNIQUE NOT NULL,
    purchase_id    BIGINT UNIQUE NOT NULL,
    number_invoice VARCHAR(50) UNIQUE NOT NULL,
    state          ENUM('issued', 'canceled') DEFAULT 'issued',
    invoice_type   ENUM('sale', 'purchase'),
    pdf_generated  BOOLEAN DEFAULT FALSE,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP NULL,
    deleted_at     TIMESTAMP NULL,
    created_by     BIGINT NULL,
    updated_by     BIGINT NULL,
    deleted_by     BIGINT NULL,

    FOREIGN KEY (company_id)  REFERENCES company(id),
    FOREIGN KEY (sale_id)     REFERENCES sale(id) ON DELETE CASCADE,
    FOREIGN KEY (purchase_id) REFERENCES purchase(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by)  REFERENCES user(id),
    FOREIGN KEY (updated_by)  REFERENCES user(id),
    FOREIGN KEY (deleted_by)  REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- SALE RETURN
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sale_return (
    id           BIGINT PRIMARY KEY AUTO_INCREMENT,
    sale_id      BIGINT NOT NULL,
    user_id      BIGINT NOT NULL,
    reason       TEXT,
    total_amount DECIMAL(12, 2) NOT NULL,
    state        ENUM('completed', 'canceled') DEFAULT 'completed',

    FOREIGN KEY (sale_id) REFERENCES sale(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- SALE RETURN DETAIL
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sale_return_detail (
    id                    BIGINT PRIMARY KEY AUTO_INCREMENT,
    sale_return_id        BIGINT UNIQUE NOT NULL,
    product_id            BIGINT UNIQUE NOT NULL,
    inventory_movement_id BIGINT UNIQUE NOT NULL,
    quantity              INT NOT NULL,
    unit_price            DECIMAL(10, 2) NOT NULL,
    subtotal              DECIMAL(12, 2) NOT NULL,
    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (sale_return_id)        REFERENCES sale_return(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id)            REFERENCES product(id),
    FOREIGN KEY (inventory_movement_id) REFERENCES inventory_movement(id)
);

-- ─────────────────────────────────────────
-- PURCHASE RETURN
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS purchase_return (
    id           BIGINT PRIMARY KEY AUTO_INCREMENT,
    purchase_id  BIGINT NOT NULL,
    user_id      BIGINT NOT NULL,
    reason       TEXT,
    total_amount DECIMAL(12, 2) NOT NULL,
    state        ENUM('completed', 'canceled') DEFAULT 'completed',

    FOREIGN KEY (purchase_id) REFERENCES purchase(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- PURCHASE RETURN DETAIL
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS purchase_return_detail (
    id                    BIGINT PRIMARY KEY AUTO_INCREMENT,
    purchase_return_id    BIGINT UNIQUE NOT NULL,
    product_id            BIGINT UNIQUE NOT NULL,
    inventory_movement_id BIGINT UNIQUE NOT NULL,
    quantity              INT NOT NULL,
    unit_cost             DECIMAL(10, 2) NOT NULL,
    subtotal              DECIMAL(12, 2) NOT NULL,
    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (purchase_return_id)    REFERENCES purchase_return(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id)            REFERENCES product(id),
    FOREIGN KEY (inventory_movement_id) REFERENCES inventory_movement(id)
);
