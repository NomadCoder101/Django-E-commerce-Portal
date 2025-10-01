from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'user__email', 'tracking_number']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        (None, {
            'fields': ('user', 'status', 'email')
        }),
        ('Addresses', {
            'fields': ('shipping_address', 'billing_address')
        }),
        ('Financial', {
            'fields': ('currency', 'exchange_rate', 'subtotal', 'shipping_cost', 'tax', 'total')
        }),
        ('Shipping', {
            'fields': ('tracking_number',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Payment', {
            'fields': ('stripe_payment_intent',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
