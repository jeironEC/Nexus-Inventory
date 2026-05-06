import uuid
from decimal import Decimal

from django.db import transaction

from nexus_inventory_backend.db.models import (
    Sale,
    SaleDetail,
    Purchase,
    PurchaseDetail,
    SaleReturn,
    SaleReturnDetail,
    PurchaseReturn,
    PurchaseReturnDetail,
    InventoryMovement,
    Invoice,
    Inventory,
)
from nexus_inventory_backend.db.enums import (
    MovementType,
    InvoiceState,
    InvoiceType,
)


def _validate_stock(details_data):
    """Valida stock suficiente para cada producto en la venta."""
    stock_errors = []
    for detail in details_data:
        product = detail["product"]
        quantity = detail["quantity"]
        try:
            inventory = Inventory.objects.get(product=product)
            if inventory.quantity < quantity:
                stock_errors.append(
                    {
                        "product_id": product.id,
                        "product_name": product.name,
                        "requested": quantity,
                        "available": inventory.quantity,
                    }
                )
        except Inventory.DoesNotExist:
            stock_errors.append(
                {
                    "product_id": product.id,
                    "product_name": product.name,
                    "error": "Product without inventory",
                }
            )
    return stock_errors


def _calculate_totals(details_data, tax_percentage):
    """Calcula subtotal, descuentos e impuestos para una venta."""
    subtotal = Decimal("0.00")
    discount_amount = Decimal("0.00")

    for detail in details_data:
        product = detail["product"]
        quantity = detail["quantity"]
        unit_price = detail["unit_price"]

        product_discount = Decimal("0.00")
        if product.discount_percentage and product.discount_percentage > 0:
            product_discount = (
                unit_price * product.discount_percentage / 100
            ) * quantity

        unit_price_final = unit_price - (
            unit_price * (product.discount_percentage or 0) / 100
        )

        subtotal += quantity * unit_price_final
        discount_amount += product_discount

    tax_base = subtotal - discount_amount
    tax_amount = (tax_base * tax_percentage / 100).quantize(Decimal("0.01"))
    total_amount = tax_base + tax_amount

    return {
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
    }


def _apply_final_prices(details_data):
    """Retorna detalles con precios finales tras aplicar descuentos."""
    result = []
    for detail in details_data:
        product = detail["product"]
        unit_price = detail["unit_price"]

        if product.discount_percentage and product.discount_percentage > 0:
            unit_price = unit_price - (unit_price * product.discount_percentage / 100)

        result.append({**detail, "unit_price_final": unit_price})
    return result


def _create_movement_and_update_inventory(product, quantity, movement_type, user):
    """Crea un movimiento de inventario y actualiza el stock."""
    inventory_movement = InventoryMovement.objects.create(
        product=product,
        user=user,
        movement_type=movement_type,
        quantity=quantity,
    )

    inventory, _ = Inventory.objects.get_or_create(
        product=product, defaults={"quantity": 0}
    )

    if movement_type == MovementType.IN:
        inventory.quantity += quantity
    else:
        inventory.quantity -= quantity
    inventory.save()

    return inventory_movement


def _create_invoice(sale_or_purchase, invoice_type, user):
    """Crea una factura asociada a una venta o compra."""
    if invoice_type == InvoiceType.SALE:
        number = f"SINV-{sale_or_purchase.pk:08d}-{uuid.uuid4().hex[:6].upper()}"
        return Invoice.objects.create(
            sale=sale_or_purchase,
            company=sale_or_purchase.company,
            invoice_type=invoice_type,
            number_invoice=number,
            state=InvoiceState.ISSUED,
            created_by=user,
        )
    else:
        number = f"PINV-{sale_or_purchase.pk:08d}-{uuid.uuid4().hex[:6].upper()}"
        return Invoice.objects.create(
            purchase=sale_or_purchase,
            company=sale_or_purchase.company,
            invoice_type=invoice_type,
            number_invoice=number,
            state=InvoiceState.ISSUED,
            created_by=user,
        )


