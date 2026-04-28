-- ─────────────────────────────────────────
-- ROLE
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS role (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(30) UNIQUE NOT NULL,
    description TEXT,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NULL,
    deleted_at  TIMESTAMP NULL
);

-- ─────────────────────────────────────────
-- USER
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user (
    id         BIGINT PRIMARY KEY AUTO_INCREMENT,
    role_id    BIGINT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL,
    email      VARCHAR(120) UNIQUE NOT NULL,
    nif        VARCHAR(20) UNIQUE NOT NULL,
    password   VARCHAR(255) NOT NULL,
    is_active  BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    deleted_at TIMESTAMP NULL,
    created_by BIGINT NULL,
    updated_by BIGINT NULL,
    deleted_by BIGINT NULL,

    FOREIGN KEY (role_id)    REFERENCES role(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    FOREIGN KEY (deleted_by) REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- PASSWORD RESET OTP
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS password_reset_otp (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id     BIGINT NOT NULL,
    email       VARCHAR(255) NOT NULL,
    otp_hash    VARCHAR(128) NOT NULL,
    is_used     BOOLEAN NOT NULL DEFAULT FALSE,
    reset_token UUID NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NULL,
    deleted_at  TIMESTAMP NULL,

    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- COMPANY
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS company (
    id           BIGINT PRIMARY KEY AUTO_INCREMENT,
    nif          VARCHAR(20) UNIQUE NOT NULL,
    name         VARCHAR(255) NOT NULL,
    address      TEXT,
    phone_number VARCHAR(50),
    email        VARCHAR(120) UNIQUE NOT NULL,
    website      TEXT,
    logo         VARCHAR(255),
    is_active    BOOLEAN NOT NULL DEFAULT TRUE,
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
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
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
    id                  BIGINT PRIMARY KEY AUTO_INCREMENT,
    category_id         BIGINT NOT NULL,
    name                VARCHAR(150) NOT NULL,
    description         TEXT,
    unique_code         VARCHAR(50) UNIQUE NOT NULL,
    sale_price          DECIMAL(10, 2) NOT NULL,
    purchase_price      DECIMAL(10, 2) NOT NULL,
    discount_percentage DECIMAL(5, 2) DEFAULT 0,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NULL,
    deleted_at          TIMESTAMP NULL,
    created_by          BIGINT NULL,
    updated_by          BIGINT NULL,
    deleted_by          BIGINT NULL,

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
    product_id BIGINT UNIQUE NOT NULL,
    quantity   INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    deleted_at TIMESTAMP NULL,
    created_by BIGINT NULL,
    updated_by BIGINT NULL,
    deleted_by BIGINT NULL,

    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    FOREIGN KEY (deleted_by) REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- CUSTOMER
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS customer (
    id           BIGINT PRIMARY KEY AUTO_INCREMENT,
    nif          VARCHAR(20) UNIQUE NOT NULL,
    first_name   VARCHAR(100) NOT NULL,
    last_name    VARCHAR(100) NOT NULL,
    email        VARCHAR(120) UNIQUE NOT NULL,
    phone_number VARCHAR(50),
    address      TEXT,
    is_active    BOOLEAN NOT NULL DEFAULT TRUE,
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
-- SALE
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sale (
    id              BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_id      BIGINT NOT NULL,
    customer_id     BIGINT NULL,
    user_id         BIGINT NOT NULL,
    discount_amount DECIMAL(12, 2) DEFAULT 0,
    subtotal        DECIMAL(12, 2) NOT NULL,
    tax_percentage  DECIMAL(5, 2) DEFAULT 21.00,
    tax_amount      DECIMAL(12, 2) DEFAULT 0,
    total_amount    DECIMAL(12, 2) NOT NULL,
    payment_method  ENUM('cash', 'card', 'transfer') DEFAULT 'cash',
    state           ENUM('completed', 'canceled') DEFAULT 'completed',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NULL,
    deleted_at      TIMESTAMP NULL,
    updated_by      BIGINT NULL,
    deleted_by      BIGINT NULL,

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
    nif          VARCHAR(20) UNIQUE NOT NULL,
    name         VARCHAR(100) NOT NULL,
    email        VARCHAR(120) UNIQUE NOT NULL,
    phone_number VARCHAR(50),
    address      TEXT,
    is_active    BOOLEAN NOT NULL DEFAULT TRUE,
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
    id           BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_id   BIGINT NOT NULL,
    supplier_id  BIGINT NOT NULL,
    user_id      BIGINT NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    state        ENUM('completed', 'canceled') DEFAULT 'completed',
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP NULL,
    deleted_at   TIMESTAMP NULL,
    updated_by   BIGINT NULL,
    deleted_by   BIGINT NULL,

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
    sale_id        BIGINT UNIQUE,
    purchase_id    BIGINT UNIQUE,
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
    FOREIGN KEY (sale_id)     REFERENCES sale(id),
    FOREIGN KEY (purchase_id) REFERENCES purchase(id),
    FOREIGN KEY (created_by)  REFERENCES user(id),
    FOREIGN KEY (updated_by)  REFERENCES user(id),
    FOREIGN KEY (deleted_by)  REFERENCES user(id),
    CHECK (
        (invoice_type = 'sale' AND sale_id IS NOT NULL AND purchase_id IS NULL) OR
        (invoice_type = 'purchase' AND purchase_id IS NOT NULL AND sale_id IS NULL)
    )
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
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP NULL,
    deleted_at   TIMESTAMP NULL,
    updated_by   BIGINT NULL,
    deleted_by   BIGINT NULL,

    FOREIGN KEY (sale_id)    REFERENCES sale(id),
    FOREIGN KEY (user_id)    REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    FOREIGN KEY (deleted_by) REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- SALE RETURN DETAIL
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sale_return_detail (
    id                    BIGINT PRIMARY KEY AUTO_INCREMENT,
    sale_return_id        BIGINT NOT NULL,
    product_id            BIGINT NOT NULL,
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
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP NULL,
    deleted_at   TIMESTAMP NULL,
    updated_by   BIGINT NULL,
    deleted_by   BIGINT NULL,

    FOREIGN KEY (purchase_id) REFERENCES purchase(id),
    FOREIGN KEY (user_id)     REFERENCES user(id),
    FOREIGN KEY (updated_by)  REFERENCES user(id),
    FOREIGN KEY (deleted_by)  REFERENCES user(id)
);

-- ─────────────────────────────────────────
-- PURCHASE RETURN DETAIL
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS purchase_return_detail (
    id                    BIGINT PRIMARY KEY AUTO_INCREMENT,
    purchase_return_id    BIGINT NOT NULL,
    product_id            BIGINT NOT NULL,
    inventory_movement_id BIGINT UNIQUE NOT NULL,
    quantity              INT NOT NULL,
    unit_cost             DECIMAL(10, 2) NOT NULL,
    subtotal              DECIMAL(12, 2) NOT NULL,
    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (purchase_return_id)    REFERENCES purchase_return(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id)            REFERENCES product(id),
    FOREIGN KEY (inventory_movement_id) REFERENCES inventory_movement(id)
);
