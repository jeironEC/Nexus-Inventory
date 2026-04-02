/**
 * ========================================
 * TEST FILE - UserService
 * ========================================
 */

import { authService, userService } from "../services/index.js";
import { PAYLOADS } from "./payloads.js";

export const tests = [
    {
        name: 'Create User',
        method: 'POST',
        endpoint: '/v1/users/',
        execute: async (context) => {
            const result = await userService.create(PAYLOADS.user);
            if (result.success && result.data?.id) context.createdUserId = result.data.id;
            return result;
        }
    },
    {
        name: 'GET All Users',
        method: 'GET',
        endpoint: '/v1/users/',
        execute: async () => await userService.getAllUsers()
    },
    {
        name: 'GET Active Users',
        method: 'GET',
        endpoint: '/v1/users/active/',
        execute: async () => await userService.getActiveUsers()
    },
    {
        name: 'GET Inactive Users',
        method: 'GET',
        endpoint: '/v1/users/inactive/',
        execute: async () => await userService.getInactiveUsers()
    },
    {
        name: 'GET User Profile',
        method: 'GET',
        endpoint: '/v1/users/me/',
        execute: async () => await userService.getUserProfile()
    },
    {
        name: 'Deactivate User',
        method: 'PATCH',
        endpoint: '/v1/users/{id}/deactivate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdUserId) throw new Error('No ID available');
            return await userService.deactivate(context.createdUserId);
        }
    },
    {
        name: 'Activate User',
        method: 'PATCH',
        endpoint: '/v1/users/{id}/activate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdUserId) throw new Error('No ID available');
            return await userService.activate(context.createdUserId);
        }
    },
    {
        name: 'Update User Profile',
        method: 'PATCH',
        endpoint: '/v1/users/me/',
        execute: async () => await userService.updateUserProfile(PAYLOADS.userUpdate)
    },
    {
        name: 'Delete User Profile',
        method: 'DELETE',
        endpoint: '/v1/users/me/',
        execute: async () => await userService.deleteUserProfile()
    }
];

export async function runTests() {
    console.log("=== UserService Tests ===\n");
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
    console.log("\n=== UserService Tests Complete ===");
}
