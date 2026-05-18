from django.conf import settings
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from nexus_inventory_backend.db.models import (
    Sale,
    SaleDetail,
    Purchase,
    PurchaseDetail,
    Inventory,
    InventoryMovement,
    Customer,
    Invoice,
    SaleReturn,
    PurchaseReturn,
)
from nexus_inventory_backend.db.enums import OperationState, InvoiceType

from api.serializers.empty import EmptySerializer
from api.serializers.reports import (
    SaleReportSerializer,
    SaleByCustomerSerializer,
    SaleByPaymentMethodSerializer,
    SaleByPeriodSerializer,
    PurchaseReportSerializer,
    PurchaseBySupplierSerializer,
    PurchaseByPeriodSerializer,
    InventoryReportSerializer,
    InventoryLowStockSerializer,
    InventoryMovementReportSerializer,
    ProductByCategorySerializer,
    ProductBySupplierSerializer,
    ProductPerformanceSerializer,
    CustomerReportSerializer,
    InvoiceSummarySerializer,
    ReturnReportSummarySerializer,
    ReturnDetailReportSerializer,
)

from api.filters.reports import (
    SaleReportFilter,
    PurchaseReportFilter,
    InventoryReportFilter,
    ProductReportFilter,
    CustomerReportFilter,
    InvoiceReportFilter,
    SaleReturnReportFilter,
    PurchaseReturnReportFilter,
)

from api.mixins.report_filter import ReportFilterMixin
from api.services.company_service import CompanyService
from api.services.reports.sale_report_service import SaleReportService
from api.services.reports.purchase_report_service import PurchaseReportService
from api.services.reports.inventory_report_service import InventoryReportService
from api.services.reports.product_report_service import ProductReportService
from api.services.reports.customer_report_service import CustomerReportService
from api.services.reports.invoice_report_service import InvoiceReportService
from api.services.reports.sale_return_report_service import SaleReturnReportService
from api.services.reports.purchase_return_report_service import (
    PurchaseReturnReportService,
)
from api.services.util_service import format_currency
from api.utils import get_trunc_func


class SaleReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las ventas del sistema.
    Utiliza parámetros de consulta para filtrar y agrupar datos.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="group_by",
                type=str,
                enum=["customer", "payment_method", "period"],
                description="Agrupar por...",
            ),
            OpenApiParameter(
                name="period",
                type=str,
                enum=["day", "week", "month", "year"],
                description="Tipo de periodo (solo si group_by=period)",
            ),
        ],
        responses={200: SaleReportSerializer},
    )
    def list(self, request):
        group_by = request.query_params.get("group_by")
        qs = self.get_filtered_queryset(Sale.objects.all(), SaleReportFilter)
        summary = SaleReportService.get_summary(qs)

        if group_by:
            qs_completed = qs.filter(state=OperationState.COMPLETED)
            if group_by == "customer":
                data = SaleReportService.get_by_customer(qs_completed)
                data = SaleByCustomerSerializer(data, many=True).data
            elif group_by == "payment_method":
                data = SaleReportService.get_by_payment_method(qs_completed)
                data = SaleByPaymentMethodSerializer(data, many=True).data
            elif group_by == "period":
                period = request.query_params.get("period", "month")
                trunc_func = get_trunc_func(period)
                data = SaleReportService.get_by_period(qs_completed, trunc_func)
                data = SaleByPeriodSerializer(data, many=True).data
            else:
                data = []
        else:
            serialized_summary = SaleReportSerializer(summary).data
            data = [serialized_summary]

        return Response({"summary": SaleReportSerializer(summary).data, "data": data})

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="group_by", type=str, enum=["customer", "payment_method", "period"]
            ),
            OpenApiParameter(
                name="period", type=str, enum=["day", "week", "month", "year"]
            ),
        ]
    )
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="group_by", type=str, enum=["customer", "payment_method", "period"]
            ),
            OpenApiParameter(
                name="period", type=str, enum=["day", "week", "month", "year"]
            ),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def sales_pdf(self, request):
        group_by = request.query_params.get("group_by")
        company = CompanyService.get_active_company()
        qs = self.get_filtered_queryset(Sale.objects.all(), SaleReportFilter)

        sections = []
        kpis = []

        if group_by:
            if group_by == "customer":
                result = SaleReportService.get_by_customer(qs)
                title = "Ventas por Cliente"
                headers = ["Cliente", "Total Ventas", "Ingresos"]
                data_rows = [
                    {
                        "values_list": [
                            item["customer_name"],
                            item["total_sales"],
                            format_currency(item["total_revenue"]),
                        ]
                    }
                    for item in result
                ]
            elif group_by == "payment_method":
                result = SaleReportService.get_by_payment_method(qs)
                title = "Ventas por Método de Pago"
                headers = ["Método", "Total Ventas", "Ingresos"]
                data_rows = [
                    {
                        "values_list": [
                            item["payment_method_display"],
                            item["total_sales"],
                            format_currency(item["total_revenue"]),
                        ]
                    }
                    for item in result
                ]
            else:
                period = request.query_params.get("period", "month")
                result = SaleReportService.get_by_period(qs, period)
                title = f"Ventas por Período ({period})"
                headers = ["Período", "Total Ventas", "Ingresos"]
                data_rows = [
                    {
                        "values_list": [
                            item["period"],
                            item["total_sales"],
                            format_currency(item["total_revenue"]),
                        ]
                    }
                    for item in result
                ]

            totals = SaleReportService.get_totals_from_list(result)
            kpis = [
                {"label": "Total Ventas", "value": totals["total_sales"]},
                {
                    "label": "Ingresos Totales",
                    "value": format_currency(totals["total_revenue"]),
                    "highlight": True,
                },
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": True}
            )
            filename = "reporte_ventas_agrupado.pdf"
        else:
            data = SaleReportService.build_sales_pdf(qs)
            title = "Reporte Detallado de Ventas"
            headers = [
                "Fecha",
                "Cliente",
                "Método",
                "Subtotal",
                "Impuesto",
                "Total",
                "Estado",
            ]
            data_rows = []
            for sale in data["sales"]:
                data_rows.append(
                    {
                        "values_list": [
                            (
                                sale["created_at"].strftime("%d/%m/%Y")
                                if hasattr(sale["created_at"], "strftime")
                                else sale["created_at"]
                            ),
                            f"{sale.get('customer__first_name', '')} {sale.get('customer__last_name', '')}".strip()
                            or "Anónimo",
                            sale["payment_method"],
                            format_currency(sale["subtotal"]),
                            format_currency(sale["tax_amount"]),
                            format_currency(sale["total_amount"]),
                            {
                                "is_badge": True,
                                "text": (
                                    "Completada"
                                    if sale["state"] == "COMPLETED"
                                    else "Cancelada"
                                ),
                                "badge_type": (
                                    "success"
                                    if sale["state"] == "COMPLETED"
                                    else "danger"
                                ),
                            },
                        ]
                    }
                )

            summary = data["summary"]
            kpis = [
                {"label": "Total Ventas", "value": summary["total_sales"]},
                {
                    "label": "Ingresos",
                    "value": format_currency(summary["total_revenue"]),
                    "highlight": True,
                },
                {"label": "Impuestos", "value": format_currency(summary["total_tax"])},
                {
                    "label": "Ticket Promedio",
                    "value": format_currency(summary["average_ticket"]),
                },
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": False}
            )
            filename = "reporte_ventas_detallado.pdf"

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": sections,
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(
            string=html_content, base_url=str(settings.MEDIA_ROOT) + "/"
        ).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{filename}"'
        return response


class PurchaseReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las compras del sistema.
    Utiliza parámetros de consulta para filtrar y agrupar datos.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name="group_by", type=str, enum=["supplier", "period"]),
            OpenApiParameter(
                name="period", type=str, enum=["day", "week", "month", "year"]
            ),
        ],
        responses={200: PurchaseReportSerializer},
    )
    def list(self, request):
        group_by = request.query_params.get("group_by")
        qs = self.get_filtered_queryset(Purchase.objects.all(), PurchaseReportFilter)
        summary = PurchaseReportService.get_summary(qs)

        if group_by:
            qs_completed = qs.filter(state=OperationState.COMPLETED)
            if group_by == "supplier":
                data = PurchaseReportService.get_by_supplier(qs_completed)
                data = PurchaseBySupplierSerializer(data, many=True).data
            elif group_by == "period":
                period = request.query_params.get("period", "month")
                trunc_func = get_trunc_func(period)
                data = PurchaseReportService.get_by_period(qs_completed, trunc_func)
                data = PurchaseByPeriodSerializer(data, many=True).data
            else:
                data = []
        else:
            serialized_summary = PurchaseReportSerializer(summary).data
            data = [serialized_summary]

        return Response(
            {"summary": PurchaseReportSerializer(summary).data, "data": data}
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name="group_by", type=str, enum=["supplier", "period"]),
            OpenApiParameter(
                name="period", type=str, enum=["day", "week", "month", "year"]
            ),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def purchases_pdf(self, request):
        group_by = request.query_params.get("group_by")
        company = CompanyService.get_active_company()
        qs = self.get_filtered_queryset(Purchase.objects.all(), PurchaseReportFilter)

        sections = []
        kpis = []

        if group_by:
            if group_by == "supplier":
                result = PurchaseReportService.get_by_supplier(qs)
                title = "Compras por Proveedor"
                headers = ["Proveedor", "Total Compras", "Gasto Total"]
                data_rows = [
                    {
                        "values_list": [
                            item["supplier_name"],
                            item["total_purchases"],
                            format_currency(item["total_spent"]),
                        ]
                    }
                    for item in result
                ]
            else:
                period = request.query_params.get("period", "month")
                trunc_func = get_trunc_func(period)
                result = PurchaseReportService.get_by_period(qs, trunc_func)
                title = f"Compras por Período ({period})"
                headers = ["Período", "Total Compras", "Gasto Total"]
                data_rows = [
                    {
                        "values_list": [
                            item["period"],
                            item["total_purchases"],
                            format_currency(item["total_spent"]),
                        ]
                    }
                    for item in result
                ]

            totals = PurchaseReportService.get_totals_from_list(result)
            kpis = [
                {"label": "Total Compras", "value": totals["total_purchases"]},
                {
                    "label": "Gasto Total",
                    "value": format_currency(totals["total_spent"]),
                    "highlight": True,
                },
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": True}
            )
            filename = "reporte_compras_agrupado.pdf"
        else:
            data = PurchaseReportService.build_purchase_pdf_data(qs)
            title = "Reporte Detallado de Compras"
            headers = ["Fecha", "Proveedor", "Subtotal", "Impuesto", "Total", "Estado"]
            data_rows = []
            for purchase in data["purchases"]:
                data_rows.append(
                    {
                        "values_list": [
                            (
                                purchase["created_at"].strftime("%d/%m/%Y")
                                if hasattr(purchase["created_at"], "strftime")
                                else purchase["created_at"]
                            ),
                            purchase.get("supplier__name", "N/A"),
                            format_currency(purchase["total_amount"]),
                            format_currency(purchase["total_amount"]),
                            {
                                "is_badge": True,
                                "text": (
                                    "Completada"
                                    if purchase["state"] == "COMPLETED"
                                    else "Cancelada"
                                ),
                                "badge_type": (
                                    "success"
                                    if purchase["state"] == "COMPLETED"
                                    else "danger"
                                ),
                            },
                        ]
                    }
                )

            summary = data["summary"]
            kpis = [
                {"label": "Total Compras", "value": summary["total_purchases"]},
                {
                    "label": "Gasto Total",
                    "value": format_currency(summary["total_spent"]),
                    "highlight": True,
                },
                {
                    "label": "Compra Promedio",
                    "value": format_currency(summary.get("average_purchase")),
                },
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": False}
            )
            filename = "reporte_compras_detallado.pdf"

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": sections,
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(
            string=html_content, base_url=str(settings.MEDIA_ROOT) + "/"
        ).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{filename}"'
        return response


class InventoryReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con el inventario del sistema.
    Incluye stock actual por producto, productos con stock bajo un umbral configurable
    y historial de movimientos de inventario (entradas y salidas).
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name="view", type=str, enum=["low_stock", "movements"]),
            OpenApiParameter(
                name="low_stock_threshold",
                type=int,
                description="Umbral para stock bajo",
            ),
        ],
        responses={200: InventoryReportSerializer(many=True)},
    )
    def list(self, request):
        view = request.query_params.get("view")

        if view == "low_stock":
            threshold = int(
                request.query_params.get(
                    "low_stock_threshold", settings.LOW_STOCK_THRESHOLD
                )
            )
            qs = self.get_filtered_queryset(
                Inventory.objects.select_related("product", "product__category").filter(
                    quantity__lte=threshold
                ),
                InventoryReportFilter,
            )
            raw_data = [
                InventoryReportService.map_low_stock(inv, threshold) for inv in qs
            ]
            summary = InventoryReportService.get_totals_for_inventory(raw_data)
            data = InventoryLowStockSerializer(raw_data, many=True).data
        elif view == "movements":
            qs = self.get_filtered_queryset(
                InventoryMovement.objects.select_related("product", "user").all(),
                InventoryReportFilter,
            )
            raw_data = [InventoryReportService.map_movement(m) for m in qs]
            summary = InventoryReportService.get_totals_for_movements(raw_data)
            data = InventoryMovementReportSerializer(raw_data, many=True).data
        else:
            qs = self.get_filtered_queryset(
                Inventory.objects.select_related("product", "product__category").all(),
                InventoryReportFilter,
            )
            raw_data = [InventoryReportService.map_inventory(inv) for inv in qs]
            summary = InventoryReportService.get_totals_for_inventory(raw_data)
            data = InventoryReportSerializer(raw_data, many=True).data

        return Response({"summary": summary, "data": data})

    @extend_schema(
        parameters=[
            OpenApiParameter(name="view", type=str, enum=["low_stock", "movements"]),
            OpenApiParameter(name="low_stock_threshold", type=int),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def inventory_pdf(self, request):
        view = request.query_params.get("view")
        company = CompanyService.get_active_company()
        kpis = []

        if view == "low_stock":
            threshold = int(
                request.query_params.get(
                    "low_stock_threshold", settings.LOW_STOCK_THRESHOLD
                )
            )
            qs = self.get_filtered_queryset(
                Inventory.objects.select_related("product", "product__category").filter(
                    quantity__lte=threshold
                ),
                InventoryReportFilter,
            )
            result = [
                InventoryReportService.map_low_stock(inv, threshold) for inv in qs
            ]
            title = f"Reporte de Bajo Stock (Umbral: {threshold})"
            headers = ["Producto", "Categoría", "Stock Actual", "Umbral", "Estado"]
            data_rows = [
                {
                    "values_list": [
                        item["product_name"],
                        item["category"],
                        item["quantity"],
                        threshold,
                        {
                            "is_badge": True,
                            "text": "Crítico" if item["quantity"] == 0 else "Bajo",
                            "badge_type": (
                                "danger" if item["quantity"] == 0 else "warning"
                            ),
                        },
                    ]
                }
                for item in result
            ]
            kpis = [
                {"label": "Productos Afectados", "value": len(result), "danger": True}
            ]
            filename = "reporte_bajo_stock.pdf"

        elif view == "movements":
            qs = self.get_filtered_queryset(
                InventoryMovement.objects.select_related("product", "user").all(),
                InventoryReportFilter,
            )
            result = [InventoryReportService.map_movement(m) for m in qs]
            totals = InventoryReportService.get_totals_for_movements(result)
            title = "Movimientos de Inventario"
            headers = ["Fecha", "Producto", "Tipo", "Cantidad", "Usuario"]
            data_rows = [
                {
                    "values_list": [
                        item["created_at"],
                        item["product_name"],
                        {
                            "is_badge": True,
                            "text": (
                                "Entrada" if item["movement_type"] == "IN" else "Salida"
                            ),
                            "badge_type": (
                                "success" if item["movement_type"] == "IN" else "info"
                            ),
                        },
                        item["quantity"],
                        item["user"],
                    ]
                }
                for item in result
            ]
            kpis = [
                {"label": "Total Entradas", "value": totals["total_in"]},
                {"label": "Total Salidas", "value": totals["total_out"]},
            ]
            filename = "reporte_movimientos.pdf"

        else:
            qs = self.get_filtered_queryset(
                Inventory.objects.select_related("product", "product__category").all(),
                InventoryReportFilter,
            )
            result = [InventoryReportService.map_inventory(inv) for inv in qs]
            totals = InventoryReportService.get_totals_for_inventory(result)
            title = "Reporte General de Inventario"
            headers = [
                "Producto",
                "Categoría",
                "Cantidad",
                "Precio Venta",
                "Valor Stock",
            ]
            data_rows = [
                {
                    "values_list": [
                        item["product_name"],
                        item["category"],
                        item["quantity"],
                        format_currency(item["sale_price"]),
                        format_currency(item["stock_value"]),
                    ]
                }
                for item in result
            ]
            kpis = [
                {"label": "Total Productos", "value": len(result)},
                {"label": "Stock Total", "value": totals["total_quantity"]},
                {
                    "label": "Valor Total Stock",
                    "value": format_currency(totals["total_stock_value"]),
                    "highlight": True,
                },
            ]
            filename = "reporte_inventario_general.pdf"

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": [
                {"headers": headers, "data": data_rows, "align_last_right": not view}
            ],
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(
            string=html_content, base_url=str(settings.MEDIA_ROOT) + "/"
        ).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{filename}"'
        return response


class ProductReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con los productos del sistema.
    Utiliza parámetros de consulta para obtener diferentes vistas.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    def _base_sale_detail_qs(self):
        return self.get_filtered_queryset(
            SaleDetail.objects.select_related(
                "product", "product__category", "sale"
            ).filter(sale__state=OperationState.COMPLETED),
            ProductReportFilter,
        )

    def _base_purchase_detail_qs(self):
        return self.get_filtered_queryset(
            PurchaseDetail.objects.select_related(
                "product", "product__category", "purchase"
            ).filter(purchase__state=OperationState.COMPLETED),
            ProductReportFilter,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="view",
                type=str,
                enum=[
                    "top_selling",
                    "low_selling",
                    "most_purchased",
                    "by_category",
                    "by_supplier",
                ],
            ),
            OpenApiParameter(
                name="limit", type=int, description="Límite de resultados"
            ),
        ],
        responses={200: EmptySerializer},
    )
    def list(self, request):
        view = request.query_params.get("view")
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))

        if view == "top_selling":
            data = ProductReportService.get_products_report(
                qs=self._base_sale_detail_qs(), order_by="-total_quantity", limit=limit
            )
            return Response(
                {
                    "summary": {"view": view, "limit": limit},
                    "data": ProductPerformanceSerializer(data, many=True).data,
                }
            )
        elif view == "low_selling":
            data = ProductReportService.get_products_report(
                qs=self._base_sale_detail_qs(), order_by="total_quantity", limit=limit
            )
            return Response(
                {
                    "summary": {"view": view, "limit": limit},
                    "data": ProductPerformanceSerializer(data, many=True).data,
                }
            )
        elif view == "most_purchased":
            data = ProductReportService.get_products_report(
                qs=self._base_purchase_detail_qs(),
                order_by="-total_quantity",
                limit=limit,
            )
            return Response(
                {
                    "summary": {"view": view, "limit": limit},
                    "data": ProductPerformanceSerializer(data, many=True).data,
                }
            )
        elif view == "by_category":
            data = ProductReportService.get_products_by_category(
                self._base_sale_detail_qs()
            )
            return Response(
                {
                    "summary": {"view": view},
                    "data": ProductByCategorySerializer(data, many=True).data,
                }
            )
        elif view == "by_supplier":
            data = ProductReportService.get_products_by_supplier(
                self._base_purchase_detail_qs()
            )
            return Response(
                {
                    "summary": {"view": view},
                    "data": ProductBySupplierSerializer(data, many=True).data,
                }
            )

        summary = ProductReportService.build_report_products(
            self._base_sale_detail_qs(), self._base_purchase_detail_qs(), limit
        )
        data = ProductPerformanceSerializer(
            summary.get("top_selling", []), many=True
        ).data

        return Response({"summary": summary, "data": data})

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="view",
                type=str,
                enum=[
                    "top_selling",
                    "low_selling",
                    "most_purchased",
                    "by_category",
                    "by_supplier",
                ],
            ),
            OpenApiParameter(name="limit", type=int),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def products_pdf(self, request):
        view = request.query_params.get("view")
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        company = CompanyService.get_active_company()
        sections = []
        kpis = []
        title = "Reporte de Productos"

        if view == "top_selling":
            result = ProductReportService.get_products_report(
                qs=self._base_sale_detail_qs(), order_by="-total_quantity", limit=limit
            )
            totals = ProductReportService.get_totals_from_report(result)
            title = "Productos Más Vendidos"
            headers = ["Producto", "Categoría", "Cant. Vendida", "Ingresos"]
            data_rows = [
                {
                    "values_list": [
                        item["product_name"],
                        item["category"],
                        item["total_quantity"],
                        format_currency(item["total_revenue"]),
                    ]
                }
                for item in result
            ]
            kpis = [
                {
                    "label": "Ingresos Totales",
                    "value": format_currency(totals["total_revenue"]),
                    "highlight": True,
                }
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": True}
            )
        elif view == "low_selling":
            result = ProductReportService.get_products_report(
                qs=self._base_sale_detail_qs(), order_by="total_quantity", limit=limit
            )
            totals = ProductReportService.get_totals_from_report(result)
            title = "Productos Menos Vendidos"
            headers = ["Producto", "Categoría", "Cant. Vendida", "Ingresos"]
            data_rows = [
                {
                    "values_list": [
                        item["product_name"],
                        item["category"],
                        item["total_quantity"],
                        format_currency(item["total_revenue"]),
                    ]
                }
                for item in result
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": True}
            )
        elif view == "most_purchased":
            result = ProductReportService.get_products_report(
                qs=self._base_purchase_detail_qs(),
                order_by="-total_quantity",
                limit=limit,
            )
            totals = ProductReportService.get_totals_from_report(
                result, amount_field="total_spent"
            )
            title = "Productos Más Comprados"
            headers = ["Producto", "Categoría", "Cant. Comprada", "Gasto Total"]
            data_rows = [
                {
                    "values_list": [
                        item["product_name"],
                        item["category"],
                        item["total_quantity"],
                        format_currency(item["total_spent"]),
                    ]
                }
                for item in result
            ]
            kpis = [
                {
                    "label": "Gasto Total",
                    "value": format_currency(totals["total_spent"]),
                    "highlight": True,
                }
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": True}
            )
        elif view == "by_category":
            result = ProductReportService.get_products_by_category(
                self._base_sale_detail_qs()
            )
            totals = ProductReportService.get_totals_by_category(result)
            title = "Ventas por Categoría"
            headers = ["Categoría", "Cant. Productos", "Cant. Vendida", "Ingresos"]
            data_rows = [
                {
                    "values_list": [
                        item["category_name"],
                        item["total_products"],
                        item["total_quantity_sold"],
                        format_currency(item["total_revenue"]),
                    ]
                }
                for item in result
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": True}
            )
        elif view == "by_supplier":
            result = ProductReportService.get_products_by_supplier(
                self._base_purchase_detail_qs()
            )
            title = "Productos por Proveedor"
            headers = ["Proveedor", "Cant. Productos", "Cant. Comprada", "Gasto Total"]
            data_rows = [
                {
                    "values_list": [
                        item["supplier_name"],
                        item["total_products"],
                        item["total_quantity_purchased"],
                        format_currency(item["total_spent"]),
                    ]
                }
                for item in result
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": True}
            )
        else:
            data = ProductReportService.build_report_products(
                self._base_sale_detail_qs(), self._base_purchase_detail_qs(), limit
            )
            title = "Resumen General de Productos"

            sections.append(
                {
                    "title": "Top Ventas",
                    "headers": ["Producto", "Cant.", "Ingresos"],
                    "data": [
                        {
                            "values_list": [
                                item["product_name"],
                                item["total_quantity"],
                                format_currency(item["total_revenue"]),
                            ]
                        }
                        for item in data["top_selling"]
                    ],
                    "align_last_right": True,
                }
            )
            sections.append(
                {
                    "title": "Más Comprados",
                    "headers": ["Producto", "Cant.", "Gasto"],
                    "data": [
                        {
                            "values_list": [
                                item["product_name"],
                                item["total_quantity"],
                                format_currency(item["total_spent"]),
                            ]
                        }
                        for item in data["most_purchased"]
                    ],
                    "align_last_right": True,
                }
            )
            kpis = [
                {"label": "Categorías", "value": len(data["by_category"])},
                {
                    "label": "Top Producto",
                    "value": (
                        data["top_selling"][0]["product_name"]
                        if data["top_selling"]
                        else "N/A"
                    ),
                },
            ]

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": sections,
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(
            string=html_content, base_url=str(settings.MEDIA_ROOT) + "/"
        ).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_productos.pdf"'
        return response


class CustomerReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con los clientes del sistema.
    Utiliza parámetros de consulta para filtrar y obtener rankings.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name="view", type=str, enum=["top"]),
            OpenApiParameter(
                name="limit", type=int, description="Límite de resultados"
            ),
        ],
        responses={200: CustomerReportSerializer(many=True)},
    )
    def list(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        qs = self.get_filtered_queryset(
            Customer.objects.filter(sales__state=OperationState.COMPLETED),
            CustomerReportFilter,
        )
        raw_data = CustomerReportService.get_summary(qs, limit)
        summary = CustomerReportService.get_totals_from_summary(raw_data)
        data = CustomerReportSerializer(raw_data, many=True).data

        return Response({"summary": summary, "data": data})

    @extend_schema(
        parameters=[
            OpenApiParameter(name="view", type=str, enum=["top"]),
            OpenApiParameter(name="limit", type=int),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def customers_pdf(self, request):
        view = request.query_params.get("view")
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        company = CompanyService.get_active_company()
        qs = self.get_filtered_queryset(
            Customer.objects.filter(sales__state=OperationState.COMPLETED),
            CustomerReportFilter,
        )
        result = CustomerReportService.get_summary(qs, limit)
        totals = CustomerReportService.get_totals_from_summary(result)

        title = (
            "Reporte de Clientes Top"
            if view == "top"
            else "Reporte General de Clientes"
        )
        headers = ["Cliente", "Total Compras", "Gasto Total"]
        data_rows = [
            {
                "values_list": [
                    item["customer_name"],
                    item["total_purchases"],
                    format_currency(item["total_spent"]),
                ]
            }
            for item in result
        ]

        kpis = [
            {"label": "Total Clientes", "value": totals["total_customers"]},
            {"label": "Total Compras", "value": totals["total_purchases"]},
            {
                "label": "Gasto Total",
                "value": format_currency(totals["total_spent"]),
                "highlight": True,
            },
        ]

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": [
                {"headers": headers, "data": data_rows, "align_last_right": True}
            ],
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(
            string=html_content, base_url=str(settings.MEDIA_ROOT) + "/"
        ).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_clientes.pdf"'
        return response


class InvoiceReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las facturas del sistema.
    Utiliza parámetros de consulta para filtrar por tipo (venta/compra).
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name="type", type=str, enum=["sale", "purchase"]),
        ],
        responses={200: InvoiceSummarySerializer},
    )
    def list(self, request):
        invoice_type = request.query_params.get("type")
        qs = Invoice.objects.all()
        if invoice_type == "sale":
            qs = qs.filter(invoice_type=InvoiceType.SALE)
        elif invoice_type == "purchase":
            qs = qs.filter(invoice_type=InvoiceType.PURCHASE)

        qs_filtered = self.get_filtered_queryset(qs, InvoiceReportFilter)

        if invoice_type == "sale":
            data = InvoiceReportService.build_sales_invoices(qs_filtered)
        elif invoice_type == "purchase":
            data = InvoiceReportService.build_purchase_invoices(qs_filtered)
        else:
            data = list(
                qs_filtered.values(
                    "id",
                    "number_invoice",
                    "created_at",
                    "state",
                    "pdf_generated",
                    "sale__customer__first_name",
                    "sale__customer__last_name",
                    "sale__total_amount",
                    "purchase__supplier__name",
                    "purchase__total_amount",
                )
            )

        summary = InvoiceReportService.get_summary(qs_filtered)

        return Response(
            {"summary": InvoiceSummarySerializer(summary).data, "data": data}
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name="type", type=str, enum=["sale", "purchase"]),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def invoices_pdf(self, request):
        invoice_type = request.query_params.get("type")
        company = CompanyService.get_active_company()
        qs = self.get_filtered_queryset(Invoice.objects.all(), InvoiceReportFilter)

        if invoice_type == "sale":
            qs = qs.filter(invoice_type=InvoiceType.SALE)
            invoices = InvoiceReportService.build_sales_invoices(qs)
            title = "Reporte de Facturas de Ventas"
            headers = ["Número", "Fecha", "Cliente", "Total", "Estado"]
            data_rows = [
                {
                    "values_list": [
                        inv["number_invoice"],
                        (
                            inv["created_at"].strftime("%d/%m/%Y")
                            if hasattr(inv["created_at"], "strftime")
                            else inv["created_at"]
                        ),
                        f"{inv.get('sale__customer__first_name', '')} {inv.get('sale__customer__last_name', '')}".strip()
                        or "Anónimo",
                        format_currency(inv["sale__total_amount"]),
                        {
                            "is_badge": True,
                            "text": (
                                "Emitida" if inv["state"] == "ISSUED" else "Cancelada"
                            ),
                            "badge_type": (
                                "success" if inv["state"] == "ISSUED" else "danger"
                            ),
                        },
                    ]
                }
                for inv in invoices
            ]
        elif invoice_type == "purchase":
            qs = qs.filter(invoice_type=InvoiceType.PURCHASE)
            invoices = InvoiceReportService.build_purchase_invoices(qs)
            title = "Reporte de Facturas de Compras"
            headers = ["Número", "Fecha", "Proveedor", "Total", "Estado"]
            data_rows = [
                {
                    "values_list": [
                        inv["number_invoice"],
                        (
                            inv["created_at"].strftime("%d/%m/%Y")
                            if hasattr(inv["created_at"], "strftime")
                            else inv["created_at"]
                        ),
                        inv.get("purchase__supplier__name", "N/A"),
                        format_currency(inv["purchase__total_amount"]),
                        {
                            "is_badge": True,
                            "text": (
                                "Emitida" if inv["state"] == "ISSUED" else "Cancelada"
                            ),
                            "badge_type": (
                                "success" if inv["state"] == "ISSUED" else "danger"
                            ),
                        },
                    ]
                }
                for inv in invoices
            ]
        else:
            invoices = list(
                qs.values(
                    "number_invoice",
                    "created_at",
                    "sale__customer__first_name",
                    "sale__customer__last_name",
                    "purchase__supplier__name",
                    "sale__total_amount",
                    "purchase__total_amount",
                    "state",
                )
            )
            title = "Reporte General de Facturas"
            headers = ["Número", "Fecha", "Cliente/Prov", "Total", "Estado"]
            data_rows = []
            for inv in invoices:
                name = (
                    f"{inv.get('sale__customer__first_name', '')} {inv.get('sale__customer__last_name', '')}".strip()
                    or inv.get("purchase__supplier__name")
                    or "N/A"
                )
                amount = inv.get("sale__total_amount") or inv.get(
                    "purchase__total_amount"
                )
                data_rows.append(
                    {
                        "values_list": [
                            inv["number_invoice"],
                            (
                                inv["created_at"].strftime("%d/%m/%Y")
                                if hasattr(inv["created_at"], "strftime")
                                else inv["created_at"]
                            ),
                            name,
                            format_currency(amount),
                            {
                                "is_badge": True,
                                "text": (
                                    "Emitida"
                                    if inv["state"] == "ISSUED"
                                    else "Cancelada"
                                ),
                                "badge_type": (
                                    "success" if inv["state"] == "ISSUED" else "danger"
                                ),
                            },
                        ]
                    }
                )

        summary = InvoiceReportService.get_summary(qs)
        kpis = [
            {"label": "Total Facturas", "value": summary["total_invoices"]},
            {
                "label": "Emitidas",
                "value": summary["issued_invoices"],
                "highlight": True,
            },
            {
                "label": "Canceladas",
                "value": summary["canceled_invoices"],
                "danger": True,
            },
            {"label": "PDFs", "value": summary["pdf_generated"]},
        ]

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": [
                {"headers": headers, "data": data_rows, "align_last_right": True}
            ],
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(
            string=html_content, base_url=str(settings.MEDIA_ROOT) + "/"
        ).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_facturas.pdf"'
        return response


class ReturnReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las devoluciones (ventas y compras).
    Utiliza el parámetro 'type' para alternar entre ventas y compras.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name="type", type=str, enum=["sale", "purchase"]),
        ],
        responses={200: ReturnReportSummarySerializer},
    )
    def list(self, request):
        return_type = request.query_params.get("type", "sale")

        if return_type == "purchase":
            qs = self.get_filtered_queryset(
                PurchaseReturn.objects.all(), PurchaseReturnReportFilter
            )
            summary = PurchaseReturnReportService.get_summary(qs)
            data = PurchaseReturnReportService.format_returns(qs)
            return Response(
                {
                    "summary": ReturnReportSummarySerializer(summary).data,
                    "data": ReturnDetailReportSerializer(data, many=True).data,
                }
            )

        qs = self.get_filtered_queryset(
            SaleReturn.objects.all(), SaleReturnReportFilter
        )
        summary = SaleReturnReportService.get_summary(qs)
        data = SaleReturnReportService.format_returns(qs)
        return Response(
            {
                "summary": ReturnReportSummarySerializer(summary).data,
                "data": ReturnDetailReportSerializer(data, many=True).data,
            }
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name="type", type=str, enum=["sale", "purchase"]),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def returns_pdf(self, request):
        return_type = request.query_params.get("type", "sale")
        company = CompanyService.get_active_company()

        if return_type == "purchase":
            qs = self.get_filtered_queryset(
                PurchaseReturn.objects.select_related(
                    "purchase", "purchase__supplier"
                ).all(),
                PurchaseReturnReportFilter,
            )
            data = PurchaseReturnReportService.get_summary(qs)
            returns_data = PurchaseReturnReportService.format_returns(qs)
            title = "Reporte de Devoluciones (Compras)"
            headers = ["Fecha", "Proveedor", "Motivo", "Total Reembolso", "Estado"]
            data_rows = [
                {
                    "values_list": [
                        (
                            item["created_at"].strftime("%d/%m/%Y")
                            if hasattr(item["created_at"], "strftime")
                            else item["created_at"]
                        ),
                        item.get("supplier_name", "N/A"),
                        item["reason"],
                        format_currency(item["total_amount"]),
                        {
                            "is_badge": True,
                            "text": (
                                "Completada"
                                if item["state"] == "COMPLETED"
                                else "Pendiente"
                            ),
                            "badge_type": (
                                "success" if item["state"] == "COMPLETED" else "warning"
                            ),
                        },
                    ]
                }
                for item in returns_data
            ]
        else:
            qs = self.get_filtered_queryset(
                SaleReturn.objects.select_related("sale", "sale__customer").all(),
                SaleReturnReportFilter,
            )
            data = SaleReturnReportService.get_summary(qs)
            returns_data = SaleReturnReportService.format_returns(qs)
            title = "Reporte de Devoluciones (Ventas)"
            headers = ["Fecha", "Cliente", "Motivo", "Total Reembolso", "Estado"]
            data_rows = [
                {
                    "values_list": [
                        (
                            item["created_at"].strftime("%d/%m/%Y")
                            if hasattr(item["created_at"], "strftime")
                            else item["created_at"]
                        ),
                        item.get("customer_name", "Anónimo"),
                        item["reason"],
                        format_currency(item["total_amount"]),
                        {
                            "is_badge": True,
                            "text": (
                                "Completada"
                                if item["state"] == "COMPLETED"
                                else "Pendiente"
                            ),
                            "badge_type": (
                                "success" if item["state"] == "COMPLETED" else "warning"
                            ),
                        },
                    ]
                }
                for item in returns_data
            ]

        kpis = [
            {"label": "Total Devoluciones", "value": data["total_returns"]},
            {
                "label": "Monto Total",
                "value": format_currency(data["total_refund_amount"]),
                "highlight": True,
            },
        ]

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": [
                {"headers": headers, "data": data_rows, "align_last_right": True}
            ],
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(
            string=html_content, base_url=str(settings.MEDIA_ROOT) + "/"
        ).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_devoluciones.pdf"'
        return response
