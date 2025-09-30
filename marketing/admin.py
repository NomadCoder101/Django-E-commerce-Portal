from django.contrib import admin
from .models import DiscountCode, PromoBanner, NewsletterSubscription

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'amount', 'is_active', 'valid_from', 'valid_until', 'uses_count']
    list_filter = ['is_active', 'discount_type', 'valid_from', 'valid_until']
    search_fields = ['code', 'description']
    readonly_fields = ['uses_count', 'created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('code', 'description', 'discount_type', 'amount')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_until', 'is_active')
        }),
        ('Usage Limits', {
            'fields': ('min_purchase', 'max_uses', 'uses_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(PromoBanner)
class PromoBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'placement', 'priority', 'is_active', 'start_date', 'end_date']
    list_filter = ['is_active', 'placement', 'start_date', 'end_date']
    search_fields = ['title', 'subtitle']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('title', 'subtitle', 'image', 'url')
        }),
        ('Display Settings', {
            'fields': ('placement', 'priority', 'is_active')
        }),
        ('Validity Period', {
            'fields': ('start_date', 'end_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
