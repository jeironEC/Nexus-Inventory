// Servicio para gestionar inventarios

import { BaseService } from "./BaseService.js";
import { URL_INVENTORIES } from "../utils/const.js";

class InventoryService extends BaseService {
    constructor() {
        super(URL_INVENTORIES);
    }
}

export const inventoryService = new InventoryService();
