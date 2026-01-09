from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency', 'description')
    list_filter = ('currency',)
    search_fields = ('name', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_total_price', 'get_currency', 'discount', 'tax', 'created_at')
    list_filter = ('created_at', 'discount', 'tax')
    filter_horizontal = ('items',)
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price()} {obj.get_currency().upper()}"
    get_total_price.short_description = 'Общая стоимость'
    
    def get_currency(self, obj):
        return obj.get_currency().upper()
    get_currency.short_description = 'Валюта'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent_off', 'stripe_coupon_id')
    search_fields = ('name', 'stripe_coupon_id')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'stripe_tax_rate_id')
    search_fields = ('name', 'stripe_tax_rate_id')
