from django.contrib import admin
from .models import *


class OrderItemInline(admin.StackedInline):  # lub StackedInline
    model = OrderItem
    extra = 0  # liczba dodatkowych pól do wyświetlenia
    readonly_fields = ('product', 'quantity', 'date_added',)


class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 0
    readonly_fields = ('customer',)


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('customer', 'total',)
    inlines = [OrderItemInline, ShippingAddressInline]


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Shipper)
admin.site.register(ProductCategory)
