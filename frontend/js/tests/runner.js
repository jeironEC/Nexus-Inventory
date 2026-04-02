/**
 * ========================================
 * TEST RUNNER - Individual Test Execution
 * ========================================
 */

import { authService } from "../services/index.js";

// Service definitions with icons
const services = [
    { id: 'user', name: 'Users', icon: '👤' },
    { id: 'role', name: 'Roles', icon: '🎭' },
    { id: 'category', name: 'Categories', icon: '📁' },
    { id: 'product', name: 'Products', icon: '📦' },
    { id: 'customer', name: 'Customers', icon: '👥' },
    { id: 'supplier', name: 'Suppliers', icon: '🚚' },
    { id: 'promotion', name: 'Promotions', icon: '🏷️' },
    { id: 'customerPromotion', name: 'Customer Promotions', icon: '🎟️' },
    { id: 'inventory', name: 'Inventory', icon: '📊' },
    { id: 'inventoryMovement', name: 'Inventory Movements', icon: '📦' },
    { id: 'sale', name: 'Sales', icon: '💰' },
    { id: 'purchase', name: 'Purchases', icon: '🛒' },
    { id: 'saleReturn', name: 'Sale Returns', icon: '↩️' },
    { id: 'purchaseReturn', name: 'Purchase Returns', icon: '🔙' },
    { id: 'invoice', name: 'Invoices', icon: '📄' },
    { id: 'report', name: 'Reports', icon: '📈' }
];

// State
let currentService = null;
let currentTests = [];
let sharedContext = {};
let passCount = 0;
let failCount = 0;

// DOM Elements
const servicesList = document.getElementById('servicesList');
const welcomePanel = document.getElementById('welcomePanel');
const detailView = document.getElementById('detailView');
const serviceTitle = document.getElementById('serviceTitle');
const runAllBtn = document.getElementById('runAllBtn');
const testGrid = document.getElementById('testGrid');
const passCountEl = document.getElementById('passCount');
const failCountEl = document.getElementById('failCount');
const totalCountEl = document.getElementById('totalCount');
const backBtn = document.getElementById('backBtn');

// Initialize services list
function initServices() {
    servicesList.innerHTML = services.map(s => `
        <button class="service-item" data-service="${s.id}">
            <span class="service-icon">${s.icon}</span>
            <span>${s.name}</span>
        </button>
    `).join('');

    servicesList.querySelectorAll('.service-item').forEach(item => {
        item.addEventListener('click', () => showService(item.dataset.service));
    });
}

// Show service detail
async function showService(serviceId) {
    currentService = serviceId;
    const service = services.find(s => s.id === serviceId);

    // Update UI
    servicesList.querySelectorAll('.service-item').forEach(item => {
        item.classList.toggle('active', item.dataset.service === serviceId);
    });

    serviceTitle.textContent = service.name;
    welcomePanel.style.display = 'none';
    detailView.classList.add('active');

    // Reset state
    passCount = 0;
    failCount = 0;
    sharedContext = {};
    updateStats();

    // Dynamically load tests from individual file
    testGrid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--sky); padding: 40px;">⏳ Cargar tests...</div>';

    const serviceName = serviceId.charAt(0).toUpperCase() + serviceId.slice(1);
    try {
        const module = await import(`./test_${serviceName}Service.js`);
        currentTests = module.tests || [];
        renderTests();
    } catch(e) {
        console.error("Failed to load test module", e);
        testGrid.innerHTML = `<div style="color: var(--danger); text-align: center; padding: 40px; grid-column: 1/-1;">Error cargando tests de ${serviceName}</div>`;
        currentTests = [];
        totalCountEl.textContent = "0";
    }
}

// Render test cards
function renderTests() {
    testGrid.innerHTML = currentTests.map((test, index) => `
        <div class="test-card" data-index="${index}">
            <div class="test-card-header">
                <span class="test-method">${test.method}</span>
                <span class="test-status"></span>
            </div>
            <div class="test-name">${test.name}</div>
            <div class="test-endpoint">${test.endpoint}</div>
            <div class="test-message" style="display: none;"></div>
        </div>
    `).join('');

    totalCountEl.textContent = currentTests.length;

    // Add click handlers
    testGrid.querySelectorAll('.test-card').forEach(card => {
        card.addEventListener('click', () => runTest(parseInt(card.dataset.index)));
    });
}

// Update stats
function updateStats() {
    passCountEl.textContent = passCount;
    failCountEl.textContent = failCount;
}

// Run single test
async function runTest(testIndex) {
    const test = currentTests[testIndex];
    const card = testGrid.querySelector(`[data-index="${testIndex}"]`);

    // Show running state
    card.classList.remove('passed', 'failed');
    card.classList.add('running');
    card.querySelector('.test-status').textContent = '⏳';
    card.querySelector('.test-message').style.display = 'none';

    try {
        if (!authService.isAuthenticated()) {
            await authService.login('jeiron@gmail.com', 'jeiron123');
        }

        // Auto-fetch ID if the test requires it but we haven't created one yet
        const contextIdKey = `created${currentService.charAt(0).toUpperCase()}${currentService.slice(1)}Id`;
        let existingId = sharedContext[contextIdKey];

        if (test.needsId && !existingId) {
            const services = await import('../services/index.js');
            const service = services[currentService + 'Service'];

            // Special cases for pluralization
            let getMethod = `getAll${currentService.charAt(0).toUpperCase()}${currentService.slice(1)}s`;
            if (currentService === 'category') getMethod = 'getAllCategories';
            if (currentService === 'inventory') getMethod = 'getAllInventories';

            if (service && service[getMethod]) {
                const list = await service[getMethod]();
                if (list && list.success && list.data && list.data.length > 0) {
                    existingId = list.data[0].id; // Pick first available ID
                    sharedContext[contextIdKey] = existingId;
                }
            }
        }

        // Live visual UI replacement for the ID testing
        if (existingId && test.endpoint.includes('{id}')) {
            card.querySelector('.test-endpoint').textContent = test.endpoint.replaceAll('{id}', existingId);
        }

        let result = await test.execute(sharedContext);

        if (result && result.success) {
            card.classList.remove('running');
            card.classList.add('passed');
            card.querySelector('.test-status').textContent = '✓';
            passCount++;
        } else {
            throw new Error(result?.message || 'Request failed');
        }
    } catch (e) {
        card.classList.remove('running');
        card.classList.add('failed');
        card.querySelector('.test-status').textContent = '✗';
        card.querySelector('.test-message').textContent = e.message;
        card.querySelector('.test-message').style.display = 'block';
        failCount++;
    }

    updateStats();
}

// Run all tests
async function runAllTests() {
    for (let i = 0; i < currentTests.length; i++) {
        await runTest(i);
        await new Promise(r => setTimeout(r, 200));
    }
}

// Event listeners
backBtn.addEventListener('click', () => {
    currentService = null;
    detailView.classList.remove('active');
    welcomePanel.style.display = 'flex';
    servicesList.querySelectorAll('.service-item').forEach(item => item.classList.remove('active'));
    currentTests = [];
});

runAllBtn.addEventListener('click', runAllTests);

// Initialize
initServices();
