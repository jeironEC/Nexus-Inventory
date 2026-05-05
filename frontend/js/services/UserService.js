// Servicio para gestionar el perfil de usuario

import { BaseService } from "./BaseService.js";
import { URL_USERS, URL_USERS_PROFILE } from "../utils/const.js";

class UserService extends BaseService {
    constructor() {
        super(URL_USERS);
    }

    // Obtiene el perfil del usuario
    async getUserProfile() {
        return await this.api.get(`${URL_USERS_PROFILE}`);
    }

    // Actualiza el perfil del usuario
    async updateUserProfile(data) {
        return await this.api.patch(`${URL_USERS_PROFILE}`, data);
    }
}

export const userService = new UserService();
