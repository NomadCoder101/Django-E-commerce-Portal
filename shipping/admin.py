from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ShippingZone, ShippingMethod, ShippingRate, ShippingAddress

@admin.register(ShippingZone)
class ShippingZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description', 'countries']

@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'calculation_type', 'is_active', 'estimated_days']
    list_filter = ['is_active', 'calculation_type']
    search_fields = ['name', 'description']
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_active')
        }),
        (_('Calculation Settings'), {
            'fields': ('calculation_type', 'estimated_days')
        }),
        (_('Tracking'), {
            'fields': ('tracking_url_template',),
            'classes': ('collapse',)
        })
    )

@admin.register(ShippingRate)
class ShippingRateAdmin(admin.ModelAdmin):
    list_display = ['shipping_method', 'shipping_zone', 'base_rate', 'weight_rate']
    list_filter = ['shipping_method', 'shipping_zone']
    search_fields = ['shipping_method__name', 'shipping_zone__name']
    fieldsets = (
        (None, {
            'fields': ('shipping_method', 'shipping_zone', 'base_rate')
        }),
        (_('Weight Based Pricing'), {
            'fields': ('weight_rate', 'min_weight', 'max_weight'),
            'classes': ('collapse',)
        }),
        (_('Order Amount Restrictions'), {
            'fields': ('min_order_amount', 'max_order_amount'),
            'classes': ('collapse',)
        })
    )

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_full_name', 'city', 'country', 'is_default']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = _('Name')
    list_filter = ['is_default', 'country', 'city']
    search_fields = ['name', 'address_line1', 'city', 'postal_code']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'is_default')
        }),
        (_('Address Details'), {
            'fields': (
                'address_line1', 'address_line2', 'city',
                'state', 'postal_code', 'country', 'phone'
            )
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
