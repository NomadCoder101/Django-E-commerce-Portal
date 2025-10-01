from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Product, ProductVariant, ProductImage

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['translations__name', 'translations__slug']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    readonly_fields = ['created_at', 'updated_at']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['created_at']

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'category', 'base_price', 'featured', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'featured', 'created_at']
    search_fields = ['translations__name', 'translations__slug', 'sku']
    list_editable = ['base_price', 'featured', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductVariantInline, ProductImageInline]

    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Pricing', {
            'fields': ('base_price', 'sku')
        }),
        ('Status', {
            'fields': ('is_active', 'featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'sku', 'price_override', 'stock_quantity', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'sku', 'product__translations__name']
    list_editable = ['price_override', 'stock_quantity', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'alt_text', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__translations__name', 'alt_text']
    list_editable = ['alt_text', 'is_primary']
    readonly_fields = ['created_at']
