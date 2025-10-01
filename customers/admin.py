from django.contrib import admin
from .models import CustomerProfile, Address

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'default_currency', 'default_language', 'marketing_consent', 'created_at']
    list_filter = ['marketing_consent', 'default_currency', 'default_language', 'created_at']
    search_fields = ['user__email', 'user__username', 'phone']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'is_default', 'city', 'country', 'created_at']
    list_filter = ['type', 'is_default', 'country', 'created_at']
    search_fields = ['user__email', 'first_name', 'last_name', 'city', 'address1']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('user', 'type', 'is_default')
        }),
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'company', 'phone')
        }),
        ('Address', {
            'fields': ('address1', 'address2', 'city', 'state', 'country', 'postal_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
