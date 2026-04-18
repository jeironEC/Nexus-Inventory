# Services
from api.services.util_service import get_raw_value


class InventoryReportService:

    @staticmethod
    def get_totals_for_inventory(result):

        return {
            "total_quantity": sum(item.get("quantity", 0) or 0 for item in result),
            "total_sale_price": sum(
                get_raw_value(item["sale_price"]) for item in result
            ),
            "total_stock_value": sum(
                get_raw_value(item["stock_value"]) for item in result
            ),
        }

    @staticmethod
    def get_totals_for_movements(result):
        return {
            "total_in": sum(
                item["quantity"] for item in result if item.get("movement_type") == "IN"
            ),
            "total_out": sum(
                item["quantity"]
                for item in result
                if item.get("movement_type") == "OUT"
            ),
        }

    @staticmethod
    def map_inventory(inv):
        sale_price = float(inv.product.sale_price) if inv.product.sale_price else 0
        stock_value = sale_price * inv.quantity

        return {
            "product_id": inv.product.id,
            "product_name": inv.product.name,
            "category": inv.product.category.name,
            "quantity": inv.quantity,
            "sale_price": sale_price,
            "stock_value": stock_value,
        }

    @staticmethod
    def map_low_stock(inv, threshold):
        return {
            "product_id": inv.product.id,
            "product_name": inv.product.name,
            "category": inv.product.category.name,
            "quantity": inv.quantity,
            "threshold": threshold,
        }

    @staticmethod
    def map_movement(m):
        return {
            "product_id": m.product.id,
            "product_name": m.product.name,
            "movement_type": m.movement_type,
            "quantity": m.quantity,
            "user": (
                f"{m.user.first_name} {m.user.last_name}" if m.user else "Unknown"
            ),
            "created_at": m.created_at,
        }
