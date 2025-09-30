from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class ShippingZone(models.Model):
    """
    Represents a shipping zone (e.g., domestic, international, specific regions)
    """
    name = models.CharField(_('Name'), max_length=100)
    countries = models.JSONField(_('Countries'), help_text=_('List of country codes in this zone'))
    description = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Shipping Zone')
        verbose_name_plural = _('Shipping Zones')

    def __str__(self):
        return self.name

class ShippingMethod(models.Model):
    """
    Represents a shipping method (e.g., Standard, Express, Next Day)
    """
    CALCULATION_TYPES = [
        ('flat', _('Flat Rate')),
        ('weight', _('Weight Based')),
        ('price', _('Order Total Based')),
    ]

    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    calculation_type = models.CharField(
        _('Calculation Type'),
        max_length=20,
        choices=CALCULATION_TYPES,
        default='flat'
    )
    is_active = models.BooleanField(_('Active'), default=True)
    estimated_days = models.PositiveIntegerField(
        _('Estimated Delivery Days'),
        help_text=_('Estimated number of days for delivery'),
        null=True,
        blank=True
    )
    tracking_url_template = models.URLField(
        _('Tracking URL Template'),
        blank=True,
        help_text=_('URL template for tracking. Use {tracking_number} as placeholder')
    )

    class Meta:
        verbose_name = _('Shipping Method')
        verbose_name_plural = _('Shipping Methods')

    def __str__(self):
        return self.name

class ShippingAddress(models.Model):
    """
    Represents a shipping address for orders
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_addresses')
    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    company = models.CharField(_('Company'), max_length=100, blank=True)
    address_line1 = models.CharField(_('Address Line 1'), max_length=255)
    address_line2 = models.CharField(_('Address Line 2'), max_length=255, blank=True)
    city = models.CharField(_('City'), max_length=100)
    state = models.CharField(_('State/Province'), max_length=100)
    country = models.CharField(_('Country'), max_length=2)
    postal_code = models.CharField(_('Postal Code'), max_length=20)
    phone = models.CharField(_('Phone Number'), max_length=50, blank=True)
    is_default = models.BooleanField(_('Default Address'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Shipping Address')
        verbose_name_plural = _('Shipping Addresses')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.address_line1}, {self.city}"

    def save(self, *args, **kwargs):
        # If this is being set as default, remove default from other addresses
        if self.is_default:
            ShippingAddress.objects.filter(
                user=self.user,
                is_default=True
            ).update(is_default=False)
        # If this is the user's only address, make it the default
        elif not self.pk and not ShippingAddress.objects.filter(user=self.user).exists():
            self.is_default = True
        super().save(*args, **kwargs)


class ShippingRate(models.Model):
    """
    Represents the rate for a shipping method in a specific zone
    """
    shipping_method = models.ForeignKey(
        ShippingMethod,
        on_delete=models.CASCADE,
        related_name='rates'
    )
    shipping_zone = models.ForeignKey(
        ShippingZone,
        on_delete=models.CASCADE,
        related_name='rates'
    )
    base_rate = models.DecimalField(
        _('Base Rate'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    weight_rate = models.DecimalField(
        _('Rate per Weight Unit'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text=_('Additional rate per weight unit (e.g., per kg)')
    )
    min_weight = models.DecimalField(
        _('Minimum Weight'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    max_weight = models.DecimalField(
        _('Maximum Weight'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    min_order_amount = models.DecimalField(
        _('Minimum Order Amount'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    max_order_amount = models.DecimalField(
        _('Maximum Order Amount'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Shipping Rate')
        verbose_name_plural = _('Shipping Rates')
        unique_together = ('shipping_method', 'shipping_zone')

    def __str__(self):
        return f"{self.shipping_method.name} - {self.shipping_zone.name}"

    def calculate_shipping_cost(self, weight=None, order_total=None):
        """
        Calculate shipping cost based on the method type and input parameters
        """
        if not self.shipping_method.is_active:
            return None

        # Check weight constraints if applicable
        if (self.min_weight and weight and weight < self.min_weight) or \
           (self.max_weight and weight and weight > self.max_weight):
            return None

        # Check order amount constraints if applicable
        if (self.min_order_amount and order_total and order_total < self.min_order_amount) or \
           (self.max_order_amount and order_total and order_total > self.max_order_amount):
            return None

        cost = self.base_rate

        # Add weight-based cost if applicable
        if self.shipping_method.calculation_type == 'weight' and weight and self.weight_rate:
            cost += weight * self.weight_rate

        return cost


