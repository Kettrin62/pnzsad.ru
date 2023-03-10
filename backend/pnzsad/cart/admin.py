from django.contrib import admin

from .models import Order, OrderItem

EMPTY_VALUE = '-пусто-'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'phoneNumber', 'comment',
        'email', 'created', 'updated',
    )
    list_filter = ('created', 'updated', 'comment')
    inlines = [OrderItemInline]
    empty_value_display = EMPTY_VALUE
    list_editable = ('comment',)


admin.site.register(Order, OrderAdmin)
