/**
 * ========================================
 * CENTRALIZED PAYLOADS
 * All test data in one place
 * ========================================
 */

const today = new Date().toISOString().split('T')[0];
const future = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

export const PAYLOADS = {
    // User
    user: {
        email: "test@nexus.com",
        password: "TestPass123!",
        role: 1
    },
    userUpdate: {
        first_name: "Updated"
    },

    // Role
    role: {
        name: "TestRole",
        description: "Test Role Description"
    },
    roleUpdate: {
        description: "Updated Description"
    },

    // Category
    category: {
        name: "TestCategory",
        description: "Test Category Description"
    },
    categoryUpdate: {
        description: "Updated Description"
    },

    // Product
    product: {
        category_id: 1,
        name: "TestProduct",
        description: "Test Product Description",
        unique_code: "TEST001",
        sale_price: 100.00,
        purchase_price: 80.00
    },
    productUpdate: {
        description: "Updated Description"
    },

    // Customer
    customer: {
        first_name: "Test",
        last_name: "Customer",
        email: "testcustomer@nexus.com",
        number_phone: "123456789",
        address: "Test Address"
    },
    customerUpdate: {
        address: "Updated Address"
    },

    // Supplier
    supplier: {
        name: "TestSupplier",
        email: "testsupplier@nexus.com",
        number_phone: "123456789",
        address: "Test Address"
    },
    supplierUpdate: {
        address: "Updated Address"
    },

    // Promotion
    promotion: {
        name: "TestPromotion",
        description: "Test Promotion Description",
        discount_percentage: 20,
        start_date: today,
        end_date: future
    },
    promotionUpdate: {
        description: "Updated Description"
    },

    // Customer Promotion
    customerPromotion: {
        customer_id: 1,
        promotion_id: 1
    },

    // Sale
    sale: {
        customer_id: 1,
        payment_method: "CASH",
        details: [
            { product_id: 1, quantity: 2, unit_price: "100.00" }
        ]
    },
    saleUpdate: {
        payment_method: "CARD"
    },

    // Purchase
    purchase: {
        supplier_id: 1,
        details: [
            { product_id: 1, quantity: 2, unit_cost: "100.00" }
        ]
    },
    purchaseUpdate: {
        supplier_id: 1
    },

    // Sale Return
    saleReturn: {
        sale_id: 1,
        reason: "Product defective",
        details: [
            { product_id: 1, quantity: 1, unit_price: "50.00" }
        ]
    },

    // Purchase Return
    purchaseReturn: {
        purchase_id: 1,
        reason: "Product defective",
        details: [
            { product_id: 1, quantity: 1, unit_cost: "50.00" }
        ]
    }
};

export default PAYLOADS;
