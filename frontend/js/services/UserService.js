import { AuthService } from "./AuthService.js";
import {
    URL_USER,
    URL_ACTIVE_USERS,
    URL_INACTIVE_USERS,
    URL_USER_PROFILE,
} from "../util/const.js";

export class UserService {
    constructor() {
        this.api = new AuthService().getApiClient();
    }

    async getAllUsers(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_USER}?${params}` : `${URL_USER}`;
        return await this.api.get(endpoint);
    }

    async create(dades) {
        return await this.api.post(`${URL_USER}`, dades);
    }

    async activate(id) {
        return await this.api.patch(`${URL_USER}${id}/activate/`);
    }

    async deactivate(id) {
        return await this.api.patch(`${URL_USER}${id}/deactivate/`);
    }

    async getActiveUsers() {
        return await this.api.get(`${URL_ACTIVE_USERS}`);
    }

    async getInactiveUsers() {
        return await this.api.get(`${URL_INACTIVE_USERS}`);
    }

    async getUserProfile() {
        return await this.api.get(`${URL_USER_PROFILE}`);
    }

    async updateUserProfile(dades) {
        return await this.api.patch(`${URL_USER_PROFILE}`, dades);
    }

    async deleteUserProfile() {
        return await this.api.delete(`${URL_USER_PROFILE}`);
    }
}
