from django.contrib import admin
from .models import Product, StockMovement


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'price',
        'quantity',
        'low_stock_threshold',
    )
    search_fields = ('name', 'sku')
    list_filter = ('quantity',)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'movement_type',
        'quantity',
        'date',
    )
    list_filter = ('movement_type', 'date')
    search_fields = ('product__name', 'product__sku')
