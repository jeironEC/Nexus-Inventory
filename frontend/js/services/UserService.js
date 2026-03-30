import { authService } from "./AuthService.js";
import {
    URL_USERS,
    URL_ACTIVE_USERS,
    URL_INACTIVE_USERS,
    URL_USERS_PROFILE,
} from "../util/const.js";

class UserService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getAllUsers(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_USERS}?${params}` : `${URL_USERS}`;
        return await this.api.get(endpoint);
    }

    async create(dades) {
        return await this.api.post(`${URL_USERS}`, dades);
    }

    async activate(id) {
        return await this.api.patch(`${URL_USERS}${id}/activate/`);
    }

    async deactivate(id) {
        return await this.api.patch(`${URL_USERS}${id}/deactivate/`);
    }

    async getActiveUsers() {
        return await this.api.get(`${URL_ACTIVE_USERS}`);
    }

    async getInactiveUsers() {
        return await this.api.get(`${URL_INACTIVE_USERS}`);
    }

    async getUserProfile() {
        return await this.api.get(`${URL_USERS_PROFILE}`);
    }

    async updateUserProfile(dades) {
        return await this.api.patch(`${URL_USERS_PROFILE}`, dades);
    }

    async deleteUserProfile() {
        return await this.api.delete(`${URL_USERS_PROFILE}`);
    }
}

export const userService = new UserService();
