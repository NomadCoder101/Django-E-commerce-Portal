from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from decimal import Decimal

class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='checkout_carts'
    )
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f"Cart {self.id} - {self.user.email if self.user else 'Anonymous'}"

    @classmethod
    def get_or_create(cls, request):
        if request.user.is_authenticated:
            cart = cls.objects.filter(user=request.user).first()
            if cart:
                return cart
            if request.session.session_key:
                # If there's an existing cart with this session key, assign it to the user
                cart = cls.objects.filter(
                    session_key=request.session.session_key,
                    user__isnull=True
                ).first()
                if cart:
                    cart.user = request.user
                    cart.save()
                    return cart
        else:
            if not request.session.session_key:
                request.session.create()
            cart = cls.objects.filter(session_key=request.session.session_key).first()
            if cart:
                return cart

        return cls.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key
        )

    def add_item(self, product, quantity=1, variant=None):
        item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()
        return item

    def remove_item(self, item_id):
        try:
            item = self.items.get(id=item_id)
            item.delete()
        except CartItem.DoesNotExist:
            pass

    def update_quantity(self, item_id, quantity):
        try:
            item = self.items.get(id=item_id)
            if quantity > 0:
                item.quantity = quantity
                item.save()
            else:
                item.delete()
        except CartItem.DoesNotExist:
            pass

    def clear(self):
        self.items.all().delete()

    def get_total(self):
        return sum(item.get_total() for item in self.items.all())

    def get_total_display(self):
        return f"{self.get_total():.2f}"

    def get_item_total_display(self, item_id):
        try:
            item = self.items.get(id=item_id)
            return f"{item.get_total():.2f}"
        except CartItem.DoesNotExist:
            return "0.00"

    @property
    def total_items(self):
        return self.items.count()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='checkout_cart_items')
    variant = models.ForeignKey(
        'catalog.ProductVariant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='checkout_cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')
        unique_together = ('cart', 'product', 'variant')

    def get_total(self):
        if self.variant:
            price = self.variant.price
        else:
            price = self.product.price
        return price * self.quantity


class OrderItem(models.Model):
    order = models.ForeignKey('CheckoutSession', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', on_delete=models.SET_NULL, null=True, related_name='checkout_order_items')
    variant = models.ForeignKey(
        'catalog.ProductVariant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checkout_order_items'
    )
    product_name = models.CharField(max_length=255)  # Store the name at time of purchase
    variant_name = models.CharField(max_length=255, blank=True)  # Store the variant name at time of purchase
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Store the price at time of purchase
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return self.quantity * self.unit_price

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')


class CheckoutSession(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('abandoned', _('Abandoned')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40)
    email = models.EmailField()
    currency = models.CharField(max_length=3)
    parent_order = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='checkout_session')
    stripe_payment_intent = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    billing_address = models.JSONField(null=True)
    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_shipping_cost(self):
        """
        Calculate the shipping cost based on the selected shipping method and address
        """
        from shipping.services import ShippingCalculator

        if not self.shipping_method or not self.shipping_address:
            return None

        cart_items = self.parent_order.items.all() if self.parent_order else []
        total_weight = sum(item.quantity * item.product.weight for item in cart_items)
        order_total = sum(item.get_total() for item in cart_items)

        calculator = ShippingCalculator(
            country_code=self.shipping_address.country,
            weight=total_weight,
            order_total=order_total
        )

        shipping_cost = calculator.calculate_cost(self.shipping_method.id)
        if shipping_cost is not None:
            self.shipping_cost = Decimal(str(shipping_cost))
            self.save(update_fields=['shipping_cost'])

        return shipping_cost

    def get_available_shipping_methods(self):
        """
        Get available shipping methods based on the shipping address and cart contents
        """
        from shipping.services import ShippingCalculator

        if not self.shipping_address:
            return []

        cart_items = self.parent_order.items.all() if self.parent_order else []
        total_weight = sum(item.quantity * item.product.weight for item in cart_items)
        order_total = sum(item.get_total() for item in cart_items)

        calculator = ShippingCalculator(
            country_code=self.shipping_address.country,
            weight=total_weight,
            order_total=order_total
        )

        return [rate.shipping_method for rate in calculator.get_available_rates()]

    def get_total(self):
        """
        Calculate the total cost including shipping
        """
        order_total = self.parent_order.get_total() if self.parent_order else Decimal('0')
        shipping_cost = self.shipping_cost or Decimal('0')
        return order_total + shipping_cost

    def __str__(self):
        return f"Checkout session {self.id} - {self.email}"


class PaymentAttempt(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('succeeded', _('Succeeded')),
        ('failed', _('Failed')),
        ('cancelled', _('Cancelled')),
    ]

    order = models.ForeignKey(CheckoutSession, on_delete=models.CASCADE, related_name='payment_attempts')
    stripe_payment_intent = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment attempt {self.id} for checkout {self.checkout_session.id}"