@transaction.atomic
def create_sale(
    details_data, tax_percentage, user, company=None, customer=None, payment_method=None
):
    """
    Crea una venta completa con detalles, movimientos de inventario y factura.

    Returns:
        Sale: La venta creada.

    Raises:
        serializers.ValidationError: Si no hay stock suficiente.
    """
    from rest_framework import serializers

    stock_errors = _validate_stock(details_data)
    if stock_errors:
        raise serializers.ValidationError(
            {"details": "Stock insufficient", "errors": stock_errors}
        )

    totals = _calculate_totals(details_data, tax_percentage)
    details_with_prices = _apply_final_prices(details_data)

    sale = Sale.objects.create(
        company=company,
        customer=customer,
        payment_method=payment_method,
        user=user,
        discount_amount=totals["discount_amount"],
        subtotal=totals["subtotal"],
        tax_percentage=tax_percentage,
        tax_amount=totals["tax_amount"],
        total_amount=totals["total_amount"],
    )

    for detail in details_with_prices:
        product = detail["product"]
        quantity = detail["quantity"]
        unit_price_final = detail["unit_price_final"]

        inventory_movement = _create_movement_and_update_inventory(
            product, quantity, MovementType.OUT, user
        )

        SaleDetail.objects.create(
            sale=sale,
            product=product,
            inventory_movement=inventory_movement,
            quantity=quantity,
            unit_price=unit_price_final,
            subtotal=quantity * unit_price_final,
        )

    _create_invoice(sale, InvoiceType.SALE, user)
    return sale


@transaction.atomic
def create_purchase(details_data, user, supplier, company=None):
    """
    Crea una compra completa con detalles, movimientos de inventario y factura.

    Returns:
        Purchase: La compra creada.
    """
    total_amount = sum(
        detail["quantity"] * detail["unit_cost"] for detail in details_data
    )

    purchase = Purchase.objects.create(
        company=company,
        supplier=supplier,
        user=user,
        total_amount=total_amount,
    )

    for detail in details_data:
        product = detail["product"]
        quantity = detail["quantity"]
        unit_cost = detail["unit_cost"]

        inventory_movement = _create_movement_and_update_inventory(
            product, quantity, MovementType.IN, user
        )

        PurchaseDetail.objects.create(
            purchase=purchase,
            product=product,
            inventory_movement=inventory_movement,
            quantity=quantity,
            unit_cost=unit_cost,
            subtotal=quantity * unit_cost,
        )

    Invoice.objects.create(
        purchase=purchase,
        company=purchase.company,
        invoice_type=InvoiceType.PURCHASE,
        number_invoice=f"PINV-{purchase.pk:08d}-{uuid.uuid4().hex[:6].upper()}",
        state=InvoiceState.ISSUED,
        created_by=user,
    )

    return purchase


@transaction.atomic
def create_sale_return(sale, details_data, reason, user):
    """
    Crea una devolución de venta con detalles y movimientos de inventario.

    Returns:
        SaleReturn: La devolución creada.
    """
    total_amount = sum(
        detail["quantity"] * detail["unit_price"] for detail in details_data
    )

    sale_return = SaleReturn.objects.create(
        sale=sale,
        reason=reason,
        user=user,
        total_amount=total_amount,
    )

    for detail in details_data:
        product = detail["product"]
        quantity = detail["quantity"]
        unit_price = detail["unit_price"]

        inventory_movement = _create_movement_and_update_inventory(
            product, quantity, MovementType.IN, user
        )

        SaleReturnDetail.objects.create(
            sale_return=sale_return,
            product=product,
            inventory_movement=inventory_movement,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=quantity * unit_price,
        )

    return sale_return


@transaction.atomic
def create_purchase_return(purchase, details_data, reason, user):
    """
    Crea una devolución de compra con detalles y movimientos de inventario.

    Returns:
        PurchaseReturn: La devolución creada.
    """
    total_amount = sum(
        detail["quantity"] * detail["unit_cost"] for detail in details_data
    )

    purchase_return = PurchaseReturn.objects.create(
        purchase=purchase,
        reason=reason,
        user=user,
        total_amount=total_amount,
    )

    for detail in details_data:
        product = detail["product"]
        quantity = detail["quantity"]
        unit_cost = detail["unit_cost"]

        inventory_movement = _create_movement_and_update_inventory(
            product, quantity, MovementType.OUT, user
        )

        PurchaseReturnDetail.objects.create(
            purchase_return=purchase_return,
            product=product,
            inventory_movement=inventory_movement,
            quantity=quantity,
            unit_cost=unit_cost,
            subtotal=quantity * unit_cost,
        )

    return purchase_return
