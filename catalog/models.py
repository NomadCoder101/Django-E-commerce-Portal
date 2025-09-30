from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from parler.models import TranslatableModel, TranslatedFields
from django.urls import reverse


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=200),
        slug=models.SlugField(_("Slug"), max_length=200, unique=True),
        description=models.TextField(_("Description"), blank=True)
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='categories', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:category_detail', args=[self.slug])


class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=200),
        slug=models.SlugField(_("Slug"), max_length=200, unique=True),
        description=models.TextField(_("Description")),
        meta_title=models.CharField(_("Meta Title"), max_length=200, blank=True),
        meta_description=models.TextField(_("Meta Description"), blank=True)
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    base_price = models.DecimalField(_("Base Price"), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sku = models.CharField(_("SKU"), max_length=50, unique=True)
    is_active = models.BooleanField(_("Active"), default=True)
    featured = models.BooleanField(_("Featured"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'name')

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    @property
    def price(self):
        return self.price_override if self.price_override else self.product.base_price
