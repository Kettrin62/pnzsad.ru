from django.contrib import admin
from .models import Order, OrderItem

EMPTY_VALUE = '-пусто-'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'email', 'address', 'postal_code',
        'city', 'created', 'updated',
    )
    list_filter = ('created', 'updated')
    inlines = [OrderItemInline]
    empty_value_display = EMPTY_VALUE


admin.site.register(Order, OrderAdmin)
