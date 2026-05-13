from django.contrib import admin
from .models import Order
import json

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('order_id', 'customer_name', 'phone_number',
                     'table_number', 'payment_type', 'total_amount',
                     'is_paid', 'ordered_at')
    list_filter   = ('is_paid', 'payment_type', 'table_number')
    search_fields = ('customer_name', 'phone_number', 'table_number')
    readonly_fields = ('order_id', 'ordered_at', 'get_items_display')
    list_editable = ('is_paid',)

    def get_items_display(self, obj):
        items = json.loads(obj.items_ordered)
        lines = [f"• {i['name']} — ₹{i['price']}" for i in items]
        return "\n".join(lines)
    get_items_display.short_description = 'Items Ordered'

    fieldsets = (
        ('Customer Info', {
            'fields': ('customer_name', 'phone_number', 'table_number', 'payment_type')
        }),
        ('Order Details', {
            'fields': ('get_items_display', 'total_amount', 'is_paid', 'ordered_at')
        }),
    )