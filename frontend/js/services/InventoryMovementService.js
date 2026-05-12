import { BaseService } from "./BaseService.js";
import { URL_INVENTORY_MOVEMENTS } from "../utils/const.js";

class InventoryMovementService extends BaseService {
    constructor() {
        super(URL_INVENTORY_MOVEMENTS);
    }
}

export const inventoryMovementService = new InventoryMovementService();
