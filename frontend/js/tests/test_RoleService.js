/**
 * ========================================
 * TEST FILE - RoleService
 * ========================================
 */

import { authService, roleService } from "../services/index.js";
import { PAYLOADS } from "./payloads.js";

export const tests = [
    {
        name: 'Create Role',
        method: 'POST',
        endpoint: '/v1/roles/',
        execute: async (context) => {
            const result = await roleService.create(PAYLOADS.role);
            if (result.success && result.data?.id) context.createdRoleId = result.data.id;
            return result;
        }
    },
    {
        name: 'GET All Roles',
        method: 'GET',
        endpoint: '/v1/roles/',
        execute: async () => await roleService.getAllRoles()
    },
    {
        name: 'GET Role By ID',
        method: 'GET',
        endpoint: '/v1/roles/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdRoleId) throw new Error('No ID available');
            return await roleService.getRoleById(context.createdRoleId);
        }
    },
    {
        name: 'GET Active Roles',
        method: 'GET',
        endpoint: '/v1/roles/active/',
        execute: async () => await roleService.getActiveRoles()
    },
    {
        name: 'GET Inactive Roles',
        method: 'GET',
        endpoint: '/v1/roles/inactive/',
        execute: async () => await roleService.getInactiveRoles()
    },
    {
        name: 'Update Role',
        method: 'PATCH',
        endpoint: '/v1/roles/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdRoleId) throw new Error('No ID available');
            return await roleService.update(context.createdRoleId, PAYLOADS.roleUpdate);
        }
    },
    {
        name: 'Deactivate Role',
        method: 'PATCH',
        endpoint: '/v1/roles/{id}/deactivate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdRoleId) throw new Error('No ID available');
            return await roleService.deactivate(context.createdRoleId);
        }
    },
    {
        name: 'Activate Role',
        method: 'PATCH',
        endpoint: '/v1/roles/{id}/activate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdRoleId) throw new Error('No ID available');
            return await roleService.activate(context.createdRoleId);
        }
    },
    {
        name: 'Delete Role',
        method: 'DELETE',
        endpoint: '/v1/roles/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdRoleId) throw new Error('No ID available');
            return await roleService.delete(context.createdRoleId);
        }
    }
];

export async function runTests() {
    console.log("=== RoleService Tests ===\n");
    if (!authService.isAuthenticated()) await authService.login("jeiron@gmail.com", "jeiron123");

    const context = {};
    for (const test of tests) {
        console.log(`Test: ${test.method} ${test.endpoint}`);
        try {
            const result = await test.execute(context);
            if (!result || !result.success) throw new Error(result?.message || 'Operation failed');
            console.log(`  ✓ ${test.name}: PASS`);
        } catch (e) {
            console.log(`  ✗ ${test.name}: FAIL -`, e.message);
        }
    }
    console.log("\n=== RoleService Tests Complete ===");
}
